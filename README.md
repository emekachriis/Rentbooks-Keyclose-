# Year-End Rental Books: launch assets

A done-for-you bookkeeping service for US rental owners whose properties are managed by outside property managers. A year of PM statements and a bank export become one reconciled, per-property workbook the owner's CPA can use to prepare Schedule E.

**Bookkeeping prepared for your CPA. Not tax advice, tax preparation or tax filing.**

| Folder | What's in it |
|---|---|
| `workbook/` | Workbook generator (`build_workbook.py`), checker (`verify.py`), PDF export (`export.py`), the fictional sample and the empty template. See `workbook/README.md`. |
| `site/` | The one-page website that Cloudflare Pages publishes. Fill the `{{PLACEHOLDERS}}` before going live. |
| `scripts/` | Rebuild the site from the sample data (`build_site.py`) and its images (`site_assets.js`). Only needed if the sample changes. |
| `launch/` | Tally form fields, outreach messages, the per-client delivery checklist, and brand name ideas. |
| `DEPLOY.md` | Step-by-step: put the site online and connect the domain. |

**This repository is public. Client files never go in it.** Keep them in `clients/` (ignored by Git) or outside the repo, and delete them 30 days after delivery (see `launch/delivery-checklist.md`).

## Sources checked (26 Nov 2026)

- Schedule E lines: IRS 2026 Schedule E draft, https://www.irs.gov/pub/irs-dft/f1040se--dft.pdf. Re-check against the final form when it's published.
- 1099-NEC threshold ($2,000 for 2026): https://www.irs.gov/instructions/i1099mec
- Cloudflare Pages and Registrar steps: developers.cloudflare.com (see `DEPLOY.md`).
