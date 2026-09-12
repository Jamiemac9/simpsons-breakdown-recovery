"""Local content for the Simpsons Breakdown Recovery area pages.

One record per area with the detail that makes a location page genuinely
useful rather than a thin template: the route we take in, the specific roads
and their access problems, the callouts we actually get, and area-specific
FAQs.

Everything here is operational description — road names, access constraints,
vehicle types. No invented customer names, job counts, prices or statistics.
The only performance figures used anywhere on the site are the ones the
business states itself: a 20-mile radius, and a 30–45 minute average local
arrival.
"""

AREAS = [
    {
        "slug": "edgbaston-breakdown-recovery",
        "name": "Edgbaston",
        "postcodes": "B15, B16 and B17",
        "distance": "Depot base",
        "eta": "15–25 minutes",
        "roads": "A456 Hagley Road, Icknield Port Road, A4540 Middleway and Chad Road",
        "intro": (
            "Edgbaston is home. Our depot sits on Icknield Port Road, which means an Edgbaston "
            "callout is the only one where we never have to cross the city to reach you. If your "
            "car will not start in the Calthorpe Estate or you have a flat on the Hagley Road, we "
            "are usually the nearest recovery truck on the road."
        ),
        "approach": (
            "Because we start from the middle of the area, response here is the quickest we offer. "
            "Instead of joining traffic from the ring road, we are straight onto the A4540 Middleway "
            "and can pick between Hagley Road, Chad Road or the Five Ways island depending on which "
            "direction the congestion is coming from."
        ),
        "landmarks": (
            "Edgbaston Village, Five Ways Island, the Hagley Road corridor, Birmingham Botanical "
            "Gardens, Edgbaston Reservoir, the Calthorpe Estate and the Priory"
        ),
        "routes": [
            ("A456 Hagley Road", "Fastest route east–west, but the curved section near Five Ways has no verge, so we stop on the kerb side and work from the pavement."),
            ("Five Ways Island", "The underpasses mean a broken-down car has to be moved off the carriageway before anything is loaded — expect us to secure the position first."),
            ("A4540 Middleway", "Our default route in and out. Middle of the day it is the quickest way around the area, mornings and evenings it is not."),
            ("Chad Road and Norfolk Road", "Residential streets with permit parking and residents' bays, so we usually need to work from the junction rather than outside your door."),
        ],
        "callouts": [
            "Dead batteries outside the apartment blocks along Hagley Road and Bath Row",
            "Cars that will not restart in the multi-storey and basement car parks around Five Ways",
            "Vehicles that have to be moved off the A456 quickly because they are blocking a live lane",
            "Pre-purchase and garage-to-garage moves for owners who need a car shifted within the postcode",
        ],
        "local_note": (
            "Two things shape almost every Edgbaston job: permit parking and the reservoir end of "
            "Icknield Port Road. If your car is in a residents' bay we may need you to be there to "
            "move it clear, and the terraced streets off Monument Road have entries tight enough "
            "that a loaded flatbed cannot get in — we winch the vehicle to the junction instead. "
            "The A456 is the other factor: a stalled car on Hagley Road blocks a lane immediately, "
            "so tell us on the phone if you are on the main road rather than a side street and we "
            "will treat it as a priority."
        ),
        "faqs": [
            ("Do you cover the whole of Edgbaston?", "Yes — both the B15 and B16 sides, including Edgbaston Village, the Calthorpe Estate, Five Ways, Chad Valley and the roads around the reservoir. If you are on a private estate road, tell us which one when you call so we can plan where to position the truck."),
            ("Can you get a car out of the Five Ways multi-storeys?", "Yes, and it is one of the most common things we get asked to do here. We carry low-profile skates and dollies for exactly this, so a car that will not start can be moved out of a tight bay without scraping the ramp or the pillars."),
            ("How quickly can you reach Edgbaston?", "Usually 15 to 25 minutes, because the depot is in the area. If we are already out on another job we will tell you honestly where the nearest truck is rather than give you a time we cannot keep."),
            ("Do you charge a call-out fee for Edgbaston jobs?", "We quote a fixed price before the truck moves. There is no separate call-out charge added on top, and no surcharge for evenings or weekends."),
        ],
        "nearby": ["harborne-breakdown-recovery", "birmingham-city-centre-breakdown-recovery", "smethwick-breakdown-recovery"],
    },
    {
        "slug": "harborne-breakdown-recovery",
        "name": "Harborne",
        "postcodes": "B17",
        "distance": "1.8 miles from the depot",
        "eta": "20–30 minutes",
        "roads": "Harborne High Street, Court Oak Road, Lordswood Road and Metchley Lane",
        "intro": (
            "Harborne is one of our quickest runs — under two miles from the depot. The High Street "
            "is narrow, busy and lined with parked cars for most of the day, and knowing exactly "
            "where a flatbed can stop without blocking the traffic behind it is the difference "
            "between a ten-minute pickup and half an hour of chaos."
        ),
        "approach": (
            "We normally come in from the reservoir side and down through Metchley Lane rather than "
            "trying to reach you along the High Street itself. That approach also puts us close to "
            "the Queen Elizabeth Hospital, which is where a good number of our Harborne jobs start."
        ),
        "landmarks": (
            "Harborne High Street, the Queen Elizabeth Hospital, the University of Birmingham, "
            "Metchley Park, Court Oak Road and Harborne Pool"
        ),
        "routes": [
            ("Harborne High Street", "Lined with parked cars and bus stops, so loading is normally done in the nearest side street or in a marked bay."),
            ("Metchley Lane", "Our preferred way in. Quiet enough to stop on, and it puts us straight into the hospital and university area."),
            ("Court Oak Road and Lordswood Road", "Wider and easier to work in, with driveways we can usually get a vehicle onto for loading."),
            ("A38 Bristol Road", "The nearest major artery. If you break down on the Bristol Road side of Harborne we treat it as a priority because it is a live dual carriageway."),
        ],
        "callouts": [
            "Staff cars that will not start after a night shift at the QE",
            "Flat tyres collected from the High Street and taken to a local tyre fitter",
            "Cars with seized brakes or locked steering that cannot be rolled onto a bed",
            "Students' and residents' cars left standing for weeks that will not turn over",
        ],
        "local_note": (
            "The Harborne job we see most is the hospital commuter: a nurse or doctor finishing a "
            "late shift to find a flat battery in a staff car park. Because those car parks have "
            "barriers and low internal clearance, we usually meet you at the barrier rather than "
            "trying to get a flatbed into the deck itself, winch the car out and load it in the "
            "main approach. The other recurring one is the High Street flat: there is almost "
            "nowhere to stop on the road itself, so we normally ask you to put your hazards on and "
            "stay with the car while we come in from a side road."
        ),
        "faqs": [
            ("Do you cover Harborne from the depot quickly?", "Yes — Harborne is 1.8 miles from Icknield Port Road, so it is one of the closest areas we cover. Typical arrival is 20 to 30 minutes depending on whether the High Street is congested."),
            ("Can you recover from the QE Hospital car parks?", "Yes. Hospital car parks normally have height barriers, so we meet you at the barrier and recover the vehicle to the main approach rather than trying to drive the flatbed into the deck. Phone us when you are at the car and we will talk you through it."),
            ("My car is on a residents' permit bay on the High Street — is that a problem?", "Not usually, but you will need to be with the vehicle. We may have to load from the nearest side street or a loading bay rather than from the bay itself, and it helps if you can be there to move it clear if a warden or traffic asks."),
            ("Can you take my car to a specific garage in Harborne?", "Yes — to any garage, tyre fitter or bodyshop you nominate, including ones on the High Street and the ones on the industrial roads off Ravenshaw Lane. Just give us the name when you book."),
        ],
        "nearby": ["edgbaston-breakdown-recovery", "birmingham-city-centre-breakdown-recovery", "halesowen-breakdown-recovery", "smethwick-breakdown-recovery"],
    },
    {
        "slug": "birmingham-city-centre-breakdown-recovery",
        "name": "Birmingham city centre",
        "postcodes": "B1, B2, B3, B4 and B5",
        "distance": "1.5 miles from the depot",
        "eta": "20–35 minutes",
        "roads": "the A38(M) Aston Expressway, the Queensway tunnels, Broad Street and Suffolk Street Queensway",
        "intro": (
            "The city centre is where most recovery firms give up. Basement car parks with tight "
            "ramps, 1.9 metre height barriers and cars that cannot be pushed make it genuinely "
            "difficult work, so we carry the skates, dollies and compact winching gear needed to "
            "get a dead vehicle out without marking it — or the building."
        ),
        "approach": (
            "City centre jobs are rarely about how fast we can drive, they are about whether we can "
            "reach the vehicle at all. We come in off the Middleway and use the ring road tunnels as "
            "far as we can, then walk the last stretch if a car park ramp will not take the truck."
        ),
        "landmarks": (
            "Bullring, Grand Central, the Mailbox, Broad Street, Paradise, the Jewellery Quarter, "
            "the Utilita Arena and the Chinese Quarter"
        ),
        "routes": [
            ("Broad Street and the Arcadian", "Bus gates and pedestrianised sections mean we have to stop on the nearest permitted section and recover across to it."),
            ("Queensway tunnels", "Never stop in the tunnels. Get to a lay-by or out of the portals first, then call us with the nearest surface marker."),
            ("A38(M) Aston Expressway", "A live motorway-standard road with no hard shoulder on parts. Treat it like a motorway breakdown and get behind the barrier."),
            ("Digbeth and Bradford Street", "Narrow, heavily parked and often busier than the main roads. We normally work from the nearest wide junction."),
        ],
        "callouts": [
            "Non-runners stuck on the third or fourth level of a multi-storey car park",
            "Cars immobilised in basement bays beneath apartment blocks around Broad Street and the Jewellery Quarter",
            "Late-night breakdowns on the ring road and around the Arcadian",
            "Vehicles that cannot be driven after an accident in the city centre leaving them blocking a lane",
        ],
        "local_note": (
            "Almost everything difficult about the city centre comes down to height and ramp "
            "angles. A typical multi-storey here has a 1.9 metre barrier, a spiral ramp and a "
            "ticket machine that will not let a recovery truck in. The way we handle it is to park "
            "outside, recover the car down to the exit deck with wheel skates, then load it in the "
            "open where there is room. If your car is in an underground basement below an apartment "
            "block, tell us the clearance on the phone — it changes the equipment we bring and it "
            "is the single most useful thing you can tell us."
        ),
        "faqs": [
            ("Can you really get a car out of a multi-storey car park?", "Yes, but not by driving the flatbed in. We recover the vehicle down and out of the deck using wheel skates, then load it outside. That is why we ask for the height barrier measurement and how many levels down you are when you call."),
            ("What if I break down in a bus gate or pedestrianised area?", "Stay with the vehicle if it is safe, put your hazards on, and call us with the nearest street name and any landmark. We work with the traffic regulations rather than against them, so we may need to position the truck on the nearest permitted road and recover across."),
            ("How long does a city centre recovery take?", "Allow 20 to 35 minutes for us to reach you, then longer than a normal job for the load itself if you are in a basement or multi-storey. We will give you a realistic picture on the phone rather than a best-case number."),
            ("Do you cover the Jewellery Quarter and Digbeth?", "Yes, both. They are tight, heavily parked and full of one-way streets, so give us the exact street and the nearest junction and we will tell you where we can position."),
            ("Can you recover an electric or hybrid car in the city centre?", "Yes. Electric and hybrid vehicles are recovered on the flatbed with the drive wheels stationary, which is exactly what a tilt-and-slide bed is for. Tell us the model when you call."),
        ],
        "nearby": ["edgbaston-breakdown-recovery", "harborne-breakdown-recovery", "perry-barr-breakdown-recovery", "erdington-breakdown-recovery"],
    },
    {
        "slug": "smethwick-breakdown-recovery",
        "name": "Smethwick",
        "postcodes": "B66 and B67",
        "distance": "2.2 miles from the depot",
        "eta": "20–30 minutes",
        "roads": "the A457 Tollhouse Way, Cape Hill, Soho Way and the A41",
        "intro": (
            "Smethwick mixes busy industrial frontages with tight Victorian terraces, and the two "
            "need completely different recovery plans. We cover the whole of the B66 and B67 "
            "postcodes including Bearwood, Cape Hill and the Galton Bridge corridor."
        ),
        "approach": (
            "Two miles from the depot, so we are usually with you quickly. We come across via the "
            "A457 or through Winson Green depending on which side of Smethwick you are on, and the "
            "industrial estates off Soho Way are straightforward for a loaded flatbed."
        ),
        "landmarks": (
            "Cape Hill, Bearwood, Galton Bridge, Smethwick Rolfe Street, the A457 Tollhouse Way "
            "and the Soho Way industrial estates"
        ),
        "routes": [
            ("A457 Tollhouse Way", "The main artery through the area and easy to work on, but fast-moving traffic means we set up beacons before loading."),
            ("Cape Hill", "Commercial frontages both sides with frequent deliveries, so kerbside space is unpredictable at trading hours."),
            ("Soho Way industrial estates", "The easiest jobs we get in Smethwick — wide yards, level ground and room to swing a full flatbed in."),
            ("Bearwood and the Hagley Road end", "Residential terraces with permit bays; normally we load from the junction rather than outside the property."),
        ],
        "callouts": [
            "Trades vans that have failed part-loaded on Cape Hill or the A457",
            "Delivery vehicles stuck at an industrial unit on Soho Way with stock still on board",
            "Cars that will not start on residential terraces where there is nowhere to park",
            "Vehicles with flat tyres collected and taken to a Smethwick tyre fitter",
        ],
        "local_note": (
            "The bulk of Smethwick work is commercial. A plumber or electrician with a loaded van "
            "broken down on Cape Hill is losing money by the hour, so we load with the tools and "
            "stock still on board and get the van back to the yard rather than stripping it out at "
            "the roadside. On the residential side, the Victorian terraces bring a different "
            "problem: narrow entries and dropped kerbs that were never designed for a lorry, so we "
            "assess on arrival whether the vehicle can be winched to a wider point before loading."
        ),
        "faqs": [
            ("Do you recover loaded work vans in Smethwick?", "Yes. We keep the tools and stock on board and load the van as it stands, then take it back to your base or a garage. If the load is unusually heavy or tall, mention it when you call so we bring the right truck."),
            ("Can you get into the Soho Way industrial estates?", "Easily — those yards are the simplest work we do because there is room to manoeuvre. The main thing is telling the site manager we are coming so the gate is open when we arrive."),
            ("Which Smethwick postcodes do you cover?", "B66 and B67 in full, covering Cape Hill, Bearwood, Galton Bridge, Smethwick Rolfe Street and the surrounding streets. We are 2.2 miles from the area so typical arrival is 20 to 30 minutes."),
            ("My car is on a terrace with no parking — can you still recover it?", "Yes. We will either winch the vehicle to a wider point on the road or load from the nearest junction. It helps enormously if you are with the car to move it clear and to keep the neighbours' access open."),
        ],
        "nearby": ["edgbaston-breakdown-recovery", "west-bromwich-breakdown-recovery", "harborne-breakdown-recovery", "birmingham-city-centre-breakdown-recovery"],
    },
    {
        "slug": "west-bromwich-breakdown-recovery",
        "name": "West Bromwich",
        "postcodes": "B70 and B71",
        "distance": "4.5 miles from the depot",
        "eta": "25–35 minutes",
        "roads": "the A41 Expressway, M5 junction 1, High Street and All Saints Way",
        "intro": (
            "West Bromwich sits right on the M5, which means a good share of our jobs here start on "
            "a slip road or a roundabout rather than a driveway. We cover the town centre, New "
            "Square, Sandwell Valley and the A41 corridor."
        ),
        "approach": (
            "Four and a half miles out. The A41 Expressway is the quickest way in and out, and from "
            "junction 1 of the M5 we can be on the motorway network within a couple of minutes if "
            "you are stranded on a slip road or the roundabout above it."
        ),
        "landmarks": (
            "New Square, Sandwell Valley, the Hawthorns, All Saints Way, the A41 Expressway and "
            "Bescot"
        ),
        "routes": [
            ("A41 Expressway", "Our main route in. Dual carriageway with no safe stopping place, so a breakdown here is treated as a priority."),
            ("M5 junction 1", "Slip roads and the island above are the highest-risk spots we work in West Bromwich. Get behind the barrier before you call."),
            ("High Street and New Square", "Retail traffic and delivery bays; we normally load from a marked bay or the nearest side street."),
            ("All Saints Way and the Hawthorns approach", "Match days make the whole area impassable, so tell us if you are near the ground on a fixture day."),
        ],
        "callouts": [
            "Breakdowns on the M5 junction 1 slip roads and the roundabout above",
            "Commercial vans that have failed outside a depot or on an industrial estate",
            "Cars recovered from New Square and town centre car parks",
            "Flat batteries on residential streets across the B70 and B71 postcodes",
        ],
        "local_note": (
            "West Bromwich is a motorway town for us. Junction 1 of the M5 has long slip roads and "
            "a complex island, and a car that stops there is in a genuinely dangerous position, so "
            "we take those calls first and talk you through getting behind the barrier while we are "
            "on the way. Away from the motorway, New Square and the High Street are the usual "
            "retail-park jobs — a car that will not start after shopping, which is normally a "
            "battery rather than anything more serious."
        ),
        "faqs": [
            ("How quickly can you reach the M5 at West Bromwich?", "It is about 4.5 miles from the depot and we use the A41 Expressway to get there, so typically 25 to 35 minutes. Motorway and slip-road calls are treated as priority because of the risk to you."),
            ("What should I do if I break down on the M5 junction 1 roundabout?", "Get off the carriageway if you can and onto the verge or a refuge, put your hazards on, and stay behind the barrier rather than beside the car. Then call us with the junction number and which direction you were travelling."),
            ("Do you cover Sandwell Valley and the Hawthorns?", "Yes, both, though on match days the roads around the ground can be closed or one-way. If you break down near the stadium on a fixture day, phone us and we will talk you through where we can realistically reach you."),
            ("Can you take my van back to a West Bromwich industrial unit?", "Yes. Give us the unit address and a contact name for the gate and we will deliver it straight there, loaded, rather than dropping it at a garage you did not ask for."),
        ],
        "nearby": ["smethwick-breakdown-recovery", "dudley-breakdown-recovery", "walsall-breakdown-recovery", "perry-barr-breakdown-recovery"],
    },
    {
        "slug": "perry-barr-breakdown-recovery",
        "name": "Perry Barr",
        "postcodes": "B42",
        "distance": "3.6 miles from the depot",
        "eta": "25–35 minutes",
        "roads": "the A34 Walsall Road, Birchfield Road, Aldridge Road and Aston Lane",
        "intro": (
            "The A34 through Perry Barr is one of the busiest dual carriageways in north "
            "Birmingham, and a broken-down vehicle there backs traffic up within minutes. We treat "
            "Perry Barr, Birchfield and the Aldridge Road as priority work."
        ),
        "approach": (
            "Just over three and a half miles. We come up through the city and out along the A34 or "
            "Birchfield Road, which means we can pick the side of the carriageway that is actually "
            "moving rather than committing to one route blind."
        ),
        "landmarks": (
            "Alexander Stadium, One Stop Shopping Centre, Perry Barr railway station, Birchfield "
            "Road, the A34 Walsall Road and Perry Park"
        ),
        "routes": [
            ("A34 Walsall Road", "Dual carriageway with limited lay-bys. A stalled car blocks a live lane, so this is always a priority call."),
            ("Birchfield Road", "The main way in and out of the area for us. Busy but slower, which makes positioning easier than the A34."),
            ("Aldridge Road", "Wider and easier to work on, with several service roads where a flatbed can sit safely."),
            ("Aston Lane and the One Stop approaches", "Retail traffic and pedestrians, so we load from the marked bays rather than the access road."),
        ],
        "callouts": [
            "Commuter breakdowns on the A34 during the morning and evening peaks",
            "Flat tyres and engine faults in and around the One Stop shopping centre",
            "Event-day traffic incidents near Alexander Stadium",
            "Residential battery and starter failures across the B42 postcode",
        ],
        "local_note": (
            "Perry Barr is dominated by one road. The A34 has long stretches with no lay-by and no "
            "hard shoulder, and when a car stops the queue forms behind it almost immediately. If "
            "you are on the A34, the single most useful thing you can do is get the car as far onto "
            "the verge or into a side road as it will roll, then call us — it takes minutes off the "
            "job because we are not having to manage live traffic while we winch. Around the One "
            "Stop and the stadium, the issue is usually access rather than distance."
        ),
        "faqs": [
            ("How quickly can you get to the A34 Walsall Road?", "Typically 25 to 35 minutes from the depot. Because the A34 is a live dual carriageway we treat those calls as priority, and we will advise you on getting clear of the carriageway while we are on the way."),
            ("Do you cover Alexander Stadium on event days?", "We cover the area, but on major event days the roads around the stadium are closed or contraflowed, which changes where we can reach you. Call us and describe the nearest gate or car park and we will plan around the closures."),
            ("Can you recover a car from the One Stop car park?", "Yes — that is a common job. Car parks there are open-air so we can normally come to the vehicle directly rather than recovering it to a barrier first."),
            ("Which postcodes around Perry Barr do you cover?", "B42 plus the surrounding streets into Birchfield, Handsworth Wood and Aston. We are 3.6 miles from the area, so arrival is normally 25 to 35 minutes."),
        ],
        "nearby": ["birmingham-city-centre-breakdown-recovery", "erdington-breakdown-recovery", "walsall-breakdown-recovery", "west-bromwich-breakdown-recovery"],
    },
    {
        "slug": "erdington-breakdown-recovery",
        "name": "Erdington",
        "postcodes": "B23 and B24",
        "distance": "5.2 miles from the depot",
        "eta": "25–40 minutes",
        "roads": "the A38 Tyburn Road, Erdington High Street, Kingsbury Road and Gravelly Hill",
        "intro": (
            "Tyburn Road is packed with industrial units and commercial traffic and it feeds "
            "straight into Spaghetti Junction. A van or lorry down on that corridor blocks a lot of "
            "people, so Erdington jobs get moved quickly. We cover the High Street, Gravelly Hill, "
            "Stockland Green and the B23 and B24 postcodes."
        ),
        "approach": (
            "Five miles out along the A38. The advantage of the Tyburn Road corridor is that it "
            "connects directly to the M6 at junction 6, so we can reach Erdington from either the "
            "city end or off the motorway depending on what the traffic is doing."
        ),
        "landmarks": (
            "Erdington High Street, the Tyburn Road industrial estates, Fort Dunlop, Gravelly Hill, "
            "Stockland Green and the M6 junction 6 approaches"
        ),
        "routes": [
            ("A38 Tyburn Road", "Long industrial corridor with frequent loading. Wide enough to work in, but heavy goods traffic means we set up beacons well before the vehicle."),
            ("Gravelly Hill and Spaghetti Junction", "The M6 junction 6 interchange. Treat it as motorway work — get clear of the carriageway and call us with the junction and direction."),
            ("Erdington High Street", "Narrow with bus stops and loading bays; we normally recover to the nearest wider junction before loading."),
            ("Kingsbury Road and Stockland Green", "Residential with driveways, which makes those jobs the easiest in the area — we can often load straight off a drive."),
        ],
        "callouts": [
            "Loaded commercial vehicles failing on Tyburn Road",
            "Cars breaking down on the approach to Spaghetti Junction and on the A38",
            "Battery failures on the residential streets around Stockland Green and Gravelly Hill",
            "Vehicles collected from garage forecourts and moved between workshops in the B23 and B24 area",
        ],
        "local_note": (
            "Tyburn Road and the M6 junction 6 approaches generate most of our Erdington work, and "
            "they are two very different problems. On Tyburn Road the road is wide and the issue is "
            "traffic volume plus the number of artic drivers who cannot see a stationary car until "
            "late — we set up early and work fast. On Gravelly Hill the issue is that it is "
            "motorway-standard with no hard shoulder in places, so the rule is the same as any "
            "motorway job: get out of the car and behind the barrier first, then call. The "
            "residential half of Erdington, by contrast, is straightforward."
        ),
        "faqs": [
            ("Do you cover the M6 at Spaghetti Junction?", "Yes. Junction 6 and the A38(M) approaches are part of our regular work, and we treat them as motorway jobs — get behind the barrier and ring us with the junction number and direction of travel."),
            ("Can you recover a loaded lorry or large van from Tyburn Road?", "Within reason. We will tell you on the phone whether the weight and height is something our flatbed can take, and if it is not we will say so rather than turn up and fail. Give us the vehicle type and approximate load."),
            ("How long to reach Erdington?", "Around 5.2 miles from the depot, so typically 25 to 40 minutes. The range is wide because the A38 and the M6 can both turn a straightforward run into a slow one."),
            ("Do you take vehicles to Erdington garages?", "Yes, to any garage, dealership or bodyshop you nominate in the B23 or B24 area, and to premises in neighbouring Aston, Witton and Sutton Coldfield."),
        ],
        "nearby": ["perry-barr-breakdown-recovery", "birmingham-city-centre-breakdown-recovery", "sutton-coldfield-breakdown-recovery", "walsall-breakdown-recovery"],
    },
    {
        "slug": "halesowen-breakdown-recovery",
        "name": "Halesowen",
        "postcodes": "B62 and B63",
        "distance": "6.4 miles from the depot",
        "eta": "25–35 minutes",
        "roads": "the A456 Manor Way, M5 junction 3 and the Halesowen bypass",
        "intro": (
            "Halesowen backs onto the M5 at junction 3, so we cover both town-centre jobs and "
            "motorway callouts from the same base. The hilly approach roads also mean we see more "
            "than our share of clutch, brake and handbrake problems."
        ),
        "approach": (
            "Six and a half miles. We come out along the A456 or drop down from the M5 depending on "
            "which side of town you are on, and both routes into Halesowen are quick outside peak "
            "hours."
        ),
        "landmarks": (
            "Halesowen town centre, Manor Way, the Cornbow Centre, M5 junction 3, and the lanes "
            "towards Romsley and Clent"
        ),
        "routes": [
            ("A456 Manor Way", "The main route in and out and the road we use most. Dual carriageway in parts, so a breakdown here needs clearing quickly."),
            ("M5 junction 3", "Our closest motorway access to you. Slip-road breakdowns are treated as priority work."),
            ("Halesowen bypass and the town centre ring", "Easier to work on than the side streets, with space for a flatbed to sit safely."),
            ("Romsley and Clent lanes", "Steep, narrow and often single-track. Expect us to approach from the nearest wider road and come to you on foot first."),
        ],
        "callouts": [
            "Clutch, brake and handbrake failures on the steeper roads around Halesowen",
            "Breakdowns on Manor Way and the bypass",
            "Motorway recoveries from the M5 junction 3 slip roads",
            "Cars stranded on the narrow lanes towards Romsley and Clent",
        ],
        "local_note": (
            "Halesowen's geography does half the work in explaining our callouts here. The town sits "
            "on a hill and a lot of the residential roads towards Romsley and Clent are steep and "
            "narrow, which is why clutch and handbrake failures show up more often than they do in "
            "flatter parts of the city. Practically, that means two things: on the lanes we may need "
            "to come to you on foot first to work out the safest way to get a loaded truck out, and "
            "a vehicle with a seized brake needs skates rather than a push. Both are normal for us — "
            "just describe the gradient and the width when you call."
        ),
        "faqs": [
            ("Why do you get more clutch problems in Halesowen?", "Because of the hills. Stop-start driving on gradients puts far more load through a clutch, and the steep residential roads towards Romsley and Clent are hard on brakes and handbrakes as well. If your car will not roll because a brake has seized, tell us and we will bring skates."),
            ("Can you reach the narrow lanes around Romsley?", "Usually yes, but we may need to walk to you first and work out the safest extraction, and we may not be able to get a loaded flatbed right to your door. Be ready for us to recover the vehicle to the nearest wider road before loading."),
            ("Do you cover M5 junction 3?", "Yes, and it is our closest motorway access to Halesowen. Slip-road breakdowns are treated as priority. Get clear of the carriageway and call us with the junction and your direction of travel."),
            ("How long is the wait to Halesowen?", "It is 6.4 miles from the depot, so typically 25 to 35 minutes. We will tell you where the nearest truck is rather than give you a number we cannot keep."),
        ],
        "nearby": ["dudley-breakdown-recovery", "harborne-breakdown-recovery", "west-bromwich-breakdown-recovery", "edgbaston-breakdown-recovery"],
    },
    {
        "slug": "dudley-breakdown-recovery",
        "name": "Dudley",
        "postcodes": "DY1, DY2 and DY3",
        "distance": "7.8 miles from the depot",
        "eta": "30–40 minutes",
        "roads": "the A4123 Birmingham New Road, Castlegate Way and Duncan Edwards Way",
        "intro": (
            "Dudley is a regular run for us, mostly along the A4123 and around Castlegate. We cover "
            "the town centre, Gornal, Sedgley, Woodsetton and the corridor towards Brierley Hill, "
            "for cars and commercial vehicles alike."
        ),
        "approach": (
            "Just under eight miles out, straight up the A4123 Birmingham New Road. It is a "
            "consistent run with no city-centre pinch points, which is why our arrival window here "
            "is tighter than you might expect for the distance."
        ),
        "landmarks": (
            "Dudley town centre, Castlegate, the Zoological Gardens, Dudley Port, Gornal, Sedgley "
            "and the A4123 Birmingham New Road"
        ),
        "routes": [
            ("A4123 Birmingham New Road", "Our main route and a fast one. Dual carriageway, so a stalled vehicle needs moving off the live lane before we load."),
            ("Castlegate Way and Duncan Edwards Way", "The town centre ring. Busy with retail traffic but wide, so positioning is straightforward."),
            ("Dudley Port and Tipton Road", "Industrial and commercial frontages with yards, which makes loading easy."),
            ("Gornal, Sedgley and the Brierley Hill corridor", "Residential and hillier; we normally work from the nearest junction or driveway."),
        ],
        "callouts": [
            "Collision recovery on the Birmingham New Road",
            "Vehicles immobilised in the town centre and Castlegate car parks",
            "Home-start battery jobs across the DY postcodes",
            "Commercial vehicle recoveries from Dudley Port and the industrial estates",
        ],
        "local_note": (
            "The A4123 shapes our Dudley work the same way the A34 shapes Perry Barr — it is the "
            "fastest way in and out but it is a dual carriageway with limited stopping space, so any "
            "breakdown on it becomes a priority job. The other thing worth knowing is that Dudley's "
            "town centre car parks are mostly open-air and multi-level rather than deep basements, "
            "which makes them easier for us than the Birmingham city centre equivalents — a dead "
            "battery here is usually a quick recovery."
        ),
        "faqs": [
            ("How long does it take you to reach Dudley?", "Typically 30 to 40 minutes. Dudley is 7.8 miles from our Edgbaston depot and the A4123 is a straightforward run, so the wait is usually more predictable than jobs closer in."),
            ("Do you cover Gornal, Sedgley and Woodsetton?", "Yes, all three, plus Dudley Port, Netherton and the Brierley Hill corridor. The hillier residential roads are narrower, so we may recover the vehicle to a junction before loading."),
            ("Can you recover a car from the Dudley town centre car parks?", "Yes. The Castlegate and town centre car parks are mostly open-air or open-deck rather than deep basements, so we can usually reach the vehicle directly instead of recovering it to a barrier."),
            ("Do you do home-start jump starts in Dudley?", "We do. A flat battery at home is one of the most common Dudley jobs we get. If the car starts and holds charge we can often get you going on the spot rather than towing it anywhere."),
        ],
        "nearby": ["halesowen-breakdown-recovery", "west-bromwich-breakdown-recovery", "walsall-breakdown-recovery", "smethwick-breakdown-recovery"],
    },
    {
        "slug": "sutton-coldfield-breakdown-recovery",
        "name": "Sutton Coldfield",
        "postcodes": "B72, B73, B74 and B75",
        "distance": "8.2 miles from the depot",
        "eta": "30–45 minutes",
        "roads": "the A5127 Lichfield Road, the A453, the Sutton bypass and The Parade",
        "intro": (
            "Sutton Coldfield's wide residential streets and driveways are straightforward for a "
            "flatbed — the awkward part is usually squeezing past parked cars on the older roads in "
            "Boldmere and Wylde Green, which is something we do every week."
        ),
        "approach": (
            "Eight miles up the A5127 or across on the A453. Once we are into Sutton the roads are "
            "more generous than inner-city Birmingham, so once we are there the job itself is "
            "usually quick."
        ),
        "landmarks": (
            "Sutton Park, The Parade, Four Oaks, Boldmere, Wylde Green, Mere Green and the A5127 "
            "Lichfield Road"
        ),
        "routes": [
            ("A5127 Lichfield Road", "The main route in and out, and a road we know well. Busy at peak times but easy to work on outside those hours."),
            ("Sutton bypass", "A453 and the bypass are our fastest routes; a breakdown here is a live-lane problem so it gets priority."),
            ("The Parade and town centre", "Restricted parking and pedestrian access, so we normally recover to the nearest permitted loading point."),
            ("Boldmere and Wylde Green residential streets", "Older roads with cars parked both sides. We assess on arrival whether a loaded flatbed can get in or whether we winch out to the junction."),
        ],
        "callouts": [
            "Cars that have not turned a wheel for months sitting on a driveway",
            "Breakdowns on the Sutton bypass and the A5127",
            "Motorcycles recovered to specialist workshops",
            "Prestige and hybrid vehicles moved to main dealers for diagnosis",
        ],
        "local_note": (
            "Sutton brings us two very different jobs. The first is the long-term driveway car — "
            "something that has stood for months and now will not start or will not roll because a "
            "brake has seized, which we recover to a garage for you rather than you having to deal "
            "with it. The second is the main-dealer run: prestige, hybrid and electric cars that "
            "need to go to a franchised workshop, where what matters to the owner is that the "
            "wheels and bodywork come back exactly as they went in. On the narrow Boldmere and Wylde "
            "Green streets we will tell you honestly on arrival whether we can load at the kerb or "
            "whether we need to move the car first."
        ),
        "faqs": [
            ("Do you recover cars that have been standing on a driveway for months?", "Yes, and it is a common Sutton job. Standing vehicles often have more than one problem — flat battery, seized brakes, sometimes a seized handbrake. Tell us what happens when you try to start it and we will bring the right kit."),
            ("Can you take my car to a main dealer for warranty work?", "Yes, to any franchised dealer you nominate. Electric and hybrid vehicles are recovered on the flatbed with the drive wheels stationary, which is what a tilt-and-slide bed is designed for."),
            ("Will a flatbed fit down Boldmere and Wylde Green streets?", "Sometimes, sometimes not — it depends entirely on how the cars are parked on the day. We will assess when we arrive, and if the street is too tight we will winch the vehicle out to the nearest junction and load there."),
            ("Do you recover motorcycles in Sutton Coldfield?", "Yes, strapped and recovered on the flatbed to your chosen workshop rather than towed. Tell us the bike when you call so we can bring the right tie-downs."),
        ],
        "nearby": ["erdington-breakdown-recovery", "perry-barr-breakdown-recovery", "walsall-breakdown-recovery", "birmingham-city-centre-breakdown-recovery"],
    },
    {
        "slug": "solihull-breakdown-recovery",
        "name": "Solihull",
        "postcodes": "B90, B91, B92 and B93",
        "distance": "8.5 miles from the depot",
        "eta": "30–45 minutes",
        "roads": "the A41 Solihull bypass, M42 junction 5, Warwick Road and Lode Lane",
        "intro": (
            "Solihull sees a higher proportion of prestige cars, hybrids and electric vehicles than "
            "almost anywhere else we work, and those need care. We recover EVs on the flatbed with "
            "the drive wheels stationary, and we treat your wheels and bodywork as if they were our "
            "own."
        ),
        "approach": (
            "About eight and a half miles, usually out along the A41 bypass or down from the M42 at "
            "junction 5. Both are quick outside peak hours and give us several ways into the area "
            "if one is congested."
        ),
        "landmarks": (
            "Touchwood, Solihull town centre, Shirley, Dorridge, Knowle, Lode Lane and the Land "
            "Rover site"
        ),
        "routes": [
            ("A41 Solihull bypass", "Our main route in. Dual carriageway, so a stalled vehicle is a live-lane problem and gets priority."),
            ("M42 junction 5", "Fast access from the motorway network. Slip-road breakdowns are treated as priority work."),
            ("Warwick Road and Lode Lane", "Wide and straightforward, with several garages and dealerships along them, so most deliveries end here anyway."),
            ("Shirley, Dorridge and Knowle", "Residential and generally easier than the inner-city equivalent — drives and forecourts make for simple loading."),
        ],
        "callouts": [
            "Electric and hybrid vehicles that cannot be driven",
            "Breakdowns on the A41 bypass and at M42 junction 5",
            "Prestige cars moved to franchised dealers and specialists",
            "Commercial and fleet vehicles recovered to Solihull business parks",
        ],
        "local_note": (
            "The technical job we get most in Solihull is electric and hybrid recovery. An EV that "
            "has stopped cannot be towed with wheels on the ground without risking the drive unit, "
            "so it goes on the flatbed, fully secured, with the parking brake released by the "
            "correct procedure for the model. If you know how your car needs to be put into "
            "transport mode, say so when you call and we will follow it. The other local factor is "
            "the number of dealerships and specialists around the A41 and Lode Lane, which means "
            "most of our Solihull deliveries are short and direct."
        ),
        "faqs": [
            ("Can you recover an electric car?", "Yes, and it is a routine job for us in Solihull. An EV goes on the flatbed with the drive wheels stationary rather than being towed, because towing with wheels down can damage the drive unit. If your car has a transport mode, tell us and we will use the correct procedure."),
            ("Do you cover the A41 bypass and M42 junction 5?", "Yes. We treat both as live-road work, so get clear of the carriageway, put your hazards on and call us with your location and direction of travel."),
            ("Can you take my car to a Solihull main dealer?", "Yes, to any dealer or independent you nominate in Solihull, Shirley, Dorridge or Knowle. Give us the name and postcode when you book and we will deliver it there directly."),
            ("Which Solihull postcodes do you cover?", "B90, B91, B92 and B93 — Solihull town centre, Shirley, Olton, Dorridge and Knowle. We are 8.5 miles from the area, so typical arrival is 30 to 45 minutes."),
        ],
        "nearby": ["halesowen-breakdown-recovery", "harborne-breakdown-recovery", "birmingham-city-centre-breakdown-recovery", "dudley-breakdown-recovery"],
    },
    {
        "slug": "walsall-breakdown-recovery",
        "name": "Walsall",
        "postcodes": "WS1, WS2 and WS3",
        "distance": "9.5 miles from the depot",
        "eta": "30–45 minutes",
        "roads": "the A34, M6 junctions 9 and 10, Pleck Road and the Broadway",
        "intro": (
            "Walsall sits between two of the busiest motorway junctions in the region. Junctions 9 "
            "and 10 of the M6 keep us busy, and we cover the town centre, Pleck, Bescot and the "
            "retail and industrial parks alongside them."
        ),
        "approach": (
            "Nine and a half miles, and the widest radius we work at. We usually route up the A34 "
            "or drop in from the M6, which means on a busy day we can approach from whichever side "
            "is moving."
        ),
        "landmarks": (
            "Walsall town centre, the Saddlers Centre, Pleck, Bescot Stadium, Bescot retail park "
            "and the M6 junctions 9 and 10"
        ),
        "routes": [
            ("M6 junctions 9 and 10", "Our busiest Walsall work. Both are large interchanges with long slip roads — treat them as motorway breakdowns and get behind the barrier."),
            ("A34 and the Broadway", "The main route into town. Wide, with retail frontages, so loading is normally straightforward."),
            ("Pleck Road and Bescot", "Industrial and commercial, with yards and loading bays that make recovery easy."),
            ("Town centre and the Saddlers Centre", "Restricted parking and bus routes; we normally recover to the nearest permitted loading point."),
        ],
        "callouts": [
            "Motorway recoveries around M6 junctions 9 and 10",
            "Warehouse and delivery vans failing at loading bays",
            "Accident clearance and vehicle movement after a collision",
            "Fleet vehicles recovered to Walsall business parks and yards",
        ],
        "local_note": (
            "Walsall is motorway and industrial work for us. Junctions 9 and 10 of the M6 are big, "
            "fast interchanges, and the length of the slip roads means a car that stops on one is "
            "in a bad position very quickly — so those calls jump the queue and we will talk you "
            "through getting behind the barrier while we are on the way. Closer to town, Pleck and "
            "Bescot are the opposite sort of job: wide yards, level ground and room to manoeuvre, "
            "which makes commercial recoveries there about the quickest work we do anywhere."
        ),
        "faqs": [
            ("Do you cover M6 junctions 9 and 10?", "Yes, regularly. Both are treated as motorway work — get clear of the carriageway, stay behind the barrier and call us with the junction number and your direction of travel."),
            ("Walsall is at the edge of your radius — can you still reach me?", "Walsall is about 9.5 miles from the depot and sits within our 20-mile radius, so yes. Typical arrival is 30 to 45 minutes, and the M6 can stretch that, so we will give you an honest window."),
            ("Can you recover fleet vehicles and vans in Walsall?", "Yes, including loaded vans and light commercial vehicles. If you manage a fleet, tell us the vehicle type and the yard address and we will deliver it back rather than to a garage."),
            ("Do you do accident recovery in Walsall?", "Yes. We clear vehicles from the scene, document the position for your insurer and recover the vehicle to whichever repairer or storage address is agreed."),
        ],
        "nearby": ["perry-barr-breakdown-recovery", "west-bromwich-breakdown-recovery", "dudley-breakdown-recovery", "sutton-coldfield-breakdown-recovery"],
    },
]

AREA_BY_SLUG = {a["slug"]: a for a in AREAS}
