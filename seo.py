"""Shared SEO builders: head meta, JSON-LD, sitemap and robots.

Keeping this in one place means a page cannot drift out of sync with the rest
of the site — the same business node, the same canonical rules and the same
Open Graph defaults are emitted everywhere.
"""

import html
import json

import site_config as cfg


def esc(text: str) -> str:
    return html.escape(text, quote=True)


# --------------------------------------------------------------------------
# Structured data
# --------------------------------------------------------------------------

def area_served_nodes():
    return [
        {"@type": "City", "name": "Birmingham"},
        {"@type": "AdministrativeArea", "name": "West Midlands"},
    ]


def business_node(*, page_url: str, name_suffix: str = "", area_name: str = None) -> dict:
    """The LocalBusiness node, shared by every page.

    `page_url` is used only for the @id so each page carries a distinct,
    addressable copy of the entity rather than colliding on one @id.
    """
    node = {
        "@type": ["AutoRepair", "EmergencyService"],
        "@id": f"{cfg.SITE_URL}/#business" if not area_name else page_url + "#business",
        "name": cfg.SITE_NAME + (f" — {name_suffix}" if name_suffix else ""),
        "legalName": cfg.SITE_NAME,
        "url": page_url,
        "telephone": cfg.PHONE_E164,
        "email": cfg.EMAIL,
        "priceRange": "££",
        "currenciesAccepted": "GBP",
        "paymentAccepted": "Cash, Bank transfer, Card",
        "image": f"{cfg.SITE_URL}/images/work-van-recovery.webp",
        "logo": {
            "@type": "ImageObject",
            "url": f"{cfg.SITE_URL}/images/logo.webp",
            "width": 661,
            "height": 143,
        },
        "foundingDate": cfg.FOUNDED_YEAR,
        "description": (
            "Family-run 24/7 breakdown recovery, vehicle towing and roadside assistance "
            "covering Birmingham and the West Midlands within a 20-mile radius of the "
            "Edgbaston depot. Cars, vans, motorbikes, 4x4s, non-runners and trailers."
        ),
        "address": {
            "@type": "PostalAddress",
            "streetAddress": cfg.ADDRESS["street"],
            "addressLocality": cfg.ADDRESS["locality"],
            "addressRegion": cfg.ADDRESS["region"],
            "postalCode": cfg.ADDRESS["postcode"],
            "addressCountry": cfg.ADDRESS["country"],
        },
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": cfg.GEO["lat"],
            "longitude": cfg.GEO["lng"],
        },
        "hasMap": cfg.GOOGLE_MAPS_CID_URL,
        "openingHoursSpecification": [{
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            "opens": "00:00",
            "closes": "23:59",
        }],
        "areaServed": (
            {"@type": "AdministrativeArea", "name": area_name}
            if area_name else area_served_nodes()
        ),
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": cfg.RATING_VALUE,
            "reviewCount": cfg.RATING_COUNT,
            "bestRating": "5",
            "worstRating": "1",
        },
        "sameAs": list(cfg.SOCIAL_PROFILES) + [cfg.GOOGLE_MAPS_CID_URL],
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Breakdown recovery and vehicle transport services",
            "itemListElement": [
                {
                    "@type": "Offer",
                    "itemOffered": {
                        "@type": "Service",
                        "name": name,
                        "description": desc,
                        "areaServed": {"@type": "City", "name": "Birmingham"},
                    },
                }
                for name, desc in cfg.SERVICES
            ],
        },
    }
    return node


def website_node() -> dict:
    return {
        "@type": "WebSite",
        "@id": f"{cfg.SITE_URL}/#website",
        "url": cfg.SITE_URL,
        "name": cfg.SITE_NAME,
        "inLanguage": "en-GB",
        "publisher": {"@id": f"{cfg.SITE_URL}/#business"},
    }


def web_page_node(*, url: str, title: str, description: str) -> dict:
    return {
        "@type": "WebPage",
        "@id": url + "#webpage",
        "url": url,
        "name": title,
        "description": description,
        "isPartOf": {"@id": f"{cfg.SITE_URL}/#website"},
        "about": {"@id": f"{cfg.SITE_URL}/#business"},
        "inLanguage": "en-GB",
    }


def breadcrumb_node(*, url: str, items: list) -> dict:
    return {
        "@type": "BreadcrumbList",
        "@id": url + "#breadcrumb",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i + 1,
                "name": name,
                **({"item": item_url} if item_url else {}),
            }
            for i, (name, item_url) in enumerate(items)
        ],
    }


def faq_node(*, url: str, faqs: list) -> dict:
    return {
        "@type": "FAQPage",
        "@id": url + "#faq",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
            for q, a in faqs
        ],
    }


def graph(*nodes) -> str:
    return json.dumps(
        {"@context": "https://schema.org", "@graph": [n for n in nodes if n]},
        indent=2,
        ensure_ascii=False,
    )


# --------------------------------------------------------------------------
# Head meta
# --------------------------------------------------------------------------

def head_meta(*, url: str, title: str, description: str, og_image: str = None,
              robots: str = "index, follow", geo_placename: str = "Edgbaston, Birmingham") -> str:
    """Canonical, robots, geo, Open Graph and Twitter tags for one page.

    Canonical always points at the production domain in site_config, never at
    the Netlify demo, so the demo can never compete with the live site.
    """
    image = og_image or f"{cfg.SITE_URL}/images/og-image.jpg"
    return f"""  <link rel="canonical" href="{esc(url)}">
  <meta name="robots" content="{esc(robots)}">
  <meta name="googlebot" content="{esc(robots)}, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
  <meta name="author" content="{esc(cfg.SITE_NAME)}">
  <meta name="theme-color" content="#070e18">

  <!-- Geo signals -->
  <meta name="geo.region" content="GB-BIR">
  <meta name="geo.placename" content="{esc(geo_placename)}">
  <meta name="geo.position" content="{cfg.GEO['lat']};{cfg.GEO['lng']}">
  <meta name="ICBM" content="{cfg.GEO['lat']}, {cfg.GEO['lng']}">

  <!-- Open Graph -->
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="{esc(cfg.SITE_NAME)}">
  <meta property="og:locale" content="en_GB">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(description)}">
  <meta property="og:url" content="{esc(url)}">
  <meta property="og:image" content="{esc(image)}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="{esc(cfg.SITE_NAME)} — 24/7 breakdown recovery in Birmingham">

  <!-- Twitter / X -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{esc(title)}">
  <meta name="twitter:description" content="{esc(description)}">
  <meta name="twitter:image" content="{esc(image)}">
  <meta name="twitter:image:alt" content="{esc(cfg.SITE_NAME)} — 24/7 breakdown recovery in Birmingham">"""


def favicon_links(prefix: str = "") -> str:
    p = prefix
    return f"""  <link rel="icon" href="{p}images/icon-32.png" sizes="32x32" type="image/png">
  <link rel="icon" href="{p}images/icon-512.png" sizes="512x512" type="image/png">
  <link rel="apple-touch-icon" href="{p}images/icon-180.png">"""