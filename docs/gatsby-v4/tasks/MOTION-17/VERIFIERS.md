# SB3-097-MOT atomic output verifiers

Result: not assessed. Answer every acceptance statement Yes or No. Only Yes passes. Each row evaluates one named output and one observable condition; subjective creative judgement is recorded separately.

| Output | Check ID | Type | Pass condition | Evidence | Answer |
|---|---|---|---|---|---|
| deliverables/event-recap.mp4 | MOTION-17/event-recap/A001 | auto | deliverables/event-recap.mp4 — File is present. | Automated file_exists result | Yes / No |
| deliverables/event-recap.mp4 | MOTION-17/event-recap/A002 | auto | deliverables/event-recap.mp4 — The file opens in a format-aware reader. | Automated decodable result | Yes / No |
| deliverables/event-recap.mp4 | MOTION-17/event-recap/A003 | auto | deliverables/event-recap.mp4 — The width is 1920 px. | Automated width result | Yes / No |
| deliverables/event-recap.mp4 | MOTION-17/event-recap/A004 | auto | deliverables/event-recap.mp4 — The height is 1080 px. | Automated height result | Yes / No |
| deliverables/event-recap.mp4 | MOTION-17/event-recap/A005 | auto | deliverables/event-recap.mp4 — The runtime is between 20 and 30 seconds. | Automated duration_range result | Yes / No |
| deliverables/event-recap.mp4 | MOTION-17/event-recap/A006 | auto | deliverables/event-recap.mp4 — The video codec is H.264. | Automated video_codec result | Yes / No |
| deliverables/event-recap.mp4 | MOTION-17/event-recap/A007 | auto | deliverables/event-recap.mp4 — The pixel format is yuv420p. | Automated pixel_format result | Yes / No |
| deliverables/event-recap.mp4 | MOTION-17/event-recap/A008 | auto | deliverables/event-recap.mp4 — The frame rate is 24 fps. | Automated frame_rate result | Yes / No |
| deliverables/event-recap.mp4 | MOTION-17/event-recap/A009 | auto | deliverables/event-recap.mp4 — The picture changes over time. | Automated moving_picture result | Yes / No |
| deliverables/event-recap.mp4 | MOTION-17/event-recap/A010 | auto | deliverables/event-recap.mp4 — The export contains an audio stream. | Automated audio_stream result | Yes / No |
| deliverables/event-recap.mp4 | MOTION-17/event-recap/A011 | auto | deliverables/event-recap.mp4 — The audio is not wholly silent. | Automated non_silent_audio result | Yes / No |
| deliverables/event-recap.mp4 | MOTION-17/event-recap/H001 | human | deliverables/event-recap.mp4 — The sequence represents the supplied event. | Approved task brief and supplied source pack | Yes / No |
| deliverables/event-recap.mp4 | MOTION-17/event-recap/H002 | human | deliverables/event-recap.mp4 — The final-card date matches the approved next-event file exactly. | Approved task brief and supplied source pack | Yes / No |
| deliverables/event-cover.png | MOTION-17/event-cover/A001 | auto | deliverables/event-cover.png — File is present. | Automated file_exists result | Yes / No |
| deliverables/event-cover.png | MOTION-17/event-cover/A002 | auto | deliverables/event-cover.png — The file opens in a format-aware reader. | Automated decodable result | Yes / No |
| deliverables/event-cover.png | MOTION-17/event-cover/A003 | auto | deliverables/event-cover.png — The width is 1080 px. | Automated width result | Yes / No |
| deliverables/event-cover.png | MOTION-17/event-cover/A004 | auto | deliverables/event-cover.png — The height is 1350 px. | Automated height result | Yes / No |
| deliverables/event-cover.png | MOTION-17/event-cover/H001 | human | deliverables/event-cover.png — At the delivered dimensions, OCR returns the complete approved text for event identity. | Approved task brief and supplied source pack | Yes / No |
| sources/event-cover.zip | MOTION-17/event-cover-source/A001 | auto | sources/event-cover.zip — The named source archive is delivered. | Automated file_exists result | Yes / No |
| sources/event-cover.zip | MOTION-17/event-cover-source/A002 | auto | sources/event-cover.zip — The source archive opens. | Automated decodable result | Yes / No |
| sources/event-cover.zip | MOTION-17/event-cover-source/A003 | auto | sources/event-cover.zip — The archive contains at least one allowed editable source artifact. | Automated editable_source_present result | Yes / No |
| sources/event-cover.zip | MOTION-17/event-cover-source/H001 | human | sources/event-cover.zip — The source opens in its stated editing application. | Editable source archive | Yes / No |
| sources/event-cover.zip | MOTION-17/event-cover-source/H002 | human | sources/event-cover.zip — The text can be edited independently of the photograph. | Editable source archive | Yes / No |
| deliverables/next-event.png | MOTION-17/next-event/A001 | auto | deliverables/next-event.png — File is present. | Automated file_exists result | Yes / No |
| deliverables/next-event.png | MOTION-17/next-event/A002 | auto | deliverables/next-event.png — The file opens in a format-aware reader. | Automated decodable result | Yes / No |
| deliverables/next-event.png | MOTION-17/next-event/A003 | auto | deliverables/next-event.png — The width is 1080 px. | Automated width result | Yes / No |
| deliverables/next-event.png | MOTION-17/next-event/A004 | auto | deliverables/next-event.png — The height is 1920 px. | Automated height result | Yes / No |
| deliverables/next-event.png | MOTION-17/next-event/H001 | human | deliverables/next-event.png — The date matches the approved next-date file. | Approved task brief and supplied source pack | Yes / No |
| deliverables/next-event.png | MOTION-17/next-event/H002 | human | deliverables/next-event.png — The ticket action remains in the safe area. | Approved task brief and supplied source pack | Yes / No |
| sources/next-event.zip | MOTION-17/next-event-source/A001 | auto | sources/next-event.zip — The named source archive is delivered. | Automated file_exists result | Yes / No |
| sources/next-event.zip | MOTION-17/next-event-source/A002 | auto | sources/next-event.zip — The source archive opens. | Automated decodable result | Yes / No |
| sources/next-event.zip | MOTION-17/next-event-source/A003 | auto | sources/next-event.zip — The archive contains at least one allowed editable source artifact. | Automated editable_source_present result | Yes / No |
| sources/next-event.zip | MOTION-17/next-event-source/H001 | human | sources/next-event.zip — The source opens in its stated editing application. | Editable source archive | Yes / No |
| sources/next-event.zip | MOTION-17/next-event-source/H002 | human | sources/next-event.zip — The text can be edited independently of the photograph. | Editable source archive | Yes / No |
