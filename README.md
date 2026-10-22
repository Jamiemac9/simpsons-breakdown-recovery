# Simpsons Breakdown Recovery Services Ltd — Website

A fast, static, multi-page website for a 24/7 breakdown recovery business in
Edgbaston, Birmingham. Built as an APX Digital demo and proposal piece.

- **Live:** https://simpsonsbreakdownrecovery.co.uk
- **Repository:** https://github.com/Jamiemac9/simpsons-breakdown-recovery

---

## What this is

A hand-built static site — no framework, no build step, no database, no
dependencies. Every page is a real HTML file, so it loads fast on a poor mobile
connection (the exact situation a stranded driver is in) and can be hosted
anywhere that serves files.

| | |
|---|---|
| Pages | 14 (homepage, 404, 12 location pages) |
| CSS | 1 file, ~31 KB |
| JS | 1 file, ~6 KB, vanilla, no libraries |
| Fonts | 2 families, preconnected, `display=swap` |
| Images | Optimised; hero background pre-blurred at build time |
| Runtime dependencies | None |

---

## Editing content

Most content is generated, not hand-edited. Change the data file and rebuild.

### Site-wide facts (phone, address, domain, rating, services)

Edit `site_config.py`, then rebuild everything:

```bash
python3 build_areas.py          # regenerate the 12 location pages
python3 build_seo.py            # regenerate robots.txt + sitemap.xml
python3 print_home_head.py      # regenerate the homepage SEO block
python3 apply_home_head.py      # inject it into index.html
```

### Location pages

Edit `areas_data.py` — one record per area — then run `python3 build_areas.py`.

Each record holds the postcodes, distance, response time, main roads, the
route-by-route access notes, the callouts the business actually gets there, a
local-knowledge paragraph and the area's FAQs.

> **Do not hand-edit the files in `areas/`.** They are generated and will be
> overwritten on the next build.

### Homepage

`index.html` is hand-authored because its copy is bespoke. Everything between
the `<!-- SEO:START -->` and `<!-- SEO:END -->` markers is generated — edit
`site_config.py` or `print_home_head.py` and re-run the two commands above.

### Brand assets

```bash
python3 build_logo.py    # logo lockup, favicons, OG share card
python3 build_hero.py    # pre-blurred hero background
```

`build_logo.py` reads the master artwork from the Desktop asset folder; update
the path at the top if the source moves. `build_hero.py` reads
`assets/hero-source.jpg`, which is the one master asset kept **in this repo** —
the client's asset folder no longer exists, so the repo copy is the only one
that survives.

> After re-running `build_hero.py`, bump the `?v=` query on both hero
> background URLs in `css/style.css`. Images are cached for a week under a
> stable filename, so without a new URL returning visitors keep the old hero.

### Analytics and the agency credit

Both are site-wide and driven from `site_config.py`:

- `GA4_ID` — the GA4 measurement ID. `seo.analytics()` writes the gtag snippet
  into the head of every page (homepage block, area pages, 404). Set it to `""`
  to drop the tag everywhere.
- `AGENCY_NAME` / `AGENCY_URL` — the "Website made by APX Digital" footer
  credit, emitted by `seo.agency_credit()`.

After changing either, rerun the full rebuild (`build_areas.py`,
`print_home_head.py`, `apply_home_head.py`).

> **Consent:** the GA4 tag fires unconditionally, exactly as supplied. GA4 sets
> cookies and UK PECR needs consent for those first. If the site is to collect
> consent, this needs Consent Mode (default denied) plus a banner before the tag
> is announced as compliant.

---

## Production — Cloudflare

The site is live on **https://simpsonsbreakdownrecovery.co.uk**.

`SITE_URL` in `site_config.py` is the single source of truth for every
canonical, the sitemap, Open Graph URLs and schema. After changing it, rebuild
with the four commands above before deploying.

### Deploy

```bash
npx wrangler login          # once per machine
npx wrangler deploy         # uploads static assets + _headers
```

Config lives in `wrangler.jsonc`. Cache and security headers live in `_headers`
(Cloudflare parses that file at deploy time; it is not served publicly).
`netlify.toml` is legacy only.

