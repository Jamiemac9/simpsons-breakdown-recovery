#!/usr/bin/env python3
"""Generate the Simpsons Breakdown Recovery location pages.

Single source of truth for the area-page template so every page shares the
same header, footer, dock and design-system classes as index.html.
"""
import os
import json
import html

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(BASE_DIR, "areas")

AREAS = [
    {
        "slug": "edgbaston-breakdown-recovery",
        "name": "Edgbaston",
        "postcodes": "B15, B16 and B17",
        "distance": "Depot base",
        "eta": "15–25 minutes",
        "roads": "A456 Hagley Road, Icknield Port Road, A4540 Middleway and Chad Road",
        "intro": "Our depot sits on Icknield Port Road, so Edgbaston is the one place we never have to cross the city to reach. When something goes wrong between Five Ways and the Botanical Gardens, we are usually the closest recovery truck to you.",
        "landmarks": "Edgbaston Village, Five Ways Island, Hagley Road, Birmingham Botanical Gardens, Edgbaston Reservoir, the Priory and the Calthorpe Estate",
        "scenarios": "Dead batteries outside Hagley Road apartment blocks, cars that will not restart in the multi-storey car parks around Five Ways, and vehicles that need moving off the A456 at short notice.",
        "nearby": ["harborne-breakdown-recovery", "birmingham-city-centre-breakdown-recovery", "smethwick-breakdown-recovery"],
    },
    {
        "slug": "harborne-breakdown-recovery",
        "name": "Harborne",
        "postcodes": "B17",
        "distance": "1.8 miles from the depot",
        "eta": "20–30 minutes",
        "roads": "Harborne High Street, Court Oak Road, Lordswood Road and Metchley Lane",
        "intro": "Harborne is one of our quickest jobs. The High Street is narrow, busy and almost permanently lined with parked cars, and we know exactly where we can safely stop a flatbed without blocking the traffic behind us.",
        "landmarks": "Harborne High Street, the Queen Elizabeth Hospital, University of Birmingham, Metchley Park, Harborne Pool and Fitness Centre and Court Oak Road",
        "scenarios": "Staff cars that will not start after a night shift at the QE, flat tyres on the High Street, and vehicles with seized brakes that cannot be moved without skates.",
        "nearby": ["edgbaston-breakdown-recovery", "birmingham-city-centre-breakdown-recovery", "halesowen-breakdown-recovery", "smethwick-breakdown-recovery"],
    },
    {
        "slug": "birmingham-city-centre-breakdown-recovery",
        "name": "Birmingham city centre",
        "postcodes": "B1, B2, B3, B4 and B5",
        "distance": "1.5 miles from the depot",
        "eta": "20–35 minutes",
        "roads": "the A38(M) Aston Expressway, the Queensway tunnels, Broad Street and Suffolk Street Queensway",
        "intro": "The city centre is where most recovery firms give up. Low ceilings, tight ramps and cars that cannot be pushed make multi-storey car parks genuinely difficult, so we carry the equipment to get vehicles out without damage.",
        "landmarks": "Bullring, Grand Central, the Mailbox, Broad Street, Paradise, the Jewellery Quarter and the Utilita Arena",
        "scenarios": "Non-runners stuck on the third level of a multi-storey with a 1.9 m height barrier, cars immobilised in basement bays beneath apartment blocks, and late-night breakdowns around Broad Street and the Arcadian.",
        "nearby": ["edgbaston-breakdown-recovery", "harborne-breakdown-recovery", "perry-barr-breakdown-recovery", "erdington-breakdown-recovery"],
    },
    {
        "slug": "smethwick-breakdown-recovery",
        "name": "Smethwick",
        "postcodes": "B66 and B67",
        "distance": "2.2 miles from the depot",
        "eta": "20–30 minutes",
        "roads": "the A457 Tollhouse Way, Cape Hill, Soho Way and the A41",
        "intro": "Smethwick's mix of busy industrial frontages and tight residential terraces means access planning matters. We cover the whole of Smethwick, including Bearwood and the Cape Hill commercial corridor.",
        "landmarks": "Cape Hill, Bearwood, Galton Bridge, Smethwick Rolfe Street, the A457 Tollhouse Way and Soho Way industrial estates",
        "scenarios": "Trades vans that have failed part-loaded on Cape Hill, delivery vehicles stuck at an industrial unit, and cars that will not start on residential terraces where parking is limited.",
        "nearby": ["edgbaston-breakdown-recovery", "west-bromwich-breakdown-recovery", "harborne-breakdown-recovery", "birmingham-city-centre-breakdown-recovery"],
    },
    {
        "slug": "west-bromwich-breakdown-recovery",
        "name": "West Bromwich",
        "postcodes": "B70 and B71",
        "distance": "4.5 miles from the depot",
        "eta": "25–35 minutes",
        "roads": "the A41 Expressway, M5 junction 1, High Street and All Saints Way",
        "intro": "West Bromwich sits right on the M5, which means a good proportion of our jobs here start on a slip road or a roundabout rather than a driveway. We cover the town centre, New Square and Sandwell Valley.",
        "landmarks": "New Square shopping centre, Sandwell Valley, the Hawthorns, All Saints Way and the A41 Expressway",
        "scenarios": "Breakdowns on the M5 junction 1 slip roads, commercial vans that have failed outside a depot, and cars recovered from shopping centre car parks.",
        "nearby": ["smethwick-breakdown-recovery", "dudley-breakdown-recovery", "walsall-breakdown-recovery", "perry-barr-breakdown-recovery"],
    },
    {
        "slug": "perry-barr-breakdown-recovery",
        "name": "Perry Barr",
        "postcodes": "B42",
        "distance": "3.6 miles from the depot",
        "eta": "25–35 minutes",
        "roads": "the A34 Walsall Road, Birchfield Road, Aldridge Road and Aston Lane",
        "intro": "The A34 through Perry Barr is one of the busiest dual carriageways in North Birmingham, and a broken-down vehicle there backs traffic up fast. We treat Perry Barr and the Birchfield corridor as priority.",
        "landmarks": "Alexander Stadium, One Stop Shopping Centre, Perry Barr railway station, Birchfield Road and the A34 Walsall Road",
        "scenarios": "Commuter breakdowns on the A34 during peak hours, flat tyres and engine faults near the One Stop centre, and event traffic incidents around Alexander Stadium.",
        "nearby": ["birmingham-city-centre-breakdown-recovery", "erdington-breakdown-recovery", "walsall-breakdown-recovery", "west-bromwich-breakdown-recovery"],
    },
    {
        "slug": "erdington-breakdown-recovery",
        "name": "Erdington",
        "postcodes": "B23 and B24",
        "distance": "5.2 miles from the depot",
        "eta": "25–40 minutes",
        "roads": "the A38 Tyburn Road, Erdington High Street, Kingsbury Road and Gravelly Hill",
        "intro": "Erdington's Tyburn Road corridor is packed with industrial units and commercial traffic, and it feeds directly into Spaghetti Junction. A van or lorry down here blocks a lot of people, so we get to it quickly.",
        "landmarks": "Erdington High Street, Tyburn Road industrial estates, Fort Dunlop, Gravelly Hill and the M6 junction 6 approaches",
        "scenarios": "Loaded commercial vehicles failing on Tyburn Road, cars breaking down on the approach to Spaghetti Junction, and battery failures on residential streets.",
        "nearby": ["perry-barr-breakdown-recovery", "birmingham-city-centre-breakdown-recovery", "sutton-coldfield-breakdown-recovery", "walsall-breakdown-recovery"],
    },
    {
        "slug": "halesowen-breakdown-recovery",
        "name": "Halesowen",
        "postcodes": "B62 and B63",
        "distance": "6.4 miles from the depot",
        "eta": "25–35 minutes",
        "roads": "the A456 Manor Way, M5 junction 3 and the Halesowen bypass",
        "intro": "Halesowen backs onto the M5 at junction 3, so we cover both town-centre jobs and motorway callouts from the same base. The hilly approach roads also mean we see more than our share of clutch and brake problems.",
        "landmarks": "Halesowen town centre, Manor Way, the Cornbow Centre, M5 junction 3 and the surrounding lanes towards Romsley and Clent",
        "scenarios": "Clutch and brake failures on the steeper roads around Halesowen, breakdowns on Manor Way and motorway recoveries from M5 junction 3.",
        "nearby": ["dudley-breakdown-recovery", "harborne-breakdown-recovery", "west-bromwich-breakdown-recovery", "edgbaston-breakdown-recovery"],
    },
    {
        "slug": "dudley-breakdown-recovery",
        "name": "Dudley",
        "postcodes": "DY1, DY2 and DY3",
        "distance": "7.8 miles from the depot",
        "eta": "30–40 minutes",
        "roads": "the A4123 Birmingham New Road, Castlegate Way and Duncan Edwards Way",
        "intro": "Dudley is a regular run for us, mostly along the A4123 and around Castlegate. We cover the town centre, Gornal, Sedgley and the corridor towards Brierley Hill.",
        "landmarks": "Dudley town centre, Castlegate, the Zoological Gardens, Dudley Port, Gornal and the A4123 Birmingham New Road",
        "scenarios": "RTC recovery on the Birmingham New Road, vehicles immobilised in the town centre car parks, and home-start battery jobs across the DY postcodes.",
        "nearby": ["halesowen-breakdown-recovery", "west-bromwich-breakdown-recovery", "walsall-breakdown-recovery", "smethwick-breakdown-recovery"],
    },
    {
        "slug": "sutton-coldfield-breakdown-recovery",
        "name": "Sutton Coldfield",
        "postcodes": "B72, B73, B74 and B75",
        "distance": "8.2 miles from the depot",
        "eta": "30–45 minutes",
        "roads": "the A5127 Lichfield Road, the A453, the Sutton bypass and The Parade",
        "intro": "Sutton Coldfield's wide residential streets and leafy driveways are straightforward for a flatbed — the tricky part is usually squeezing past parked cars on the older roads in Boldmere and Wylde Green, which is second nature to us.",
        "landmarks": "Sutton Park, The Parade, Four Oaks, Boldmere, Wylde Green, Mere Green and the A5127 Lichfield Road",
        "scenarios": "Cars that have not turned a wheel for months on a driveway, breakdowns on the Sutton bypass and motorcycles recovered to specialist workshops.",
        "nearby": ["erdington-breakdown-recovery", "perry-barr-breakdown-recovery", "walsall-breakdown-recovery", "birmingham-city-centre-breakdown-recovery"],
    },
    {
        "slug": "solihull-breakdown-recovery",
        "name": "Solihull",
        "postcodes": "B90, B91, B92 and B93",
        "distance": "8.5 miles from the depot",
        "eta": "30–45 minutes",
        "roads": "the A41 Solihull bypass, M42 junction 5, Warwick Road and Lode Lane",
        "intro": "Solihull sees a higher proportion of prestige cars, hybrids and electric vehicles, and those need care. We recover EVs on flatbeds with the drive wheels stationary, and we treat bodywork and wheels as if they were our own.",
        "landmarks": "Touchwood, Solihull town centre, Shirley, Dorridge, Knowle, Lode Lane and the Land Rover site",
        "scenarios": "Electric and hybrid vehicles that cannot be driven, breakdowns on the A41 bypass, and motorway callouts from M42 junction 5.",
        "nearby": ["halesowen-breakdown-recovery", "harborne-breakdown-recovery", "birmingham-city-centre-breakdown-recovery", "dudley-breakdown-recovery"],
    },
    {
        "slug": "walsall-breakdown-recovery",
        "name": "Walsall",
        "postcodes": "WS1, WS2 and WS3",
        "distance": "9.5 miles from the depot",
        "eta": "30–45 minutes",
        "roads": "the A34, M6 junctions 9 and 10, Pleck Road and the Broadway",
        "intro": "Walsall sits between two of the busiest motorway junctions in the region. Junction 9 and 10 of the M6 keep us busy, and we cover the town centre, Pleck and Bescot alongside them.",
        "landmarks": "Walsall town centre, the Saddlers Centre, Pleck, Bescot Stadium, Bescot retail park and the M6 junctions 9 and 10",
        "scenarios": "Motorway recoveries around M6 junctions 9 and 10, warehouse and delivery vans failing at loading bays, and accident clearance.",
        "nearby": ["perry-barr-breakdown-recovery", "west-bromwich-breakdown-recovery", "dudley-breakdown-recovery", "sutton-coldfield-breakdown-recovery"],
    },
]

