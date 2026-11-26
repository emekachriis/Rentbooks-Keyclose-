# Stripe integration (no server needed)

Stripe hosts everything: the checkout page, the receipts and invoices, and the payment pages. The website only links to a Stripe **Payment Link**, so no secret key ever goes near the site.

**Status (26 Nov 2026): built and tested in test mode (sandbox) only.**

- A live account needs Stripe to accept your business. Stripe's country list shows **Nigeria as "Extended network" via Paystack**, not direct sign-up. Live Stripe therefore needs a business in a supported country (for example a US company through Stripe Atlas).
- Check with Stripe before you rely on this for real money.

**Keys:** never put a key in this repo (it is public; `.gitignore` blocks `*.env`). Set it in your terminal only:

```bash
export STRIPE_API_KEY=sk_test_...
```

## What's set up

| Stripe product | What it does here | Script |
|---|---|---|
| **Payments** | One Payment Link: "2026 year-end rental books" at $149, plus an optional "Additional property" at $49 that the buyer can add (1 to 29 extra). After paying, the buyer sees a message linking to the upload form, and gets an invoice PDF by email. | `setup_stripe.py` |
| **Invoicing** | Emailed invoice for custom orders (more than 10 properties, or owners who'd rather pay an invoice). Total is always $149 + $49 × (properties − 1). | `send_invoice.py` |
| **Crypto** | Stablecoin payments shown at checkout, as long as Stripe offers them to the account. Stripe handles the wallet side and settles to your Stripe balance in US dollars, so you hold no crypto and run no wallet. | `setup_stripe.py` |
| **Billing** | Not used: the service is a one-off yearly purchase. If you later want automatic renewal for 2027, it would be a yearly subscription price. Ask Claude. | |

The disclaimer ("Bookkeeping prepared for your CPA. Not tax advice, tax preparation or tax filing.") appears in four places: the product description, under the Pay button, on the confirmation page, and on every invoice (description and footer).

## Commands

```bash
python3 stripe/setup_stripe.py --intake-url https://tally.so/r/xxxxxx
```
Creates or reuses the product, the prices and the Payment Link. It also switches crypto on and prints `CHECKOUT_URL`. It's safe to run again: rerun it with the Tally link once you have one, so the confirmation page points to it.

```bash
python3 stripe/send_invoice.py --email owner@example.com --name "Pat Owner" --properties 12
```
Creates and emails an invoice ($688 for 12 properties). Add `--draft` to review it in the Dashboard first.

## Tested (test mode)

- A checkout with 1 extra property was paid with test card 4242 4242 4242 4242: $198.00, status paid, invoice issued with the disclaimer in its description and footer, invoice PDF available.
- A 12-property invoice was created and sent: $688.00, with a pay-online link.
- Crypto appears as a payment option at checkout. A crypto payment itself was **not** test-paid.

## Going live (only once Stripe accepts your business)

1. Activate the account in the Dashboard and add your payout bank account.
2. Use the **live** secret key: `export STRIPE_API_KEY=sk_live_...` and run `setup_stripe.py` again. Live mode has its own products and links.
3. Check that crypto is still offered in live mode: Stripe limits it by business country and type.
4. Put the live Payment Link URL into `site/index.html` in place of `{{CHECKOUT_URL}}` (3 places). Never put a **test** link on the public site.
5. In the Dashboard, check **Settings → Payment methods**. Affirm, Klarna and Cash App Pay are on by default, so turn off anything you don't want.
6. Turn on email notifications for successful payments, so you know when to expect the client's documents.
