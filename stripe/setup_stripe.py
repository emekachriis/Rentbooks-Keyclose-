#!/usr/bin/env python3
"""
Create (or reuse) everything Keyclose needs in Stripe, using the Stripe CLI.

  export STRIPE_API_KEY=sk_test_...        # NEVER commit a key; this repo is public
  python3 stripe/setup_stripe.py [--intake-url https://tally.so/r/xxxx]

Safe to run more than once: prices are found by lookup_key, the payment link by metadata.

Creates:
  Product  "2026 year-end rental books"
  Price    keyclose_2026_first_property   $149 one-time
  Price    keyclose_2026_extra_property   $49 one-time
  Payment Link: first property (fixed, qty 1) + optional "Additional property" (buyer picks 1-29),
                invoice PDF after payment, confirmation message pointing to the upload form.
  Crypto: switched on as a payment method, if Stripe offers it to the account.

Prints the Payment Link URL: that is {{CHECKOUT_URL}} for the website.
Bookkeeping prepared for your CPA. Not tax advice, tax preparation or tax filing.
"""
import argparse
import json
import os
import subprocess
import sys

YEAR = "2026"
LINK_TAG = f"keyclose-{YEAR}-checkout"
DISCLAIMER = "Bookkeeping prepared for your CPA. Not tax advice, tax preparation or tax filing."


def call(method, path, params=()):
    """Call the Stripe API through the CLI (`stripe get|post <path> -d k=v`). Exits on any API error."""
    cmd = ["stripe", method, path]
    for k, v in params:
        cmd += ["-d", f"{k}={v}"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    try:
        out = json.loads(r.stdout)
    except json.JSONDecodeError:
        sys.exit(f"stripe {method} {path} failed:\n{r.stdout}\n{r.stderr}")
    if isinstance(out, dict) and "error" in out:
        sys.exit(f"Stripe error on {method} {path}: {out['error'].get('message')}")
    return out


def get_price(lookup_key):
    res = call("get", "/v1/prices", [("lookup_keys[]", lookup_key), ("active", "true")])["data"]
    return res[0] if res else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--intake-url", default="{{INTAKE_URL}}",
                    help="Tally form link shown on the confirmation page")
    a = ap.parse_args()
    key = os.environ.get("STRIPE_API_KEY", "")
    if not key.startswith(("sk_test_", "sk_live_", "rk_")):
        sys.exit("Set STRIPE_API_KEY first (sk_test_... for testing).")
    mode = "LIVE" if key.startswith("sk_live_") else "test"
    print(f"Stripe mode: {mode}")
    meta = [("metadata[service]", "year-end-books"), ("metadata[year]", YEAR)]

    first, extra = get_price(f"keyclose_{YEAR}_first_property"), get_price(f"keyclose_{YEAR}_extra_property")
    if not first:
        prod = call("post", "/v1/products", [
            ("name", f"{YEAR} year-end rental books"),
            ("description", "One reconciled, per-property workbook (Excel plus a PDF summary) from your "
             f"{YEAR} property manager statements and bank export, for your CPA. Delivered within 5 business "
             "days of complete documents. One property = one address. " + DISCLAIMER)] + meta)
        first = call("post", "/v1/prices", [("product", prod["id"]), ("currency", "usd"), ("unit_amount", "14900"),
                                             ("lookup_key", f"keyclose_{YEAR}_first_property"),
                                             ("nickname", "First property")])
        print("created product + $149 price", first["id"])
    else:
        print("reusing $149 price", first["id"])
    if not extra:
        # Its own product, so it reads "Additional property" at checkout.
        prod = call("post", "/v1/products", [
            ("name", "Additional property"),
            ("description", f"Each extra property (one address) in the same {YEAR} workbook.")] + meta)
        extra = call("post", "/v1/prices", [("product", prod["id"]), ("currency", "usd"), ("unit_amount", "4900"),
                                             ("lookup_key", f"keyclose_{YEAR}_extra_property"),
                                             ("nickname", "Additional property")])
        print("created product + $49 price", extra["id"])
    else:
        print("reusing $49 price", extra["id"])

    # Crypto (stablecoins, settled to your Stripe balance in USD): switch it on in the account's default
    # payment-method configuration. Stripe decides eligibility; if it isn't offered, this just reports it.
    cfgs = call("get", "/v1/payment_method_configurations", [("limit", "10")])["data"]
    cfg = next((c for c in cfgs if c.get("is_default")), cfgs[0] if cfgs else None)
    if cfg and cfg.get("crypto", {}).get("display_preference", {}).get("value") != "on":
        r = subprocess.run(["stripe", "post", f"/v1/payment_method_configurations/{cfg['id']}",
                            "-d", "crypto[display_preference][preference]=on"], capture_output=True, text=True)
        try:
            cr = json.loads(r.stdout)
        except json.JSONDecodeError:
            cr = {"error": {"message": r.stdout or r.stderr}}
        print("crypto:", cr["error"]["message"] if "error" in cr else "enabled")
    elif cfg:
        print("crypto: already enabled")

    links = call("get", "/v1/payment_links", [("active", "true"), ("limit", "100")])["data"]
    link = next((l for l in links if l.get("metadata", {}).get("tag") == LINK_TAG), None)
    confirmation = (f"Thank you. Next step: upload your {YEAR} PM statements and bank export here: {a.intake_url} "
                    "Your workbook arrives within 5 business days of complete documents. " + DISCLAIMER)
    common = [("after_completion[type]", "hosted_confirmation"),
              ("after_completion[hosted_confirmation][custom_message]", confirmation)]
    if link:
        link = call("post", f"/v1/payment_links/{link['id']}", common)
        print("updated payment link", link["id"])
    else:
        link = call("post", "/v1/payment_links", [
            ("line_items[0][price]", first["id"]), ("line_items[0][quantity]", "1"),
            ("optional_items[0][price]", extra["id"]), ("optional_items[0][quantity]", "1"),
            ("optional_items[0][adjustable_quantity][enabled]", "true"),
            ("optional_items[0][adjustable_quantity][minimum]", "1"),
            ("optional_items[0][adjustable_quantity][maximum]", "29"),
            ("customer_creation", "always"),
            ("invoice_creation[enabled]", "true"),
            ("invoice_creation[invoice_data][description]", f"{YEAR} year-end rental books. {DISCLAIMER}"),
            ("invoice_creation[invoice_data][footer]", DISCLAIMER),
            ("custom_text[submit][message]", "$149 for the first property, plus $49 for each additional property "
             "(one property = one address). " + DISCLAIMER),
            ("metadata[tag]", LINK_TAG)] + common)
        print("created payment link", link["id"])
    print()
    print("CHECKOUT_URL =", link["url"])
    if mode == "test":
        print("(test mode: pay with card 4242 4242 4242 4242, any future date, any CVC)")


if __name__ == "__main__":
    main()