AREA_BY_SLUG = {a["slug"]: a for a in AREAS}

HEAD = """<!DOCTYPE html>
<html lang="en-GB">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <meta name="robots" content="index, follow">

  <meta name="geo.region" content="GB-BIR">
  <meta name="geo.placename" content="{name}, Birmingham">

  <meta property="og:title" content="{og_title}">
  <meta property="og:description" content="{description}">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="en_GB">
  <meta property="og:image" content="../images/simpsons-white-van-recovery.jpg">

  <link rel="icon" href="../images/Simpsons-Breakdown-New-Logo.png.webp">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@700;800;900&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../css/style.css">

  <script type="application/ld+json">
{jsonld}
  </script>
</head>
<body>

<a class="skip-link" href="#main">Skip to content</a>

<div class="ticker">
  <div class="shell ticker__inner">
    <div class="ticker__left">
      <span class="ticker__live"><span class="dot"></span> {tick_name} recovery on call</span>
      <span class="ticker__detail">{postcodes} &bull; typical arrival {eta}</span>
    </div>
    <a class="ticker__call" href="tel:07706057962">07706 057962</a>
  </div>
</div>

<header class="site-header">
  <div class="shell site-header__inner">

    <a href="../index.html" class="brand" aria-label="Simpsons Breakdown Recovery Services Ltd — home">
      <span class="brand__plate">
        <img class="brand__logo" src="../images/Simpsons-Breakdown-New-Logo.png.webp" width="300" height="212" alt="Simpsons Breakdown Recovery Services Ltd logo">
      </span>
      <span class="brand__text">
        <span class="brand__name">Simpsons</span>
        <span class="brand__sub">Breakdown Recovery</span>
      </span>
    </a>

    <nav class="nav" aria-label="Main">
      <a href="../index.html">Home</a>
      <a href="../index.html#services">Services</a>
      <a href="../index.html#areas" class="is-active">Areas covered</a>
      <a href="../index.html#reviews">Reviews</a>
      <a href="../index.html#gallery">Our fleet</a>
      <a href="../index.html#faq">FAQ</a>
      <a href="../index.html#contact">Contact</a>
    </nav>

    <div class="header-actions">
      <a href="{wa_generic}" target="_blank" rel="noopener" class="btn btn--green btn--sm">
        <svg class="icon" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path d="M12.03 6.17c-3.18 0-5.76 2.59-5.76 5.77 0 1.3.38 2.27 1.02 3.28l-.58 2.13 2.18-.57c.98.58 1.91.93 3.14.93 3.18 0 5.77-2.59 5.77-5.77 0-3.19-2.58-5.77-5.77-5.77zm3.39 8.24c-.14.4-.84.77-1.17.82-.3.05-.68.06-1.09-.07-.25-.08-.58-.19-.99-.36-1.74-.75-2.87-2.5-2.96-2.62-.09-.11-.71-.94-.71-1.79s.45-1.27.61-1.45c.16-.17.35-.22.46-.22h.33c.11 0 .25-.04.39.3.14.35.49 1.2.53 1.29.04.09.07.19.01.3-.06.12-.09.19-.17.29l-.26.3c-.09.09-.18.18-.08.36.1.17.45.74.96 1.2.66.59 1.22.77 1.4.86.17.09.27.07.37-.04.1-.12.43-.51.55-.68.12-.17.23-.14.39-.09.16.06 1.01.48 1.18.56.17.09.29.13.33.2.05.07.05.42-.1.83z"/></svg>
        WhatsApp
      </a>
      <a href="tel:07706057962" class="btn btn--red btn--sm">
        <svg class="icon" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/></svg>
        <span class="nowrap">07706 057962</span>
      </a>
      <button class="menu-toggle" id="menuToggle" type="button" aria-label="Menu" aria-expanded="false" aria-controls="mobileNav">
        <span></span><span></span><span></span>
      </button>
    </div>
  </div>

  <nav class="mobile-nav" id="mobileNav" aria-label="Mobile">
    <a href="../index.html">Home</a>
    <a href="../index.html#services">Services</a>
    <a href="../index.html#areas">Areas covered</a>
    <a href="../index.html#reviews">Reviews</a>
    <a href="../index.html#gallery">Our fleet</a>
    <a href="../index.html#faq">FAQ</a>
    <a href="../index.html#contact">Contact</a>
    <div class="mobile-nav__cta">
      <a href="tel:07706057962" class="btn btn--red btn--block">Call 07706 057962</a>
      <a href="{wa_generic}" target="_blank" rel="noopener" class="btn btn--green btn--block">Send WhatsApp location</a>
    </div>
  </nav>
</header>

<main id="main">

  <nav class="breadcrumb" aria-label="Breadcrumb">
    <div class="shell breadcrumb__inner">
      <a href="../index.html">Home</a>
      <span class="breadcrumb__sep" aria-hidden="true">/</span>
      <a href="../index.html#areas">Areas covered</a>
      <span class="breadcrumb__sep" aria-hidden="true">/</span>
      <span aria-current="page">{name} breakdown recovery</span>
    </div>
  </nav>

  <section class="hero">
    <div class="shell hero__grid">
      <div>
        <span class="pill"><span class="dot"></span> {distance} &bull; 20-mile radius</span>

        <h1>Breakdown recovery <span class="hero__accent">{name}</span></h1>

        <p class="lead hero__lead">{intro}</p>

        <div class="hero__cta">
          <a href="tel:07706057962" class="btn btn--red btn--lg">
            <svg class="icon" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/></svg>
            Call 07706 057962
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

      <div class="panel panel--glow">
        <div class="panel__head">
          <span class="panel__title">{name} at a glance</span>
        </div>

        <div class="stat-grid">
          <div class="stat">
            <div class="stat__value">{eta}</div>
            <div class="stat__label">Typical arrival</div>
          </div>
          <div class="stat">
            <div class="stat__value stat__value--green">24/7</div>
            <div class="stat__label">Day and night</div>
          </div>
        </div>

        <ul class="check-list mb-lg">
          <li><strong>Postcodes:</strong> {postcodes}</li>
          <li><strong>Distance from depot:</strong> {distance}</li>
          <li><strong>Main roads:</strong> {roads}</li>
          <li>Cars, vans, 4x4s, motorbikes and non-runners</li>
          <li>Fixed price agreed before we set off</li>
        </ul>

        <a href="tel:07706057962" class="btn btn--red btn--block">Confirm a {name} callout</a>
      </div>
    </div>
  </section>

  <section class="metrics">
    <div class="shell grid grid-4">
      <div class="metric">
        <span class="metric__icon">
          <svg class="icon" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
        </span>
        <span>
          <span class="metric__value">{eta}</span>
          <span class="metric__label">Typical {name} arrival</span>
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
          <span class="metric__label">20 years in Birmingham</span>
        </span>
      </div>
      <div class="metric">
        <span class="metric__icon">
          <svg class="icon" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.7 16.7L13.4 20.9a2 2 0 01-2.8 0l-4.3-4.2a8 8 0 1111.4 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
        </span>
        <span>
          <span class="metric__value">Edgbaston</span>
          <span class="metric__label">Depot base, B16</span>
        </span>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="shell">
      <div class="section-head">
        <span class="eyebrow">Local knowledge</span>
        <h2>Recovering in {name}</h2>
        <p class="muted">What we actually get called out for here, and the places we know to plan for.</p>
      </div>

      <div class="grid grid-2">
        <article class="panel">
          <h3 class="mb-sm">Roads and landmarks we know</h3>
          <p class="muted small mb-md">{landmarks}.</p>
          <p class="muted small mb-0">
            Our drivers work these roads every day, so we know which junctions have nowhere safe to stop,
            which residential streets have room to swing a flatbed, and which car parks have a height
            barrier we will not fit under until the vehicle is loaded outside.
          </p>
        </article>

        <article class="panel">
          <h3 class="mb-sm">What we get called for</h3>
          <p class="muted small mb-0">{scenarios}</p>
        </article>
      </div>
    </div>
  </section>

  <section class="section section--alt">
    <div class="shell">
      <div class="section-head">
        <span class="eyebrow">How it works</span>
        <h2>Three steps to being back on the road</h2>
      </div>

      <div class="grid grid-3">
        <article class="panel">
          <div class="stat__value mb-sm">01</div>
          <h3 class="mb-sm">Call or send your pin</h3>
          <p class="muted small mb-0">Ring <a href="tel:07706057962" class="text-red"><strong>07706 057962</strong></a> or WhatsApp your location. You speak to Dean or an operator on the road, not a call centre.</p>
        </article>
        <article class="panel">
          <div class="stat__value mb-sm">02</div>
          <h3 class="mb-sm">Fixed price, real ETA</h3>
          <p class="muted small mb-0">We agree the price before anything moves, check live traffic and give you a realistic arrival window for {name}.</p>
        </article>
        <article class="panel">
          <div class="stat__value mb-sm">03</div>
          <h3 class="mb-sm">Loaded and delivered</h3>
          <p class="muted small mb-0">Your vehicle is winched onto the tilt-and-slide bed and taken wherever you want it — home, garage, dealership or tyre fitter.</p>
        </article>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="shell">
      <div class="section-head">
        <span class="eyebrow">Services in {name}</span>
        <h2>What we can recover for you</h2>
      </div>

      <div class="stack">
        <article class="service-row">
          <div class="service-row__num">01</div>
          <div class="service-row__name">
            <h3>Car recovery {name}</h3>
            <span class="service-row__tag">Most requested</span>
          </div>
          <p class="service-row__desc">Non-starters, clutch and gearbox failures, suspension damage and vehicles that cannot be driven — recovered to the garage you choose.</p>
          <div class="service-row__cta"><a href="tel:07706057962" class="btn btn--red">Call for a tow</a></div>
        </article>

        <article class="service-row">
          <div class="service-row__num">02</div>
          <div class="service-row__name">
            <h3>Van &amp; commercial recovery</h3>
            <span class="service-row__tag">Trades and fleets</span>
          </div>
          <p class="service-row__desc">Transit, Vivaro, Sprinter and minibus-class vehicles recovered loaded, so your tools and stock travel with you.</p>
          <div class="service-row__cta"><a href="tel:07706057962" class="btn btn--red">Call for a van tow</a></div>
        </article>

        <article class="service-row">
          <div class="service-row__num">03</div>
          <div class="service-row__name">
            <h3>Low-clearance recovery</h3>
            <span class="service-row__tag">Difficult access</span>
          </div>
          <p class="service-row__desc">Wheel skates, dollies and compact winching for multi-storey and basement car parks, seized brakes and locked steering.</p>
          <div class="service-row__cta"><a href="../index.html#contact" class="btn btn--ghost">Ask about access</a></div>
        </article>

        <article class="service-row">
          <div class="service-row__num">04</div>
          <div class="service-row__name">
            <h3>Jump starts &amp; roadside help</h3>
            <span class="service-row__tag">Batteries and wheels</span>
          </div>
          <p class="service-row__desc">12V and 24V boosters for flat batteries at home or work, plus flat-tyre transport to your preferred fitter.</p>
          <div class="service-row__cta"><a href="tel:07706057962" class="btn btn--ghost">Get roadside help</a></div>
        </article>
      </div>
    </div>
  </section>

  <section class="section section--alt">
    <div class="shell">
      <div class="section-head">
        <span class="eyebrow">Verified Google reviews</span>
        <h2>What customers say</h2>
        <p class="muted">Real reviews from drivers we have recovered across Birmingham and the West Midlands.</p>
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
        <span class="eyebrow">Common questions</span>
        <h2>{name} recovery FAQs</h2>
      </div>

      <div class="faq">
        <div class="faq__item is-open">
          <button class="faq__q" type="button">
            <span>How quickly can you reach {name}?</span>
            <span class="faq__chev" aria-hidden="true">▾</span>
          </button>
          <div class="faq__a"><div><p>Typically {eta} from your call, depending on traffic and which truck is nearest. We run a 20-mile radius from our Edgbaston depot, and {name} sits {distance}. When you ring 07706 057962 you speak to a driver who can see where our vehicles are and give you a genuine arrival window.</p></div></div>
        </div>

        <div class="faq__item">
          <button class="faq__q" type="button">
            <span>Which {name} postcodes do you cover?</span>
            <span class="faq__chev" aria-hidden="true">▾</span>
          </button>
          <div class="faq__a"><div><p>We cover {postcodes}, along with the surrounding streets and the main routes through {name} — {roads}. If you are just outside these postcodes, call with your location and we will tell you straight away whether we can get to you.</p></div></div>
        </div>

        <div class="faq__item">
          <button class="faq__q" type="button">
            <span>Do you charge more for nights or weekends in {name}?</span>
            <span class="faq__chev" aria-hidden="true">▾</span>
          </button>
          <div class="faq__a"><div><p>No. We quote a fixed price before the truck is dispatched, whatever the hour. There is no after-hours loading added later and no charge for getting a price from us.</p></div></div>
        </div>

        <div class="faq__item">
          <button class="faq__q" type="button">
            <span>Can you get a car out of a car park in {name}?</span>
            <span class="faq__chev" aria-hidden="true">▾</span>
          </button>
          <div class="faq__a"><div><p>Yes. Multi-storey and basement car parks are one of our specialities. We carry low-profile wheel skates, dollies and compact winching equipment, so a vehicle that will not start or will not roll can be moved out without damage to the bodywork, wheels or the building.</p></div></div>
        </div>
      </div>
    </div>
  </section>
"""

