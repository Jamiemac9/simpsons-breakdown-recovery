#!/usr/bin/env python3
"""Generate the Simpsons Breakdown Recovery location pages.

Single source of truth for the area-page template, so all twelve pages share
the same header, footer, dock, floating WhatsApp button and design-system
classes as index.html.

Content comes from `areas_data.py`. Run this after editing that file:

    python3 build_areas.py
"""

import html
import json
import os
import pathlib

import site_config as cfg
import seo
from areas_data import AREAS, AREA_BY_SLUG

BASE_DIR = pathlib.Path(__file__).resolve().parent
OUT_DIR = BASE_DIR / "areas"

WHATSAPP = cfg.WHATSAPP_NUMBER
PHONE = cfg.PHONE_DISPLAY
PHONE_TEL = cfg.PHONE_TEL
WORK_TEASERS = [
    (
        "work-van-recovery.webp", 1100, 1100,
        "Simpsons Breakdown Recovery flatbed loading a white Renault Trafic work van in Birmingham",
        "Van recovery",
        "Work vans and panel vans winched onto the flatbed and taken to your garage.",
    ),
    (
        "work-cat-service-truck.webp", 960, 720,
        "Plant service truck with a mounted crane loaded on a Simpsons flatbed recovery truck",
        "Commercial",
        "Heavy and awkward commercial loads, recovered from dealer yards and sites.",
    ),
    (
        "work-trailer-load.webp", 1100, 1100,
        "Catering trailer loaded on a Simpsons Breakdown Recovery flatbed at a showground",
        "Trailers",
        "Catering units, box trailers and event transport, booked in advance.",
    ),
]

# Photography reused from the homepage "Our Work" section. Each entry is
# (filename, width, height, alt text, badge, caption).


def wa(message: str) -> str:
    return "https://wa.me/" + WHATSAPP + "?text=" + message.replace(" ", "%20")


def e(text: str) -> str:
    """HTML-escape for use in element text."""
    return html.escape(text, quote=False)


def build_faqs(area: dict) -> list:
    """The four standing questions plus the area's own specific ones."""
    standing = [
        (
            f"How quickly can you reach {area['name']}?",
            f"Typically {area['eta']} from your call, depending on traffic and which truck is "
            f"nearest. We run a 20-mile radius from our Edgbaston depot and {area['name']} sits "
            f"{area['distance']}. When you ring {PHONE} you speak to a driver who can see where our "
            f"vehicles are and give you a genuine arrival window rather than a best guess.",
        ),
        (
            f"Which {area['name']} postcodes do you cover?",
            f"We cover {area['postcodes']}, along with the surrounding streets and the main routes "
            f"through the area — {area['roads']}. If you are just outside these postcodes, call with "
            f"your location and we will tell you straight away whether we can get to you.",
        ),
        (
            f"Do you charge more for nights or weekends in {area['name']}?",
            "No. We quote a fixed price before the truck is dispatched, whatever the hour. There is "
            "no after-hours loading added later, no hidden mileage surcharge, and no charge for "
            "getting a price from us.",
        ),
        (
            f"Can you get a car out of a car park in {area['name']}?",
            "Yes. Multi-storey and basement car parks are one of our specialities. We carry "
            "low-profile wheel skates, dollies and compact winching equipment, so a vehicle that "
            "will not start or will not roll can be moved out without damage to the bodywork, the "
            "wheels or the building.",
        ),
    ]
    return standing + list(area["faqs"])


def page_title(area: dict) -> str:
    """SERP title, kept under Google's ~60 character truncation point.

    Longer area names ("City Centre Birmingham") would push the title past the
    limit, so those fall back to a shorter brand suffix rather than being
    truncated mid-word in the results page.
    """
    name = area.get("title_name", area["name"])
    full = f"Breakdown Recovery {name} | 24/7 Simpsons Recovery"
    if len(full) <= 60:
        return full
    return f"Breakdown Recovery {name} | 24/7 Simpsons"


