// Builds "Adobe & Design Freelance Opportunities" .docx — narrative entries grouped by vertical.
const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, AlignmentType, LevelFormat,
  ExternalHyperlink, HeadingLevel, BorderStyle, PageBreak, TableOfContents, PageNumber,
  Header, Footer
} = require("docx");

const FL = "https://www.freelancer.com";

// Each listing: { title, platform, tools:[], budget, location, posted, url, desc }
const SECTIONS = [
  {
    vertical: "Fashion & Apparel",
    listings: [
      { title: "Sublimated Streetwear Jersey Design", platform: "Freelancer.com", tools: ["Illustrator","Photoshop"], budget: "$25 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/fashion-design/sublimated-streetwear-jersey-design", desc: "Bold, vibrant sublimated jersey for an Australian streetwear label with brand name, logo and barbed-wire detail; layered print-ready files." },
      { title: "Apparel Designer & Tech Pack Specialist", platform: "Freelancer.com", tools: ["Illustrator","Photoshop"], budget: "$13/hr avg", location: "Remote", posted: "Active", url: FL+"/projects/fashion-design/apparel-designer-tech-pack-specialist", desc: "Design oversized tees, polos and shirts from concept through to factory-ready tech packs." },
      { title: "Four Detailed Bikini Tech Packs", platform: "Freelancer.com", tools: ["Illustrator"], budget: "$305 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/adobe-illustrator/four-detailed-bikini-tech-packs", desc: "Four factory-ready bikini tech packs with flat sketches, measurements and specifications." },
      { title: "Refine 8 Luxury Printed Scarves (print-ready files)", platform: "Freelancer.com", tools: ["Photoshop"], budget: "$49 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/fashion-design/refine-luxury-printed-scarves-create", desc: "Refine cotton-modal scarf print concepts (leopard, snake) and prepare production-ready files." },
      { title: "Symbol Logo for Fashion Brand", platform: "Freelancer.com", tools: ["Illustrator","Photoshop"], budget: "$173 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/branding/symbol-logo-for-fashion-brand", desc: "Distinctive symbol-only logo for a new fashion label, for garment tags, embroidery and packaging." },
      { title: "Art Nouveau Streetwear Collection", platform: "Freelancer.com", tools: ["Illustrator","Photoshop"], budget: "$176 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/fashion-design/art-nouveau-streetwear-collection", desc: "Original Art Nouveau graphics for a full streetwear line with floral, organic patterns." },
      { title: "Fashion Sketching (campaign visuals)", platform: "Freelancer.com", tools: ["Illustrator"], budget: "$18/hr avg", location: "Remote", posted: "Active", url: FL+"/projects/adobe-illustrator/fashion-sketching", desc: "Minimalist sketches with line work and bold abstract shapes for campaign visuals." },
      { title: "Premium Streetwear Logo Design", platform: "Freelancer.com", tools: ["Photoshop"], budget: "$16 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/creative-design/premium-streetwear-logo-design", desc: "Premium, modern, unique logo for a clothing/streetwear brand." },
      { title: "Cartoon Airplane Merch Graphics", platform: "Freelancer.com", tools: ["Illustrator","Photoshop"], budget: "$337 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/vector-design/cartoon-airplane-merch-graphics", desc: "Cohesive cartoon airplane illustrations for merchandise across t-shirts, hoodies and pins." },
      { title: "Sophisticated Logo Design for Softer Days (bamboo baby clothing)", platform: "Freelancer.com", tools: ["Illustrator","Photoshop"], budget: "$185 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/branding/sophisticated-logo-design-for-softer", desc: "Premium, expandable logo for a bamboo baby-clothing brand." },
      { title: "DAVILLE SOUL - AI Campaign Creative Brief (luxury streetwear)", platform: "Freelancer.com", tools: ["After Effects","Premiere Pro"], budget: "$150 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/motion-graphics/daville-soul-campaign-creative-brief", desc: "AI artist/designer for a luxury streetwear fashion campaign with cinematic photography." },
      { title: "Minimalist Towel Label Design", platform: "Freelancer.com", tools: ["Illustrator"], budget: "$8/hr avg", location: "Remote", posted: "Active", url: FL+"/projects/adobe-illustrator/minimalist-towel-label-design-needed", desc: "Professional minimalist label for a towel brand featuring name and logo." }
    ]
  },
  {
    vertical: "Food, Restaurant & Beverage",
    listings: [
      { title: "Authentic Logo Creation for Donut Shop (Crossroads Donuts)", platform: "Freelancer.com (contest)", tools: ["Illustrator","Photoshop"], budget: "$20 guaranteed", location: "Remote", posted: "Active", url: FL+"/contest/authentic-logo-creation-for-donut-shop-2749067", desc: "Warm, memorable logo incorporating a donut and crossroads concept." },
      { title: "Frubloom Healthy Food Logo", platform: "Freelancer.com (contest)", tools: ["Illustrator","Photoshop"], budget: "$20 guaranteed", location: "Remote", posted: "Active", url: FL+"/contest/frubloom-healthy-food-logo-2748935", desc: "Fresh, vibrant logo for a healthy-food brand with fruit symbolism and letter-F integration." },
      { title: "Modern Corn Puff Logo Design (pufuleti)", platform: "Freelancer.com (contest)", tools: ["Illustrator","Photoshop"], budget: "$35 guaranteed", location: "Remote", posted: "Active", url: FL+"/contest/modern-corn-puff-logo-design-2748734", desc: "Modern, clean logo for a corn-puff snack brand with a muted neutral palette." },
      { title: "FSSAI-Compliant Chicken Label Redesign", platform: "Freelancer.com", tools: ["Illustrator"], budget: "$21 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/label-design/fssai-compliant-chicken-label-redesign", desc: "Redesign a ready-to-eat chicken label to FSSAI regulations with appetizing imagery and icons." },
      { title: "Luxury Energy Drink Packaging", platform: "Freelancer.com", tools: ["Illustrator","Photoshop"], budget: "$95 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/packaging-design/luxury-energy-drink-packaging", desc: "Premium energy-drink label communicating natural ingredients, with 3D mock-ups." },
      { title: "Minimalist Earth-Toned Spice Packaging Design", platform: "Freelancer.com", tools: ["Illustrator"], budget: "$53 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/packaging-design/minimalist-earth-toned-spice-packaging", desc: "Modern minimalist spice packaging in earth tones with nutrition facts, brand story and recipes." },
      { title: "Food & Beverage Label Design", platform: "Freelancer.com", tools: ["Illustrator","Photoshop"], budget: "$9/hr avg", location: "Remote", posted: "Active", url: FL+"/projects/label-design/food-beverage-label-design-40486372", desc: "Fresh shelf-ready label with 2-3 concepts, mock-ups and print-ready files." },
      { title: "Graphic Designer Needed for Two-Sided Restaurant Table Menu", platform: "PeoplePerHour", tools: ["Illustrator"], budget: "$116", location: "Remote", posted: "17 days ago", url: "https://www.peopleperhour.com/freelance-jobs/design/graphic-design/graphic-designer-needed-for-two-sided-restaurant-table-menu-4496353", desc: "Print and digital two-sided restaurant menu, delivered as an editable Illustrator file." },
      { title: "Canva Cafe Menu Designer Needed (Editable A4)", platform: "PeoplePerHour", tools: ["Canva"], budget: "$74", location: "Remote", posted: "17 days ago", url: "https://www.peopleperhour.com/freelance-jobs/design/graphic-design/canva-caf%C3%A9-menu-designer-needed-editable-a4-i-have-the-mock-4496221", desc: "Recreate a brunch/juice-bar menu in Canva, three-column layout, print-ready." },
      { title: "Restaurant Menu (SmashBurger, retro/street-food)", platform: "Freelancer.com", tools: ["Illustrator","Photoshop"], budget: "$7/hr avg", location: "Remote", posted: "3 days left", url: FL+"/projects/menu-design/restaurant-menu-40480887", desc: "Creative one-page retro street-food menu with burgers, sides and beverages sections." },
      { title: "Restaurant Brand Manual Redesign", platform: "Freelancer.com", tools: ["Illustrator","Photoshop"], budget: "$206 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/brand-management/restaurant-brand-manual-redesign", desc: "Updated brand manual with new color scheme, typography and full branding guidelines." },
      { title: "Bakery B2B Catalog Development", platform: "Freelancer.com", tools: ["InDesign","Creative Cloud"], budget: "$53 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/catalog-design/bakery-catalog-development", desc: "Digital PDF catalog for a bakery targeting distributors, with descriptions, pricing and images." },
      { title: "Creative Packaging Design for Food Product", platform: "Freelancer.com", tools: ["Illustrator","Photoshop"], budget: "$14 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/packaging-design/creative-packaging-design-for-food", desc: "Innovative food/beverage packaging emphasizing creativity and compliance." },
      { title: "Full restaurant brand: logo, menu, shop sign, uniform", platform: "PeoplePerHour", tools: ["Not specified"], budget: "$118", location: "Remote", posted: "1 month ago", url: "https://www.peopleperhour.com/freelance-jobs/design/logo-design/we-need-a-logo-design-4493570", desc: "Comprehensive brand design for a restaurant including logo, menu, shop sign and uniforms." },
      { title: "Cooking Video Editing Specialist", platform: "Freelancer.com", tools: ["After Effects","Premiere Pro"], budget: "$11 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/video-post-editing/cooking-video-editing-specialist", desc: "Polish raw cooking content into 5-15 min episodes with transitions, music and ingredient overlays." },
      { title: "Luxurious FMCG Packaging Design (B2B hamper)", platform: "Freelancer.com", tools: ["Illustrator","Photoshop"], budget: "$63 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/packaging-design/luxurious-fmcg-packaging-design", desc: "B2B hamper concept with outer box, internal layout, product cards and branding." }
    ]
  },
  {
    vertical: "Wedding & Stationery",
    listings: [
      { title: "Classic Vintage Digital Wedding Invites", platform: "Freelancer.com", tools: ["Creative Cloud","Photoshop","Illustrator"], budget: "$80 avg bid", location: "Remote", posted: "6 days left", url: FL+"/projects/invitation-design/classic-vintage-digital-wedding-invites", desc: "Beautiful digital wedding invitations in a classic/vintage style, delivered as PDFs." },
      { title: "Modern Wedding Invitation Print Design", platform: "Freelancer.com", tools: ["Illustrator","Photoshop"], budget: "$83 avg bid", location: "Remote", posted: "4 days left", url: FL+"/projects/print-design/modern-wedding-invitation-print-design", desc: "Polish and finalize a clean modern wedding invitation for print production from an existing sketch." },
      { title: "High-End Wedding Photo Retouching", platform: "Freelancer.com (contest)", tools: ["Lightroom","Photoshop"], budget: "$21 guaranteed", location: "Remote", posted: "Active", url: FL+"/contest/highend-wedding-photo-retouching-2748954", desc: "Enhance 5 wedding photos: sky color correction, background refinement and professional finishing." },
      { title: "Engagement Party Photojournalism", platform: "Freelancer.com", tools: ["Photoshop"], budget: "$180-$540", location: "Local", posted: "Active", url: FL+"/projects/photography/engagement-party-photojournalism", desc: "Candid photojournalistic coverage of an engagement party with edited deliverables." }
    ]
  },
  {
    vertical: "Party, Events & Promotion",
    listings: [
      { title: "Design 'You're The Party' Logo (event-planning brand)", platform: "Freelancer.com (contest)", tools: ["Illustrator","Photoshop"], budget: "$120 guaranteed (urgent)", location: "Remote", posted: "Active", url: FL+"/contest/design-ldquoyoursquore-the-partyrdquo-logo-2748901", desc: "Modern, sleek yet playful logo for an event-planning brand using 'YTP' initials." },
      { title: "Concert Poster & Thumbnail Design", platform: "Freelancer.com", tools: ["Illustrator","Photoshop"], budget: "$215 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/poster-design/concert-poster-thumbnail-design", desc: "A3 poster, web banner and matching thumbnail for a live concert (date, venue, ticket link)." },
      { title: "Professional Event Banner Image (community festival)", platform: "PeoplePerHour", tools: ["Not specified"], budget: "$54", location: "Remote", posted: "22 days ago", url: "https://www.peopleperhour.com/freelance-jobs/design/graphic-design/professional-event-banner-image-4495286", desc: "Polished 1900x900px event banner reflecting community festival themes." },
      { title: "Event Program Booklet Brochure Design", platform: "Freelancer.com", tools: ["InDesign"], budget: "$89 avg bid", location: "Remote", posted: "3 days left", url: FL+"/projects/print-design/event-program-booklet-brochure-design", desc: "Multi-page event program booklet with sponsor logos and a fresh visual identity." },
      { title: "Exhibition Posters, Brochure & Card Design", platform: "Freelancer.com", tools: ["InDesign","Illustrator","Photoshop"], budget: "$60 avg bid", location: "Remote", posted: "3 days left", url: FL+"/projects/business-cards/exhibition-posters-brochure-card-design", desc: "Back-lit poster standees, take-away brochure and business cards for a trade exhibition." },
      { title: "Playful Sign & Flyer Design", platform: "Freelancer.com", tools: ["Illustrator","Photoshop"], budget: "$25 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/print-design/playful-sign-flyer-design", desc: "3m x 1.5m front-facing sign plus matching flyer variations for ongoing collaboration." }
    ]
  },
  {
    vertical: "Health, Wellness & Medical",
    listings: [
      { title: "Authentic Lifestyle Photography for Virtual Healthcare Meta Ads", platform: "Freelancer.com", tools: ["Photoshop (editing)"], budget: "$116 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/photo-editing/authentic-lifestyle-photography-for", desc: "Produce 10-12 authentic lifestyle photos for Meta ads featuring virtual healthcare services." },
      { title: "Reproduce Logos for 3 Brands (Danugur Dermatology)", platform: "PeoplePerHour", tools: ["Not specified"], budget: "$77", location: "Remote", posted: "17 days ago", url: "https://www.peopleperhour.com/freelance-jobs/design/logo-design/i-need-logos-reproduced-for-3-separate-brands-4496452", desc: "Reproduce a dermatology group's logos in all formats for stationery, signage and group branding." },
      { title: "Health Awareness Trifold Display", platform: "Freelancer.com", tools: ["InDesign"], budget: "$28 avg bid", location: "Remote", posted: "3 days left", url: FL+"/projects/educational-research/health-awareness-trifold-display", desc: "Creative health-awareness trifold display with engaging visuals and persuasive messaging." },
      { title: "Marketing Material Design for Cool Point Cryotherapy", platform: "Freelancer.com (contest)", tools: ["Illustrator","Photoshop"], budget: "$10 guaranteed (featured)", location: "Remote", posted: "6 days left", url: FL+"/contest/creative-marketing-material-design-for-cool-point-cryotherapy-2747688", desc: "Postcards, flyers and brochures for cryotherapy services (pain, body sculpting, recovery)." },
      { title: "Branding for a Pilates Studio", platform: "Contra (dated Jun 2025 - may be stale)", tools: ["Not specified"], budget: "$250-$450 one-time", location: "Remote", posted: "Jun 2025", url: "https://contra.com/featured-jobs/freelance-logo-design-jobs", desc: "Complete branding project for a pilates studio business." },
      { title: "Create a Baby Book Pamphlet (developmental milestones)", platform: "Freelancer.com", tools: ["InDesign","Illustrator","Creative Cloud"], budget: "$116 avg bid", location: "Remote", posted: "5 days left", url: FL+"/projects/content-writing/create-baby-book-pamphlet", desc: "Guidance pamphlet for a baby-book box with developmental milestone tips and logo integration." },
      { title: "Minimalist Colorful PDF Guides (nervous-system / parenting education)", platform: "Freelancer.com", tools: ["Canva","Illustrator","Photoshop"], budget: "$83 avg bid", location: "Remote", posted: "3 days left", url: FL+"/projects/canva/minimalist-colorful-pdf-design-canva", desc: "Polished parenting / nervous-system education PDF guides with minimalist colorful design." }
    ]
  },
  {
    vertical: "Real Estate, Construction & Property",
    listings: [
      { title: "Sleek Tenant Services Brochure Design (real estate division)", platform: "Freelancer.com (contest)", tools: ["InDesign","Illustrator"], budget: "$50 guaranteed", location: "Remote", posted: "4 days left", url: FL+"/contest/sleek-tenant-services-brochure-design-edt-2748988", desc: "Single-page print-ready brochure for a real estate division with dark backdrop and accent color." },
      { title: "AI Video Editor for Real Estate", platform: "Freelancer.com", tools: ["Premiere Pro","After Effects"], budget: "$8 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/adobe-premiere-pro/video-editor-for-real-estate", desc: "Real estate and construction content with drone footage, color grading and AI workflows." },
      { title: "Construction Capability Statement Design", platform: "Freelancer.com (contest)", tools: ["Illustrator","Photoshop"], budget: "$37 guaranteed", location: "Remote", posted: "5 days left", url: FL+"/contest/construction-capability-statement-design-2748311", desc: "Professional capability statement emphasizing completed commercial projects with photos." },
      { title: "Instagram Revamp for Construction Brand (espacio gradnja)", platform: "Freelancer.com", tools: ["Lightroom","Premiere Pro","Photoshop","Canva"], budget: "$134 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/adobe-premiere-pro/instagram-revamp-for-construction-brand", desc: "Build a polished, minimalist Instagram profile from raw construction/electrical photos and video." },
      { title: "Urgent Cinematic Construction Progress Reel", platform: "Freelancer.com", tools: ["After Effects","Premiere Pro"], budget: "$59 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/ai-video/cinematic-construction-progress-reel", desc: "Polished 20-30s construction-progress video with worker footage, drone shots and color grading." },
      { title: "Modern Landscaping Logo Design (Wright Stand on Mowers)", platform: "Freelancer.com", tools: ["Illustrator","Photoshop"], budget: "$295 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/adobe-illustrator/modern-landscaping-logo-design-40490252", desc: "Modern sleek landscaping logo featuring company name, mowing lines, in black and yellow." },
      { title: "Bold Earthworks Logo Creation (Meares Earthworks)", platform: "Freelancer.com", tools: ["Illustrator","Photoshop"], budget: "$53 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/adobe-illustrator/bold-earthworks-logo-creation", desc: "Bold, striking logo with stylized digger imagery in blue/black/white." },
      { title: "SCUBE Solar Lighting Brochure Design (B2B dealers)", platform: "Freelancer.com", tools: ["Illustrator","Photoshop"], budget: "$48 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/product-design/scube-solar-lighting-brochure-design-40488521", desc: "Premium 8-12 page product brochure for a solar-lighting brand targeting dealers." },
      { title: "3D Animator for Solar Structure Installation", platform: "Freelancer.com", tools: ["After Effects","Blender"], budget: "$143 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/rendering/animator-for-solar-structure", desc: "Professional 3D animation demonstrating step-by-step solar mounting structure installation." },
      { title: "Horticulture Company Profile With Photos", platform: "Freelancer.com", tools: ["InDesign","Illustrator"], budget: "$10 avg bid", location: "Remote", posted: "3 days left", url: FL+"/projects/indesign/horticulture-company-profile-with-photos", desc: "Fresh marketing company profile for a horticulture firm with services and project imagery." }
    ]
  },
  {
    vertical: "Automotive, Industrial & Agriculture",
    listings: [
      { title: "Modern Auto Locksmith Logo", platform: "Freelancer.com", tools: ["Illustrator"], budget: "$49 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/vector-design/modern-auto-locksmith-logo", desc: "Sleek modern mobile auto-locksmith logo in blue/white with a stylized car-key graphic." },
      { title: "KRONE BiG M Vector Series (agricultural mowers)", platform: "Freelancer.com", tools: ["Illustrator","Photoshop"], budget: "$91 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/vector-design/krone-big-vector-series", desc: "Clean minimalist line-art illustrations of each KRONE BiG M mower generation." },
      { title: "Truck Graphic (rear of a 4x4 truck)", platform: "PeoplePerHour", tools: ["Not specified"], budget: "$118 (pre-funded)", location: "Remote", posted: "6 days ago", url: "https://www.peopleperhour.com/freelance-jobs/design/graphic-design/truck-graphic-4498829", desc: "Design a cool graphic for the rear of a 4x4 truck with company-name branding." },
      { title: "Vintage Sugarcane Logo (Atkinson Agricultural)", platform: "Freelancer.com (contest)", tools: ["Illustrator","Photoshop"], budget: "$35 guaranteed", location: "Remote", posted: "Active", url: FL+"/contest/vintage-sugarcane-logo-design-for-atkinson-agricultural-2748710", desc: "Timeless vintage-inspired logo featuring sugarcane imagery." },
      { title: "Modernized InDesign Catalogue (farmers/gamekeepers trade)", platform: "Freelancer.com", tools: ["InDesign","Illustrator"], budget: "$431 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/print-design/modernized-indesign-catalogue-creation", desc: "Clean trade catalogue with a modernized layout and reusable templates." },
      { title: "14-Page Agriculture Franchise Prospectus Design", platform: "Freelancer.com", tools: ["Illustrator"], budget: "$133 avg bid", location: "Remote", posted: "3 days left", url: FL+"/projects/content-writing/page-franchise-prospectus-design", desc: "14-page franchise prospectus with persuasive copy, infographics and established branding." }
    ]
  },
  {
    vertical: "Sports & Fitness",
    listings: [
      { title: "YouTube Logo & Banner - Gimnasio Virtual (fitness channel)", platform: "PeoplePerHour", tools: ["Not specified"], budget: "Quote requested", location: "Remote", posted: "15 days ago", url: "https://www.peopleperhour.com/freelance-jobs/design/logo-design/creation-of-youtube-logo-shape-gimnasio-virtual-4496819", desc: "Logo and YouTube banner/cover for a fitness YouTube channel." },
      { title: "Brandenburg Bucking Bulls Logo (rodeo, graffiti-style)", platform: "Freelancer.com (contest)", tools: ["Illustrator","Photoshop"], budget: "$28 guaranteed", location: "Remote", posted: "Active", url: FL+"/contest/brandenburg-bucking-bulls-logo-design-edt-2748707", desc: "Modern graffiti-style logo with fluoro colors and fire for a bucking-bulls brand." },
      { title: "Dynamic Soccer Recruiting Reel", platform: "Freelancer.com", tools: ["After Effects","Premiere Pro","Final Cut"], budget: "$96 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/video-production/dynamic-soccer-recruiting-reel", desc: "Sharp highlight reel from full match video showcasing midfield/center-back roles." },
      { title: "Hockey Highlight Reel Creator", platform: "Freelancer.com", tools: ["After Effects","Premiere Pro","DaVinci"], budget: "$10/hr avg", location: "Remote", posted: "Active", url: FL+"/projects/adobe-premiere-pro/hockey-highlight-reel-creator-40490272", desc: "3-5 minute hockey highlight reels with pivotal plays, stat overlays and broadcast-quality editing." },
      { title: "Perth Hyrox Race Highlight", platform: "Freelancer.com", tools: ["Premiere Pro","Photoshop"], budget: "$30-$250", location: "Perth (Local)", posted: "Active", url: FL+"/projects/photography/perth-hyrox-race-highlight", desc: "Fast-paced 2-3 minute 4K highlight video plus an edited gallery from full race coverage." },
      { title: "Filmora NFL Video Editor Needed", platform: "Freelancer.com", tools: ["After Effects"], budget: "$100 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/audio-editing/filmora-nfl-video-editor-needed", desc: "Ongoing NFL video production with episode assembly, stat cards and a consistent visual language." },
      { title: "Brand Identity & Instagram Posts (sports collectibles)", platform: "PeoplePerHour", tools: ["Not specified"], budget: "$108", location: "Remote", posted: "13 days ago", url: "https://www.peopleperhour.com/freelance-jobs/design/graphic-design/designer-needed-help-create-our-brand-identity-and-insta-po-4497345", desc: "Complete brand identity plus Instagram posts/reels for a sports-collectibles business." }
    ]
  },
  {
    vertical: "Technology, SaaS & Startups",
    listings: [
      { title: "Modern Logo Design for MAVLEX (technical services)", platform: "Freelancer.com", tools: ["Illustrator","Photoshop"], budget: "$80 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/vector-design/modern-logo-design-for-mavlex", desc: "Clean modern logo on the MAVLEX initials with a muted, sophisticated palette." },
      { title: "Bento UI Animation Demo", platform: "Freelancer.com", tools: ["After Effects","Motion Design"], budget: "$78 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/ui-design/bento-animation-demo", desc: "Animated video showcasing UI components with bento-grid animation and light/dark transition." },
      { title: "Fast Turnaround SAAS & POS Promo", platform: "Freelancer.com", tools: ["After Effects","Premiere Pro"], budget: "$28 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/motion-graphics/fast-turnaround-saas-pos-promo", desc: "Campaign video for a SaaS platform and POS system: 55s vertical and 25-30s horizontal cuts." },
      { title: "Product Launch Promo Video Design", platform: "Freelancer.com", tools: ["After Effects","Premiere Pro"], budget: "$34 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/motion-graphics/product-launch-promo-video-design", desc: "High-impact 30-60s product-launch promo with storyboard, motion design and sound bed." },
      { title: "Product Launch Trailer & Demo using Adobe After Effects", platform: "Freelancer.com", tools: ["After Effects","Premiere Pro"], budget: "$59 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/motion-graphics/product-launch-trailer-demo-using", desc: "30-45s trailer plus 2-3 min demo showcasing product features with clean motion graphics." },
      { title: "Animated Tech Reels (SQL / Python / Power BI explainers)", platform: "Freelancer.com", tools: ["After Effects","Motion Graphics"], budget: "$14 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/video-editing/animated-tech-reels-creation", desc: "Three faceless Instagram Reels as animated explainers with a minimal aesthetic." },
      { title: "Email Marketing Template Suite - Klaviyo", platform: "PeoplePerHour", tools: ["Figma","Adobe XD"], budget: "$54/hr", location: "Remote", posted: "18 hours ago", url: "https://www.peopleperhour.com/freelance-jobs/design/graphic-design/email-marketing-template-suite-klaviyo-4499867", desc: "Design 10-12 branded lifecycle email templates exportable from design platforms." },
      { title: "Modern Website Redesign Finishing Touches", platform: "Freelancer.com", tools: ["Adobe XD","Figma"], budget: "$30-$250", location: "Remote", posted: "Active", url: FL+"/projects/adobe-xd/modern-website-redesign-finishing", desc: "Polish a staging website with refined typography and mobile optimization before launch." },
      { title: "Adobe InDesign Proposal & SOQ Template System (engineering)", platform: "Freelancer.com", tools: ["InDesign"], budget: "$108 avg bid", location: "Remote", posted: "4 days left", url: FL+"/projects/print-design/adobe-indesign-proposal-statement", desc: "Reusable proposal / statement-of-qualifications template system for an engineering firm." },
      { title: "Professional Media Kit Design (speaker/podcast/author)", platform: "Freelancer.com", tools: ["InDesign","Illustrator","Canva"], budget: "$116 avg bid", location: "Remote", posted: "4 days left", url: FL+"/projects/branding/professional-media-kit-design-for", desc: "Premium media kit emphasizing faith, growth and purpose with professional branding." },
      { title: "Premium Conference Keynote Presentation Design", platform: "Freelancer.com", tools: ["Photoshop","Illustrator","Canva"], budget: "$79 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/canva/premium-conference-keynote-presentation", desc: "Transform a 46-slide workshop deck into a premium conference keynote (TED / Y Combinator style)." },
      { title: "Inenergy Pitch Deck (10 slides, energy consultancy)", platform: "PeoplePerHour", tools: ["PowerPoint"], budget: "$91", location: "Remote", posted: "16 days ago", url: "https://www.peopleperhour.com/freelance-jobs/design/graphic-design/project-inenergy-pitch-deck-10-slides-4496698", desc: "Minimalist 10-slide pitch deck with McKinsey-style aesthetics and photorealistic imagery." },
      { title: "Convert InDesign Presentation into Editable PowerPoint", platform: "PeoplePerHour", tools: ["InDesign"], budget: "$116", location: "Remote", posted: "18 hours ago", url: "https://www.peopleperhour.com/freelance-jobs/design/graphic-design/convert-in-design-presentation-into-a-fully-editable-powerpo-4499874", desc: "Convert a 208-page corporate brochure from InDesign to PowerPoint with identical formatting." }
    ]
  },
  {
    vertical: "E-commerce, Retail & Product",
    listings: [
      { title: "Fashion Brand Graphics / Creative Assets (boho brand)", platform: "Freelancer.com", tools: ["Creative Suite","Photoshop","Canva"], budget: "$22/hr avg", location: "Remote", posted: "Active", url: FL+"/projects/branding/fashion-brand-graphics-creative-assets", desc: "Graphics for a boho fashion brand across EDMs, website banners, social media and packaging." },
      { title: "Amazon Merch VA & Designer", platform: "Freelancer.com", tools: ["Photoshop","Canva"], budget: "$122 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/seo-writing/amazon-merch-designer", desc: "Own the design pipeline for Amazon Merch on Demand, creating original t-shirt designs weekly." },
      { title: "E-commerce Product Photography & Editing", platform: "Freelancer.com", tools: ["Lightroom","Photoshop"], budget: "$339 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/adobe-lightroom/product-foto-coete-infamtil-photography-40489519", desc: "E-commerce product shots on plain backgrounds, multiple angles, high-resolution edited files." },
      { title: "Clone Packaging Design to Exact .ai/Vector Match", platform: "PeoplePerHour", tools: ["Illustrator"], budget: "$108", location: "Remote", posted: "21 days ago", url: "https://www.peopleperhour.com/freelance-jobs/design/graphic-design/clone-packaging-design-to-exact-ai-vector-match-4495542", desc: "Recreate packaging designs from photos as exact vector-matched Illustrator files." },
      { title: "Product Catalog Design (print + digital)", platform: "Freelancer.com", tools: ["Illustrator","InDesign"], budget: "$12 avg bid", location: "Remote", posted: "3 days left", url: FL+"/projects/adobe-illustrator/product-catalog-design", desc: "Professional 1-10 page product catalog in print-ready PDF and digital formats." },
      { title: "Design a Product Catalog PDF (13-15 pages)", platform: "PeoplePerHour", tools: ["Not specified"], budget: "$67", location: "Remote", posted: "15 days ago", url: "https://www.peopleperhour.com/freelance-jobs/design/graphic-design/design-a-product-catalog-pdf-4496982", desc: "Clean, professional 13-15 page product catalog PDF with images, pricing and modern layout." },
      { title: "Eye-Catching Packaging Design (CMYK, 3D mock-ups)", platform: "Freelancer.com", tools: ["Illustrator"], budget: "$11/hr avg", location: "Remote", posted: "4 days left", url: FL+"/projects/adobe-illustrator/eye-catching-packaging-design-needed", desc: "Fresh professional packaging in vector format with print-ready CMYK files and 3D mock-ups." },
      { title: "Product Packaging Bag Design", platform: "Freelancer.com", tools: ["Creative Suite","Illustrator"], budget: "$47 avg bid", location: "Remote", posted: "5 days left", url: FL+"/projects/packaging-design/product-packaging-bag-design", desc: "Creative plastic-bag packaging design with a focus on innovative aesthetics." }
    ]
  },
  {
    vertical: "Photo Editing, Retouching & Restoration",
    listings: [
      { title: "Photo Colour Correction for Mood", platform: "Freelancer.com", tools: ["Photoshop","Lightroom"], budget: "$23 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/color-grading/photo-colour-correction-for-mood", desc: "Batch color treatment balancing tones, shadows and highlights for a distinct artistic mood." },
      { title: "Quick Photo Background Removal", platform: "Freelancer.com", tools: ["Photoshop"], budget: "$12 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/background-removal/quick-photo-background-removal-40489742", desc: "Strip backgrounds from an image set and deliver transparent PNGs with crisp edges." },
      { title: "Portrait White-Background Editing (batch 200-250)", platform: "Freelancer.com", tools: ["Photoshop"], budget: "$6/hr avg", location: "Remote", posted: "Active", url: FL+"/projects/graphic-design/portrait-white-background-editing", desc: "Batch-edit 200-250 portraits, removing backgrounds and adding a studio-white backdrop." },
      { title: "Old Photo Tear Restoration ASAP", platform: "Freelancer.com", tools: ["Photoshop"], budget: "$7/hr avg", location: "Remote", posted: "Active", url: FL+"/projects/photo-restoration/old-photo-tear-restoration-asap", desc: "Remove scratches, clean and rebuild damaged old photos at high quality." },
      { title: "Edit Photo to Remove Person", platform: "Freelancer.com", tools: ["Photoshop"], budget: "$27 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/image-processing/edit-photo-remove-person", desc: "Remove the middle person from a three-person photo while preserving the champagne-spray effect." },
      { title: "Professional Video and Photo Editing", platform: "PeoplePerHour", tools: ["Not specified"], budget: "$23", location: "Remote", posted: "18 days ago", url: "https://www.peopleperhour.com/freelance-jobs/design/logo-design/professional-video-and-photo-editing-4496080", desc: "Photo/video work including background changes, color correction, retouching and social content." },
      { title: "Graphic Design Aligned with Brand Standards", platform: "Freelancer.com", tools: ["Photoshop"], budget: "$32 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/adobe-photoshop/graphic-design-aligned-with-brand", desc: "Create social posts, banners and slides strictly following existing brand guidelines." }
    ]
  },
  {
    vertical: "Music, Film, Publishing & Media",
    listings: [
      { title: "Mystical 6x9 Book Cover Redesign", platform: "Freelancer.com (contest)", tools: ["Illustrator","Photoshop"], budget: "$75 guaranteed", location: "Remote", posted: "Active", url: FL+"/contest/mystical-x-book-cover-redesign-2749039", desc: "Modify a book cover to 6x9 with deepened purples, a subtle horizon glow and prominent text." },
      { title: "Book Cover: Clean up Front Cover & Produce Full Cover", platform: "Freelancer.com", tools: ["Photoshop","Illustrator"], budget: "$57 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/photoshop/book-cover-clean-current-front", desc: "Retouch an AI-generated cover, fix artifacts and produce a full wrap-around version." },
      { title: "Modern Adult Movie Poster Design", platform: "Freelancer.com", tools: ["Illustrator","Photoshop"], budget: "$209 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/adobe-illustrator/modern-adult-movie-poster-design", desc: "Modern-style movie poster with a tight deadline." },
      { title: "YouTube Channel Setup for Original Music (banner, logo)", platform: "Freelancer.com", tools: ["Photoshop"], budget: "$326 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/youtube/youtube-channel-setup-for-original", desc: "Professional YouTube channel with banner, logo, playlists and description for music videos." },
      { title: "Sweet Light-Hearted Romance Book Trailer", platform: "Freelancer.com", tools: ["After Effects"], budget: "$106 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/after-effects/sweet-light-hearted-romance-trailer", desc: "Fun, sweet video trailer for a new romance book with bright playful visuals." },
      { title: "Realistic Children's Book Illustrations", platform: "Freelancer.com", tools: ["Not specified"], budget: "$171 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/creative-design/realistic-children-book-illustrations-40488596", desc: "Create 10+ realistic, age-appropriate illustrations for a children's book." },
      { title: "Polish Ebook Layout (Word or InDesign)", platform: "Freelancer.com", tools: ["InDesign"], budget: "$129 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/typography/polish-ebook-polish-word-indesign", desc: "Lay out a 60-page Polish manuscript with professional typography and image placement." },
      { title: "Ingram-Ready PDF-to-EPUB", platform: "Freelancer.com", tools: ["InDesign"], budget: "$47 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/publishing/ingram-ready-pdf-epub", desc: "Rebuild a 54-page PDF manuscript as a clean EPUB passing IngramSpark validation." },
      { title: "QuarkXPress Book Compilation & Cover", platform: "Freelancer.com", tools: ["QuarkXPress","InDesign","Photoshop"], budget: "$992 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/indesign/quark-book-compilation-cover", desc: "Merge 13 Quark files into a single 461-page master document with a cover for print." },
      { title: "YouTube Thumbnail Designer for High-CTR Thumbnails", platform: "PeoplePerHour", tools: ["Not specified"], budget: "$54", location: "Remote", posted: "4 days ago", url: "https://www.peopleperhour.com/freelance-jobs/design/graphic-design/youtube-thumbnail-designer-for-high-ctr-thumbnails-4499110", desc: "Eye-catching, high-conversion YouTube thumbnails with a professional modern design." },
      { title: "Hand-Drawn Teen Story Animations (YouTube series)", platform: "Freelancer.com", tools: ["After Effects","2D Animation"], budget: "$68 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/2d-animation/hand-drawn-teen-story-animations", desc: "Hand-drawn 2D animated YouTube series with character design, rigging and full production." },
      { title: "Anime VTuber Model Creation", platform: "Freelancer.com", tools: ["2D Animation"], budget: "$429 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/2d-animation/anime-vtuber-model-creation-40488799", desc: "Anime-style male VTuber model with rigging for live streaming." },
      { title: "Fantasy Anime Webtoon Illustrator", platform: "Freelancer.com", tools: ["Digital Art"], budget: "$19 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/digital-art/fantasy-anime-webtoon-illustrator", desc: "Illustrate a webtoon episode in a fantasy anime style with detailed backgrounds." },
      { title: "Remove Flicker From 15-Sec Clips (Elvis performance)", platform: "Freelancer.com", tools: ["After Effects","Premiere Pro","DaVinci"], budget: "$140 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/adobe-premiere-pro/remove-flicker-from-sec-clips", desc: "Remove persistent flicker from 15-second performance clips for promotional use." }
    ]
  },
  {
    vertical: "Video Editing & Motion Graphics (cross-industry)",
    listings: [
      { title: "Merge iPhone Clips with Music", platform: "Freelancer.com", tools: ["After Effects","Premiere Pro","DaVinci"], budget: "$224 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/adobe-premiere-pro/merge-iphone-clips-with-music", desc: "Combine 4-5 clips chronologically with ambient music, captions, and color/audio balancing." },
      { title: "Edit Trendy Instagram Reels", platform: "Freelancer.com", tools: ["After Effects","Final Cut"], budget: "$10/hr avg", location: "Remote", posted: "Active", url: FL+"/projects/social-media-marketing/edit-trendy-instagram-reels", desc: "Turn raw vertical clips into Reels with punchy text overlays, trending audio and transitions." },
      { title: "Reels & TikTok Video Editor Needed", platform: "Freelancer.com", tools: ["After Effects","Premiere Pro","Final Cut"], budget: "$2/hr avg", location: "Remote", posted: "Active", url: FL+"/projects/adobe-premiere-pro/reels-tiktok-video-editor-needed-40489074", desc: "Scroll-stopping 30-60s trend-driven clips with transitions, color-grading and audio leveling." },
      { title: "Clean Social Promo Video Edits", platform: "Freelancer.com", tools: ["After Effects","Premiere Pro","DaVinci","Final Cut"], budget: "$10 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/adobe-premiere-pro/clean-social-promo-video-edits", desc: "Polished short-form content for Instagram, YouTube Shorts, TikTok and X with color correction." },
      { title: "Company Promotional Video Editing", platform: "Freelancer.com", tools: ["After Effects","Premiere Pro","DaVinci","Final Cut"], budget: "$18 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/motion-graphics/company-promotional-video-editing-needed", desc: "Polished promo pieces from raw footage with on-brand overlays and color correction." },
      { title: "Instagram/Facebook Reels Video Editor", platform: "Freelancer.com", tools: ["After Effects","Motion Graphics"], budget: "$27 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/motion-graphics/instagram-facebook-reels-video-editor", desc: "Story-driven reels with transitions, motion graphics and branded endings." },
      { title: "Fun YouTube Podcast Editing", platform: "Freelancer.com", tools: ["After Effects","Premiere Pro","DaVinci","Final Cut"], budget: "$28 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/adobe-premiere-pro/fun-youtube-podcast-editing", desc: "Shape raw podcast footage into an engaging episode with light graphics and logo integration." },
      { title: "Faceless Business Documentary Editing", platform: "Freelancer.com", tools: ["After Effects","Premiere Pro"], budget: "$107 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/sound-design/faceless-business-documentary-editing", desc: "Faceless business documentaries combining voice-over, stock footage and subtle animation." },
      { title: "Short Commercial Video Editor Required", platform: "Freelancer.com", tools: ["After Effects","Motion Graphics"], budget: "$23 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/motion-graphics/short-commercial-video-editor-required", desc: "Story-driven commercial reels with smooth transitions, motion graphics and color correction." },
      { title: "Retail Signage Motion Graphics", platform: "Freelancer.com", tools: ["After Effects"], budget: "$922 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/after-effects/retail-signage-motion-graphics", desc: "Looping digital-signage pieces for retail shipping stores in portrait and landscape." },
      { title: "Weekly 28-Minute Video Assemblies", platform: "Freelancer.com", tools: ["After Effects","Premiere Pro","DaVinci"], budget: "$336 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/adobe-premiere-pro/weekly-minute-video-assemblies", desc: "Monthly production of five 28-minute shows with branded open/close sequences." },
      { title: "Energetic Facebook Product Showcase Video", platform: "Freelancer.com", tools: ["After Effects","Premiere Pro"], budget: "$14/hr avg", location: "Remote", posted: "Active", url: FL+"/projects/motion-graphics/energetic-facebook-product-showcase", desc: "Snappy 15-30s product-showcase video with fast cuts, kinetic text and a clear CTA." }
    ]
  },
  {
    vertical: "Finance, Crypto & Professional Services",
    listings: [
      { title: "Investor-Ready Pitch Deck Design", platform: "Freelancer.com", tools: ["Keynote"], budget: "$78 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/financial-analysis/investor-ready-pitch-deck-design", desc: "Polished, data-driven pitch deck for funding orgs with business model and market analysis." },
      { title: "Interactive Market Analysis Videos (trading)", platform: "Freelancer.com", tools: ["After Effects","Premiere Pro"], budget: "$6/hr avg", location: "Remote", posted: "Active", url: FL+"/projects/content-creation/interactive-market-analysis-videos", desc: "Market-analysis videos extracting trading narratives from live charts with on-screen drawing." },
      { title: "Professional Report Design (44 & 26 page reports)", platform: "PeoplePerHour", tools: ["Not specified"], budget: "$118", location: "Remote", posted: "13 days ago", url: "https://www.peopleperhour.com/freelance-jobs/design/graphic-design/professional-report-design-4497412", desc: "Transform two reports into professionally designed, branded landscape-A4 documents." }
    ]
  },
  {
    vertical: "Pets & Animals",
    listings: [
      { title: "Premium Pet Care Packaging Design (Ayurvedic grooming)", platform: "Freelancer.com", tools: ["Illustrator"], budget: "$243 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/packaging-design/premium-pet-care-packaging-design", desc: "Premium packaging for an Ayurvedic pet-grooming brand: shampoo label wrap and balm jar label with botanical illustrations." }
    ]
  },
  {
    vertical: "General / Cross-Industry Branding & Graphics",
    note: "A representative selection of cross-industry logo, branding, social-media and print work that is not tied to a single vertical. Many more similar micro-gigs are live on the same Freelancer.com and PeoplePerHour feeds and can be pulled on request.",
    listings: [
      { title: "Maintenance Service Promo Poster", platform: "Freelancer.com", tools: ["Illustrator","Photoshop"], budget: "$177 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/adobe-illustrator/maintenance-service-promo-poster", desc: "Striking digital poster for a maintenance service with bold headline, logo and a clear CTA." },
      { title: "Modern Business Promo Design (flyer + mailer + landing)", platform: "Freelancer.com", tools: ["Illustrator","Photoshop"], budget: "$5/hr avg", location: "Remote", posted: "Active", url: FL+"/projects/web-design/modern-business-promo-design", desc: "Flyer, A4 mailer envelope and a redesigned landing page using company branding." },
      { title: "Company Logo Design (cards, web, print files)", platform: "Freelancer.com", tools: ["Illustrator","Photoshop"], budget: "$77 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/creative-design/company-logo-design-40490052", desc: "Create appropriate files for an existing logo: contact cards, website and printed documents." },
      { title: "Minimalist Logo Design", platform: "Freelancer.com", tools: ["Illustrator","Photoshop"], budget: "$12 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/creative-design/minimalist-logo-design-40490169", desc: "Minimalist logo incorporating both text and an icon in a modern or classic style." },
      { title: "Logo, Brochure & Business Card Design", platform: "Freelancer.com", tools: ["Illustrator","InDesign"], budget: "$193 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/adobe-illustrator/logo-brochure-business-card-design-40489264", desc: "Refresh brand identity with a distinctive logo, brochure and matching two-sided business card." },
      { title: "Classic Cleaning Service Logo Design (SiteScrub)", platform: "Freelancer.com (contest)", tools: ["Illustrator"], budget: "$25 guaranteed", location: "Remote", posted: "Active", url: FL+"/contest/classic-cleaning-service-logo-design-2748977", desc: "Classic professional logo for a post-construction cleaning service in blues and white." },
      { title: "Commercial Cleaning Leaflet Design", platform: "Freelancer.com", tools: ["Illustrator","InDesign","Photoshop"], budget: "$99 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/print-design/commercial-cleaning-leaflet-design", desc: "Two print-ready leaflets for a cleaning company - one for offices, one for estate agents." },
      { title: "Social Media Graphics (Facebook / Instagram / X)", platform: "Freelancer.com", tools: ["Illustrator","Photoshop"], budget: "$19/hr avg", location: "Remote", posted: "Active", url: FL+"/projects/social-media-marketing/social-media-graphics-40489884", desc: "Consistent post images, story formats and ad banners across social platforms." },
      { title: "Modern Social Media Thumbnail", platform: "Freelancer.com", tools: ["Photoshop","Illustrator","Canva"], budget: "$7/hr avg", location: "Remote", posted: "Active", url: FL+"/projects/social-media-marketing/modern-social-media-thumbnail", desc: "Modern-minimalistic 1080x1080 thumbnail poster with a clean focal element." },
      { title: "Daily LinkedIn Content & Flyers", platform: "Freelancer.com", tools: ["Creative Cloud","Canva","Photoshop"], budget: "$59 avg bid", location: "Remote", posted: "6 days left", url: FL+"/projects/content-writing/daily-linkedin-content-flyers", desc: "Daily LinkedIn posts with visuals/copy plus complementary campaign flyers matching brand identity." },
      { title: "Minimal Corporate Tri-Fold Brochure", platform: "Freelancer.com", tools: ["Illustrator","InDesign"], budget: "$17/hr avg", location: "Remote", posted: "3 days left", url: FL+"/projects/adobe-illustrator/minimal-corporate-tri-fold-brochure", desc: "Clean blue-themed tri-fold brochure with generous whitespace and vector artwork." },
      { title: "Professional Brochure Image Design", platform: "Freelancer.com", tools: ["Photoshop","Illustrator"], budget: "$300 avg bid", location: "Remote", posted: "6 days left", url: FL+"/projects/adobe-photoshop/professional-brochure-image-design", desc: "Single high-resolution press-ready image for a flyer/brochure run." },
      { title: "Custom Vibrant Abstract Sticker Pack", platform: "Freelancer.com", tools: ["Illustrator","Photoshop"], budget: "$21 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/vector-design/custom-vibrant-abstract-sticker-pack", desc: "Around 10 vibrant abstract stickers with bold patterns and geometry." },
      { title: "Creative Graphics for Kids' Room", platform: "Freelancer.com", tools: ["Photoshop","Illustrator"], budget: "$14 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/graphic-design/creative-graphics-design-for-kids", desc: "Charming graphics suitable for kids' rooms, backgrounds and product illustrations." },
      { title: "Corporate PPT Design Enhancement", platform: "Freelancer.com", tools: ["Creative Suite","Photoshop","Illustrator"], budget: "$16 avg bid", location: "Remote", posted: "6 days left", url: FL+"/projects/visual-design/corporate-ppt-design-enhancement", desc: "Improve a PowerPoint layout with a professional corporate theme emphasizing images and visuals." },
      { title: "PowerPoint Company Profile Design", platform: "Freelancer.com", tools: ["InDesign","Photoshop"], budget: "$59 avg bid", location: "Remote", posted: "6 days left", url: FL+"/projects/corporate-identity/powerpoint-company-profile-design", desc: "Polished company profile in PowerPoint/PDF with consistent typography and brand imagery." },
      { title: "Business Logo Design (GO2 Removals)", platform: "PeoplePerHour", tools: ["Not specified"], budget: "$108", location: "Remote", posted: "1 day ago", url: "https://www.peopleperhour.com/freelance-jobs/design/logo-design/business-logo-design-4499693", desc: "Premium minimalist logo rebrand for a removals/storage business targeting affluent customers." },
      { title: "Logo Vectorising & Tidy-Up", platform: "PeoplePerHour", tools: ["Illustrator"], budget: "$8", location: "Remote", posted: "21 days ago", url: "https://www.peopleperhour.com/freelance-jobs/design/logo-design/we-need-logo-vectorising-and-tidying-up-4495365", desc: "Convert font letters to precise vectors, harmonize strokes and deliver scalable files." }
    ]
  }
];