`audit.py` and `audit_live.py` assert that no sitewide `X-Robots-Tag: noindex`
header is present — an inverted guard so a demo block cannot silently
de-index production.

### Domain history

The site briefly used the bridge domain `sb24tow.co.uk` while the real domain
was still with a third-party management company. That cutover is finished.
Do not point `SITE_URL`, citations or Search Console properties back at the
bridge.

---

## Verification tooling

Run these after any change. All are in the repo.

```bash
python3 check_links.py                       # every internal link + anchor resolves
python3 audit.py                             # 790 on-page checks across all 14 pages
node smoke.mjs <url> home                    # homepage behaviour (29 assertions)
node smoke.mjs <url> area                    # location page behaviour (26 assertions)
node shoot.mjs <url> out.png <w> <h>         # screenshot at a true device width
node shoot.mjs <url> out.png 1440 900 --at="#work"   # screenshot one section
```

Changes to the hero image, the service rows or the footer have their own
measurement tools, because "looks fine" is not evidence:

```bash
# Overlap geometry for the service rows at 1001-1728px + hero backdrop capture.
# Needs Playwright; run it with a python that has it installed.
~/Sites/scrape-lead-finder/.venv/bin/python diag_layout.py http://127.0.0.1:8811/index.html
python3 check_hero_contrast.py               # WCAG AA for h1 + lead on the backdrop
python3 verify_analytics.py <url>            # GA4 loads, configures, credit renders
~/Sites/scrape-lead-finder/.venv/bin/python shoot_changes.py   # before/after evidence
```

`diag_layout.py` measures each service-row CTA button against its grid column and
the paragraph beside it — the original fixed 168px column made the "Emergency
motorway tow" button overrun by 57px and collide with the copy by 39px.
`check_hero_contrast.py` measures the real backdrop pixels under the hero text;
it exits non-zero if the white heading or the lead paragraph drops below 4.5:1.
`shoot_changes.py` rebuilds the "before" state from git and injected CSS rather
than staged files, so the comparison cannot flatter the change.

Regenerate the proposal screenshots (written to `demo/`, not committed):

```bash
B=https://simpsonsbreakdownrecovery.co.uk
node shoot.mjs "$B/"                    demo/01-desktop-hero.png 1440 900
node shoot.mjs "$B/"                    demo/02-mobile-hero.png    390 844
node shoot.mjs "$B/"                    demo/03-our-work.png      1440 1000 --at="#work"
node shoot.mjs "$B/"                    demo/04-areas.png         1440 1000 --at="#areas"
node shoot.mjs "$B/areas/solihull-breakdown-recovery.html" demo/05-area-page.png 1440 1000
node shoot.mjs "$B/"                    demo/06-modal.png         1440 900  --keep-modal
```

`smoke.mjs` and `shoot.mjs` drive headless Chrome over CDP. Both need a browser
listening on port 9333 first:

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu --remote-debugging-port=9333 \
  --user-data-dir=/tmp/simpsons-cdp about:blank &
```

**Why CDP rather than `--window-size`:** macOS clamps a headless Chrome window
to about 500px, so a `--window-size=390` screenshot is really a 500px render
cropped to 390px. That fakes clipping that isn't there and hides real overflow.
`shoot.mjs` sets device metrics explicitly and reports the true scroll width.

---

## Notes for whoever picks this up

- **`Recovery2.png` in the customer's asset folder is not their truck.** It
  shows a vehicle branded *"TURBO CAR…"* — another firm's flatbed. It is
  deliberately excluded from the site.
- **Only verified social profiles are in the schema.** `sameAs` currently lists
  only the X account. Add Facebook, Instagram and TikTok URLs to
  `SOCIAL_PROFILES` in `site_config.py` once the owner confirms them — wrong
  URLs actively harm entity matching in search.
- **Photo captions describe what is genuinely in each image.** The NottyBites
  catering trailer and the Finning CAT service truck are real jobs visible in
  the photography; nothing has been invented.
- **Response times are the business's own figures** (30–45 minute average local
  arrival, 20-mile radius, 229 Google reviews, trading since 2005). No
  performance claim on the site was invented for the build.
