# SB3-004-PHO trajectory

**Intent:** Consistent but distinct houses; natural water and stone; no fabricated glow, crushed blacks, or overselling.

## Adobe action log

1. `image_auto_straighten` — `{"uprightMode": "auto", "constrainCrop": true}`
2. `image_apply_auto_tone` — `{}`
3. `image_apply_adjustments` — `"task-specific white balance, luminance and restrained saturation"`
4. `image_apply_preset` — `"task-specific approved preset"`
5. `image_apply_adjustments` — `{"highlights": -60, "darks": 40}`
6. `image_crop_and_resize` — `{"width": 1920, "height": 1080, "fit": "reframe", "focus": "subject", "quality": 7}`

## Intermediate snapshot

`trajectory/intermediate/oliveto_bedroom_after_tone.png`

## Rationale

One restrained coastal grade unifies the collection; the hero system uses the pool as the place-first anchor and an opaque blue information rail for reliable booking legibility.

## Retries and tradeoffs

- **multi-edit preset**: zero-result response; retried in connector-safe batches; all 12 succeeded.
- **hero crop quality**: workspace rejected value 100; allowed range max 7; retried at quality 7.

## Crop verification

Landscape subject detection returned a centered fallback for all three pool frames; visual review confirmed the compositions retain pool, architecture and cove without unacceptable clipping.

## Output verification

- `deliverables/booking-hero-oliveto.png` — exists=True; bytes=3092008; sha256=`bc9c1db1f5b6798a0f9237853cec942bc7c4c198455b62231051ed3cba44d01a`
- `deliverables/booking-hero-scogliera.png` — exists=True; bytes=2520098; sha256=`b52e3a1d04d93ae0758d721381ec89def2a875754b57c25d4e4ea969816d0895`
- `deliverables/booking-hero-verranza.png` — exists=True; bytes=3117598; sha256=`36a1af36415c4614f0d7c7bd85f4fbbe26949a6adfadad8fcd72a55f504f311a`
- `deliverables/villa-collection.pdf` — exists=True; bytes=5458645; sha256=`e0678d0fd45d750da0441e34efa23c46c71bf003180d1d0ee3507784d6696a22`

## Status

production complete; independent benchmark creative review remains external