FOOTER = """</main>

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
            <img class="brand__logo" src="../images/Simpsons-Breakdown-New-Logo.png.webp" width="300" height="212" alt="Simpsons Breakdown Recovery Services Ltd logo">
          </span>
        </a>
        <p class="muted small mb-md">
          Family-run 24/7 breakdown recovery and roadside assistance, based in Edgbaston, Birmingham and
          covering a 20-mile radius. Trading since 2005.
        </p>
        <p class="muted tiny mb-0">
          289 Icknield Port Road (at the rear), Edgbaston, Birmingham B16 0AG<br>
          <a href="tel:07706057962" style="color:#fff">07706 057962</a> &bull;
          <a href="mailto:simpsonsbreakdownrecoveryltd@gmail.com">simpsonsbreakdownrecoveryltd@gmail.com</a>
        </p>
      </div>

      <div class="footer-col">
        <h4>Nearby areas</h4>
        <ul class="footer-links">
{nearby_links}
          <li><a href="../index.html#areas">All 12 areas &rarr;</a></li>
        </ul>
      </div>

      <div class="footer-col">
        <h4>Services</h4>
        <ul class="footer-links">
          <li><a href="../index.html#services">Car recovery Birmingham</a></li>
          <li><a href="../index.html#services">Motorway recovery</a></li>
          <li><a href="../index.html#services">Van &amp; commercial towing</a></li>
          <li><a href="../index.html#services">Low-clearance extraction</a></li>
          <li><a href="../index.html#services">Jump starts</a></li>
        </ul>
      </div>

      <div class="footer-col">
        <h4>Emergency</h4>
        <p class="muted small mb-md">Open 24 hours a day, 7 days a week.</p>
        <a href="tel:07706057962" class="btn btn--red btn--block mb-sm">Call 07706 057962</a>
        <a href="{wa_generic}" target="_blank" rel="noopener" class="btn btn--green btn--block mb-md">Send WhatsApp location</a>
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
  <a href="tel:07706057962" class="dock__btn btn--red">
    <svg class="icon" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/></svg>
    Call now
  </a>
  <a href="{wa_area}" target="_blank" rel="noopener" class="dock__btn btn--green">WhatsApp pin</a>
</div>

<script src="../js/main.js"></script>
<script>document.getElementById('year').textContent = new Date().getFullYear();</script>
</body>
</html>
"""


