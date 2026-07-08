```json
{
  "job": {
    "job_name": "Head In The Clouds Tee",
    "garment": "black 100% cotton tee",
    "garment_colour": "black",
    "press": "automatic",
    "stations": 6,
    "total_screens": 4
  },
  "halftone": {
    "lpi": 55,
    "dot_shape": "round",
    "screen_angle_deg": 22,
    "min_printable_dot_pct": 10,
    "max_dot_pct_on_underbase": 75
  },
  "dot_gain": {
    "expected_gain_pct": 22,
    "choke_px": 2,
    "underbase_choke_px": 1.5,
    "note": "Choke is needed to compensate for dot gain and prevent ink spread on absorbent fabric, especially on a dark garment."
  },
  "underbase": {
    "strategy": "white underbase printed first then flashed",
    "underbase_ink": "white",
    "flash": true,
    "highlight_white": false
  },
  "screen_budget": {
    "max_screens": 4,
    "mesh_per_colour": [
      110,
      200,
      200,
      200
    ],
    "registration_tolerance_mm": 0.3
  },
  "print_order": [
    "White Underbase",
    "Lavender",
    "Cobalt",
    "Deep Purple"
  ]
}
```