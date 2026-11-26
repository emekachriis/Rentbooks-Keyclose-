# Delivery checklist (one per paid client)

Copy this into a note for each client and tick it off as you go. Commands run from the `workbook/` folder.

**Golden rule:** client files never go into this Git repo (it is public). Keep them in `clients/<surname>/`, which `.gitignore` blocks, or in a folder outside the repo.

---

## A. Order and intake (day 0)

- [ ] Lemon Squeezy order received. Note the order number, email and **number of properties paid for**.
- [ ] Tally submission received with the same email (or order number).
- [ ] Number of properties on the form = number paid for. If not, email the client before starting: either they pay for the difference, or you agree which properties are included.
- [ ] Create the client folder: `clients/<surname>/` (inside the repo folder, which is ignored, or anywhere outside it).
- [ ] Download every uploaded file from Tally into that folder.
- [ ] Add a row to your client log: name, email, order #, properties, date documents complete, due date, delivery date, **deletion date**.

## B. Document check (within 1 business day)

- [ ] For each property: are all 12 monthly statements there (Jan to Dec 2026)?
- [ ] Bank export covers Jan to Dec 2026 and is the account the PM pays into?
- [ ] No passwords or logins were sent. If any were, tell the client to change them and delete the message.
- [ ] Email the client **once**, with a complete list of anything missing. Template:

> Hi [name], thanks, I've got your files. Before I start I need: [Oak St: August and November statements], [bank export for December]. Your 5 business days start when these arrive. If a statement can't be found, I'll note the month on the Exceptions sheet for your CPA.

- [ ] Documents complete → write the **due date** (5 business days later) in the log. If the client says a statement can't be had, treat the documents as complete on that date.

## C. Build the workbook

- [ ] Generate a template with the client's property names:
  ```bash
  python3 build_workbook.py --template-only --properties "Oak St" "Elm Ave" --template-name ../clients/<surname>/<surname>-rental-books-2026.xlsx
  ```
- [ ] Open it in Excel (or LibreOffice). Fill in the **Summary**: owner name, "Prepared by / date", "Files received".
- [ ] **Ledger, per property, per month:** enter gross rent, management fee, leasing fee, repairs and other PM charges exactly as the statement shows them. Never enter a netted figure. Put Y/N in "Statement received". Describe every "Other" charge. Enter reserve held (+) or released (−) if the PM holds one.
- [ ] Check each month: the Ledger's **Net owner distribution** = the statement's net payout. If not, find the line you missed before moving on.
- [ ] **Bank tie-out:** enter each month's deposit(s) from the bank export, with the date and memo.
- [ ] Every shaded difference → one row on **Exceptions** (type, property, month, amount, what you found, what to check, Status = Open).
- [ ] **Owner-paid expenses** (from the bank export or the client's list) → the Owner-paid column on the **Schedule E map**, on the line you'd expect, **and** an Exceptions row for each so the CPA confirms it.
- [ ] Missing statements → an Exceptions row ("Missing month") for each.
- [ ] Unclear PM charges → an Exceptions row ("Unclassified charge"); leave them in Other (line 19).
- [ ] **Contractors:** list every payee from the repair lines, with service, property, who paid (PM or owner) and the 2026 total. The "Check" rows at the bottom must show a zero difference against ledger repairs.
- [ ] Re-check the Schedule E line names against the **final** 2026 Schedule E once the IRS publishes it (the generator uses the May 2026 draft): https://www.irs.gov/forms-pubs/about-schedule-e-form-1040

## D. Check

- [ ] Save, then run:
  ```bash
  python3 verify.py ../clients/<surname>/<surname>-rental-books-2026.xlsx
  ```
  It must report **0 errors**, and every non-zero difference it lists must have an Exceptions row.
- [ ] Read the Summary status line. It should say exactly what you expect.
- [ ] Spot-check 3 random months against the original PDFs.
- [ ] The disclaimer is on the Summary (it's built in; just don't delete it).

## E. Deliver (on or before the due date)

- [ ] Make the PDF summary:
  ```bash
  python3 export.py ../clients/<surname>/<surname>-rental-books-2026.xlsx
  ```
- [ ] Email the client both files: `<surname>-rental-books-2026.xlsx` and `<surname>-rental-books-2026-summary.pdf`. Template:

> Hi [name], your 2026 books are attached: the workbook (Excel) and a PDF summary. Please forward both to your CPA. The Exceptions sheet lists [N] items for you or your CPA to look at; the main one is [one line]. This is bookkeeping prepared for your CPA, not tax advice, tax preparation or tax filing. As promised, I'll delete your files and my working copies on [deletion date]. Reply if you have any questions before then.

- [ ] Log the delivery date. Set **deletion date = delivery date + 30 days** in your calendar, with a reminder.

## F. Deletion (on the deletion date)

Delete everything for this client:

- [ ] The submission (with its uploaded files) in **Tally**.
- [ ] The local client folder `clients/<surname>/`, then empty the trash / recycle bin.
- [ ] Copies in Downloads, on your desktop, and in any cloud sync folder (Google Drive, iCloud, Dropbox, OneDrive), including their trash.
- [ ] Email attachments, both received and sent (delete the messages or the attachments, then empty the email trash).
- [ ] Keep only your log row (name, email, order #, dates). It contains no financial data.
- [ ] Mark "Deleted on [date]" in the log.

## Refunds

Follow the refund policy you publish on the site (`{{REFUND_POLICY}}`). Issue refunds from the order page in the Lemon Squeezy dashboard, then run section F for that client.