def page_description(area: dict) -> str:
    """Meta description, kept under 160 characters so it is not cut off."""
    return (
        f"24/7 breakdown recovery in {area['name']}. Typical arrival {area['eta']}, "
        f"fixed prices and 229 five-star reviews. Call Simpsons on {PHONE}."
    )


def build_jsonld(area: dict, faqs: list) -> str:
    """Structured data for a location page, assembled from the shared builders."""
    url = f"{cfg.SITE_URL}/areas/{area['slug']}.html"
    title = page_title(area)
    description = page_description(area)
    return seo.graph(
        seo.business_node(page_url=url, name_suffix=area["name"], area_name=area["name"]),
        seo.website_node(),
        seo.web_page_node(url=url, title=title, description=description),
        seo.breadcrumb_node(url=url, items=[
            ("Home", f"{cfg.SITE_URL}/"),
            ("Areas Covered", f"{cfg.SITE_URL}/#areas"),
            (f"{area['name']} breakdown recovery", None),
        ]),
        seo.faq_node(url=url, faqs=faqs),
    )


def build_page(area: dict) -> str:
    faqs = build_faqs(area)
    page_url = f"{cfg.SITE_URL}/areas/{area['slug']}.html"
    page_head_title = page_title(area)
    page_desc = page_description(area)
    wa_area = wa(
        f"Hello Simpsons Recovery, I have broken down in {area['name']}. "
        f"Here is my location:"
    )
    wa_generic = wa("Hello Simpsons Recovery, I need help with my vehicle.")

    nearby_tiles = "\n".join(
        f"""        <a class="area-tile" href="{slug}.html">
          <span>
            <span class="area-tile__name">{e(AREA_BY_SLUG[slug]['name'])}</span>
            <span class="area-tile__meta">{e(AREA_BY_SLUG[slug]['distance'])}</span>
          </span>
          <span class="area-tile__arrow" aria-hidden="true">&rarr;</span>
        </a>"""
        for slug in area["nearby"]
        if slug in AREA_BY_SLUG
    )

    nearby_links = "\n".join(
        f'          <li><a href="{slug}.html">{e(AREA_BY_SLUG[slug]["name"])}</a></li>'
        for slug in area["nearby"]
        if slug in AREA_BY_SLUG
    )

    route_rows = "\n".join(
        f"""          <li>
            <strong class="text-cyan">{e(road)}</strong>
            <span class="muted small">{e(note)}</span>
          </li>"""
        for road, note in area["routes"]
    )

    callout_items = "\n".join(
        f"            <li>{e(item)}</li>" for item in area["callouts"]
    )

    faq_items = "\n".join(
        f"""        <div class="faq__item{' is-open' if i == 0 else ''}">
          <button class="faq__q" type="button">
            <span>{e(q)}</span>
            <span class="faq__chev" aria-hidden="true">▾</span>
          </button>
          <div class="faq__a"><div><p>{e(a)}</p></div></div>
        </div>"""
        for i, (q, a) in enumerate(faqs)
    )

    work_cards = "\n".join(
        f"""        <article class="work-card">
          <div class="work-card__media">
            <img src="../images/{fname}" width="{w}" height="{h}" loading="lazy" decoding="async"
                 alt="{e(alt)}">
            <span class="work-card__badge">{e(badge)}</span>
          </div>
          <div class="work-card__body">
            <p>{e(caption)}</p>
            <div class="work-card__meta"><span>Birmingham &amp; West Midlands</span><span>Flatbed recovery</span></div>
          </div>
        </article>"""
        for fname, w, h, alt, badge, caption in WORK_TEASERS
    )

    return f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(page_head_title)}</title>
  <meta name="description" content="{e(page_desc)}">

{seo.head_meta(url=page_url, title=page_head_title, description=page_desc,
               geo_placename=f"{e(area['name'])}, Birmingham")}

{seo.favicon_links('../')}
  <link rel="preload" as="image" href="../images/logo.webp">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@700;800;900&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../css/style.css">

  <script type="application/ld+json">
{build_jsonld(area, faqs)}
  </script>