def wa_url(message):
    return "https://wa.me/447706057962?text=" + message.replace(" ", "%20").replace(",", "%2C").replace("&", "%26")


def build_jsonld(area):
    return json.dumps({
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": ["AutoRepair", "EmergencyService"],
                "@id": f"https://www.simpsonsbreakdownrecovery.co.uk/areas/{area['slug']}.html",
                "name": f"Simpsons Breakdown Recovery Services Ltd — {area['name']}",
                "url": f"https://www.simpsonsbreakdownrecovery.co.uk/areas/{area['slug']}.html",
                "telephone": "+447706057962",
                "priceRange": "££",
                "parentOrganization": {
                    "@type": "Organization",
                    "name": "Simpsons Breakdown Recovery Services Ltd",
                },
                "address": {
                    "@type": "PostalAddress",
                    "streetAddress": "289 Icknield Port Road, At the rear",
                    "addressLocality": "Edgbaston, Birmingham",
                    "addressRegion": "West Midlands",
                    "postalCode": "B16 0AG",
                    "addressCountry": "GB",
                },
                "areaServed": {"@type": "AdministrativeArea", "name": area["name"]},
                "openingHoursSpecification": [{
                    "@type": "OpeningHoursSpecification",
                    "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                    "opens": "00:00",
                    "closes": "23:59",
                }],
                "aggregateRating": {
                    "@type": "AggregateRating",
                    "ratingValue": "4.9",
                    "reviewCount": "229",
                    "bestRating": "5",
                    "worstRating": "1",
                },
            },
            {
                "@type": "BreadcrumbList",
                "@id": f"https://www.simpsonsbreakdownrecovery.co.uk/areas/{area['slug']}.html#breadcrumb",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.simpsonsbreakdownrecovery.co.uk/"},
                    {"@type": "ListItem", "position": 2, "name": "Areas covered", "item": "https://www.simpsonsbreakdownrecovery.co.uk/#areas"},
                    {"@type": "ListItem", "position": 3, "name": f"{area['name']} breakdown recovery"},
                ],
            },
            {
                "@type": "FAQPage",
                "@id": f"https://www.simpsonsbreakdownrecovery.co.uk/areas/{area['slug']}.html#faq",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": f"How quickly can you reach {area['name']}?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": f"Typically {area['eta']} from your call, depending on traffic and which truck is nearest. We operate a 20-mile radius from our Edgbaston depot and {area['name']} sits {area['distance']}.",
                        },
                    },
                    {
                        "@type": "Question",
                        "name": f"Which {area['name']} postcodes do you cover?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": f"We cover {area['postcodes']}, along with the surrounding streets and main routes including {area['roads']}.",
                        },
                    },
                    {
                        "@type": "Question",
                        "name": f"Do you charge more for nights or weekends in {area['name']}?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": "No. We quote a fixed price before the truck is dispatched, whatever the hour, with no after-hours loading added later.",
                        },
                    },
                ],
            },
        ],
    }, indent=2, ensure_ascii=False)


