# GEMS Profino — lead-generation website

Prototype built by **Foretek Solution and Services (OPC) Pvt Ltd** for GEMS
Profino, a loan facilitator (DSA) in Chennai. Provided complimentary; the
domain is purchased by the client.

Plain HTML, CSS and JavaScript. No build step, no dependencies, no framework.
Open `index.html` in a browser and it works.

---

## This is a prototype

Every page carries a black banner reading `PROTOTYPE`, and every unconfirmed
figure is marked with a dotted gold underline (`class="tbc"`, with the reason
in its `title`). **Do not make this live while those are in place** — the rates,
bank names and testimonials are sample content, and publishing them would be
an inaccurate public claim.

What the client still owes us is listed in `../CLIENT_INFO_REQUIRED.txt`.

---

## Local preview

```bash
python -m http.server 5173
# then open http://127.0.0.1:5173
```

A plain file open (`file:///…/index.html`) also works, but relative links
behave better over HTTP.

---

## Files

```
index.html              Home — hero estimate, rate sheet, process, FAQ, form
home-loan.html          ┐
property-loan.html      │ One page per product, each targeting its own
business-loan.html      │ search keyword ("home loan in Chennai")
car-loan-new.html       │
car-loan-used.html      ┘
about.html              Company background
contact.html            Phone, WhatsApp, address, map, form
privacy-policy.html     DPDP Act 2023 draft — client must approve
terms.html              Terms and DSA disclaimer — client must approve
thank-you.html          Conversion page. noindex. Tracking fires here.

assets/css/styles.css   All styles. Every colour is a token in :root.
assets/js/main.js       All behaviour. All settings are in CONFIG at the top.
assets/img/             Logo and icons, extracted from the client's creative

tools/gen-loan-pages.py    Regenerates the five loan pages from one template
tools/gen-static-pages.py  Regenerates about/contact/privacy/terms/thank-you

vercel.json             Caching and security headers
robots.txt  sitemap.xml  SEO
```

### About the generators

`tools/*.py` are one-time authoring tools, **not a build step**. The `.html`
files they produce are committed and can be edited directly. Run a generator
only when changing something shared by every page — the header, footer, or the
enquiry form — so the pages do not drift apart. Editing a generated page by
hand is fine; just remember a later regeneration would overwrite it.

---

## Changing the design

**Colours.** Edit only the `:root` block at the top of
`assets/css/styles.css`. Nothing else in the stylesheet hardcodes a colour, so
the whole site re-themes from those few lines.

The current palette was sampled out of the client's own logo rather than
guessed, which is why the logo PNG sits on the page background with no visible
seam:

| Token | Value | Role |
|---|---|---|
| `--forest` | `#04512F` | Logo green — buttons, links |
| `--gold` | `#CF9C35` | Logo gold — accents only |
| `--cream` | `#FFE7D1` | Page background, matching the creatives |
| `--ink` | `#14241B` | Body text |

If you change `--cream`, the logo will show a pale rectangle behind it —
`assets/img/logo.png` has a transparent background but was keyed out of a
`#FFE7D1` JPEG, so a very different background may reveal fringing. Ask the
client for the original logo file if the palette changes substantially.

**Fonts.** Archivo (headings), IBM Plex Sans (body), IBM Plex Mono (all rates,
amounts and EMI figures). Change them in `:root` and in the Google Fonts
`<link>` in each page's `<head>`.

---

## Going live — checklist