</head>
<body>

<a class="skip-link" href="#main">Skip to content</a>

<div class="ticker">
  <div class="shell ticker__inner">
    <div class="ticker__left">
      <span class="ticker__live"><span class="dot"></span> {e(area['name'])} recovery on call</span>
      <span class="ticker__detail">{e(area['postcodes'])} &bull; typical arrival {e(area['eta'])}</span>
    </div>
    <span class="ticker__note">Open 24 hours, 7 days a week</span>
  </div>
</div>

<header class="site-header">
  <div class="shell site-header__inner">

    <a href="../index.html" class="brand" aria-label="Simpsons Breakdown Recovery Services Ltd — home">
      <span class="brand__plate">
        <img class="brand__logo" src="../images/logo.webp" width="661" height="143" alt="Simpsons Breakdown Recovery Services Ltd" fetchpriority="high" decoding="async">
      </span>
    </a>

    <nav class="nav" aria-label="Main">
      <a href="../index.html">Home</a>
      <a href="../index.html#services">Services</a>
      <a href="../index.html#areas" class="is-active">Areas Covered</a>
      <a href="../index.html#work">Our Work</a>
      <a href="../index.html#faq">FAQ</a>
    </nav>

    <div class="header-actions">
      <a href="tel:{PHONE.replace(' ', '')}" class="btn btn--red btn--sm">
        <svg class="icon" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/></svg>
        <span class="nowrap">{PHONE}</span>
      </a>
      <button class="menu-toggle" id="menuToggle" type="button" aria-label="Menu" aria-expanded="false" aria-controls="mobileNav">
        <span></span><span></span><span></span>
      </button>
    </div>
  </div>

  <nav class="mobile-nav" id="mobileNav" aria-label="Mobile">
    <a href="../index.html">Home</a>
    <a href="../index.html#services">Services</a>
    <a href="../index.html#areas">Areas Covered</a>
    <a href="../index.html#work">Our Work</a>
    <a href="../index.html#faq">FAQ</a>
    <div class="mobile-nav__cta">
      <a href="tel:{PHONE.replace(' ', '')}" class="btn btn--red btn--block">Call {PHONE}</a>
    </div>
  </nav>
</header>