def build_page(area):
    nearby_links = "\n".join(
        '          <li><a href="{slug}.html">{name}</a></li>'.format(
            slug=slug, name=AREA_BY_SLUG[slug]["name"]
        )
        for slug in area["nearby"]
        if slug in AREA_BY_SLUG
    )

    wa_area = wa_url(
        f"Hello Simpsons Recovery, I have broken down in {area['name']}. Here is my location:"
    )
    wa_generic = wa_url("Hello Simpsons Recovery, I need help with my vehicle.")

    head = HEAD.format(
        title=f"Breakdown Recovery {area['name']} | 24/7 Car &amp; Van Towing | Simpsons Recovery",
        og_title=f"Breakdown Recovery {area['name']} | Simpsons Breakdown Recovery Services Ltd",
        description=(
            f"24/7 breakdown recovery in {area['name']} ({area['postcodes']}). "
            f"Typical arrival {area['eta']}. Cars, vans and motorbikes recovered from "
            f"{area['distance']}. Call a local operator on 07706 057962."
        ),
        name=html.escape(area["name"]),
        tick_name=html.escape(area["name"]).upper(),
        postcodes=html.escape(area["postcodes"]),
        eta=html.escape(area["eta"]),
        distance=html.escape(area["distance"]),
        roads=html.escape(area["roads"]),
        intro=html.escape(area["intro"]),
        landmarks=html.escape(area["landmarks"]),
        scenarios=html.escape(area["scenarios"]),
        jsonld=build_jsonld(area),
        wa_area=wa_area,
        wa_generic=wa_generic,
    )

    footer = FOOTER.format(nearby_links=nearby_links, wa_generic=wa_generic, wa_area=wa_area)
    return head + footer


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    for area in AREAS:
        path = os.path.join(OUT_DIR, area["slug"] + ".html")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(build_page(area))
        print("wrote", path)


if __name__ == "__main__":
    main()
