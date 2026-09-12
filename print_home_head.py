#!/usr/bin/env python3
"""Print the homepage head block and JSON-LD, generated from the shared modules.

index.html is hand-authored (it is the one page with bespoke copy), so its head
is pasted in from this output rather than assembled at build time. Run this
after changing site_config.py and paste the result between the markers in
index.html:

    python3 print_home_head.py

Keeping it generated here means the homepage cannot drift out of sync with the
location pages on canonicals, Open Graph defaults or the business schema.
"""

import pathlib

import site_config as cfg
import seo

TITLE = "Breakdown Recovery Birmingham | 24/7 Simpsons Recovery"
DESC = (
    "24/7 breakdown recovery across Birmingham and the West Midlands. 30–45 minute "
    "average local arrival and 229 five-star Google reviews. Call 07706 057962."
)
URL = f"{cfg.SITE_URL}/"

FAQS = [
    ("How fast can you reach me if I break down in Birmingham?",
     "Our average local response time is 30 to 45 minutes across central Birmingham, "
     "Edgbaston, Harborne, Smethwick and along the M5 and M6 corridors. When you call "
     "07706 057962 you speak directly to Dean or a local driver who checks live traffic "
     "and gives you an exact ETA."),
    ("What should I do if I break down on the M6 or M5?",
     "Pull well onto the hard shoulder or into an emergency refuge area, turn the wheels "
     "away from the carriageway, switch on your hazard lights and exit through the "
     "passenger side behind the safety barrier. Call Simpsons on 07706 057962 or send a "
     "WhatsApp location pin so our flatbed can be dispatched directly."),
    ("Can you recover a car from an underground or low-ceiling car park?",
     "Yes. We carry low-profile wheel skates, dollies and winching equipment for "
     "difficult extractions including underground multi-storey bays, locked brakes, "
     "seized steering and flat tyres."),
    ("Do you tow trailers, catering units and plant?",
     "We do. As well as cars and vans we move catering trailers, box trailers and "
     "commercial vehicles such as plant service trucks. These are usually planned jobs "
     "booked in advance."),
    ("Do you charge extra at night or at weekends?",
     "No. We agree a fixed price before we set off, day or night, with no hidden mileage "
     "loading and no after-hours premium added afterwards."),
    ("Where can you take my vehicle?",
     "Anywhere you choose: your home driveway, your own local garage, a main dealership, "
     "a tyre fitter or a bodyshop. We also do long-distance vehicle transport."),
    ("Which postcodes do you cover?",
     "We run a 20-mile radius from Edgbaston (B16), covering Birmingham and the West "
     "Midlands including B1-B17, B23, B24, B42, B62-B75, B90-B93, B66-B71, DY1-DY3 and "
     "WS1-WS3, plus the M5, M6 and M42."),
]


def main() -> None:
    """Print the generated head block and JSON-LD for inspection.

    apply_home_head.py imports this module and writes the real output into
    index.html; this entry point exists so the pieces can be eyeballed.
    """
    meta = seo.head_meta(url=URL, title=TITLE, description=DESC)
    ld = seo.graph(
        seo.business_node(page_url=URL),
        seo.website_node(),
        seo.web_page_node(url=URL, title=TITLE, description=DESC),
        seo.faq_node(url=URL, faqs=FAQS),
    )
    print("--- meta ---")
    print(meta)
    print()
    print(f"--- json-ld ({len(ld):,} chars) ---")
    print(ld)


if __name__ == "__main__":
    main()