<main id="main">

  <nav class="breadcrumb" aria-label="Breadcrumb">
    <div class="shell breadcrumb__inner">
      <a href="../index.html">Home</a>
      <span class="breadcrumb__sep" aria-hidden="true">/</span>
      <a href="../index.html#areas">Areas Covered</a>
      <span class="breadcrumb__sep" aria-hidden="true">/</span>
      <span aria-current="page">{e(area['name'])} breakdown recovery</span>
    </div>
  </nav>

  <section class="hero">
    <div class="hero__bg" aria-hidden="true"></div>
    <div class="hero__scrim" aria-hidden="true"></div>

    <div class="shell hero__inner">
      <span class="pill"><span class="dot"></span> {e(area['distance'])} &bull; 20-mile radius</span>

      <h1>Breakdown recovery <span class="hero__accent">{e(area['name'])}</span></h1>

      <p class="lead hero__lead">{e(area['intro'])}</p>

      <div class="hero__cta">
        <a href="tel:{PHONE.replace(' ', '')}" class="btn btn--red btn--lg">
          <svg class="icon" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/></svg>
          Call {PHONE}
        </a>
        <a href="{wa_area}" target="_blank" rel="noopener" class="btn btn--green btn--lg">
          <svg class="icon" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path d="M12.03 6.17c-3.18 0-5.76 2.59-5.76 5.77 0 1.3.38 2.27 1.02 3.28l-.58 2.13 2.18-.57c.98.58 1.91.93 3.14.93 3.18 0 5.77-2.59 5.77-5.77 0-3.19-2.58-5.77-5.77-5.77zm3.39 8.24c-.14.4-.84.77-1.17.82-.3.05-.68.06-1.09-.07-.25-.08-.58-.19-.99-.36-1.74-.75-2.87-2.5-2.96-2.62-.09-.11-.71-.94-.71-1.79s.45-1.27.61-1.45c.16-.17.35-.22.46-.22h.33c.11 0 .25-.04.39.3.14.35.49 1.2.53 1.29.04.09.07.19.01.3-.06.12-.09.19-.17.29l-.26.3c-.09.09-.18.18-.08.36.1.17.45.74.96 1.2.66.59 1.22.77 1.4.86.17.09.27.07.37-.04.1-.12.43-.51.55-.68.12-.17.23-.14.39-.09.16.06 1.01.48 1.18.56.17.09.29.13.33.2.05.07.05.42-.1.83z"/></svg>
          Send WhatsApp location
        </a>
      </div>

      <a class="review-badge" href="https://share.google/FIO6KZSxKO3p8ohXX" target="_blank" rel="noopener">
        <span class="stars" aria-hidden="true">★★★★★</span>
        <span><strong style="color:#fff">4.9 rating</strong> &bull; 229 Google reviews</span>
        <span class="review-badge__link">Read them &rarr;</span>
      </a>
    </div>
  </section>

  <section class="metrics">
    <div class="shell grid grid-4">
      <div class="metric">
        <span class="metric__icon">
          <svg class="icon" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
        </span>
        <span>
          <span class="metric__value">{e(area['eta'])}</span>
          <span class="metric__label">Typical {e(area['name'])} arrival</span>
        </span>
      </div>
      <div class="metric">
        <span class="metric__icon metric__icon--amber">
          <svg class="icon" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true"><path d="M9.05 2.93c.3-.92 1.6-.92 1.9 0l1.07 3.29a1 1 0 00.95.69h3.46c.97 0 1.37 1.24.59 1.81l-2.8 2.03a1 1 0 00-.36 1.12l1.07 3.29c.3.92-.76 1.69-1.54 1.12l-2.8-2.03a1 1 0 00-1.18 0l-2.8 2.03c-.78.57-1.84-.2-1.54-1.12l1.07-3.29a1 1 0 00-.36-1.12L2.98 8.72c-.78-.57-.38-1.81.59-1.81h3.46a1 1 0 00.95-.69l1.07-3.29z"/></svg>
        </span>
        <span>
          <span class="metric__value">229 reviews</span>
          <span class="metric__label">Five-star Google rated</span>
        </span>
      </div>
      <div class="metric">
        <span class="metric__icon metric__icon--green">
          <svg class="icon" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.6-4A12 12 0 0112 2.9 12 12 0 013.4 6 12 12 0 003 9c0 5.6 3.8 10.3 9 11.6 5.2-1.3 9-6 9-11.6 0-1-.1-2-.4-3z"/></svg>
        </span>
        <span>
          <span class="metric__value">Est. 2005</span>
          <span class="metric__label">Trading since</span>
        </span>
      </div>
      <div class="metric">
        <span class="metric__icon">
          <svg class="icon" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.7 16.7L13.4 20.9a2 2 0 01-2.8 0l-4.3-4.2a8 8 0 1111.4 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
        </span>
        <span>
          <span class="metric__value">{e(area['postcodes'])}</span>
          <span class="metric__label">Postcodes covered</span>
        </span>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="shell">
      <div class="section-head">
        <span class="eyebrow">How we get to you</span>
        <h2>Recovering in {e(area['name'])}</h2>
        <p class="muted">{e(area['approach'])}</p>
      </div>

      <div class="grid grid-2">
        <article class="panel">
          <h3 class="mb-md">The roads we know here</h3>
          <ul class="route-list">
{route_rows}
          </ul>
        </article>

        <article class="panel">
          <h3 class="mb-sm">What we get called for</h3>
          <ul class="check-list mb-lg">
{callout_items}
          </ul>
          <h3 class="mb-sm">Landmarks and areas covered</h3>
          <p class="muted small mb-0">{e(area['landmarks'])}.</p>
        </article>
      </div>

      <div class="panel panel--glow mt-lg">
        <h3 class="mb-sm">Local knowledge: what makes {e(area['name'])} different</h3>
        <p class="muted mb-0">{e(area['local_note'])}</p>
      </div>
    </div>
  </section>

  <section class="section section--alt">
    <div class="shell">
      <div class="section-head">
        <span class="eyebrow">What we can recover for you</span>
        <h2>Services in {e(area['name'])}</h2>
        <p class="muted">Cars, vans, motorbikes, 4x4s, non-runners, trailers and commercial vehicles — all recovered on the flatbed, fully insured.</p>
      </div>

      <div class="stack">
        <article class="service-row">
          <div class="service-row__num">01</div>
          <div class="service-row__name">
            <h3>Car recovery {e(area['name'])}</h3>
            <span class="service-row__tag">Most requested</span>
          </div>
          <p class="service-row__desc">Non-starters, clutch and gearbox failures, suspension damage and cars that cannot be driven — recovered to whichever garage, dealer or driveway you choose.</p>
          <div class="service-row__cta"><a href="tel:{PHONE.replace(' ', '')}" class="btn btn--red">Call for a tow</a></div>
        </article>

        <article class="service-row">
          <div class="service-row__num">02</div>
          <div class="service-row__name">
            <h3>Van &amp; commercial recovery</h3>
            <span class="service-row__tag">Trades and fleets</span>
          </div>
          <p class="service-row__desc">Transit, Vivaro, Sprinter, Boxer and minibus-class vehicles recovered loaded, so your tools and stock travel with you rather than being unloaded at the roadside.</p>
          <div class="service-row__cta"><a href="tel:{PHONE.replace(' ', '')}" class="btn btn--red">Call for a van tow</a></div>
        </article>

        <article class="service-row">
          <div class="service-row__num">03</div>
          <div class="service-row__name">
            <h3>Low-clearance &amp; underground recovery</h3>
            <span class="service-row__tag">Difficult access</span>
          </div>
          <p class="service-row__desc">Wheel skates, dollies and compact winching for multi-storey and basement car parks, seized brakes and locked steering — the jobs other firms turn down.</p>
          <div class="service-row__cta"><a href="../index.html#contact" class="btn btn--ghost">Ask about access</a></div>
        </article>

        <article class="service-row">
          <div class="service-row__num">04</div>
          <div class="service-row__name">
            <h3>Jump starts, batteries &amp; roadside help</h3>
            <span class="service-row__tag">12V and 24V</span>
          </div>
          <p class="service-row__desc">Heavy-duty boosters for a flat battery at home or at work, freeing a seized wheel or brake disc, and taking a flat-tyre vehicle to your preferred fitter.</p>
          <div class="service-row__cta"><a href="tel:{PHONE.replace(' ', '')}" class="btn btn--ghost">Get roadside help</a></div>
        </article>

        <article class="service-row">
          <div class="service-row__num">05</div>
          <div class="service-row__name">
            <h3>Trailers, catering units &amp; plant</h3>
            <span class="service-row__tag">Planned transport</span>
          </div>
          <p class="service-row__desc">Catering trailers, box trailers and commercial plant service vehicles moved between sites, events and yards — normally booked ahead of time rather than as an emergency.</p>
          <div class="service-row__cta"><a href="tel:{PHONE.replace(' ', '')}" class="btn btn--ghost">Book transport</a></div>
        </article>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="shell">
      <div class="section-head">
        <span class="eyebrow">Real jobs, real trucks</span>
        <h2>Our work</h2>
        <p class="muted">Genuine jobs from across Birmingham and the West Midlands — the same trucks that cover {e(area['name'])}.</p>
      </div>

      <div class="grid grid-3">
{work_cards}
      </div>

      <div class="center mt-lg">
        <a href="../index.html#work" class="btn btn--ghost">See more of our work &rarr;</a>
      </div>
    </div>
  </section>

  <section class="section section--alt">
    <div class="shell">
      <div class="section-head">
        <span class="eyebrow">Verified Google reviews</span>
        <h2>What customers say</h2>
        <p class="muted">Unedited reviews from drivers we have recovered across Birmingham and the West Midlands.</p>
      </div>

      <div class="grid grid-3">
        <article class="review">
          <div>
            <div class="review__head">
              <div class="review__who">
                <span class="avatar">MG</span>
                <span>
                  <span class="review__name">Matt Griffiths</span>
                  <span class="review__source">Google review</span>
                </span>
              </div>
              <span class="stars" aria-hidden="true">★★★★★</span>
            </div>
            <p class="review__quote">“Impeccable service from Simpsons breakdown recovery. Really tricky job getting my non starter car out of an underground garage with a low ceiling and tight corners. Both Dean and Jaden handled the task expertly and provided an excellent and freindly service.”</p>
          </div>
          <span class="review__tag">✓ Low-ceiling extraction</span>
        </article>

        <article class="review">
          <div>
            <div class="review__head">
              <div class="review__who">
                <span class="avatar" style="background:#be185d">SM</span>
                <span>
                  <span class="review__name">Stasenko ML</span>
                  <span class="review__source">Google review</span>
                </span>
              </div>
              <span class="stars" aria-hidden="true">★★★★★</span>
            </div>
            <p class="review__quote">“Friendly and quick service. Had a break down, which obviously made my day bad. But the guy overturned my mood into a good one. The price was very good too, compared to others, I would even say that the price was amazing.”</p>
          </div>
          <span class="review__tag">✓ Fair, competitive pricing</span>
        </article>

        <article class="review">
          <div>
            <div class="review__head">
              <div class="review__who">
                <span class="avatar" style="background:#047857">JL</span>
                <span>
                  <span class="review__name">Joshua L</span>
                  <span class="review__source">Google review</span>
                </span>
              </div>
              <span class="stars" aria-hidden="true">★★★★★</span>
            </div>
            <p class="review__quote">“Last minute call after I got a flat tyre and needed to get home. Extremely punctual, professional, and all round great service from Dean!!! Definitely a number I'll keep saved for if I'm in need of recovery again!”</p>
          </div>
          <span class="review__tag">✓ Last-minute callout</span>
        </article>
      </div>

      <div class="center mt-lg">
        <a href="https://share.google/FIO6KZSxKO3p8ohXX" target="_blank" rel="noopener" class="btn btn--blue">Read all 229 reviews on Google</a>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="shell">
      <div class="section-head">
        <span class="eyebrow">Straightforward and stress-free</span>
        <h2>How a {e(area['name'])} recovery works</h2>
      </div>

      <div class="grid grid-3">
        <article class="panel">
          <div class="stat__value mb-sm">01</div>
          <h3 class="mb-sm">Call or send your pin</h3>
          <p class="muted small mb-0">Ring <a href="tel:{PHONE.replace(' ', '')}" class="text-red"><strong>{PHONE}</strong></a> or WhatsApp your location. You speak to Dean or an operator on the road, not a call centre.</p>
        </article>
        <article class="panel">
          <div class="stat__value mb-sm">02</div>
          <h3 class="mb-sm">Fixed price, real ETA</h3>
          <p class="muted small mb-0">We agree the price before anything moves, check live traffic and give you a realistic arrival window for {e(area['name'])} — {e(area['eta'])}.</p>
        </article>
        <article class="panel">
          <div class="stat__value mb-sm">03</div>
          <h3 class="mb-sm">Loaded and delivered</h3>
          <p class="muted small mb-0">Your vehicle is winched onto the tilt-and-slide bed, strapped down and taken wherever you want it — home, garage, dealership or tyre fitter.</p>
        </article>
      </div>
    </div>
  </section>

  <section class="section section--alt">
    <div class="shell">
      <div class="section-head">
        <span class="eyebrow">Nearby</span>
        <h2>We also cover</h2>
        <p class="muted">Areas close to {e(area['name'])} that we recover in every day.</p>
      </div>

      <div class="grid grid-4">
{nearby_tiles}
        <a class="area-tile" href="../index.html#areas">
          <span>
            <span class="area-tile__name">All areas</span>
            <span class="area-tile__meta">20-mile radius from Edgbaston</span>
          </span>
          <span class="area-tile__arrow" aria-hidden="true">&rarr;</span>
        </a>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="shell">
      <div class="section-head">
        <span class="eyebrow">Common questions</span>
        <h2>{e(area['name'])} recovery FAQs</h2>
      </div>

      <div class="faq">
{faq_items}
      </div>
    </div>
  </section>

  <section class="section section--deep">
    <div class="shell center">
      <span class="eyebrow">Broken down in {e(area['name'])} right now?</span>
      <h2 class="mb-md">Speak to a local recovery operator</h2>
      <p class="muted mb-lg">Tell us where you are and what you're driving. We'll confirm the quickest practical next step and a fixed price.</p>
      <div class="row" style="justify-content:center">
        <a href="tel:{PHONE.replace(' ', '')}" class="btn btn--red btn--lg">Call {PHONE}</a>
        <a href="{wa_area}" target="_blank" rel="noopener" class="btn btn--green btn--lg">Send WhatsApp location</a>
      </div>
    </div>
  </section>

