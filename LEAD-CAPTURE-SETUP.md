# FSO — Lead Capture & Score Email · Setup Guide

This explains how the FSO Diagnostic (and the contact form) capture every lead
for you **and** email the respondent their score.

---

## What now happens

When someone finishes the 15-question diagnostic, they're asked for their
**name and email** (mobile and company optional) *before* the score is shown —
so every completed diagnostic becomes a lead you own. On submit, the site sends
one small POST containing their details **and** their computed score and
dimension breakdown to an endpoint you control. That endpoint then:

1. **records the lead** for you (e.g. a row in a Google Sheet), and
2. **emails the score** to the respondent, and
3. **notifies you** so you never miss a lead.

The contact form works the same way (it just has no score).

```
  Visitor finishes diagnostic
        │  name + email + score + breakdown  (POST)
        ▼
  Your endpoint  ──►  Google Sheet (your lead database)
        ├──────────►  Email to you        (new lead alert)
        └──────────►  Email to respondent (their FSO Score)
```

> Nothing is sent until you set the endpoint. Until then the score still shows
> on screen, and the lead is logged to the browser console — so you can preview
> the whole flow before wiring anything up.

---

## Why you need an "endpoint" at all

A website's front-end code **cannot send email by itself** — email needs a
server, and putting mail credentials in a public web page would be insecure.
So the page hands the lead to a small service you own, and that service sends
the mail. Below are three ways to run that service. **Option A is recommended:
it's free, you own the data, and it sends the branded score email.**

---

## Option A — Google Apps Script  (recommended · free · you own the data)

This uses your own Google account. ~10 minutes, no coding.

> **Which Google account to use.** The script sends email **as the account it's
> built in**. For the score emails to come from **connect@fsoworld.com**, sign in
> to Google as **connect@fsoworld.com** (your Google Workspace account) before
> doing the steps below, and create the sheet + script there. `OWNER_EMAIL` in
> the script is already set to `connect@fsoworld.com`, so lead alerts land there
> too. (If connect@fsoworld.com isn't a Google/Workspace mailbox yet, you'll
> need to add it to Google Workspace first, or build the script in another Google
> account — in which case emails send from that account instead.)

1. **Create the lead sheet.** Go to **sheets.new**, name it e.g. "FSO Leads".
   Copy the long ID from the URL between `/d/` and `/edit`:
   `https://docs.google.com/spreadsheets/d/`**`THIS_IS_THE_ID`**`/edit`

2. **Open the script editor.** In that sheet: **Extensions → Apps Script**.
   Delete any sample code.

3. **Paste the script.** Open `integrations/google-apps-script.gs` from this
   project, copy the whole file, and paste it in.

4. **Edit the CONFIG lines at the top:**
   - `OWNER_EMAIL` — where you want lead alerts (e.g. your inbox).
   - `SHEET_ID` — paste the ID from step 1.
   - `BOOKING_URL` — your Calendly / booking link (used in the score email).

5. **Deploy as a Web App.** Click **Deploy → New deployment** → gear icon →
   **Web app**. Set **Execute as: Me**, **Who has access: Anyone**. Click
   **Deploy**. Approve the permissions prompt (it needs to send email as you and
   write to your sheet — that's expected). Copy the **Web app URL** it gives you
   (ends in `/exec`).

6. **Plug the URL into the site** (two places):
   - `assets/js/diagnostic.js` → `FSO_CONFIG.submitEndpoint = "PASTE_URL"`
   - `assets/js/main.js` → `var CONTACT_ENDPOINT = "PASTE_URL"`

7. **Test.** Open the site, complete the diagnostic with your own email. Within
   a minute you should get: a new row in the sheet, a "new lead" email to
   `OWNER_EMAIL`, and the branded **FSO Score** email in the address you entered.

**Updating the script later:** after editing the `.gs`, click **Deploy → Manage
deployments → (edit) → Version: New version → Deploy** to publish the change.
Gmail sending limits on a free account are ~100 recipients/day (~1,500 on
Workspace) — plenty for a diagnostic, and easy to raise later.

---

## Option B — Web3Forms  (fastest · no Google needed)

Good if you just want leads in your inbox quickly. It can also send the
respondent a simple confirmation, though the nicely-formatted score email in
Option A is worth the extra few minutes.

1. Go to **web3forms.com**, enter your email, get a free **Access Key**.
2. In `assets/js/diagnostic.js`, set `submitEndpoint` to
   `https://api.web3forms.com/submit`.
3. Add your key to the payload: near the top of `submitLead`, add
   `lead.access_key = "YOUR_ACCESS_KEY";` (an access key is safe to expose).
4. To auto-reply to the respondent, also add
   `lead.replyto = email;` and enable "Auto (Re)Reply" in your Web3Forms
   dashboard. The score fields (`score`, `band`, `summary`) are included in
   what you receive.
5. Do the same in `assets/js/main.js` for the contact form if you like.

---

## Option C — EmailJS  (branded emails, no server, optional)

If you don't want to use Google, EmailJS can send two templated emails
(one to you, one to the respondent) from the browser. Create templates at
**emailjs.com**, then call their SDK inside `submitLead`. This keeps the
polished score email without Apps Script, but has lower free monthly limits.
(Ask and I can wire this variant in.)

---

## The "ask email first" behaviour

By default the score is **gated** — the respondent must enter name + email to
see it, which captures every completion. To show the score first and ask for
the email afterwards instead, open `assets/js/diagnostic.js` and set:

```js
gateResults: false
```

Everything else stays the same; the capture form simply appears **below** the
result rather than before it.

---

## Privacy & good practice

- Only ask for what you'll use — the form requires just name + email.
- The on-page copy already promises no spam and no sharing; honour it.
- If you'll email people ongoing marketing (beyond their report), add a line of
  consent and an unsubscribe path to stay compliant with local rules.
- The score email includes a short note that the diagnostic is an indicative
  self-assessment, not a formal FSO certification — keep that.

---

## Quick reference — where the endpoint goes

| File | Line to edit | For |
|------|--------------|-----|
| `assets/js/diagnostic.js` | `submitEndpoint: ""` | Diagnostic leads + score email |
| `assets/js/main.js` | `var CONTACT_ENDPOINT = "";` | Contact-form enquiries |

Both can use the **same** URL — the script routes on the `source` field
(`fso-diagnostic` vs `fso-contact`).
