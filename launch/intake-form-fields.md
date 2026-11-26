# Tally intake form: exact fields

Build this in Tally (free plan) as one page, with the fields in this order. Text in quotes is exactly what the client sees. "Required" means switch on Tally's *Required* toggle.

Form title: **"Send your 2026 documents"**

Intro text block (put at the top of the form):

> "Upload your 2026 property manager statements and a bank export. I'll check them within one business day and tell you if anything is missing. Your workbook arrives within 5 business days of complete documents.
> Please do not send passwords or logins. I never need them.
> This is bookkeeping prepared for your CPA. It is not tax advice, tax preparation or tax filing."

---

## Fields

| # | Tally block | Label (shown to client) | Settings / options | Help text (shown under the label) |
|---|---|---|---|---|
| 1 | Short answer | "Full name" | Required | |
| 2 | Email | "Email address" | Required | "Use the same email you paid with, so I can match your order." |
| 3 | Short answer | "Order number" | Optional | "From your payment receipt email. Leave blank if you can't find it." |
| 4 | Number | "Number of properties" | Required. Min 1, max 30 | "The number of properties you paid for. One property = one address (a duplex or fourplex at one address counts as one)." |
| 5 | Long answer | "Your properties" | Required | "One line per property: a short name or the street address, and the property manager. Example: 12 Oak St, Northstar Property Management" |
| 6 | Long answer | "Property manager name(s)" | Required | "List every property manager who managed any of these properties in 2026, including any you changed from during the year." |
| 7 | Dropdown | "Year" | Required. One option only: **2026** | "This service covers January to December 2026." |
| 8 | File upload | "PM statements for 2026" | Required. Allow multiple files. Accept PDF, CSV, XLSX | "Every monthly owner statement, January to December, from each property manager. A year-end summary also helps if your PM provides one." |
| 9 | File upload | "Bank export for 2026" | Required. Allow multiple files. Accept CSV, PDF, XLSX | "A CSV export (or PDF statements) for January to December 2026 from the account that receives your PM payouts. You may black out account numbers: I only need dates, amounts and descriptions." |
| 10 | File upload | "1099s your PM issued (if any)" | Optional. Allow multiple files. Accept PDF | |
| 11 | File upload | "Expenses you paid yourself, outside the PM" | Optional. Allow multiple files. Accept PDF, CSV, XLSX, JPG, PNG | "Receipts or a simple list (date, payee, amount, property) for anything you paid directly, like insurance or a repair." |
| 12 | Long answer | "Months you already know are missing" | Optional | "For example: 'Oak St, August: PM hasn't sent it yet.'" |
| 13 | Long answer | "Anything else I should know" | Optional | "For example: you changed PMs mid-year, sold a property, or your CPA asked for something specific." |
| 14 | Checkboxes | "Please confirm" | Required: **all three** must be ticked (in Tally, set the minimum number of selections to 3) | |

Field 14 options (exact wording):

- [ ] "I understand this is bookkeeping prepared for my CPA. It is not tax advice, tax preparation or tax filing."
- [ ] "I understand my uploaded files and all working copies will be deleted 30 days after my workbook is delivered."
- [ ] "I have not included any passwords, logins or full account numbers."

---

## Form settings

- **Thank-you page:** "Thanks. I've got your files and will confirm within one business day whether anything is missing. Questions: hello@{{DOMAIN}}"
- **Self email notifications:** on, to your email, so you know the moment a client submits.
- **Respondent email:** optional. If you use it, copy the thank-you text into it.
- **Close form / limit responses:** off.
- **Check before you go live:** Tally's current file-size and storage limits on the free plan. Owners with many statements may hit a per-file limit. If they do, ask them to zip the files by property, or to email them.

## Where the link goes

- On the site, `{{INTAKE_URL}}` = the Tally share link (the "Send documents" button and the "Already paid? Send documents" link).
- In Lemon Squeezy: put the same link in the product's **confirmation / receipt message**, so every buyer is sent straight to the upload form after paying.
