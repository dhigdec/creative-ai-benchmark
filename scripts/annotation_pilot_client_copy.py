"""Client-facing copy for the ten annotation pilot briefs."""

from textwrap import dedent


BRIEFS = {
    "PHOTO-04": dedent("""\
        Three villas, one recognisable collection

        We look after three houses on the Ligurian coast. We want the booking imagery to feel like one collection without making Oliveto, Scogliera and Verranza look interchangeable. Please keep the real stone, limewash, water and afternoon light; the attached examples show the over-processed look we want to avoid.

        We need a booking hero for each villa. Use that villa's own photograph and name. Show its lowest 2027 nightly rate from rates_2027.csv as a "from" price, name the season that rate belongs to, and make the booking action easy to read.

        We also need a six-page comparison brochure. Give each house a clear identity and include its sleeping capacity, minimum stay and nightly rate for each of the three seasons in rates_2027.csv. Please use the gate monogram at least once. The owner's note includes permissions and exclusions; follow those when selecting photographs and copy.
    """).strip(),
    "PHOTO-06": dedent("""\
        Ada Hollis family archive

        We are putting together an archive of Ada's photographs for a family reunion. We have nine scans, and we need two finished versions of each one: a careful restoration master and a share image that relatives can keep.

        Please repair visible damage without changing Ada's features or inventing details that are not in the photograph. On the share images, keep the whole print, including its original border; trim only the album page or scanner bed around it. Add a short caption on a Paper White margin outside the picture, using the approved record for the year, place and people shown.

        The first five scans are monochrome and should stay that way. The remaining four are colour photographs and should remain in colour. The set should feel respectful of the period rather than newly staged.
    """).strip(),
    "PHOTO-08": dedent("""\
        Meridian Motors listing and forecourt images

        Our vehicles were photographed in three different bays, and the lighting makes our listings look inconsistent. We need an orderly showroom look while keeping each car's actual paint and condition honest.

        Please make six vehicle sales cards, one for each stock record. Pair each card with a photograph of that vehicle and include its stock number, year, make, model, trim, mileage, asking price and certification tier from the intake register. The enquiry line should invite buyers to ask Meridian Motors in Portland, Maine, about that stock number.

        We also need one forecourt campaign image featuring all six vehicles and no others. Give each its own photograph and year/make/model caption, and include our compass roundel. Please do not retouch away visible condition details that a buyer would need to know about.
    """).strip(),
    "PHOTO-10": dedent("""\
        Northgrove product images and capsule launch

        Customers choose our basics by colour and fabric, so the garments must look consistent without losing their real colour, shape or texture.

        Please make six designed product-page modules at 1440 x 1800 px as PNGs, one for each supplied style. northgrove_placements.txt also mentions an older 1600 x 2000 JPEG hero; that is not the file we need for this job. Use the style names in northgrove_copy.txt. Keep each photographed colourway true to the garment and use only colourway names approved for that style in northgrove_colourways.csv.

        We also need a six-page launch carousel with a coherent direction across the capsule. Open with Northgrove and the supplied mark, prepared as clean artwork within our type system. Close with the approved shopping line from northgrove_copy.txt, exactly as written.
    """).strip(),
    "PHOTO-19": dedent("""\
        Speaker portraits for Cascadia Founders Summit

        Eighteen speakers have sent us photographs taken in very different settings. We need them to sit together in the programme and on stage screens without making the people look alike.

        Please make one speaker card for each person in speakers.csv. Match the right portrait to the right speaker, make their name the strongest line, and include their role, affiliation and session. The role should still read on a phone. Use the CFS mark shown on summit_badge_2025_PRINTER.pdf.

        We also need one announcement for the summit itself, not for an individual speaker. "Cascadia Founders Summit" should be the headline, with the approved date and a clear invitation to register. We have not supplied a registration URL or deadline, so please do not add one. Do not introduce a ticket price beyond the stated pass range.
    """).strip(),
    "PHOTO-20": dedent("""\
        Astrid Vellacourt speaking and investor materials

        We are preparing Astrid's speaking and investor materials. The photography and supporting pieces should feel like one considered professional identity, grounded in her industrial-design practice.

        The set includes a speaker booking one-pager, three confirmed-talk announcements, three banners and nine talk cards. The one-pager should use the approved biography and give each talk title with its one-line subject. Its booking contact is Astrid Vellacourt - Vellacourt & Sund.

        For the announcements, use the supplied announcement wording with the correct event name, date and talk title from each record. These are 1080 x 1350 px posts, not squares. Each banner needs the matching talk title, event name, date and supplied portrait. Each talk card needs that record's title, event, date and format. Please use the wording and dates as provided rather than rewriting them.
    """).strip(),
    "PHOTO-24": dedent("""\
        Lunara autumn campaign and dealer files

        We need an autumn campaign image and a separate set of clear dealer-facing files. The campaign may use a richer tonal treatment; the product information must remain accurate, especially dial colour and finish.

        Please make one key visual featuring a single named watch, five product-page features, and one dealer launch sheet covering all five references. The key visual should keep the watch dominant. For each product feature, use the matching case and the reference, caliber, case metal and dial finish exactly as listed in lunara_register.csv. On the dealer sheet, pair each watch photograph with its reference, dial finish and caliber, and include the supplied timing line word for word.

        The old certificate is a visual reference for the product, not a typography template. Follow the current brand type rules for the new files.
    """).strip(),
    "PHOTO-26": dedent("""\
        Thornmere autumn wholesale collection

        Our ceramics and textiles were photographed under two different lighting rigs. We want the twenty pieces to read as one warm autumn range, while keeping the indigo, reactive glazes and woven patterns true to the objects.

        Please create a styled collection spread that brings all twenty supplied products together. We also need a wholesale presentation for trade buyers. Give each featured object its correct name, dimensions, materials, care line and price from thornmere_autumn_skus.csv. Open the presentation with Thornmere Home as the main heading, then lead buyers through the range in a useful order.
    """).strip(),
    "PHOTO-28": dedent("""\
        Verda's second-studio launch

        We are opening a second reformer studio on Calloway Row. The launch should feel calm and welcoming, and it should show the room we actually have. The two room photographs are dusky; please improve them rather than substituting an invented studio.

        We need a launch-page composition, a class announcement and a booking story. Show our own room in the launch page and include every class and price from roster_2027.csv, along with a clear way to book. For the class announcement, pair the pictured instructor with their own class, price and validity from the roster. Identify the instructor by their full name and place the cutout on solid Warm Off White or Sage. Keep the booking action inside the story's safe area.

        Use the supplied verda_logo_web.png wordmark on all three pieces. Keep its letterforms rather than retyping it; on screen it stays on one line and no larger than 34 px. On the launch page, place it above the headline as its own lockup.
    """).strip(),
    "LAYOUT-15": dedent("""\
        Aldervale Mutual producer counter cards

        The printer who made our counter cards has closed. We have the last press file and need a reusable design for this year's producer run, not a one-off imitation.

        Please prepare fourteen producer-specific cards. Each card needs the correct producer and office information from its record. Reproduce the full Disclosure Text exactly and keep it inside the trim. Do not add a district line; the supplied records do not identify one.

        The old press file shows which information belongs on a card, but it is not the type or colour standard for this run. Use the attached Aldervale identity for the new layout, and set the licence line and office as body text.
    """).strip(),
}


BRAND_ABOUT = {
    "PHOTO-04": (
        "Verranza Coastal Retreats is a collection of three coastal villas in Liguria, Italy. "
        "Guests book whole houses directly or through a small network of travel agents. "
        "The brand relies on honest photographs of the houses, stone and water rather than a polished resort look."
    ),
    "PHOTO-10": (
        "Northgrove is a Burlington, Vermont apparel label making everyday basics at an accessible premium price. "
        "Customers shop the range by garment, colour and fabric, so the visual identity needs to make those differences easy to trust."
    ),
    "LAYOUT-15": (
        "Aldervale Mutual is a regulated insurer serving households in central Vermont. "
        "Its local producers use plain, reliable materials to explain cover and contact details without a hard sell."
    ),
}
