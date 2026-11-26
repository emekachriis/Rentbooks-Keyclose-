# Putting the website online (beginner's guide)

**What you'll end up with:** your page live at `https://yourname.com`, hosted free on Cloudflare Pages, with the domain bought through Cloudflare Registrar. It takes about an hour. Nothing here needs the command line.

Cloudflare's menus were checked against its documentation on 26 Nov 2026. If a button has a slightly different name when you get there, look for the closest match.

**Cost:** Pages hosting is free. The .com domain is the only cost: Cloudflare shows the price before you pay, so check it fits your budget. Auto-renew is **on** by default, so the same price will be charged again next year unless you turn it off.

---

## Step 0. Fill in the placeholders (15 min)

The site must not go live with `{{...}}` showing.

1. You'll need these first:
   - your brand name (see `launch/names.md`);
   - your Lemon Squeezy checkout link;
   - your Tally form link (see `launch/intake-form-fields.md`);
   - your contact email;
   - your refund policy (one or two sentences);
   - a two-to-three-sentence bio;
   - your domain. If you haven't bought it yet, fill everything else now and come back for `{{DOMAIN}}` after Step 3.
2. On GitHub, open the repo, go to `site/index.html` and click the **pencil icon** (Edit).
3. Press **Ctrl+F** (Cmd+F on a Mac) and search for `{{`. Replace each placeholder everywhere it appears:

   | Placeholder | Replace with | Example |
   |---|---|---|
   | `{{BRAND}}` | brand name | `Keyclose` |
   | `{{CHECKOUT_URL}}` | Lemon Squeezy checkout link | `https://….lemonsqueezy.com/checkout/buy/…` |
   | `{{INTAKE_URL}}` | Tally form link | `https://tally.so/r/…` |
   | `{{EMAIL}}` | contact email | `hello@yourname.com` |
   | `{{REFUND_POLICY}}` | your refund policy | |
   | `{{BIO}}` | your short bio | |
   | `{{DOMAIN}}` | domain only, no `https://` and no `/` | `yourname.com` |

4. Search for `{{` once more: there should be **no results**. (The comment block at the very top of the file lists the placeholder names; you can leave that or delete it.)
5. Click **Commit changes**.

**The repo is public.** Anything you put in `index.html` (your email, for example) is visible on GitHub, just as it is on the live site. Never put passwords or client files in this repo.

## Step 1. Make sure the code is on the `main` branch

Cloudflare publishes one branch as the live site. Right now the work is on a branch called `claude/epic-wright-qos6qe`.

- Easiest: ask Claude to push it to `main` for you.
- Or on GitHub: open the repo → **Pull requests** → **New pull request**. If GitHub can't compare the branches because `main` doesn't exist yet, go to **Settings → Branches** instead and rename the branch to `main`.

## Step 2. Create the Cloudflare Pages project (15 min)

1. Sign up at **dash.cloudflare.com** (free) and **verify your email address**. You'll need a verified email to buy a domain later.
2. In the left menu, open **Workers & Pages**.
3. Click **Create application** → choose the **Pages** tab → **Connect to Git**.
4. Choose **GitHub** → **Install & Authorize**. When GitHub asks which repositories, choose **Only select repositories** → `Rentbooks-Keyclose-`. Then click **Begin setup**.
5. Fill in the form exactly like this:

   | Field | Value |
   |---|---|
   | Project name | your brand in lowercase, e.g. `keyclose` (this becomes `keyclose.pages.dev`) |
   | Production branch | `main` |
   | Framework preset | **None** |
   | Build command | `exit 0` |
   | Build output directory | `site` |
   | Root directory (advanced) | leave empty |
   | Environment variables | none |

   `site` matters: it means only the website folder is published. The workbook scripts stay off the internet.
6. Click **Save and Deploy**. Wait about a minute, then **Continue to project**.
7. Open the `https://<project>.pages.dev` link. Check on your phone too: every button should open the right Tally or Lemon Squeezy page, and the sample PDF should download.

From now on, **every change committed to `main` goes live automatically** within a minute or two.

*Cloudflare's note:* a project connected to Git can't later be switched to "Direct Upload" (drag and drop). That's fine: you don't need it.

## Step 3. Buy the domain (10 min)

1. In the Cloudflare dashboard, open **Domain Registration → Register Domains** (it may be shown as **Register domains**).
2. Type the name you chose → **Search** → **Purchase** next to the .com.
3. Choose the term (1 year is fine) in the **Payment option** drop-down. Check the price shown.
4. Enter your contact details. They must be **complete and accurate**, or the registration can be suspended. Cloudflare hides your personal details from public WHOIS where the registry allows.
5. Enter payment → read the agreements → **Complete purchase**.
6. **Check your inbox for the domain verification email and click it.** If you don't, the domain can be put on hold.

If your card is declined, try another card that allows international USD payments. Don't buy the domain somewhere else and then move it: that takes longer and is harder.

## Step 4. Connect the domain to the site (10 min, plus a short wait)

1. **Workers & Pages** → your project → **Custom domains** → **Set up a domain**.
2. Type `yourname.com` → **Continue** → **Activate domain**. Because the domain is already on Cloudflare, it creates the DNS record for you.
3. Repeat for `www.yourname.com`, so both addresses work.
4. Wait until both show **Active** (usually a few minutes; occasionally up to a day). Then open `https://yourname.com`: the padlock should show.

If you see an "Error 522", the domain was added in DNS by hand instead of through **Custom domains**. Remove the manual record and use **Set up a domain**.

## Step 5. Final checks before you send a single DM

- [ ] `https://yourname.com` loads on your phone, with no `{{` anywhere on the page.
- [ ] **Get started** opens the Lemon Squeezy checkout. Buy one test order in Lemon Squeezy's test mode if it has one; otherwise buy for real and refund yourself.
- [ ] After paying, the receipt message links to the Tally form.
- [ ] Submit the Tally form once yourself with a dummy PDF, then delete that submission.
- [ ] The sample PDF downloads.
- [ ] Share your link in a private chat (WhatsApp, for example): the preview should show the green image with the workbook crops.
- [ ] The email address on the site actually receives mail.

## Changing the site later

Edit `site/index.html` on GitHub (pencil icon) → **Commit changes** on `main`. Cloudflare redeploys automatically; check the project's **Deployments** tab if it doesn't appear within a few minutes.
