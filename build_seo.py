#!/usr/bin/env python3
"""Generate robots.txt and sitemap.xml from site_config.

Run after build_areas.py so the sitemap matches the pages that actually exist:

    python3 build_areas.py && python3 build_seo.py
"""

import pathlib
import datetime

import site_config as cfg

ROOT = pathlib.Path(__file__).resolve().parent


def build_robots() -> str:
    return f"""# {cfg.SITE_NAME}
# {cfg.SITE_URL}
#
# The site is fully crawlable — it is the live site, not a demo. The noindex
# header that guarded the Netlify preview has been removed (see netlify.toml).
# /404.html is disallowed because it is an error page with no search value.

User-agent: *
Allow: /
Disallow: /404.html

# Nothing here needs throttling, but the aggressive scrapers get blocked.
User-agent: AhrefsBot
Crawl-delay: 10

User-agent: SemrushBot
Crawl-delay: 10

Sitemap: {cfg.SITE_URL}/sitemap.xml
"""


def build_sitemap() -> str:
    today = datetime.date.today().isoformat()
    entries = []

    # Homepage: highest priority, changes often.
    entries.append((f"{cfg.SITE_URL}/", today, "weekly", "1.0"))

    # Location pages: the main local-SEO surface.
    for slug in cfg.AREA_SLUGS:
        entries.append((f"{cfg.SITE_URL}/areas/{slug}.html", today, "monthly", "0.9"))

    body = "\n".join(
        f"""  <url>
    <loc>{loc}</loc>
    <lastmod>{lastmod}</lastmod>
    <changefreq>{freq}</changefreq>
    <priority>{prio}</priority>
  </url>"""
        for loc, lastmod, freq, prio in entries
    )

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{body}
</urlset>
"""


def main() -> None:
    robots = ROOT / "robots.txt"
    robots.write_text(build_robots(), encoding="utf-8")
    print(f"wrote {robots}")

    sitemap = ROOT / "sitemap.xml"
    sitemap.write_text(build_sitemap(), encoding="utf-8")
    print(f"wrote {sitemap} ({len(cfg.AREA_SLUGS) + 1} URLs)")


if __name__ == "__main__":
    main()