</main>

<div class="modal" id="legalModal" role="dialog" aria-modal="true" aria-hidden="true">
  <div class="modal__box">
    <button class="modal__close" type="button" data-close-legal aria-label="Close">&times;</button>
    <h3 id="legalTitle" class="mb-md">Terms &amp; conditions</h3>
    <div class="muted small">
      <h4 class="mb-sm">Terms of service</h4>
      <p class="mb-md">
        Simpsons Breakdown Recovery Services Ltd provides 24/7 vehicle recovery, towing and roadside
        assistance across Birmingham and the surrounding 20-mile radius. Prices are agreed before the
        recovery vehicle is dispatched. Customers must ensure the vehicle is accessible and that keys are
        available. Any specific hazard — locked steering, seized wheels, severe damage or restricted
        clearance — must be disclosed when booking. Once a truck has been dispatched, a call-out charge may
        apply if the job is cancelled.
      </p>
      <h4 class="mb-sm">Privacy policy</h4>
      <p class="mb-0">
        We collect only the information needed to carry out a recovery: your name, contact number, vehicle
        registration and location details. That information is used for dispatch, invoicing and our own
        records, and is never sold or passed to marketing lists. Data is held in line with UK GDPR. For any
        query or deletion request, email
        <a href="mailto:simpsonsbreakdownrecoveryltd@gmail.com" class="text-cyan">simpsonsbreakdownrecoveryltd@gmail.com</a>.
      </p>
    </div>
  </div>
