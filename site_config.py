"""Single source of truth for the site's identity, contact details and SEO data.

Every generated page, the sitemap and robots.txt read from here, so moving the
site from the Netlify demo to the customer's own domain is a one-line change
to SITE_URL followed by a rebuild:

    python3 build_areas.py && python3 build_seo.py

Facts here are the ones the business states itself. Nothing is invented.
"""

# --- Where the site will live in production --------------------------------
# The customer's existing domain. While the demo runs on Netlify this is still
# the correct canonical target: it tells search engines which URL is the real
# one, so the demo never competes with the live site.
SITE_URL = "https://www.simpsonsbreakdownrecovery.co.uk"

# The domain the demo is served from, excluded from indexing via a Netlify
# header (see netlify.toml). Kept here for documentation only.
DEMO_URL = "https://simpsons-recovery-birmingham.netlify.app"

SITE_NAME = "Simpsons Breakdown Recovery Services Ltd"
SITE_SHORT = "Simpsons Breakdown Recovery"

# --- Contact ---------------------------------------------------------------
PHONE_DISPLAY = "07706 057962"
PHONE_TEL = "07706057962"          # for tel: links
PHONE_E164 = "+447706057962"       # for schema.org
WHATSAPP_NUMBER = "447706057962"   # for wa.me links
EMAIL = "simpsonsbreakdownrecoveryltd@gmail.com"

ADDRESS = {
    "street": "289 Icknield Port Road, At the rear",
    "locality": "Edgbaston, Birmingham",
    "region": "West Midlands",
    "postcode": "B16 0AG",
    "country": "GB",
}
GEO = {"lat": "52.4844", "lng": "-1.9351"}

# --- Established facts ------------------------------------------------------
FOUNDED_YEAR = "2005"
RATING_VALUE = "4.9"
RATING_COUNT = "229"
GOOGLE_REVIEWS_URL = "https://share.google/FIO6KZSxKO3p8ohXX"
GOOGLE_MAPS_CID_URL = "https://maps.google.com/?cid=7538252664488705060"

# --- Social profiles, used for schema.org sameAs ---------------------------
# Only profiles confirmed to exist are listed. Wrong sameAs URLs actively hurt
# entity matching in search, so add the rest only once the owner supplies the
# exact page URLs:
#   Facebook  — "Simpsons breakdown recovery services ltd"
#   Instagram — linked from the Google Business profile
#   TikTok    — linked from the Google Business profile
SOCIAL_PROFILES = [
    "https://x.com/SRecoveryl15565",
]

# --- Service areas ----------------------------------------------------------
AREA_SLUGS = [
    "edgbaston-breakdown-recovery",
    "harborne-breakdown-recovery",
    "birmingham-city-centre-breakdown-recovery",
    "smethwick-breakdown-recovery",
    "west-bromwich-breakdown-recovery",
    "perry-barr-breakdown-recovery",
    "erdington-breakdown-recovery",
    "halesowen-breakdown-recovery",
    "dudley-breakdown-recovery",
    "sutton-coldfield-breakdown-recovery",
    "solihull-breakdown-recovery",
    "walsall-breakdown-recovery",
]

# --- Services, used for the OfferCatalog in the business schema -------------
SERVICES = [
    ("Car recovery Birmingham", "24/7 car recovery and towing for non-starters, clutch and gearbox failures, suspension damage and accident damage."),
    ("Motorway recovery", "Priority recovery from hard shoulders and emergency refuge areas on the M6, M5 and M42 and the A38(M)."),
    ("Van and commercial vehicle recovery", "Loaded vans, minibuses and light commercial vehicles recovered with the load on board."),
    ("Low-clearance and underground recovery", "Wheel skates, dollies and compact winching for multi-storey and basement car parks, seized brakes and locked steering."),
    ("Jump starts and flat batteries", "12V and 24V jump starts at home, at work or at the roadside, plus flat-tyre transport."),
    ("Trailer, catering unit and plant transport", "Catering trailers, box trailers and commercial plant vehicles moved between sites and events."),
    ("Accident and non-runner transport", "Scene clearance, documented transport for insurance claims and movement of non-runners between garages."),
]