// ---- Expansion pass: new platforms (We Work Remotely, Guru) + thinner/new verticals ----
const GU = "https://www.guru.com";
const MORE = [
  { vertical: "Fashion & Apparel", listings: [
    { title: "Loungewear Tech Pack Creation", platform: "Freelancer.com", tools: ["Illustrator","CAD/CAM"], budget: "$118 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/adobe-illustrator/loungewear-tech-pack-creation", desc: "Translate moodboards for three loungewear sets into production-ready tech packs with measurements." },
    { title: "Graphic Designer for Ethnic Brand (sarees & lehengas)", platform: "Freelancer.com", tools: ["Photoshop"], budget: "$52 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/digital-marketing/graphic-designer-for-ethnic-brand", desc: "Visually stunning banners for an ethnic-wear brand for website and social media." },
    { title: "Playful Lifestyle Brand Identity (apparel, caps, shoes, toys)", platform: "Freelancer.com", tools: ["Illustrator","InDesign","Photoshop"], budget: "$179 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/packaging-design/playful-lifestyle-brand-identity", desc: "Single energetic identity spanning apparel, caps, shoes, toys and puzzles with bold color play." },
    { title: "Core Visual Identity for BACKY (lifestyle/apparel)", platform: "Freelancer.com", tools: ["Illustrator","Branding"], budget: "$104 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/branding/core-visual-identity-design-for", desc: "Core visual identity for a premium lifestyle and apparel brand inspired by backyard/BBQ culture." }
  ]},
  { vertical: "Food, Restaurant & Beverage", listings: [
    { title: "Modern Minimalist Coffee Brand Refresh", platform: "Freelancer.com (contest)", tools: ["Illustrator","InDesign","Photoshop"], budget: "$214 guaranteed (featured)", location: "Remote", posted: "Active", url: FL+"/contest/modern-minimalist-coffee-brand-refresh-2748715", desc: "Fresh cohesive look for a coffee company: logo and retail packaging with neutral tones and embossed gold." },
    { title: "Authentic Italian Restaurant Logo (Cavatelli)", platform: "Freelancer.com (contest)", tools: ["Illustrator","Photoshop"], budget: "$100 guaranteed (featured)", location: "Remote", posted: "Active", url: FL+"/contest/authentic-italian-restaurant-logo-design-2748465", desc: "Distinctive logo for a forthcoming Italian kitchen and wine bar capturing tradition with a fresh aesthetic." },
    { title: "Modern Logo Redesign for Chicken Restaurant", platform: "Freelancer.com (contest)", tools: ["Illustrator","Photoshop"], budget: "$50 guaranteed", location: "Remote", posted: "Active", url: FL+"/contest/modern-logo-redesign-for-chicken-restaurant-2748567", desc: "Redesign and modernize the logo for a charcoal-grilled roasted-chicken business in red and black." },
    { title: "Traditional Japanese Ramen Poster", platform: "Freelancer.com", tools: ["Photoshop"], budget: "$14 avg bid", location: "Remote", posted: "3 days left", url: FL+"/projects/graphic-design/traditional-japanese-ramen-poster", desc: "Striking A3 poster for an authentic Japanese ramen restaurant with a traditional visual style." },
    { title: "Modern Premium Pickle Label Design (Amazon/Flipkart)", platform: "Freelancer.com", tools: ["Illustrator","Photoshop"], budget: "$53 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/label-design/modern-premium-pickle-label-design", desc: "Standout label for a new pickle line for online marketplaces, sleek black/white/grey aesthetic." }
  ]},
  { vertical: "Sports & Fitness", listings: [
    { title: "FIFA 2026 Stars Poster Design", platform: "Freelancer.com", tools: ["Photoshop"], budget: "$26 avg bid", location: "Remote", posted: "4 days left", url: FL+"/projects/adobe-photoshop/fifa-stars-poster-design", desc: "High-impact poster celebrating the 2026 World Cup with cinematic compositing of star players." },
    { title: "Finalize Mouthguard Packaging Files", platform: "Freelancer.com", tools: ["Illustrator","Photoshop"], budget: "$58 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/packaging-design/finalize-mouthguard-packaging-files", desc: "Turn concept mock-ups into production-ready packaging files with proper bleeds and CMYK conversion." }
  ]},
  { vertical: "Automotive, Industrial & Agriculture", listings: [
    { title: "Modern Automotive Care Label Design", platform: "Freelancer.com", tools: ["Illustrator","Photoshop"], budget: "$50 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/label-design/modern-automotive-care-label-design", desc: "Striking labels for an automotive-care product line with a modern, premium feel." },
    { title: "Luxury Poster Design - Midjourney (automotive/travel/architecture)", platform: "Guru", tools: ["Midjourney","AI design"], budget: "Not specified", location: "Remote", posted: "28 May 2026", url: GU+"/jobs/luxury-poster-design-midjourney/2118462", desc: "Premium luxury poster designs spanning automotive, travel, architecture and lifestyle themes." }
  ]},
  { vertical: "Technology, SaaS & Startups", listings: [
    { title: "Email & Promo Graphic Design + Banner", platform: "Freelancer.com", tools: ["Photoshop","Illustrator","Figma"], budget: "$69 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/email-marketing/email-promo-graphic-design-banner", desc: "Modern email templates plus supporting banners and ad graphics for marketing campaigns." },
    { title: "Professional LinkedIn Banner Design (IT Operations)", platform: "Freelancer.com (contest)", tools: ["Illustrator","Photoshop"], budget: "$67 guaranteed", location: "Remote", posted: "Active", url: FL+"/contest/professional-linkedin-banner-design-2748783", desc: "1584x396 LinkedIn banner capturing IT-operations expertise with technical visuals." },
    { title: "Vibrant Social & Web Graphics", platform: "Freelancer.com", tools: ["Illustrator","Photoshop","Figma"], budget: "$73 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/social-media-marketing/vibrant-social-web-graphics", desc: "Bold, energetic visuals across social platforms and website graphics." },
    { title: "Display Banners Showcasing Brand Values", platform: "Freelancer.com", tools: ["Photoshop","Illustrator"], budget: "$29 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/adobe-photoshop/display-banners-showcasing-brand-values", desc: "Four static banner creatives in standard ad sizes showcasing company core values." },
    { title: "Graphic Artist for Printing & Signage Co (Houston)", platform: "Guru", tools: ["Illustrator","Canva"], budget: "$8-$15/hr", location: "Houston, TX", posted: "31 May 2026", url: GU+"/jobs/graphic-artist/2118504", desc: "Ongoing part-time graphic artist working in Illustrator and Canva for a printing/signage company." }
  ]},
  { vertical: "E-commerce, Retail & Product", listings: [
    { title: "Amazon A+ Content and Image Designer", platform: "Freelancer.com", tools: ["Photoshop"], budget: "$45 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/amazon/amazon-content-image-designer", desc: "A+ content and 6+ high-quality product images per listing for three Amazon listings." },
    { title: "E-Commerce Packshot & Artwork Adaptations", platform: "Freelancer.com", tools: ["Illustrator","Photoshop","3D"], budget: "$58 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/packaging-design/commerce-packshot-artwork-adaptations", desc: "Turn final packaging files into platform-ready packshots for Amazon and Shopify." },
    { title: "Google Performance Max Image Assets (60 assets)", platform: "Freelancer.com", tools: ["Canva","Photoshop","Figma"], budget: "$113 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/canva/google-performance-max-image-assets", desc: "60 premium Performance Max ad assets in landscape, square and portrait formats plus logos." },
    { title: "Elegant Facebook Carousel Ad Design", platform: "Freelancer.com", tools: ["Photoshop","Illustrator"], budget: "$29 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/adobe-photoshop/elegant-facebook-carousel-design", desc: "5-6 Facebook carousel images featuring best-selling products with refined aesthetics." },
    { title: "Resize 5-6 Photos for Online Seller Site", platform: "Guru", tools: ["Photo editing"], budget: "$10 per photo", location: "Remote", posted: "20 May 2026", url: GU+"/jobs/need-photos-resized/2118310", desc: "Resize roughly 5-6 photos for an online seller listing." }
  ]},
  { vertical: "Music, Film, Publishing & Media", listings: [
    { title: "Official Main Poster for Bengali Feature Film AUTOBI", platform: "Freelancer.com (contest)", tools: ["Photoshop","Illustrator"], budget: "$26 guaranteed", location: "Remote", posted: "3 days left", url: FL+"/contest/design-the-official-main-poster-for-bengali-feature-film-quotautobiquot-2747502", desc: "Official main theatrical/digital poster for an upcoming Bengali feature film." },
    { title: "Deadly Day Movie Poster (thriller)", platform: "Freelancer.com (contest)", tools: ["Photoshop","Illustrator","InDesign"], budget: "$100 guaranteed", location: "Remote", posted: "5 days left", url: FL+"/contest/deadly-day-poster-design-2743169", desc: "Movie poster for a thriller featuring social-media influencers, built from provided film stills." },
    { title: "Realistic Movie Poster Recreation (photo masking/blending)", platform: "Freelancer.com", tools: ["Photoshop"], budget: "$313 avg bid", location: "Remote", posted: "1 day left", url: FL+"/projects/adobe-photoshop/realistic-movie-poster-recreation", desc: "Rebuild AI key art for a reality-show poster by replacing AI elements with masked hi-res photos." },
    { title: "Techno Gamer Shorts Thumbnails (gaming/YouTube)", platform: "Freelancer.com", tools: ["Photoshop"], budget: "$197 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/adobe-photoshop/techno-gamer-shorts-thumbnails", desc: "Batch of energetic YouTube Shorts thumbnails with game characters at 1080x1920." },
    { title: "AI Storyboard Artist for Cinematic Film", platform: "Guru", tools: ["Midjourney","Stable Diffusion"], budget: "Under $250", location: "Remote", posted: "24 May 2026", url: GU+"/jobs/ai-storyboard-artist-for-cinematic-film/2118400", desc: "Create a cinematic storyboard using AI-generated imagery." },
    { title: "Paperback & Kindle Book Formatter", platform: "Guru", tools: ["Book layout"], budget: "Under $250", location: "Remote", posted: "27 May 2026", url: GU+"/jobs/paperback-kindle-book-formatter-needed/2118427", desc: "Turn completed manuscripts into clean, professional, reader-friendly print and Kindle interiors." }
  ]},
  { vertical: "Photo Editing, Retouching & Restoration", listings: [
    { title: "Photoshop / Illustrator Artist to Change Image", platform: "Guru", tools: ["Photoshop","Illustrator"], budget: "Under $250", location: "Remote", posted: "5 hours ago", url: GU+"/jobs/photoshop-illustrato-artist-change-image/2118574", desc: "Skilled Photoshop/Illustrator artist to modify an image; available immediately." },
    { title: "Photoshop Expert (3D designs, short project)", platform: "Guru", tools: ["Photoshop"], budget: "$100 or less", location: "United States", posted: "30 May 2026", url: GU+"/jobs/photoshop-expert/2118493", desc: "Photoshop expert skilled in 3D designs for a short project." }
  ]},
  { vertical: "Pets & Animals", listings: [
    { title: "Dog-Care Brand Logo (hand caring for a canine)", platform: "Guru", tools: ["Not specified"], budget: "$250-$500", location: "Remote", posted: "1 Jun 2026", url: GU+"/jobs/logo-design/2118523", desc: "Uniquely designed logo resembling a human hand caring for a canine." }
  ]},
  { vertical: "Beauty, Cosmetics & Personal Care", listings: [
    { title: "Luxury Skincare Brand Creation (Rakaan)", platform: "Freelancer.com", tools: ["Illustrator","Photoshop","Branding"], budget: "$466 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/branding/luxury-skincare-brand-creation", desc: "Complete visual identity for a skincare line: elegant minimal design for black jars and serum bottles." },
    { title: "Minimalist Skincare Logo", platform: "Freelancer.com (contest)", tools: ["Illustrator","Photoshop"], budget: "$20 guaranteed", location: "Remote", posted: "Active", url: FL+"/contest/minimalist-skincare-logo-2747981", desc: "Logo for a skincare cosmetics brand with an icon derived from the name, elegant fonts and earthy colors." },
    { title: "Nature-Inspired Perfume Book Box (fragrance packaging)", platform: "Freelancer.com (contest)", tools: ["Illustrator","Illustration"], budget: "$50 guaranteed", location: "Remote", posted: "Active", url: FL+"/contest/natureinspired-perfume-book-box-2747190", desc: "Luxury book-style rigid box for a fragrance with organic graphics, delicate florals and pastels." },
    { title: "AI Designer for Beauty + Skincare", platform: "Guru", tools: ["AI design tools"], budget: "$250-$500", location: "Remote", posted: "28 May 2026", url: GU+"/jobs/ai-designer-for-beauty-skincare/2118469", desc: "Create elevated lifestyle AI imagery and content for beauty brands." },
    { title: "Motion / 3D Animator for Skincare Videos", platform: "Guru", tools: ["Cinema 4D","3D animation"], budget: "$250-$500", location: "Remote", posted: "28 May 2026", url: GU+"/jobs/motion3d-animator-for-skincare-videos/2118468", desc: "Motion designer/animator for premium educational skincare videos." }
  ]},
  { vertical: "Nonprofit, Religious & Community", listings: [
    { title: "Festive Eid al-Adha Poster Design", platform: "Freelancer.com", tools: ["Illustrator","Photoshop"], budget: "$216 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/adobe-illustrator/festive-eid-adha-poster-design", desc: "Vibrant print-ready poster capturing Eid al-Adha with festive colors, crescents and geometric motifs." },
    { title: "Church Connection Group Visual Identity (GC - Grupos de Conexao)", platform: "Freelancer.com (contest)", tools: ["Illustrator","Photoshop"], budget: "$101 guaranteed", location: "Remote", posted: "Active", url: FL+"/contest/criar-identidade-visual-quotgcmdashgrupos-de-conexatildeoquot-2746471", desc: "Modern minimalist visual identity for a church connection group with a puzzle-inspired logo." },
    { title: "Design Prayer Cards - Anxiety Line (Catholic therapists)", platform: "Guru", tools: ["Graphic design"], budget: "Not specified", location: "Remote", posted: "23 May 2026", url: GU+"/jobs/design-prayer-cards-anxiety-line/2118371", desc: "Expand a prayer-card collection designed for Catholic therapists." },
    { title: "Event Poster - Run for Hope 2026 (charity)", platform: "Freelancer.com", tools: ["Illustrator","Photoshop"], budget: "$8/hr avg", location: "Remote", posted: "3 days left", url: FL+"/projects/advertisement-design/event-poster-40480884", desc: "Energetic colorful poster promoting a community charity event with date, location and registration." },
    { title: "Outdoor Street Banner for Bluelight Event (emergency services)", platform: "Freelancer.com (contest)", tools: ["Illustrator","Photoshop","InDesign"], budget: "$25 guaranteed", location: "Remote", posted: "Active", url: FL+"/contest/outdoor-street-banner-design-for-bluelight-event-firefighters-police-ambulance-2748052", desc: "6m x 1m outdoor street banner for a firefighters/police/ambulance community event." }
  ]},
  { vertical: "Education & Children", listings: [
    { title: "Islamic Children's Flashcard Design", platform: "Freelancer.com", tools: ["Illustrator","Photoshop","Illustration"], budget: "$108 avg bid", location: "Remote", posted: "Active", url: FL+"/projects/illustration/islamic-children-flashcard-design", desc: "Polish rough-laid-out Islamic flashcard sets into commercially ready products with cartoonish artwork." },
    { title: "Minimalist Educational Poster (Poster Edukasi)", platform: "Freelancer.com", tools: ["Illustrator","Photoshop"], budget: "$17 avg bid", location: "Remote", posted: "5 days left", url: FL+"/projects/poster-design/desain-poster-edukasi-minimalis", desc: "Minimalist educational poster/brochure with clean layout, typography and simple icons." },
    { title: "Cartoon Dog Kids App Page Design (Zili mascot)", platform: "Freelancer.com (contest)", tools: ["Illustration"], budget: "$1000 guaranteed", location: "Remote", posted: "Active", url: FL+"/contest/cartoon-dog-kids-app-page-design-2748706", desc: "Premium sample page for a children's learning app featuring a dog mascot." }
  ]},
  { vertical: "Remote / In-house Design Roles (employer-posted)", note: "Salaried or contract roles posted by hiring companies (We Work Remotely, Guru) - a complement to the per-project gigs above. Salary bands are shown exactly as the board displayed them.", listings: [
    { title: "Brand Designer - Contra", platform: "We Work Remotely", tools: ["Not specified"], budget: "$25k-$49k/yr band (Contract)", location: "San Francisco, CA", posted: "23 days ago", url: "https://weworkremotely.com/remote-jobs/contra-brand-designer-7", desc: "Contract brand designer role at Contra." },
    { title: "Graphic Designer - MailerLite", platform: "We Work Remotely", tools: ["Not specified"], budget: "$25k-$49k/yr band (Full-Time)", location: "USA", posted: "2 days ago", url: "https://weworkremotely.com/remote-jobs/mailerlite-graphic-designer", desc: "Full-time remote graphic designer role at email-marketing company MailerLite." },
    { title: "Creative Performance Designer - Nabu Global", platform: "We Work Remotely", tools: ["Not specified"], budget: "Full-Time", location: "Dubai / Remote", posted: "13 days ago", url: "https://weworkremotely.com/remote-jobs/nabu-global-fze-creative-performance-designer", desc: "Full-time creative performance designer at Nabu Global FZE." },
    { title: "Lead Product Designer - Blink Health", platform: "We Work Remotely", tools: ["Not specified"], budget: "Full-Time", location: "United States", posted: "16 days ago", url: "https://weworkremotely.com/remote-jobs/blink-health-lead-product-designer", desc: "Lead product designer role at Blink Health." },
    { title: "Turkish-Speaking Video & Motion Graphics Designer - XM", platform: "We Work Remotely", tools: ["Video","Motion Graphics"], budget: "$25k-$49k/yr band (Full-Time)", location: "Cyprus / Remote", posted: "21 days ago", url: "https://weworkremotely.com/remote-jobs/xm-turkish-speaking-video-motion-graphics-designer", desc: "Full-time video and motion graphics designer (Turkish-speaking) at trading firm XM." },
    { title: "Long-Term Video Editor for YouTube Channel", platform: "Guru", tools: ["Video editing"], budget: "Under $250", location: "Remote", posted: "1 Jun 2026", url: GU+"/jobs/long-term-video-editor-for-youtube-chann/2118511", desc: "Ongoing remote video editor for a YouTube channel." },
    { title: "Versatile Canva Graphic Designer Needed", platform: "Freelancer.com", tools: ["Canva"], budget: "$19/hr avg", location: "Remote", posted: "Active", url: FL+"/projects/canva/versatile-canva-graphic-designer-needed", desc: "All-round graphic designer fluent in Canva for logos, social media and packaging mock-ups." }
  ]}
];
MORE.forEach(m => { const ex = SECTIONS.find(s => s.vertical === m.vertical); if (ex) { ex.listings.push(...m.listings); } else { SECTIONS.push(m); } });