</div>

<footer class="site-footer">
  <div class="shell">
    <div class="footer-grid">
      <div class="footer-col">
        <a href="../index.html" class="brand mb-md" aria-label="Simpsons Breakdown Recovery — home">
          <span class="brand__plate">
            <img class="brand__logo" src="../images/logo.webp" width="661" height="143" alt="Simpsons Breakdown Recovery Services Ltd" loading="lazy" decoding="async">
          </span>
        </a>
        <p class="muted small mb-md">
          Family-run 24/7 breakdown recovery and roadside assistance, based in Edgbaston, Birmingham and
          covering a 20-mile radius. Trading since 2005.
        </p>
        <p class="muted tiny mb-0">
          289 Icknield Port Road (at the rear), Edgbaston, Birmingham B16 0AG<br>
          <a href="tel:{PHONE.replace(' ', '')}" style="color:#fff">{PHONE}</a> &bull;
          <a href="mailto:simpsonsbreakdownrecoveryltd@gmail.com">simpsonsbreakdownrecoveryltd@gmail.com</a>
        </p>
      </div>

      <div class="footer-col">
        <h4>Nearby areas</h4>
        <ul class="footer-links">
{nearby_links}
          <li><a href="../index.html#areas">View all 12 areas &rarr;</a></li>
        </ul>
      </div>

      <div class="footer-col">
        <h4>Services</h4>
        <ul class="footer-links">
          <li><a href="../index.html#services">Car recovery Birmingham</a></li>
          <li><a href="../index.html#services">Motorway recovery M6 / M5 / M42</a></li>
          <li><a href="../index.html#services">Van &amp; commercial towing</a></li>
          <li><a href="../index.html#services">Low-clearance extraction</a></li>
          <li><a href="../index.html#services">Trailer &amp; catering unit transport</a></li>
        </ul>
      </div>

      <div class="footer-col">
        <h4>Emergency</h4>
        <p class="muted small mb-md">Open 24 hours a day, 7 days a week.</p>
        <a href="tel:{PHONE.replace(' ', '')}" class="btn btn--red btn--block mb-sm">Call {PHONE}</a>
        <a href="{wa_generic}" target="_blank" rel="noopener" class="btn btn--green btn--block mb-md">Message on WhatsApp</a>
        <ul class="footer-links">
          <li><a href="https://share.google/FIO6KZSxKO3p8ohXX" target="_blank" rel="noopener">Google reviews</a></li>
          <li><a href="#" data-legal="Terms &amp; conditions">Terms &amp; conditions</a></li>
          <li><a href="#" data-legal="Privacy policy">Privacy policy</a></li>
        </ul>
      </div>
    </div>

    <div class="footer-bottom">
      <span>&copy; <span id="year">2026</span> Simpsons Breakdown Recovery Services Ltd. Registered in England &amp; Wales.</span>
      <nav aria-label="Legal">
        <a href="#" data-legal="Terms &amp; conditions">Terms</a>
        <a href="#" data-legal="Privacy policy">Privacy</a>
        <a href="../index.html#contact">Contact</a>
      </nav>
    </div>
  </div>
