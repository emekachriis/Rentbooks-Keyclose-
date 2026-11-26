# Setting up payment (Lemon Squeezy) and the upload form (Tally)

Do these before filling `{{CHECKOUT_URL}}` and `{{INTAKE_URL}}` on the site. Menu names in these apps change; if a button is named differently, look for the closest match.

---

## 0. Check payouts FIRST (before you build anything)

Before you rely on Lemon Squeezy, confirm in its **payout settings** (and its help docs) that it can pay out to you **in your country, by a method you can actually receive**: a bank account in your name, or PayPal. Payout support varies by country and changes over time. If it can't pay you, find out now, not after a client has paid.

Also expect Lemon Squeezy to **review your store** before it can take live payments. Reviewers usually look for a live website that clearly describes the service, the price and a refund policy. Your site has all three (the refund policy is in the FAQ), so deploy the site (DEPLOY.md) before you apply.

## 1. Lemon Squeezy product

Pricing is $149 for the first property plus $49 for each extra, which a single price × quantity can't express. Use **one product with one variant per number of properties**:

| Variant name | Price |
|---|---|
| 1 property | $149 |
| 2 properties | $198 |
| 3 properties | $247 |
| 4 properties | $296 |
| 5 properties | $345 |
| 6 properties | $394 |
| 7 properties | $443 |
| 8 properties | $492 |
| 9 properties | $541 |
| 10 properties | $590 |

(Formula: $149 + $49 × (properties − 1). For more than 10, ask buyers to email you, and create a custom checkout for them.)

- **Product name:** "2026 year-end rental books"
- **Description** (paste this): "One reconciled, per-property workbook (Excel plus a PDF summary) from your 2026 property manager statements and bank export, for your CPA. Delivered within 5 business days of complete documents. One property = one address. Bookkeeping prepared for your CPA: not tax advice, tax preparation or tax filing."
- **Type:** single payment (not a subscription).
- **Confirmation / receipt message:** "Thanks for your order. Next step: upload your documents here: [your Tally link]. Your workbook arrives within 5 business days of complete documents. Questions: hello@[your domain]"
- **Checkout link** for `{{CHECKOUT_URL}}`: use the product's share/checkout link, then **open it yourself and check the buyer can choose the number of properties**. If your link only ever opens one variant, tell Claude, and the "Get started" button can link to a small price picker instead.

## 2. Tally form

Build it exactly as in `launch/intake-form-fields.md`. Then:

- Copy the form's **share link** (it looks like `https://tally.so/r/xxxxxx`). That's `{{INTAKE_URL}}`.
- Paste the same link into the Lemon Squeezy confirmation message above.
- Submit one test with a dummy PDF, check the notification email reaches you, then delete the test submission.

## 3. Put the links on the site

Follow DEPLOY.md Step 0: on GitHub, edit `site/index.html`, replace `{{CHECKOUT_URL}}` (3 places) and `{{INTAKE_URL}}` (2 places), and commit to `main`. Or paste both links to Claude and it will do it.