// ---- Upwork pass (captured from public newest-first job feed via signed-in browser) ----
const UP = "https://www.upwork.com/nx/search/jobs/?q=graphic%20design&sort=recency";
const MORE2 = [
  { vertical: "Music, Film, Publishing & Media", listings: [
    { title: "eBook + Paperback Cover for Amazon Kindle (Romance, ongoing)", platform: "Upwork (public job feed)", tools: ["Cover / Graphic design"], budget: "Fixed - $75 est", location: "Remote", posted: "4 hours ago", url: UP, desc: "Eye-catching eBook and paperback covers for Steamy Contemporary Romance novels on an ongoing basis." },
    { title: "KDP Interior Layout Designer - 60-Page Family Emergency Binder", platform: "Upwork (public job feed)", tools: ["Layout","InDesign"], budget: "Fixed - $150 est", location: "Remote", posted: "4 hours ago", url: UP, desc: "Format a 60-page landscape document/ledger, print-ready for Amazon KDP upload (11x8.5in)." }
  ]},
  { vertical: "Finance, Crypto & Professional Services", listings: [
    { title: "Engagement Letter Brochure (financial advisory firm)", platform: "Upwork (public job feed)", tools: ["InDesign","Illustrator"], budget: "Fixed - $30-$50", location: "Remote", posted: "6 hours ago", url: UP, desc: "Polished, print-ready marketing brochure for a wealth/financial-advisory firm with existing branding." },
    { title: "Bifold Rack Card for Personal Injury Law Firm", platform: "Upwork (public job feed)", tools: ["Illustrator","Print/Layout"], budget: "Fixed - $30-$50", location: "Remote (LA County, CA)", posted: "9 hours ago", url: UP, desc: "Professional bifold rack card for print distribution for a personal-injury law firm." }
  ]},
  { vertical: "Real Estate, Construction & Property", listings: [
    { title: "Logo Design for Landscape Studio (Long Boy Studios)", platform: "Upwork (public job feed)", tools: ["Photoshop","Logo / 3D"], budget: "Fixed - $300 est", location: "Remote", posted: "7 hours ago", url: UP, desc: "Clean professional brand mark for a landscape-design studio, for contracts, invoices and drawings." }
  ]},
  { vertical: "General / Cross-Industry Branding & Graphics", listings: [
    { title: "Capabilities Slick Sheet for Sole Proprietor", platform: "Upwork (public job feed)", tools: ["InDesign","Illustrator"], budget: "Hourly - Intermediate", location: "Remote", posted: "4 hours ago", url: UP, desc: "Editable one-page capabilities sheet template for a small business." },
    { title: "Ongoing Graphic Design - Email, Social, Packaging, Logos", platform: "Upwork (public job feed)", tools: ["Illustrator"], budget: "Hourly - $20-$45", location: "Remote", posted: "6 hours ago", url: UP, desc: "Misc ongoing work: product packaging, email graphics, social, magazine ads and the occasional logo." },
    { title: "Logo and Label Design in Canva", platform: "Upwork (public job feed)", tools: ["Canva","Illustrator","Photoshop"], budget: "Hourly - $15-$35", location: "Remote", posted: "7 hours ago", url: UP, desc: "Create a logo and product labels in Canva aligned to the brand identity." }
  ]},
  { vertical: "Remote / In-house Design Roles (employer-posted)", listings: [
    { title: "Graphic Designer (ongoing contract, 5+ yrs, USA/PST)", platform: "Upwork (public job feed)", tools: ["Photoshop","Illustrator","InDesign","After Effects","XD","Figma","Canva"], budget: "Hourly - Expert, 6+ months", location: "Remote (USA, PST)", posted: "9 hours ago", url: UP, desc: "Ongoing contract designer for events, campaigns, music-release covers, web and integrated marketing; full Adobe Creative Suite." }
  ]}
];
MORE2.forEach(m => { const ex = SECTIONS.find(s => s.vertical === m.vertical); if (ex) { ex.listings.push(...m.listings); } else { SECTIONS.push(m); } });