</footer>

<div class="dock">
  <a href="tel:{PHONE.replace(' ', '')}" class="dock__btn btn--red">
    <svg class="icon" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/></svg>
    Call now
  </a>
  <a href="{wa_area}" target="_blank" rel="noopener" class="dock__btn btn--green">WhatsApp pin</a>
</div>

<a class="fab" href="{wa_generic}" target="_blank" rel="noopener" aria-label="Chat with Simpsons Breakdown Recovery on WhatsApp">
  <svg class="icon" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path d="M12.03 6.17c-3.18 0-5.76 2.59-5.76 5.77 0 1.3.38 2.27 1.02 3.28l-.58 2.13 2.18-.57c.98.58 1.91.93 3.14.93 3.18 0 5.77-2.59 5.77-5.77 0-3.19-2.58-5.77-5.77-5.77zm3.39 8.24c-.14.4-.84.77-1.17.82-.3.05-.68.06-1.09-.07-.25-.08-.58-.19-.99-.36-1.74-.75-2.87-2.5-2.96-2.62-.09-.11-.71-.94-.71-1.79s.45-1.27.61-1.45c.16-.17.35-.22.46-.22h.33c.11 0 .25-.04.39.3.14.35.49 1.2.53 1.29.04.09.07.19.01.3-.06.12-.09.19-.17.29l-.26.3c-.09.09-.18.18-.08.36.1.17.45.74.96 1.2.66.59 1.22.77 1.4.86.17.09.27.07.37-.04.1-.12.43-.51.55-.68.12-.17.23-.14.39-.09.16.06 1.01.48 1.18.56.17.09.29.13.33.2.05.07.05.42-.1.83z"/></svg>
  <span class="fab__label">Chat on WhatsApp</span>
</a>

<script src="../js/main.js"></script>
<script>document.getElementById('year').textContent = new Date().getFullYear();</script>
</body>
</html>
"""


def main() -> None:
    os.makedirs(OUT_DIR, exist_ok=True)
    for area in AREAS:
        path = OUT_DIR / f"{area['slug']}.html"
        path.write_text(build_page(area), encoding="utf-8")
        print(f"wrote {path} ({path.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
