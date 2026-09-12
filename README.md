# Simpsons Breakdown Recovery Services Ltd — Website

A fast, static, multi-page website for a 24/7 breakdown recovery business in
Edgbaston, Birmingham. Built as an APX Digital demo and proposal piece.

- **Demo:** https://simpsons-recovery-birmingham.netlify.app
- **Repository:** https://github.com/Jamiemac9/simpsons-breakdown-recovery
- **Production domain (target):** https://www.simpsonsbreakdownrecovery.co.uk

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

Both read the master artwork from the Desktop asset folder; update the paths at
the top of each file if the source moves.

---

## Going live on the customer's domain

Everything canonical in the HTML already points at
`https://www.simpsonsbreakdownrecovery.co.uk`. To switch over:

1. **Remove the demo noindex.** In `netlify.toml`, delete the block between
   `DEMO ONLY — remove this block` and `END DEMO ONLY`. *If you skip this, the
   live site will be invisible to Google.*

2. **Confirm the domain** in `site_config.py` (`SITE_URL`), then run the four
   build commands above and redeploy.

3. **Update the Google Business Profile** website field to the new domain.

4. **Submit the sitemap** in Google Search Console:
   `https://www.simpsonsbreakdownrecovery.co.uk/sitemap.xml`

### Hosting options

The site is plain static files, so any of these work:

- **Cloudflare Pages** — best fit. Free, global CDN, free SSL, and it can hold
  the domain's DNS. To deploy: connect the GitHub repo, leave the build command
  empty, set the output directory to `/`. Add the custom domain in Pages →
  Custom domains, then point the registrar's nameservers at Cloudflare.
  Runtime headers live in a `_headers` file (not `netlify.toml`).
- **Namecheap** — fine as the *registrar*, but its shared hosting is slower and
  you would lose the free CDN. Recommend using Namecheap only to buy/renew the
  domain and pointing DNS at Cloudflare.
- **Existing host** — the customer already owns
  `simpsonsbreakdownrecovery.co.uk` (it runs the current WordPress site). The
  cheapest path is to deploy here and repoint DNS, rather than buying a domain.

---

## Verification tooling

Run these after any change. All three are in the repo.

```bash
python3 check_links.py                       # every internal link + anchor resolves
node smoke.mjs <url> home                    # homepage behaviour (25 assertions)
node smoke.mjs <url> area                    # location page behaviour (22 assertions)
node shoot.mjs <url> out.png <w> <h>         # screenshot at a true device width
node shoot.mjs <url> out.png 1440 900 --at="#work"   # screenshot one section
```

Regenerate the proposal screenshots (written to `demo/`, not committed):

```bash
B=https://simpsons-recovery-birmingham.netlify.app
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