// ---------- rendering ----------
const HMETA = { color: "555555", italics: true, size: 19 };
const children = [];

// Title block
children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 1200, after: 60 },
  children: [new TextRun({ text: "Adobe & Design Freelance Opportunities", bold: true, size: 52, font: "Arial" })] }));
children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 60 },
  children: [new TextRun({ text: "Aggregated job, freelance & gig postings for Adobe / Creative Cloud work, organized by industry vertical", size: 24, color: "444444" })] }));
children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 40 },
  children: [new TextRun({ text: "Listings captured: 3 June 2026", size: 22, color: "666666" })] }));

const total = SECTIONS.reduce((n, s) => n + s.listings.length, 0);
children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 240 },
  children: [new TextRun({ text: total + " listings across " + SECTIONS.length + " verticals  |  Sources: Freelancer.com, PeoplePerHour, Upwork, We Work Remotely, Guru, Contra", size: 22, color: "666666" })] }));

children.push(new Paragraph({ children: [new PageBreak()] }));

// About / methodology
children.push(new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("About This Report")] }));
const aboutBullets = [
  "Scope: open postings where a business or individual is hiring for Adobe / design work - Photoshop, Illustrator, InDesign, Lightroom, After Effects, Premiere Pro, Adobe XD, Firefly, Express, plus the design tasks these tools are used for (logos, branding, photo retouching, packaging, flyers, brochures, social graphics, video/motion).",
  "Method: these listings were gathered from the public job feeds of Freelancer.com, PeoplePerHour, Upwork, We Work Remotely and Guru (plus a Contra page), extracted live. Every entry is a real posting with a working source link - nothing here is invented.",
  "How to read an entry: each listing shows the platform, the budget exactly as the platform displayed it (Freelancer figures are the platform's 'average bid' estimate, not a fixed price), location, how recently it was posted, the Adobe/design tools named or implied, a one-line description, and a direct link to the posting.",
  "Source notes & gaps: Upwork listings were captured from its public newest-first job search via the browser; per-job Upwork permalinks are not included, so each Upwork link opens that search page (find the role by its title). Reddit's hiring boards (r/forhire, r/HungryArtists, etc.) could not be accessed at all - they block the crawler and are also blocked by the browser tool's safety policy. RemoteOK renders its listings client-side and could not be read. The Contra entries returned with June 2025 dates and may be stale; they are flagged inline.",
  "This is a deliberately broad first pass. Deeper sweeps (more categories, more platforms, more verticals, and the signed-in Upwork/Reddit sources) can be added on request."
];
aboutBullets.forEach(t => children.push(new Paragraph({ numbering: { reference: "bullets", level: 0 }, spacing: { after: 80 }, children: [new TextRun({ text: t, size: 22 })] })));

