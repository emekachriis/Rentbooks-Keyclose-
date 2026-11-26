#!/usr/bin/env python3
"""
Send a Stripe invoice for a custom order, e.g. an owner with more than 10 properties,
or anyone who prefers an emailed invoice to the checkout link.

  export STRIPE_API_KEY=sk_test_...        # NEVER commit a key; this repo is public
  python3 stripe/send_invoice.py --email owner@example.com --name "Pat Owner" --properties 12 [--days 7] [--draft]

Uses the same $149 / $49 prices that setup_stripe.py created (found by lookup_key), so the
total is always $149 + $49 x (properties - 1). Stripe emails the invoice with a pay-online link
(in test mode Stripe does not email real people). --draft creates it without sending, for review.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from setup_stripe import DISCLAIMER, YEAR, call, get_price  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--email", required=True)
    ap.add_argument("--name", required=True)
    ap.add_argument("--properties", type=int, required=True, help="number of properties (addresses)")
    ap.add_argument("--days", type=int, default=7, help="days until the invoice is due")
    ap.add_argument("--intake-url", default="{{INTAKE_URL}}")
    ap.add_argument("--draft", action="store_true", help="create but do not finalize or send")
    a = ap.parse_args()
    if not os.environ.get("STRIPE_API_KEY", "").startswith(("sk_", "rk_")):
        sys.exit("Set STRIPE_API_KEY first.")
    if not 1 <= a.properties <= 100:
        sys.exit("--properties must be between 1 and 100")

    first, extra = get_price(f"keyclose_{YEAR}_first_property"), get_price(f"keyclose_{YEAR}_extra_property")
    if not (first and extra):
        sys.exit("Prices not found. Run stripe/setup_stripe.py first.")

    found = call("get", "/v1/customers", [("email", a.email), ("limit", "1")])["data"]
    cust = found[0] if found else call("post", "/v1/customers", [("email", a.email), ("name", a.name)])
    print("customer", cust["id"], "(reused)" if found else "(new)")

    inv = call("post", "/v1/invoices", [
        ("customer", cust["id"]), ("collection_method", "send_invoice"), ("days_until_due", str(a.days)),
        ("auto_advance", "false"),
        ("description", f"{YEAR} year-end rental books for {a.properties} propert"
                        f"{'y' if a.properties == 1 else 'ies'} (one property = one address). "
                        f"After paying, upload your documents here: {a.intake_url}"),
        ("footer", DISCLAIMER), ("metadata[service]", "year-end-books"), ("metadata[properties]", str(a.properties))])
    call("post", "/v1/invoiceitems", [("customer", cust["id"]), ("invoice", inv["id"]),
                                      ("pricing[price]", first["id"]), ("quantity", "1")])
    if a.properties > 1:
        call("post", "/v1/invoiceitems", [("customer", cust["id"]), ("invoice", inv["id"]),
                                          ("pricing[price]", extra["id"]), ("quantity", str(a.properties - 1))])
    inv = call("get", f"/v1/invoices/{inv['id']}")
    expected = 14900 + 4900 * (a.properties - 1)
    if inv["amount_due"] != expected:
        sys.exit(f"Total mismatch: invoice {inv['amount_due']} vs expected {expected}. Draft left for review: {inv['id']}")
    print(f"invoice {inv['id']} total ${inv['amount_due'] / 100:,.2f}")
    if a.draft:
        print("draft only: review it in the Dashboard, then send it there")
        return
    inv = call("post", f"/v1/invoices/{inv['id']}/finalize")
    inv = call("post", f"/v1/invoices/{inv['id']}/send")
    print("sent:", inv["status"], inv["number"])
    print("pay link:", inv["hosted_invoice_url"])


if __name__ == "__main__":
    main()
