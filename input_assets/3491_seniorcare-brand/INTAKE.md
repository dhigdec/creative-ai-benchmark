# INTAKE — Graphic Designer for Premium Senior Home Care / Dignity-First Brand (Long-Term Partner)

**Task 3491** · Express Template Design · Brochures · feasibility: **template** · source: [upwork posting](https://www.upwork.com/nx/search/jobs/?q=Graphic%20Designer%20for%20Premium%20Senior%20Home%20Care%20/%20Dignit)

## The simulated client
**Modern Care Collective** — premium private senior home care. *Dignity-First Care, Compassion Always.*
Palette: Ivory Whisper `#F8F4ED` (primary), Forest Dignity `#4A6D5A` (secondary), Rose Terracotta `#CB9D8C` (accent)  
Fonts: headings **Lora**, body **Libre Franklin**  
Voice: Our brand voice is warm, empathetic, and reassuring, speaking with understated elegance and genuine respect. We aim to foster trust and comfort, always prioritizing dignity over clinical formality or patronizing tones.

## Input assets supplied (what the agent picks up)

| # | File / value | Fulfils client input | Generator |
|---|---|---|---|
| 1 | `assets/mcc_logo.png` | Modern Care Collective logo (bespoke logo development itself is out of scope — human-desig | gemini/gemini-3-pro-image |
| 2 | `assets/care_01.jpg` | Warm/empathetic caregiver + senior photography | openai/gpt-image-2 |
| 3 | `assets/care_02.jpg` | Warm/empathetic caregiver + senior photography | openai/gpt-image-2 |
| 4 | `assets/care_03.jpg` | Warm/empathetic caregiver + senior photography | openai/gpt-image-2 |
| 5 | `assets/care_04.jpg` | Warm/empathetic caregiver + senior photography | openai/gpt-image-2 |
| 6 | `assets/care_05.jpg` | Warm/empathetic caregiver + senior photography | openai/gpt-image-2 |
| 7 | `assets/services_copy.json` | Copy: services, family/caregiver-facing messaging | gemini/gemini-2.5-flash |
| 8 | `assets/services_copy.md` | Copy: services, family/caregiver-facing messaging | gemini/gemini-2.5-flash |

## Decisions & assumptions (items the brief left open)
- **Modern Care Collective logo (bespoke logo development itself is out of scope — human-designed)** → The client's human-designed logo is SIMULATED by a generated stand-in file (mcc_logo.png) so the collateral workflow can run; in production the client's real file drops into assets/ unchanged  
  *why:* Brief says the logo arrives from the client; the pilot needs a concrete file to place.
- **Brand colours + typography (warm, premium, dignity-first) — to be defined** → Defined in persona.json: warm cream / deep sage / soft terracotta palette + serif/humanist font pairing — presented as the proposal the brief asks for  
  *why:* 'To be defined' is exactly what the persona stage produces.
- **Deliverables: brochures, flyers, social media graphics, LinkedIn posts, website assets; print + digital sizes — confirm** → Agent output spec: A4 tri-fold brochure + A5 flyer + 1080x1080/1080x1920 social + 1200x627 LinkedIn; sizes flagged for confirmation  
  *why:* Standard sizes assumed where the brief defers.

## Next step — the Adobe workflow the agent runs
```
asset_add_file (logo once supplied + warm caregiver/senior photos + brand assets) -> search_design (Express brochure + flyer + social + LinkedIn post templates, warm/premium) -> fill_text (dignity-first care copy, services) -> document_convert_pdf (print-ready brochures/flyers) -> image_crop_and_resize (social/LinkedIn sizes) -> asset_preview_file
```

Coverage: 5 client inputs — 3 supplied as assets, 2 resolved by recorded decisions, 0 uncovered. **ready_for_agent: True**

## Original client brief (verbatim)
> We are Modern Care Collective, a new premium home care provider based in Alpharetta, GA. We’re building a warm, respectful, trustworthy, and modern brand that truly puts both seniors and caregivers first — dignity-first care. We are looking for a talented Graphic Designer to grow with us as a long-term partner (part-time to start, with potential to scale as the company grows). **What You’ll Do:** - Develop and evolve our full visual brand identity (logos, color palette, typography, comprehensive style guide) - Create high-quality marketing materials (brochures, flyers, social media graphics, LinkedIn posts, website assets) - Design caregiver and family-facing collateral that feels premium, empathetic, warm, and professional **MUST HAVE Experience:** - Portfolio examples in senior care, home care, assisted living, hospice, non-medical caregiving, or very similar senior/wellness brands - Proven ability to create warm, empathetic, and premium-feeling designs for families and caregivers (not just clinical or generic healthcare) - Strong experience with branding, logo design, print collateral, brochures, and social media graphics **Requirements:** - Proficiency in Adobe Illustrator, Adobe InDesign, and Adobe Photoshop - Excellent English communication and ability to collaborate regularly - Available for occasional Zoom calls during US Eastern Time (9am–5pm ET) **Details:** - Part-time / flexible hours to start (10–20+ hours per month, can grow) - Long-term partnership preferred — we want someone who will grow with the company - Hourly rate: $25–$45/hr depending on experience and quality - Fully remote Please include in your proposal: - Direct link to your portfolio (Behance, personal site, or PDF) with clear senior/home care examples - Brief example of your work for senior care, home care, hospice, or similar - Why you’re interested in designing for a dignity-first home care brand - Your availability for occasional ET Zoom calls and how many hours/month you can start with