### 1. Enquiry delivery
Create a free access key at [web3forms.com](https://web3forms.com) using the
client's official email, then set it in `assets/js/main.js`:

```js
formKey: 'REPLACE_WITH_WEB3FORMS_ACCESS_KEY',
```

Until this is set the form runs in **demo mode**: it validates, shows the
thank-you page, and sends nothing. Send a test enquiry after setting it and
confirm the email arrives.

### 2. Confirm the WhatsApp number
`assets/js/main.js` → `CONFIG.whatsapp` (currently `919841525074`, taken from
the creatives). It also appears in `tel:` links in each page's header, footer
and mobile bar — search for `9841525074`.

### 3. Real rates
`assets/js/main.js` → `CONFIG.rates` drives the EMI estimates. The rates shown
in the rate sheet and on each loan page are separate, in the HTML. Both must
match what the client actually places at.

### 4. Tracking
Each page has a commented-out block in `<head>`. Uncomment it and replace:

- `G-XXXXXXXXXX` — GA4 measurement ID
- `AW-XXXXXXXXX` — Google Ads conversion ID
- Meta Pixel ID, if Meta campaigns will run

`main.js` already fires events on every meaningful action, and no change is
needed there:

| Event | When |
|---|---|
| `generate_lead` | Enquiry form submitted successfully |
| `conversion` | Thank-you page loaded |
| `whatsapp_click` | Any WhatsApp button |
| `call_click` | Any phone link |
| `slip_apply` | "Check what I qualify for" on the estimate |

Every event carries the product, so spend can be attributed per loan type.
Mark `/thank-you.html` as the conversion destination in Google Ads.

### 5. Replace every placeholder
Find them all:

```bash
grep -rn 'class="tbc"\|PLACEHOLDER\|REPLACE_WITH' *.html assets/js/main.js
```

Remove the `tbc` class as each value is confirmed. The pages with the most
outstanding items are `index.html`, `contact.html` and `privacy-policy.html`.

### 6. Legal sign-off
`privacy-policy.html` and `terms.html` are drafts. The client must approve
both, and nominate a grievance officer as the DPDP Act requires. Google and
Meta will not approve finance ads without a reachable privacy policy.

### 7. Remove the prototype banner
One line in each of the 11 pages:

```bash
grep -rln 'proto-banner' *.html
```

Delete the `<div class="proto-banner">…</div>` block from each. Do this last —
it is the safeguard against launching with sample rates.

### 8. Update the domain
`https://gemsprofino.com` is assumed throughout — in `<link rel="canonical">`,
the Open Graph tags, `robots.txt`, `sitemap.xml` and the structured data in
`index.html`. If the real domain differs:

```bash
grep -rn 'gemsprofino.com' . --include=*.html --include=*.xml --include=*.txt
```

### 9. Structured data
`index.html` ends with a `FinancialService` JSON-LD block containing a
placeholder address. Fill in the real address and hours — this is what feeds
the Google Business Profile and local search results.

---

## Deploying

Vercel, from this repository:

1. [vercel.com/new](https://vercel.com/new) → import `abhi15072004/gems-profino`
2. Framework preset: **Other**. No build command, no output directory.
3. Deploy. Every push to `main` redeploys automatically, and pull requests get
   their own preview URL.

Add the client's domain under Project → Settings → Domains, then point the
registrar's DNS at the records Vercel shows. The client controls the domain, so
they will either need to add those records or grant registrar access.

---

## Accessibility and robustness

- Scroll reveal is progressive enhancement. An inline script in `<head>` adds
  a `.js` class, and only then does CSS hide the blocks it animates in — so if
  scripting fails, every block is simply visible. **Do not remove that inline
  script**, and do not hide content in CSS without the same guard.
- Keyboard focus is visible throughout, and `prefers-reduced-motion` disables
  all animation.
- The form validates without relying on native browser bubbles, so every error
  is announced in the page.
- Placeholder markers use both a colour tint and a dotted rule, so they do not
  depend on colour alone.

---

## Known limitations

- The logo was extracted from a WhatsApp JPEG. It is sharp enough at the sizes
  used here, but the original vector file would be better — particularly for
  print or a larger hero treatment.
- URLs keep their `.html` extension. This is deliberate and matches the
  canonical tags. Enabling `cleanUrls` in `vercel.json` later would also
  require updating every internal link and canonical.
- Web3Forms' free tier allows 250 submissions per month. If campaigns push
  past that, move to a paid tier or a small serverless function.

---

## A note on caching

`assets/css/styles.css` and `assets/js/main.js` are served with
`max-age=0, must-revalidate`, deliberately. Their filenames carry no content
hash, so caching them immutably would leave returning visitors on an old build
for up to a year — an edit to the stylesheet would simply never reach them.
ETags keep the revalidation cheap, and Vercel's CDN still serves from the edge.

If you ever add a build step that fingerprints filenames
(`styles.a1b2c3.css`), then — and only then — switch those back to
`max-age=31536000, immutable`.

Images are cached for a week. To change one immediately, rename the file and
update the reference rather than relying on cache expiry.