// Contents
children.push(new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { before: 240 }, children: [new TextRun("Contents")] }));
children.push(new TableOfContents("Verticals", { hyperlink: true, headingStyleRange: "1-1" }));
children.push(new Paragraph({ children: [new PageBreak()] }));

// Vertical sections
SECTIONS.forEach((section, si) => {
  if (si > 0) children.push(new Paragraph({ children: [new PageBreak()] }));
  children.push(new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun(section.vertical)] }));
  children.push(new Paragraph({ spacing: { after: section.note ? 60 : 160 },
    children: [new TextRun({ text: section.listings.length + (section.listings.length === 1 ? " listing" : " listings"), italics: true, size: 20, color: "777777" })] }));
  if (section.note) children.push(new Paragraph({ spacing: { after: 160 }, children: [new TextRun({ text: section.note, italics: true, size: 20, color: "777777" })] }));

  section.listings.forEach(it => {
    // Title
    children.push(new Paragraph({ spacing: { before: 120, after: 20 }, keepNext: true,
      children: [new TextRun({ text: it.title, bold: true, size: 24, font: "Arial" })] }));
    // Meta line
    const metaBits = [it.platform, "Budget: " + it.budget, it.location, "Posted: " + it.posted].filter(Boolean).join("   |   ");
    children.push(new Paragraph({ spacing: { after: 20 }, children: [new TextRun(Object.assign({ text: metaBits }, HMETA))] }));
    // Tools
    children.push(new Paragraph({ spacing: { after: 20 }, children: [
      new TextRun({ text: "Adobe / tools: ", bold: true, size: 20, color: "1F4E79" }),
      new TextRun({ text: (it.tools && it.tools.length ? it.tools.join(", ") : "Not specified"), size: 20, color: "1F4E79" })
    ] }));
    // Description
    children.push(new Paragraph({ spacing: { after: 20 }, children: [new TextRun({ text: it.desc, size: 22 })] }));
    // Link
    children.push(new Paragraph({ spacing: { after: 160 }, children: [
      new ExternalHyperlink({ link: it.url, children: [new TextRun({ text: "View the posting", style: "Hyperlink", size: 20 })] })
    ] }));
  });
});

const doc = new Document({
  styles: {
    default: { document: { run: { font: "Arial", size: 22 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 30, bold: true, font: "Arial", color: "1F4E79" },
        paragraph: { spacing: { before: 240, after: 120 }, outlineLevel: 0,
          border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: "1F4E79", space: 4 } } } }
    ]
  },
  numbering: {
    config: [
      { reference: "bullets", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 540, hanging: 260 } } } }] }
    ]
  },
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER,
      children: [ new TextRun({ text: "Adobe & Design Freelance Opportunities  -  ", size: 16, color: "999999" }),
        new TextRun({ text: "Page ", size: 16, color: "999999" }), new TextRun({ children: [PageNumber.CURRENT], size: 16, color: "999999" }) ] })] }) },
    children
  }]
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync("/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads/Adobe_Design_Freelance_Opportunities.docx", buffer);
  console.log("WROTE docx with " + total + " listings across " + SECTIONS.length + " verticals");
});
