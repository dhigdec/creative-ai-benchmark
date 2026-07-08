# INTAKE — Reality Show Graphic Designer

**Task 502** · Express Template Design · Social Media Graphics · feasibility: **template** · source: [freelancer posting](https://www.freelancer.com/projects/social-media-marketing/Reality-Show-Graphic-Designer)

## The simulated client
**The Lock House** — Reality Competition Television. *Unlock the Drama. Face the Truth.*
Palette: Deep Teal `#00566B` (primary), Midnight Black `#000000` (secondary), Electric Gold `#FFD700` (accent)  
Fonts: headings **Archivo**, body **Inter**  
Voice: Our tone is intensely dramatic and suspenseful, aiming to create a sense of high-stakes intrigue. It should feel bold and energetic, reflecting the competitive nature and emotional intensity of the show.

## Input assets supplied (what the agent picks up)

| # | File / value | Fulfils client input | Generator |
|---|---|---|---|
| 1 | `assets/show_copy.json` | Copy: contestant intros, voting/elimination text, episode details | gemini/gemini-2.5-flash |
| 2 | `assets/show_copy.md` | Copy: contestant intros, voting/elimination text, episode details | gemini/gemini-2.5-flash |
| 3 | `assets/show_logo.png` | Show logo ('The Lock House') + brand colours | gemini/gemini-3-pro-image |
| 4 | `assets/contestant_01_anya-sharma.jpg` | Contestant photos | openai/gpt-image-2 |
| 5 | `assets/contestant_02_marcus-mac-thorne.jpg` | Contestant photos | openai/gpt-image-2 |
| 6 | `assets/contestant_03_isabella-izzy-rossi.jpg` | Contestant photos | openai/gpt-image-2 |
| 7 | `assets/contestant_04_kai-tanaka.jpg` | Contestant photos | openai/gpt-image-2 |
| 8 | `assets/contestant_05_brenda-bree-jenkins.jpg` | Contestant photos | openai/gpt-image-2 |
| 9 | `assets/contestant_06_liam-o-connell.jpg` | Contestant photos | openai/gpt-image-2 |
| 10 | `assets/sponsor_logo_01.png` | Sponsor logos | gemini/gemini-3-pro-image |
| 11 | `assets/sponsor_logo_02.png` | Sponsor logos | gemini/gemini-3-pro-image |

## Decisions & assumptions (items the brief left open)
- **Counts: 20-30 creatives** → Input set sized so the agent can compose 20-30 creatives (6 contestant intros x platforms + episode/voting/elimination posts + thumbnails + banners)  
  *why:* The count binds the agent's output, not the input assets.
- **Targets: IG/FB/YouTube posts, thumbnails, event banners + standees (print sizes)** → Agent output spec: 1080x1080/1080x1920 social, 1280x720 thumbnails, banners per template; standee assumed 33x80in @150dpi — confirm  
  *why:* Standee size unstated in brief; 33x80 is the retail-standard pull-up.

## Next step — the Adobe workflow the agent runs
```
search_design (Express poster / social / banner / YouTube-thumbnail templates) -> fill_text (contestant names, episode/voting copy) -> asset_add_file (contestant photos + show logo + sponsor logos) -> image_remove_background (contestant cut-outs) -> image_crop_and_resize (IG/FB/YouTube + banner/standee sizes) -> asset_preview_file
```

Coverage: 6 client inputs — 4 supplied as assets, 2 resolved by recorded decisions, 0 uncovered. **ready_for_agent: True**

## Original client brief (verbatim)
> Graphic Designer Needed for Reality Show Branding & Social Media Content
> Description:
> We are launching a new reality show called The Lock House and are looking for a creative graphic designer to work with us on an ongoing basis.
> Scope of Work:
> Social media post designs (Instagram, Facebook, YouTube)
> Contestant introduction posters
> Elimination and voting creatives
> Teaser and promotional graphics
> Sponsor branding creatives
> Event banners and standees
> Logo refinements and brand identity materials
> Thumbnails and digital marketing creatives
> Requirements:
> Strong portfolio in social media and promotional design
> Experience with Photoshop, Illustrator, Canva, or similar tools
> Ability to create modern, attention-grabbing designs
> Quick turnaround and good communication
> Hindi/Indian audience understanding is a plus
> Project Details:
> Reality Show: The Lock House
> Initial requirement: 20–30 creatives
> Potential for long-term collaboration throughout the season
> Please share your portfolio and expected pricing (per design or monthly basis).
> When Applying, Please Mention:
> Your portfolio link
> Previous entertainment/event-related work (if any)
> Your pricing structure
> Turnaround time for urgent creatives
> We are looking for someone who can help build a strong and exciting visual identity for the show from launch to finale.