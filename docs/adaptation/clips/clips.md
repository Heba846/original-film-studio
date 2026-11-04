# Clip production list (paste into Google Flow)

73 clip rows: 71 to generate (10 credits each = 710 credits), 2 reused approved clips (0 credits). All prompts are silent, no dialogue, fixed or locked camera. `clips.csv` holds the same data in columns.

How to use: for each clip, attach the listed keyframe still (start frame) and the approved face reference(s), paste the prompt, paste the negative prompt, generate 8 s. Clips are in film order. `cut in` / `cut out` give the pose to match when cutting from one clip to the next.


## s01 (CH00, narration 12.92 s) - 2 clip(s)

**Timing / bridge:** 2 clips = 16 s vs 12.92 s: c1 plays 0-8, c2 trimmed to 4.92-12.92 (drop its first 3 s).

### s01_c1  (NEW, start +0.0 s)

- Narration cue: "Two shots. That's all it took." / "Ten past four that Friday morning, crouched behind my own bumper..."
- Attach: KF s01 still as start frame; REF-NICO (approved face)
- Cut in: keyframe pose  |  Cut out: Nico head turned toward stairwell door, pistol hanging in LEFT hand
- Risk: gun hand, splint side
- **Prompt** (886 chars):

```
Painterly gouache-and-oil illustrated realism, cinematic noir, visible brush texture, film grain, 16:9. St. Brigid's hospital garage level 2, concrete pillars, dark stairwell door, orange sodium lights, cold rain, wet reflective concrete. Nico: 34, dark wavy hair, stubble, gray eyes, thin white scar through LEFT eyebrow, ruined charcoal suit, pistol in LEFT hand, white plaster splint on RIGHT forearm, fingertips to below elbow. Fallen man in dark coat by a silver sedan, face turned away. Start: Nico stands over him, pistol low in LEFT hand, splinted arm at his chest. He lowers the pistol to point at the floor, then turns his head to the stairwell door. End: gun hanging at his left side, head turned to the door. Camera: low wide, locked off behind a car bumper, rain drips in foreground. Silent, mouths relaxed. No zoom, cuts or morphing; faces and outfits match the reference.
```

- **Negative:**

```
text, subtitles, watermark, logo, zoom, push-in, camera shake, morphing, face drift, changed outfit, extra fingers, fused fingers, deformed hands, extra limbs, duplicate people, speaking, lip sync, talking mouth, blood, gore, visible wound, photorealistic, 3d render, cartoon, camera movement, pan, tilt, necklace, chain, ring, earrings, bracelet, any jewelry, splint on LEFT arm, black splint, missing splint, splint on hand only, gun in RIGHT hand
```

### s01_c2  (NEW, start +4.92 s)

- Narration cue: "...what a life ending sounds like in concrete."
- Attach: KF s01 still as start frame; REF-NICO (approved face); optional: last frame of s01_c1 as start frame if Flow allows, else rely on KF
- Cut in: Nico head turned toward stairwell door, pistol hanging in LEFT hand  |  Cut out: Stairwell door latched, Nico motionless
- Risk: door physics
- **Prompt** (848 chars):

```
Painterly gouache-and-oil illustrated realism, cinematic noir, visible brush texture, film grain, 16:9. St. Brigid's hospital garage level 2, concrete pillars, dark stairwell door, orange sodium lights, cold rain, wet reflective concrete. Nico: 34, dark wavy hair, stubble, gray eyes, thin white scar through LEFT eyebrow, pistol low in LEFT hand, white plaster splint on RIGHT forearm, fingertips to below elbow, standing foreground-left. Start: Nico still, looking at the stairwell door in the background. The heavy stairwell door swings slowly shut on its closer and latches, a sliver of orange light narrowing across the wet floor. Nico does not move. Rain drips off the bumper. End: door closed, Nico motionless. Camera: same low wide angle, locked off. Silent, mouths relaxed. No zoom, cuts or morphing; faces and outfits match the reference.
```

- **Negative:**

```
text, subtitles, watermark, logo, zoom, push-in, camera shake, morphing, face drift, changed outfit, extra fingers, fused fingers, deformed hands, extra limbs, duplicate people, speaking, lip sync, talking mouth, blood, gore, visible wound, photorealistic, 3d render, cartoon, camera movement, pan, tilt, necklace, chain, ring, earrings, bracelet, any jewelry, splint on LEFT arm, black splint, missing splint, splint on hand only, gun in RIGHT hand
```


## s02 (CH00, narration 23.49 s) - 3 clip(s)

**Timing / bridge:** 3 clips = 24 s vs 23.49 s: c3 trimmed by 0.5 s. Last frame must hand off to the approved s03 clip.

### s02_c1  (NEW, start +0.0 s)

- Narration cue: "I looked over the hood. A man was sliding down the side of a silver sedan, a gun a foot from his open hand."
- Attach: KF s02 still as start frame; REF-NICO (approved face)
- Cut in: keyframe pose  |  Cut out: Nico waist-up, pistol low in LEFT hand
- Risk: gun, unwanted hand movement
- **Prompt** (830 chars):

```
Painterly gouache-and-oil illustrated realism, cinematic noir, visible brush texture, film grain, 16:9. St. Brigid's hospital garage level 2, concrete pillars, dark stairwell door, orange sodium lights, cold rain, wet reflective concrete. A dark-coated man slumped against a silver sedan, face turned away, open palm on wet concrete, pistol one foot from his hand, nothing graphic. Start: extreme low close on his open hand and the pistol, rain striking the gun and puddle rings spreading. The hand does not move. Slow tilt up past the pistol to the legs and torso of Nico standing over him, pistol in his LEFT hand. End: framed on Nico from the waist up. Camera: very slow tilt up from the hand to Nico, steady speed, no other camera move. Silent, mouths relaxed. No zoom, cuts or morphing; faces and outfits match the reference.
```

- **Negative:**

```
text, subtitles, watermark, logo, zoom, push-in, camera shake, morphing, face drift, changed outfit, extra fingers, fused fingers, deformed hands, extra limbs, duplicate people, speaking, lip sync, talking mouth, blood, gore, visible wound, photorealistic, 3d render, cartoon, necklace, chain, ring, earrings, bracelet, any jewelry, splint on LEFT arm, black splint, missing splint, splint on hand only, gun in RIGHT hand
```

### s02_c2  (NEW, start +8.0 s)

- Narration cue: "The man standing over him held a different gun, in his left hand."
- Attach: KF s02 still as start frame; REF-NICO (approved face); optional: last frame of s02_c1 as start frame if Flow allows, else rely on KF
- Cut in: Nico waist-up, pistol low in LEFT hand  |  Cut out: Pistol pointed at floor in LEFT hand, grip settled
- Risk: gun grip, finger count
- **Prompt** (828 chars):

```
Painterly gouache-and-oil illustrated realism, cinematic noir, visible brush texture, film grain, 16:9. St. Brigid's hospital garage level 2, concrete pillars, dark stairwell door, orange sodium lights, cold rain, wet reflective concrete. Nico: 34, dark wavy hair, stubble, gray eyes, thin white scar through LEFT eyebrow, ruined charcoal suit, pistol in LEFT hand, white plaster splint on RIGHT forearm, fingertips to below elbow held to his chest. Start: medium shot, pistol hanging in his LEFT hand. He awkwardly re-grips it with his LEFT hand, thumb and fingers settling, then lets the muzzle point at the floor. The splinted arm stays against his chest. End: pistol pointed at the floor, grip settled. Camera: medium shot locked off. Silent, mouths relaxed. No zoom, cuts or morphing; faces and outfits match the reference.
```

- **Negative:**

```
text, subtitles, watermark, logo, zoom, push-in, camera shake, morphing, face drift, changed outfit, extra fingers, fused fingers, deformed hands, extra limbs, duplicate people, speaking, lip sync, talking mouth, blood, gore, visible wound, photorealistic, 3d render, cartoon, camera movement, pan, tilt, necklace, chain, ring, earrings, bracelet, any jewelry, splint on LEFT arm, black splint, missing splint, splint on hand only, gun in RIGHT hand
```

### s02_c3  (NEW, start +15.49 s)

- Narration cue: "His right arm was in the plaster splint I had built thirty minutes earlier, in bay fourteen, with my own two hands."
- Attach: KF s02 still as start frame; REF-NICO (approved face); optional: last frame of s02_c2 as start frame if Flow allows, else rely on KF
- Cut in: Pistol pointed at floor in LEFT hand, grip settled  |  Cut out: Eyes lifting to the lens (feeds s03 reused clip)
- Risk: splint side, finger twitch
- **Prompt** (857 chars):

```
Painterly gouache-and-oil illustrated realism, cinematic noir, visible brush texture, film grain, 16:9. St. Brigid's hospital garage level 2, concrete pillars, dark stairwell door, orange sodium lights, cold rain, wet reflective concrete. Nico: 34, dark wavy hair, stubble, gray eyes, thin white scar through LEFT eyebrow, ruined charcoal suit, white plaster splint on RIGHT forearm, fingertips to below elbow held against his chest, fingertips visible at the end of the plaster. Start: medium close on the splinted RIGHT forearm against his chest, plaster fingertips poking out. He breathes, the fingertips twitch slightly, he winces. He then lifts his gray eyes up and toward the camera. End: eyes meeting the lens, calm and tired. Camera: medium close, locked off. Silent, mouths relaxed. No zoom, cuts or morphing; faces and outfits match the reference.
```

- **Negative:**

```
text, subtitles, watermark, logo, zoom, push-in, camera shake, morphing, face drift, changed outfit, extra fingers, fused fingers, deformed hands, extra limbs, duplicate people, speaking, lip sync, talking mouth, blood, gore, visible wound, photorealistic, 3d render, cartoon, camera movement, pan, tilt, necklace, chain, ring, earrings, bracelet, any jewelry, splint on LEFT arm, black splint, missing splint, splint on hand only, gun in RIGHT hand
```


## s03 (CH00, narration 5.26 s) - 1 clip(s)

**Timing / bridge:** Approved clip, trim to 5.26 s. Check scar on LEFT eyebrow; if it is mirrored, flip or regenerate.

### s03_c1  (REUSE, start +0.0 s)

- Narration cue: "Go back inside, Dr. Marlowe. You were never here." (Lion)
- Attach: Approved clip "Man turning head in garage"
- Cut out: Nico looking into the lens, calm and tired  |  Risk: REUSE; check scar is on LEFT eyebrow


## s04 (CH00, narration 21.0 s) - 2 clip(s)

**Timing / bridge:** Gap 8-13 s: bridge with a painted still (wet floor reflections, drifting rain, 3% slow drift) or a held first frame of c2. Do not stretch c1.

### s04_c1  (NEW, start +0.0 s)

- Narration cue: "I went back inside. Three days later I married him."
- Attach: KF s04 still as start frame; REF-IVY (approved face); REF-NICO (approved face)
- Cut in: keyframe pose  |  Cut out: Ivy at the doorway threshold, back to camera
- Risk: small faces at distance
- **Prompt** (865 chars):

```
Painterly gouache-and-oil illustrated realism, cinematic noir, visible brush texture, film grain, 16:9. St. Brigid's hospital garage level 2, concrete pillars, dark stairwell door, orange sodium lights, cold rain, wet reflective concrete. Ivy: 28, freckles, red messy bun with a pen through it, bare neck, bare hands, navy scrubs, small figure; Nico tiny and far behind her in orange light, charcoal suit, white plaster splint on RIGHT forearm, fingertips to below elbow. Start: Ivy stands between two concrete pillars, back to the camera, a phone charger cord in her fist, Nico far behind her. She turns her back on him fully and walks steadily toward the glass doorway, never looking back. End: she reaches the threshold of the doorway. Camera: wide high angle, locked off. Silent, mouths relaxed. No zoom, cuts or morphing; faces and outfits match the reference.
```

- **Negative:**

```
text, subtitles, watermark, logo, zoom, push-in, camera shake, morphing, face drift, changed outfit, extra fingers, fused fingers, deformed hands, extra limbs, duplicate people, speaking, lip sync, talking mouth, blood, gore, visible wound, photorealistic, 3d render, cartoon, camera movement, pan, tilt, necklace, chain, ring, earrings, bracelet, any jewelry, splint on LEFT arm, black splint, missing splint, splint on hand only
```

### s04_c2  (NEW, start +13.0 s)

- Narration cue: "...Stay to the end and you'll hear one sentence I swore to under oath..."
- Attach: KF s04 still as start frame; REF-IVY (approved face); REF-NICO (approved face); optional: last frame of s04_c1 as start frame if Flow allows, else rely on KF
- Cut in: Ivy at the doorway threshold, back to camera  |  Cut out: Door shut, Nico alone in the orange light
- Risk: door, tiny Nico
- **Prompt** (781 chars):

```
Painterly gouache-and-oil illustrated realism, cinematic noir, visible brush texture, film grain, 16:9. St. Brigid's hospital garage level 2, concrete pillars, dark stairwell door, orange sodium lights, cold rain, wet reflective concrete. Ivy: 28, freckles, red messy bun with a pen through it, bare neck, bare hands, navy scrubs; Nico small and far behind, white plaster splint on RIGHT forearm, fingertips to below elbow. Start: Ivy at the doorway. She steps through, the door swings closed behind her. In the distance Nico slowly turns his head to watch the door close, then stands alone in the orange light. End: door shut, Nico alone and still. Camera: same wide high angle, locked off. Silent, mouths relaxed. No zoom, cuts or morphing; faces and outfits match the reference.
```

- **Negative:**

```
text, subtitles, watermark, logo, zoom, push-in, camera shake, morphing, face drift, changed outfit, extra fingers, fused fingers, deformed hands, extra limbs, duplicate people, speaking, lip sync, talking mouth, blood, gore, visible wound, photorealistic, 3d render, cartoon, camera movement, pan, tilt, necklace, chain, ring, earrings, bracelet, any jewelry, splint on LEFT arm, black splint, missing splint, splint on hand only
```


## s07 (CH01, narration 40.07 s) - 2 clip(s)

**Timing / bridge:** c1 (approved) at 0-8 s (it may be 5 s). Gap 8-28 s: bridge with two painted stills (stitch close-up, steel tray with needle driver) with light camera drift, then c2. After c2 about 4 s of still before s08.

### s07_c1  (REUSE, start +0.0 s)

- Narration cue: "Bay fourteen. A clean cut across the inside of his right forearm. Gray eyes..."
- Attach: Approved hospital bandage clip
- Cut out: Ivy lifts her eyes from the bandage toward Nico; Nico's gray eyes turn to her  |  Risk: REUSE; check RIGHT arm and LEFT-eyebrow scar

### s07_c2  (NEW, start +28.0 s)

- Narration cue: "At 3:20 I put one stitch into the tendon itself and eleven in the skin. Twice his eyes went to the clock..."
- Attach: KF s07 still as start frame; REF-IVY (approved face); REF-NICO (approved face); optional: last frame of s07_c1 as start frame if Flow allows, else rely on KF
- Cut in: Ivy lifts her eyes from the bandage toward Nico; Nico's gray eyes turn to her  |  Cut out: Nico's eyes on Ivy's bowed head
- Risk: gloved hands, clock face
- **Prompt** (837 chars):

```
Painterly gouache-and-oil illustrated realism, cinematic noir, visible brush texture, film grain, 16:9. St. Brigid's ER bay 14, curtain, steel tray, cold buzzing fluorescent light. Ivy: 28, freckles, red messy bun with a pen through it (gloves on, navy scrubs, no ring, no chain); Nico: 34, dark wavy hair, stubble, gray eyes, thin white scar through LEFT eyebrow, his bare RIGHT forearm with a long closed row of stitches lies on the tray, no splint yet. Start: Ivy's gloved hands rest on a gauze pad on his forearm. Nico's gray eyes follow her hands, flick up to a round wall clock, hold, then return to her face. Ivy keeps her head bowed and smooths the tape once. End: his eyes on her face. Camera: close two-shot over the forearm, locked off. Silent, mouths relaxed. No zoom, cuts or morphing; faces and outfits match the reference.
```

- **Negative:**

```
text, subtitles, watermark, logo, zoom, push-in, camera shake, morphing, face drift, changed outfit, extra fingers, fused fingers, deformed hands, extra limbs, duplicate people, speaking, lip sync, talking mouth, blood, gore, visible wound, photorealistic, 3d render, cartoon, camera movement, pan, tilt, necklace, chain, ring, earrings, bracelet, any jewelry, splint, cast, splint on LEFT arm
```


## s09 (CH02, narration 17.91 s) - 2 clip(s)

**Timing / bridge:** 2 clips = 16 s vs 17.91 s: c1 at 0-8, c2 at 9.91-17.91; 1.9 s gap, hold the c1 end frame or cut to a rain-on-concrete insert still.

### s09_c1  (NEW, start +0.0 s)

- Narration cue: "At 4:10, two shots went off, so close together they sounded like one word. I counted."
- Attach: KF s09 still as start frame; REF-IVY (approved face)
- Cut in: keyframe pose  |  Cut out: Ivy crouched behind the bumper, eyes wide
- Risk: crouch pose, charger cord
- **Prompt** (794 chars):

```
Painterly gouache-and-oil illustrated realism, cinematic noir, visible brush texture, film grain, 16:9. St. Brigid's hospital garage level 2, concrete pillars, dark stairwell door, orange sodium lights, cold rain, wet reflective concrete. Ivy: 28, freckles, red messy bun with a pen through it, bare neck, bare hands, navy scrubs, charger cord in her fist; her hatchback beside her. Start: Ivy standing at her hatchback's driver door holding a phone charger. She flinches, drops into a crouch behind the car, charger still in her fist, other arm over her head, eyes shut, then eyes open. End: crouched small behind the bumper, eyes wide. Camera: low, locked off, from behind a parked car, Ivy in profile. Silent, mouths relaxed. No zoom, cuts or morphing; faces and outfits match the reference.
```

- **Negative:**

```
text, subtitles, watermark, logo, zoom, push-in, camera shake, morphing, face drift, changed outfit, extra fingers, fused fingers, deformed hands, extra limbs, duplicate people, speaking, lip sync, talking mouth, blood, gore, visible wound, photorealistic, 3d render, cartoon, camera movement, pan, tilt, necklace, chain, ring, earrings, bracelet, any jewelry
```

### s09_c2  (NEW, start +9.91 s)

- Narration cue: "Footsteps. Something heavy hitting a car door. At nine, I looked."
- Attach: KF s09 still as start frame; REF-IVY (approved face); optional: last frame of s09_c1 as start frame if Flow allows, else rely on KF
- Cut in: Ivy crouched behind the bumper, eyes wide  |  Cut out: Ivy's eyes just above the hood line, looking ahead
- Risk: hand placement
- **Prompt** (703 chars):

```
Painterly gouache-and-oil illustrated realism, cinematic noir, visible brush texture, film grain, 16:9. St. Brigid's hospital garage level 2, concrete pillars, dark stairwell door, orange sodium lights, cold rain, wet reflective concrete. Ivy: 28, freckles, red messy bun with a pen through it, bare neck, bare hands, navy scrubs, both hands on the wet bumper. Start: Ivy crouched, fingers pale on the wet metal. She slowly raises her head over the hood until her eyes clear the edge, breathing fast, staring ahead. End: eyes just above the hood, looking toward the stairwell. Camera: low, locked off, same angle. Silent, mouths relaxed. No zoom, cuts or morphing; faces and outfits match the reference.
```

- **Negative:**

```
text, subtitles, watermark, logo, zoom, push-in, camera shake, morphing, face drift, changed outfit, extra fingers, fused fingers, deformed hands, extra limbs, duplicate people, speaking, lip sync, talking mouth, blood, gore, visible wound, photorealistic, 3d render, cartoon, camera movement, pan, tilt, necklace, chain, ring, earrings, bracelet, any jewelry
```


## s10 (CH02, narration 27.74 s) - 2 clip(s)

**Timing / bridge:** Gaps 0-8 and 16-19.7 s: bridge with the s09 c2 final frame as a still and an insert of the fallen man's boots (still).

### s10_c1  (NEW, start +8.0 s)

- Narration cue: "I stood up and went toward him with my hands out, my brain a full step behind, screaming."
- Attach: KF s10 still as start frame; REF-IVY (approved face); REF-NICO (approved face)
- Cut in: keyframe pose  |  Cut out: Ivy mid-stride with hands out, eyes on the fallen man
- Risk: hands, walking
- **Prompt** (796 chars):

```
Painterly gouache-and-oil illustrated realism, cinematic noir, visible brush texture, film grain, 16:9. St. Brigid's hospital garage level 2, concrete pillars, dark stairwell door, orange sodium lights, cold rain, wet reflective concrete. Ivy: 28, freckles, red messy bun with a pen through it, bare neck, bare hands, navy scrubs; the fallen man in a dark coat on the floor far ahead, face turned away, nothing graphic. Start: Ivy crouched behind the hatchback. She stands and steps out around the car with both empty hands held out in front, palms down, then stops mid-stride. End: Ivy mid-step, hands out, eyes on the fallen man. Camera: medium wide over Ivy's shoulder from her hiding place, locked off. Silent, mouths relaxed. No zoom, cuts or morphing; faces and outfits match the reference.
```

- **Negative:**

```
text, subtitles, watermark, logo, zoom, push-in, camera shake, morphing, face drift, changed outfit, extra fingers, fused fingers, deformed hands, extra limbs, duplicate people, speaking, lip sync, talking mouth, blood, gore, visible wound, photorealistic, 3d render, cartoon, camera movement, pan, tilt, necklace, chain, ring, earrings, bracelet, any jewelry
```

### s10_c2  (NEW, start +19.74 s)

- Narration cue: "He's gone, Dottoressa. Go." (Lion)
- Attach: KF s10 still as start frame; REF-IVY (approved face); REF-NICO (approved face); optional: last frame of s10_c1 as start frame if Flow allows, else rely on KF
- Cut in: Ivy mid-stride with hands out, eyes on the fallen man  |  Cut out: Nico between Ivy and the fallen man
- Risk: LEFT-hand gun, splint side
- **Prompt** (868 chars):

```
Painterly gouache-and-oil illustrated realism, cinematic noir, visible brush texture, film grain, 16:9. St. Brigid's hospital garage level 2, concrete pillars, dark stairwell door, orange sodium lights, cold rain, wet reflective concrete. Ivy: 28, freckles, red messy bun with a pen through it, bare neck, bare hands, hands out; Nico: 34, dark wavy hair, stubble, gray eyes, thin white scar through LEFT eyebrow, charcoal suit, pistol in LEFT hand pointing at floor, white plaster splint on RIGHT forearm, fingertips to below elbow against his chest. Start: Ivy frozen mid-stride, hands out. Nico takes one pace to his left, putting himself between her and the fallen man, gaze on her, one slow head shake. Ivy halts. End: Nico blocking the way. Camera: medium wide, locked off. Silent, mouths relaxed. No zoom, cuts or morphing; faces and outfits match the reference.
```

- **Negative:**

```
text, subtitles, watermark, logo, zoom, push-in, camera shake, morphing, face drift, changed outfit, extra fingers, fused fingers, deformed hands, extra limbs, duplicate people, speaking, lip sync, talking mouth, blood, gore, visible wound, photorealistic, 3d render, cartoon, camera movement, pan, tilt, necklace, chain, ring, earrings, bracelet, any jewelry, splint on LEFT arm, black splint, missing splint, splint on hand only, gun in RIGHT hand
```


## s11 (CH02, narration 25.8 s) - 2 clip(s)

**Timing / bridge:** Gaps 0-4, 12-14, 22-25.8 s: bridge with s10 c2 end frame and a stairwell-door still.

### s11_c1  (NEW, start +4.0 s)

- Narration cue: "Behind him, in the stairwell, feet were going down fast. Then they stopped."
- Attach: KF s11 still as start frame; REF-IVY (approved face)
- Cut in: keyframe pose  |  Cut out: Eyes forward, jaw set
- Risk: face drift
- **Prompt** (742 chars):

```
Painterly gouache-and-oil illustrated realism, cinematic noir, visible brush texture, film grain, 16:9. St. Brigid's hospital garage level 2, concrete pillars, dark stairwell door, orange sodium lights, cold rain, wet reflective concrete. Ivy: 28, freckles, red messy bun with a pen through it, bare neck, bare hands, navy scrubs, orange light on her face, a stairwell door soft in the background. Start: tight close-up of Ivy frozen, empty hands raised at the edge of frame. Her eyes flick to the stairwell door behind her, hold, her breath comes shallow, then eyes return forward. End: eyes fixed forward, jaw set. Camera: tight close-up, locked off. Silent, mouths relaxed. No zoom, cuts or morphing; faces and outfits match the reference.
```

- **Negative:**

```
text, subtitles, watermark, logo, zoom, push-in, camera shake, morphing, face drift, changed outfit, extra fingers, fused fingers, deformed hands, extra limbs, duplicate people, speaking, lip sync, talking mouth, blood, gore, visible wound, photorealistic, 3d render, cartoon, camera movement, pan, tilt, necklace, chain, ring, earrings, bracelet, any jewelry
```

### s11_c2  (NEW, start +14.0 s)

- Narration cue: "I counted his breaths. Seven. Eight. Nine. Ten... I was fourteen."
- Attach: KF s11 still as start frame; REF-IVY (approved face); optional: last frame of s11_c1 as start frame if Flow allows, else rely on KF
- Cut in: Eyes forward, jaw set  |  Cut out: Eyes lowered and wet, tears not falling
- Risk: tears may fall: reject if they do
- **Prompt** (663 chars):

```
Painterly gouache-and-oil illustrated realism, cinematic noir, visible brush texture, film grain, 16:9. St. Brigid's hospital garage level 2, concrete pillars, dark stairwell door, orange sodium lights, cold rain, wet reflective concrete. Ivy: 28, freckles, red messy bun with a pen through it, bare neck, bare hands, navy scrubs, orange light on her face. Start: same close-up. She counts silently: her gaze slowly lowers, eyes glassy, one slow blink, jaw tight, lips pressed. Tears gather but do not fall. End: eyes lowered, wet, held. Camera: tight close-up, locked off. Silent, mouths relaxed. No zoom, cuts or morphing; faces and outfits match the reference.
```

- **Negative:**

```
text, subtitles, watermark, logo, zoom, push-in, camera shake, morphing, face drift, changed outfit, extra fingers, fused fingers, deformed hands, extra limbs, duplicate people, speaking, lip sync, talking mouth, blood, gore, visible wound, photorealistic, 3d render, cartoon, camera movement, pan, tilt, necklace, chain, ring, earrings, bracelet, any jewelry
```


## s16 (CH04, narration 30.21 s) - 3 clip(s)

**Timing / bridge:** 3 clips = 24 s over 30.21 s. Gaps 0-2, 10-11 and 19-21.5 s: hold previous end frames for 1-2 s; the last 6 s after c3 is a painted still of the card on the chair arm.

### s16_c1  (NEW, start +2.0 s)

- Narration cue: "Marry me. A wife can't be forced to testify against her husband." (Lion)
- Attach: KF s16 still as start frame; REF-IVY (approved face); REF-NICO (approved face)
- Cut in: keyframe pose  |  Cut out: Nico and Ivy facing each other, Ivy's head still
- Risk: two faces, splint side
- **Prompt** (886 chars):

```
Painterly gouache-and-oil illustrated realism, cinematic noir, visible brush texture, film grain, 16:9. Ivy's Bay Ridge walk-up living room at night, radiator, mother's armchair, window, dim lamp, R-train light flickering across both faces. Nico: 34, dark wavy hair, stubble, gray eyes, thin white scar through LEFT eyebrow, dark sweater, white plaster splint on RIGHT forearm, fingertips to below elbow at his waist, by the window; Ivy: 28, freckles, red messy bun with a pen through it, bare neck, bare hands, clothes as in keyframe. Start: Nico at the window, Ivy facing him, arms crossed. Nico turns to face her; Ivy's brows lift, she breathes out through her nose and slowly shakes her head. Train light flickers across both faces. End: facing each other. Camera: tight two-shot, locked off. Silent, mouths relaxed. No zoom, cuts or morphing; faces and outfits match the reference.
```

- **Negative:**

```
text, subtitles, watermark, logo, zoom, push-in, camera shake, morphing, face drift, changed outfit, extra fingers, fused fingers, deformed hands, extra limbs, duplicate people, speaking, lip sync, talking mouth, blood, gore, visible wound, photorealistic, 3d render, cartoon, camera movement, pan, tilt, necklace, chain, ring, earrings, bracelet, any jewelry, splint on LEFT arm, black splint, missing splint, splint on hand only
```

### s16_c2  (NEW, start +11.0 s)

- Narration cue: "I held up the subpoena. 'I'd rather testify.'"
- Attach: KF s16 still as start frame; REF-IVY (approved face); REF-NICO (approved face); optional: last frame of s16_c1 as start frame if Flow allows, else rely on KF
- Cut in: Nico and Ivy facing each other, Ivy's head still  |  Cut out: Subpoena held up, Nico reading
- Risk: paper shape, hands
- **Prompt** (758 chars):

```
Painterly gouache-and-oil illustrated realism, cinematic noir, visible brush texture, film grain, 16:9. Ivy's Bay Ridge walk-up living room at night, radiator, mother's armchair, window, dim lamp, R-train light flickering across both faces. Ivy: 28, freckles, red messy bun with a pen through it, bare neck, bare hands, everyday clothes; Nico dark sweater, white plaster splint on RIGHT forearm, fingertips to below elbow, partly in frame. Start: facing each other. Ivy raises the folded subpoena to eye level between them with one hand, steady; Nico's gray eyes move to the paper and read. End: subpoena held up, Nico's eyes on it. Camera: tight two-shot, locked off. Silent, mouths relaxed. No zoom, cuts or morphing; faces and outfits match the reference.
```

- **Negative:**

```
text, subtitles, watermark, logo, zoom, push-in, camera shake, morphing, face drift, changed outfit, extra fingers, fused fingers, deformed hands, extra limbs, duplicate people, speaking, lip sync, talking mouth, blood, gore, visible wound, photorealistic, 3d render, cartoon, camera movement, pan, tilt, necklace, chain, ring, earrings, bracelet, any jewelry, splint on LEFT arm, black splint, missing splint, splint on hand only
```

### s16_c3  (NEW, start +21.5 s)

- Narration cue: "He set a black card on the arm of my mother's chair... 'When, Dottoressa.'"
- Attach: KF s16 still as start frame; REF-IVY (approved face); REF-NICO (approved face); optional: last frame of s16_c2 as start frame if Flow allows, else rely on KF
- Cut in: Subpoena held up, Nico reading  |  Cut out: Black card on the armchair arm
- Risk: LEFT-hand rule, card has no text
- **Prompt** (848 chars):

```
Painterly gouache-and-oil illustrated realism, cinematic noir, visible brush texture, film grain, 16:9. Ivy's Bay Ridge walk-up living room at night, radiator, mother's armchair, window, dim lamp, R-train light flickering across both faces. Nico: 34, dark wavy hair, stubble, gray eyes, thin white scar through LEFT eyebrow, dark sweater, white plaster splint on RIGHT forearm, fingertips to below elbow, standing beside the armchair; Ivy: 28, freckles, red messy bun with a pen through it, bare neck, bare hands. Start: Nico's gaze on Ivy. His LEFT hand lays a plain black card on the arm of the armchair, fingers release it, hand withdraws. Ivy's eyes follow the card then lift to him. End: card lying on the chair arm. Camera: medium two-shot, locked off. Silent, mouths relaxed. No zoom, cuts or morphing; faces and outfits match the reference.
```

- **Negative:**

```
text, subtitles, watermark, logo, zoom, push-in, camera shake, morphing, face drift, changed outfit, extra fingers, fused fingers, deformed hands, extra limbs, duplicate people, speaking, lip sync, talking mouth, blood, gore, visible wound, photorealistic, 3d render, cartoon, camera movement, pan, tilt, necklace, chain, ring, earrings, bracelet, any jewelry, splint on LEFT arm, black splint, missing splint, splint on hand only
```


## s20 (CH05, narration 37.41 s) - 2 clip(s)

**Timing / bridge:** Gaps 9-16 and 24-37 s: bridge with painted stills (Lucia's cross close, old photographs on the wall, Tommy's face) with light drift.

### s20_c1  (NEW, start +1.0 s)

- Narration cue: "The door opened. A small woman in black... Every man stood, even Tommy."
- Attach: KF s20 still as start frame; REF-IVY (approved face); REF-NICO (approved face)
- Cut in: keyframe pose  |  Cut out: Everyone standing, Lucia in the doorway
- Risk: many bodies, chairs
- **Prompt** (840 chars):

```
Painterly gouache-and-oil illustrated realism, cinematic noir, visible brush texture, film grain, 16:9. Vescari's restaurant back room at night, dark wood, framed photos of men in hats, long table, warm low light. Lucia: small, black buttoned dress, gold cross, silver-streaked hair pulled tight, standing in the doorway. Men at the table: gray-haired lawyer with bow tie, buzz-cut Tommy. Ivy: 28, freckles, red messy bun with a pen through it, bare neck, bare hands, oversized gray cardigan. Start: men seated, Lucia still in the doorway. The lawyer, then Tommy, then Nico (splint RIGHT) push their chairs back and stand one after another; Ivy stands last. Lucia does not move. End: everyone standing. Camera: medium wide on the doorway, locked off. Silent, mouths relaxed. No zoom, cuts or morphing; faces and outfits match the reference.
```

- **Negative:**

```
text, subtitles, watermark, logo, zoom, push-in, camera shake, morphing, face drift, changed outfit, extra fingers, fused fingers, deformed hands, extra limbs, duplicate people, speaking, lip sync, talking mouth, blood, gore, visible wound, photorealistic, 3d render, cartoon, camera movement, pan, tilt, necklace, chain, ring, earrings, bracelet, any jewelry, splint on LEFT arm, black splint, missing splint, splint on hand only
```

### s20_c2  (NEW, start +16.0 s)

- Narration cue: "Her eyes went to her son's arm, my splint, and back to me."
- Attach: KF s20 still as start frame; REF-IVY (approved face); REF-NICO (approved face); optional: last frame of s20_c1 as start frame if Flow allows, else rely on KF
- Cut in: Everyone standing, Lucia in the doorway  |  Cut out: Lucia and Ivy facing each other
- Risk: face drift, 4 people
- **Prompt** (787 chars):

```
Painterly gouache-and-oil illustrated realism, cinematic noir, visible brush texture, film grain, 16:9. Vescari's restaurant back room at night, dark wood, framed photos of men in hats, long table, warm low light. Lucia: black dress, gold cross, silver hair; Nico white plaster splint on RIGHT forearm, fingertips to below elbow; Ivy: 28, freckles, red messy bun with a pen through it, bare neck, bare hands, gray cardigan sleeves over her hands. Start: everyone standing. Lucia's eyes travel to her son's splinted arm, then to Ivy. She takes one slow step into the room, chin high. Ivy holds her ground, hands in her sleeves. End: Lucia and Ivy facing each other. Camera: medium wide, locked off. Silent, mouths relaxed. No zoom, cuts or morphing; faces and outfits match the reference.
```

- **Negative:**

```
text, subtitles, watermark, logo, zoom, push-in, camera shake, morphing, face drift, changed outfit, extra fingers, fused fingers, deformed hands, extra limbs, duplicate people, speaking, lip sync, talking mouth, blood, gore, visible wound, photorealistic, 3d render, cartoon, camera movement, pan, tilt, necklace, chain, ring, earrings, bracelet, any jewelry, splint on LEFT arm, black splint, missing splint, splint on hand only
```


## s21 (CH06, narration 23.58 s) - 1 clip(s)

**Timing / bridge:** Single clip placed at 3-11 s; 11-23.6 s: Nico's face still and the portrait still.

### s21_c1  (NEW, start +3.0 s)

- Narration cue: "My thumb came in. My first finger came in. The other two stopped halfway..."
- Attach: KF s21 still as start frame; REF-NICO (approved face)
- Cut in: keyframe pose  |  Cut out: Hand open on the desk, two fingers half-curled
- Risk: finger anatomy: most likely to fail, expect re-rolls
- **Prompt** (851 chars):

```
Painterly gouache-and-oil illustrated realism, cinematic noir, visible brush texture, film grain, 16:9. Nico's study, dark green leather desk, desk lamp, father's portrait, single warm desk lamp, dark room. Nico: 34, dark wavy hair, stubble, gray eyes, thin white scar through LEFT eyebrow, dark sweater, white plaster splint on RIGHT forearm, fingertips to below elbow resting on the green leather desk, fingertips protruding from the plaster. Start: the splinted RIGHT hand lies on the desk. He tries to make a fist: only the thumb and first finger curl in; the other two stop halfway and tremble. His jaw tightens in pain. He gives up and lets the fingers lie still. End: hand open on the desk, fingers half-curled. Camera: close, locked off, desk lamp glow. Silent, mouths relaxed. No zoom, cuts or morphing; faces and outfits match the reference.
```

- **Negative:**

```
text, subtitles, watermark, logo, zoom, push-in, camera shake, morphing, face drift, changed outfit, extra fingers, fused fingers, deformed hands, extra limbs, duplicate people, speaking, lip sync, talking mouth, blood, gore, visible wound, photorealistic, 3d render, cartoon, camera movement, pan, tilt, necklace, chain, ring, earrings, bracelet, any jewelry, splint on LEFT arm, black splint, missing splint, splint on hand only
```


## s25 (CH07, narration 23.09 s) - 2 clip(s)

**Timing / bridge:** Gap 8-15 s: bridge with a still of the candy bowl and Priya's can; last 0 s: ends with c2.

### s25_c1  (NEW, start +0.0 s)

- Narration cue: "...unwrapping my third butterscotch... 'Blink twice if this is a hostage situation.'"
- Attach: KF s25 still as start frame; REF-IVY (approved face)
- Cut in: keyframe pose  |  Cut out: Ivy looking toward the chamber door
- Risk: candy wrapper hands, hidden lips
- **Prompt** (682 chars):

```
Painterly gouache-and-oil illustrated realism, cinematic noir, visible brush texture, film grain, 16:9. judge's wood-paneled chambers, candy bowl of butterscotch, morning daylight, soft daylight. Priya: tall, yellow sundress, jean jacket, energy drink can. Ivy: 28, freckles, red messy bun, navy dress, bare hands, bare neck. Start: Ivy unwrapping a butterscotch candy. Priya leans in and whispers behind her cupped hand, her lips hidden; Ivy's eyes slide sideways to her while her fingers keep twisting the wrapper. End: wrapper crumpled, Ivy looking at the door. Camera: medium, locked off. Silent, mouths relaxed. No zoom, cuts or morphing; faces and outfits match the reference.
```

- **Negative:**

```
text, subtitles, watermark, logo, zoom, push-in, camera shake, morphing, face drift, changed outfit, extra fingers, fused fingers, deformed hands, extra limbs, duplicate people, speaking, lip sync, talking mouth, blood, gore, visible wound, photorealistic, 3d render, cartoon, camera movement, pan, tilt, necklace, chain, ring, earrings, bracelet, any jewelry
```

### s25_c2  (NEW, start +15.09 s)

- Narration cue: "Theo wore a tie borrowed from Rocco that hung past his belt. I fixed his knot."
- Attach: KF s25 still as start frame; REF-IVY (approved face); optional: last frame of s25_c1 as start frame if Flow allows, else rely on KF
- Cut in: Ivy looking toward the chamber door  |  Cut out: Tie smooth, her hands falling away
- Risk: hands on tie
- **Prompt** (636 chars):

```
Painterly gouache-and-oil illustrated realism, cinematic noir, visible brush texture, film grain, 16:9. judge's wood-paneled chambers, candy bowl of butterscotch, morning daylight, soft daylight. Theo: thin, borrowed navy tie with gold anchors, far too long. Ivy: red messy bun, navy dress, bare hands, bare neck. Start: Ivy faces Theo. Her hands fix the knot of his too-long tie, tighten it, and smooth it flat against his shirt; Theo stands stiff, ears slightly red. End: tie smoothed, Ivy's hands lowering. Camera: medium two-shot, locked off. Silent, mouths relaxed. No zoom, cuts or morphing; faces and outfits match the reference.
```

- **Negative:**

```
text, subtitles, watermark, logo, zoom, push-in, camera shake, morphing, face drift, changed outfit, extra fingers, fused fingers, deformed hands, extra limbs, duplicate people, speaking, lip sync, talking mouth, blood, gore, visible wound, photorealistic, 3d render, cartoon, camera movement, pan, tilt, necklace, chain, ring, earrings, bracelet, any jewelry
```


## s27 (CH07, narration 30.73 s) - 3 clip(s)

**Timing / bridge:** 3 clips = 24 s over 30.73 s. Gaps 8-10 and 18-22.7 s: hold end frames; the steps crowd is a painted still.

### s27_c1  (NEW, start +0.0 s)

- Narration cue: "The ring was his grandmother's, a square emerald, far too big. It slid around my finger."
- Attach: KF s27 still as start frame; REF-IVY (approved face); REF-NICO (approved face)
- Cut in: keyframe pose  |  Cut out: Ring on Ivy's LEFT ring finger, stone upward
- Risk: HIGHEST: ring on correct finger, finger count
- **Prompt** (717 chars):

```
Painterly gouache-and-oil illustrated realism, cinematic noir, visible brush texture, film grain, 16:9. judge's chambers, then courthouse steps, daylight. Nico's LEFT hand and Ivy's LEFT hand, the right hand and edge of a white plaster splint just in view. A too-large square-cut cloudy deep-green emerald ring on a thin worn gold band, nothing else on either hand. Start: Nico's LEFT hand holds Ivy's LEFT hand, the ring at her fingertip. He slides the ring onto her ring finger; it goes on loose. Her other hand holds his wrist. End: ring on her LEFT ring finger, stone upward. Camera: extreme close on the hands, locked off. Silent, mouths relaxed. No zoom, cuts or morphing; faces and outfits match the reference.
```

- **Negative:**

```
text, subtitles, watermark, logo, zoom, push-in, camera shake, morphing, face drift, changed outfit, extra fingers, fused fingers, deformed hands, extra limbs, duplicate people, speaking, lip sync, talking mouth, blood, gore, visible wound, photorealistic, 3d render, cartoon, camera movement, pan, tilt, ring on a chain, necklace, pendant, earrings, bracelet, second ring, splint on LEFT arm, black splint, missing splint, splint on hand only
```

### s27_c2  (NEW, start +10.0 s)

- Narration cue: "'Rosa had big hands,' he said. 'She made bread.'"
- Attach: KF s27 still as start frame; REF-IVY (approved face); REF-NICO (approved face); optional: last frame of s27_c1 as start frame if Flow allows, else rely on KF
- Cut in: Ring on Ivy's LEFT ring finger, stone upward  |  Cut out: Hand loosely closed, ring turned to palm
- Risk: ring rotation, finger count
- **Prompt** (593 chars):

```
Painterly gouache-and-oil illustrated realism, cinematic noir, visible brush texture, film grain, 16:9. judge's chambers, then courthouse steps, daylight. Ivy's LEFT hand with the too-large square emerald ring on the ring finger, nothing else. Start: her hand is raised in front of her. The loose ring slowly rotates around her finger until the stone turns to her palm; her fingers curl closed around it to hold it still. End: loose fist, stone turned to the palm. Camera: close on the hand, locked off. Silent, mouths relaxed. No zoom, cuts or morphing; faces and outfits match the reference.
```

- **Negative:**

```
text, subtitles, watermark, logo, zoom, push-in, camera shake, morphing, face drift, changed outfit, extra fingers, fused fingers, deformed hands, extra limbs, duplicate people, speaking, lip sync, talking mouth, blood, gore, visible wound, photorealistic, 3d render, cartoon, camera movement, pan, tilt, ring on a chain, necklace, pendant, earrings, bracelet, second ring, splint on LEFT arm, black splint, missing splint, splint on hand only
```

### s27_c3  (NEW, start +22.73 s)

- Narration cue: "Nico kissed me, slow and warm, the plaster along my spine. It was for the cameras."
- Attach: KF s27 still as start frame; REF-IVY (approved face); REF-NICO (approved face); optional: last frame of s27_c2 as start frame if Flow allows, else rely on KF
- Cut in: Hand loosely closed, ring turned to palm  |  Cut out: Faces inches apart, Ivy annoyed
- Risk: two faces, kiss, splint side
- **Prompt** (812 chars):

```
Painterly gouache-and-oil illustrated realism, cinematic noir, visible brush texture, film grain, 16:9. judge's chambers, then courthouse steps, daylight. Nico: 34, dark wavy hair, stubble, gray eyes, thin white scar through LEFT eyebrow, dark suit, white plaster splint on RIGHT forearm, fingertips to below elbow; Ivy: 28, freckles, red messy bun, navy dress; emerald ring on her LEFT hand; reporters' camera flashes. Start: on the courthouse steps, Nico turns Ivy to him with his LEFT hand at her waist, the splinted arm along her back, and kisses her slowly while camera flashes pop around them; her eyes stay open. They part; her eyes narrow, annoyed. End: faces inches apart. Camera: medium on the steps, locked off. Silent, mouths relaxed. No zoom, cuts or morphing; faces and outfits match the reference.
```

- **Negative:**

```
text, subtitles, watermark, logo, zoom, push-in, camera shake, morphing, face drift, changed outfit, extra fingers, fused fingers, deformed hands, extra limbs, duplicate people, speaking, lip sync, talking mouth, blood, gore, visible wound, photorealistic, 3d render, cartoon, camera movement, pan, tilt, ring on a chain, necklace, pendant, earrings, bracelet, second ring, splint on LEFT arm, black splint, missing splint, splint on hand only
```


## s33 (CH08, narration 19.26 s) - 2 clip(s)

**Timing / bridge:** 2 clips = 16 s over 19.26 s. Gap 8-11.26 s: hold the c1 end frame.

### s33_c1  (NEW, start +0.0 s)

- Narration cue: "he pulled the pen out of my hair with his left hand."
- Attach: KF s33 still as start frame; REF-IVY (approved face); REF-NICO (approved face)
- Cut in: keyframe pose  |  Cut out: Ivy's hair loose, pen in Nico's LEFT hand
- Risk: pen, hair, LEFT hand
- **Prompt** (880 chars):

```
Painterly gouache-and-oil illustrated realism, cinematic noir, visible brush texture, film grain, 16:9. Ivy's third-floor bedroom beside a connecting door with a brass bolt on her side, warm low lamp. Nico: 34, dark wavy hair, stubble, gray eyes, thin white scar through LEFT eyebrow, dark sweater, black plastic splint on RIGHT forearm, three velcro straps, small white cross on wrist strap; Ivy: 28, freckles, red messy bun with a pen through it, square emerald ring (too big) on LEFT ring finger, nothing at neck, cardigan. Start: Ivy leans against his chest, shoulders trembling. Nico's LEFT hand rises behind her head and slides the pen out of her bun; red hair falls to her shoulders. End: pen in his LEFT hand, her hair loose. Camera: medium two-shot, locked off, brass bolt visible. Silent, mouths relaxed. No zoom, cuts or morphing; faces and outfits match the reference.
```

- **Negative:**

```
text, subtitles, watermark, logo, zoom, push-in, camera shake, morphing, face drift, changed outfit, extra fingers, fused fingers, deformed hands, extra limbs, duplicate people, speaking, lip sync, talking mouth, blood, gore, visible wound, photorealistic, 3d render, cartoon, camera movement, pan, tilt, ring on a chain, necklace, pendant, earrings, bracelet, second ring, splint on LEFT arm, white plaster splint, missing splint
```

### s33_c2  (NEW, start +11.26 s)

- Narration cue: "I kissed him. He kissed me back. I stopped. 'That one wasn't for anyone.'"
- Attach: KF s33 still as start frame; REF-IVY (approved face); REF-NICO (approved face); optional: last frame of s33_c1 as start frame if Flow allows, else rely on KF
- Cut in: Ivy's hair loose, pen in Nico's LEFT hand  |  Cut out: Foreheads nearly touching, Ivy's hand on his chest
- Risk: face drift in kiss
- **Prompt** (796 chars):

```
Painterly gouache-and-oil illustrated realism, cinematic noir, visible brush texture, film grain, 16:9. Ivy's third-floor bedroom beside a connecting door with a brass bolt on her side, warm low lamp. Nico: 34, dark wavy hair, stubble, gray eyes, thin white scar through LEFT eyebrow, dark sweater, black plastic splint on RIGHT forearm, three velcro straps, small white cross on wrist strap; Ivy with loose red hair, emerald ring on her LEFT finger. Start: faces close. Ivy rises on her toes and kisses him with closed lips, then draws back and opens her eyes, her hand flat on his chest. Nico stays still. Closed-door scene, kiss only. End: foreheads nearly touching. Camera: medium two-shot, locked off. Silent, mouths relaxed. No zoom, cuts or morphing; faces and outfits match the reference.
```

- **Negative:**

```
text, subtitles, watermark, logo, zoom, push-in, camera shake, morphing, face drift, changed outfit, extra fingers, fused fingers, deformed hands, extra limbs, duplicate people, speaking, lip sync, talking mouth, blood, gore, visible wound, photorealistic, 3d render, cartoon, camera movement, pan, tilt, ring on a chain, necklace, pendant, earrings, bracelet, second ring, splint on LEFT arm, white plaster splint, missing splint
```


## s34 (CH08, narration 47.19 s) - 2 clip(s)

**Timing / bridge:** Large gaps (11-22 s, 30-47 s): bridge with painted stills: Bell's phone lock screen note, the Volvo's driver window, Priya's missed-call phone.

### s34_c1  (NEW, start +3.0 s)

- Narration cue: "At 6:41 Friday morning, Priya called. Dr. Bell was dead in his Volvo..."
- Attach: KF s34 still as start frame; REF-IVY (approved face)
- Cut in: keyframe pose  |  Cut out: Ivy and Reyes standing at the tape
- Risk: walking, tape
- **Prompt** (777 chars):

```
Painterly gouache-and-oil illustrated realism, cinematic noir, visible brush texture, film grain, 16:9. St. Brigid's hospital garage level 2, concrete pillars, dark stairwell door, Friday dawn, yellow police tape around a silver Volvo, pale gray dawn, last orange lights, wet concrete. Ivy: 28, freckles, red messy bun with a pen through it, thin gold chain hidden under her top, no ring visible, navy scrubs; Reyes: rain jacket, dark hair. Start: Ivy walks into frame from the left toward the yellow tape around the silver Volvo and stops. Her arms fall to her sides. Reyes beside her turns her head to Ivy. Wind stirs the tape. End: both standing at the tape. Camera: wide, locked off. Silent, mouths relaxed. No zoom, cuts or morphing; faces and outfits match the reference.
```

- **Negative:**

```
text, subtitles, watermark, logo, zoom, push-in, camera shake, morphing, face drift, changed outfit, extra fingers, fused fingers, deformed hands, extra limbs, duplicate people, speaking, lip sync, talking mouth, blood, gore, visible wound, photorealistic, 3d render, cartoon, camera movement, pan, tilt, visible necklace, visible pendant, ring on finger, earrings, bracelet
```

### s34_c2  (NEW, start +22.0 s)

- Narration cue: "The note was a lie, and whoever wrote it..."
- Attach: KF s34 still as start frame; REF-IVY (approved face); optional: last frame of s34_c1 as start frame if Flow allows, else rely on KF
- Cut in: Ivy and Reyes standing at the tape  |  Cut out: Ivy arms folded, eyes on the Volvo
- Risk: mild
- **Prompt** (758 chars):

```
Painterly gouache-and-oil illustrated realism, cinematic noir, visible brush texture, film grain, 16:9. St. Brigid's hospital garage level 2, concrete pillars, dark stairwell door, Friday dawn, yellow police tape around a silver Volvo, pale gray dawn, last orange lights, wet concrete. Ivy: 28, freckles, red messy bun with a pen through it, thin gold chain hidden under her top, no ring visible, navy scrubs; Reyes in rain jacket. Start: Ivy staring at the Volvo. She slowly shakes her head, then folds her arms tight across her chest and steps back half a pace. Reyes watches her sideways. End: Ivy arms folded, eyes on the car. Camera: wide, locked off, same angle. Silent, mouths relaxed. No zoom, cuts or morphing; faces and outfits match the reference.
```

- **Negative:**

```
text, subtitles, watermark, logo, zoom, push-in, camera shake, morphing, face drift, changed outfit, extra fingers, fused fingers, deformed hands, extra limbs, duplicate people, speaking, lip sync, talking mouth, blood, gore, visible wound, photorealistic, 3d render, cartoon, camera movement, pan, tilt, visible necklace, visible pendant, ring on finger, earrings, bracelet
```


## s36 (CH09, narration 45.35 s) - 2 clip(s)

**Timing / bridge:** Gaps 8-12 s and 20-45 s: the garage flashback in the narration is covered by s37 clips and stills.

### s36_c1  (NEW, start +0.0 s)

- Narration cue: "In the ER, Enzo grabbed my sleeve and told me... 'I shot him.'"
- Attach: KF s36 still as start frame; REF-IVY (approved face)
- Cut in: keyframe pose  |  Cut out: Enzo's grip tight on Ivy's sleeve
- Risk: hand grip, finger count
- **Prompt** (698 chars):

```
Painterly gouache-and-oil illustrated realism, cinematic noir, visible brush texture, film grain, 16:9. St. Brigid's ER bay, hospital bed, cold buzzing fluorescent light. Enzo: 21, gold curls flat with sweat, pale, oxygen cannula, hospital gown. Ivy: 28, freckles, red messy bun with a pen through it, thin gold chain hidden under her top, no ring visible, navy scrubs with a cardigan. Start: Enzo lying in the bed. His hand reaches up and grips Ivy's sleeve; she leans close; his eyes stay locked on hers, frightened, lips pressed. End: knuckles white on her sleeve. Camera: close, hospital bed, locked off. Silent, mouths relaxed. No zoom, cuts or morphing; faces and outfits match the reference.
```

- **Negative:**

```
text, subtitles, watermark, logo, zoom, push-in, camera shake, morphing, face drift, changed outfit, extra fingers, fused fingers, deformed hands, extra limbs, duplicate people, speaking, lip sync, talking mouth, blood, gore, visible wound, photorealistic, 3d render, cartoon, camera movement, pan, tilt, visible necklace, visible pendant, ring on finger, earrings, bracelet
```

### s36_c2  (NEW, start +12.0 s)

- Narration cue: "Nico took the gun out of his hand and told him to go."
- Attach: KF s36 still as start frame; REF-IVY (approved face); optional: last frame of s36_c1 as start frame if Flow allows, else rely on KF
- Cut in: Enzo's grip tight on Ivy's sleeve  |  Cut out: Ivy's hand resting on Enzo's, eyes closed
- Risk: hand overlap
- **Prompt** (683 chars):

```
Painterly gouache-and-oil illustrated realism, cinematic noir, visible brush texture, film grain, 16:9. St. Brigid's ER bay, hospital bed, cold buzzing fluorescent light. Enzo: gold curls, cannula, gown. Ivy: 28, freckles, red messy bun with a pen through it, thin gold chain hidden under her top, no ring visible, navy scrubs with a cardigan. Start: grip on her sleeve. Ivy lays her free hand over his and gently loosens his fingers; Enzo closes his eyes, turns his face to the ceiling, and a tear runs down to his temple. End: eyes closed, her hand resting on his. Camera: close, locked off. Silent, mouths relaxed. No zoom, cuts or morphing; faces and outfits match the reference.
```

- **Negative:**

```
text, subtitles, watermark, logo, zoom, push-in, camera shake, morphing, face drift, changed outfit, extra fingers, fused fingers, deformed hands, extra limbs, duplicate people, speaking, lip sync, talking mouth, blood, gore, visible wound, photorealistic, 3d render, cartoon, camera movement, pan, tilt, visible necklace, visible pendant, ring on finger, earrings, bracelet
```


## s37 (CH09, narration 49.81 s) - 3 clip(s)

**Timing / bridge:** Gaps are large (8-11, 19-33, 41-49.8 s); the two shots are NOT shown. Cover with stills: sedan, stairwell door, Enzo's shoes, then Ivy coming around the car (still).

### s37_c1  (NEW, start +0.0 s)

- Narration cue: "Frankie called me at two minutes past four. By the stairs, where the lights are out."
- Attach: KF s37 still as start frame; REF-NICO (approved face)
- Cut in: keyframe pose  |  Cut out: Nico stopped, head turned toward the silver sedan
- Risk: walking, splint side
- **Prompt** (853 chars):

```
Painterly gouache-and-oil illustrated realism, cinematic noir, visible brush texture, film grain, 16:9. St. Brigid's hospital garage level 2, concrete pillars, dark stairwell door, lights out above the stairs, silver sedan near the stairwell, dark ramp, a few orange lights, cold rain, wet concrete. Nico: 34, dark wavy hair, stubble, gray eyes, thin white scar through LEFT eyebrow, ruined charcoal suit, white plaster splint on RIGHT forearm, fingertips to below elbow against his chest, LEFT hand empty. Start: wide from Nico's side, a dark ramp. Nico walks slowly up the ramp toward a silver sedan near the stairwell, wet floor reflecting, his LEFT hand empty. He stops and turns his head toward the sedan. End: stopped, head turned. Camera: wide, locked off. Silent, mouths relaxed. No zoom, cuts or morphing; faces and outfits match the reference.
```

- **Negative:**

```
text, subtitles, watermark, logo, zoom, push-in, camera shake, morphing, face drift, changed outfit, extra fingers, fused fingers, deformed hands, extra limbs, duplicate people, speaking, lip sync, talking mouth, blood, gore, visible wound, photorealistic, 3d render, cartoon, camera movement, pan, tilt, necklace, chain, ring, earrings, bracelet, any jewelry, splint on LEFT arm, black splint, missing splint, splint on hand only
```

### s37_c2  (NEW, start +11.0 s)

- Narration cue: "He was crouched behind a silver sedan, crying, a gun in his hand that he did not raise."
- Attach: KF s37 still as start frame; REF-NICO (approved face); optional: last frame of s37_c1 as start frame if Flow allows, else rely on KF
- Cut in: Nico stopped, head turned toward the silver sedan  |  Cut out: Frankie looking up at the dark stairwell
- Risk: gun must not rise
- **Prompt** (775 chars):

```
Painterly gouache-and-oil illustrated realism, cinematic noir, visible brush texture, film grain, 16:9. St. Brigid's hospital garage level 2, concrete pillars, dark stairwell door, lights out above the stairs, silver sedan near the stairwell, dark ramp, a few orange lights, cold rain, wet concrete. Frankie: 44, good dark coat, crouched behind a silver sedan, face partly turned away or in shadow, a pistol hanging loose in his hand, not raised, nothing graphic. Start: Frankie crouched, shoulders shaking, crying. His head snaps toward the dark stairwell above; the loose gun stays low at his knee. End: Frankie looking up at the stairwell, gun still low. Camera: medium, locked off. Silent, mouths relaxed. No zoom, cuts or morphing; faces and outfits match the reference.
```

- **Negative:**

```
text, subtitles, watermark, logo, zoom, push-in, camera shake, morphing, face drift, changed outfit, extra fingers, fused fingers, deformed hands, extra limbs, duplicate people, speaking, lip sync, talking mouth, blood, gore, visible wound, photorealistic, 3d render, cartoon, camera movement, pan, tilt, necklace, chain, ring, earrings, bracelet, any jewelry
```

### s37_c3  (NEW, start +33.0 s)

- Narration cue: "I took it from him with the wrong hand. I said, Go, Enzo. Go."
- Attach: KF s37 still as start frame; REF-NICO (approved face); optional: last frame of s37_c2 as start frame if Flow allows, else rely on KF
- Cut in: Frankie looking up at the dark stairwell  |  Cut out: Nico holding the gun low in his LEFT hand, Enzo backing away
- Risk: gun handoff, LEFT hand
- **Prompt** (883 chars):

```
Painterly gouache-and-oil illustrated realism, cinematic noir, visible brush texture, film grain, 16:9. St. Brigid's hospital garage level 2, concrete pillars, dark stairwell door, lights out above the stairs, silver sedan near the stairwell, dark ramp, a few orange lights, cold rain, wet concrete. Enzo: 21, gold curls, gray jacket, pistol hanging in hand. Nico: 34, dark wavy hair, stubble, gray eyes, thin white scar through LEFT eyebrow, white plaster splint on RIGHT forearm, fingertips to below elbow. Start: Enzo at the foot of the stairwell, pistol hanging low, wide-eyed, shaking. Nico steps in from the left and takes the pistol from Enzo's hand with his LEFT hand, muzzle to the floor. Enzo backs away. End: Nico holds the gun low in his LEFT hand. Camera: medium wide, locked off. Silent, mouths relaxed. No zoom, cuts or morphing; faces and outfits match the reference.
```

- **Negative:**

```
text, subtitles, watermark, logo, zoom, push-in, camera shake, morphing, face drift, changed outfit, extra fingers, fused fingers, deformed hands, extra limbs, duplicate people, speaking, lip sync, talking mouth, blood, gore, visible wound, photorealistic, 3d render, cartoon, camera movement, pan, tilt, necklace, chain, ring, earrings, bracelet, any jewelry, splint on LEFT arm, black splint, missing splint, splint on hand only, gun in RIGHT hand
```


## s43 (CH12, narration 62.4 s) - 4 clip(s)

**Timing / bridge:** 4 clips = 32 s over 62.4 s. Gaps: bridge with stills (ledger page, rosary close, funeral-week page, Sal's portrait, Lincoln exterior). Do NOT loop clips.

### s43_c1  (NEW, start +4.0 s)

- Narration cue: "One-ten in the morning, in my uncle's garage... This time I opened the glove box."
- Attach: KF s43 still as start frame; REF-NICO (approved face)
- Cut in: keyframe pose  |  Cut out: Glove box open, Nico looking at the notebook
- Risk: latch, props
- **Prompt** (857 chars):

```
Painterly gouache-and-oil illustrated realism, cinematic noir, visible brush texture, film grain, 16:9. Sal's dim private garage, one bare bulb, old gray Lincoln Town Car, dim single bulb, cold concrete, breath fog. Nico: 34, dark wavy hair, stubble, gray eyes, thin white scar through LEFT eyebrow, dark sweater, black plastic splint on RIGHT forearm, three velcro straps, small white cross on wrist strap, alone, 1:10 a.m. Start: Nico beside the open passenger door of the gray Lincoln. His LEFT hand presses the glove box latch; the door drops open and a small light comes on, showing a black notebook with an elastic band, a tissue pack, a rosary, and candy wrappers. End: glove box open, his eyes on the notebook. Camera: medium, locked off, three-quarter angle. Silent, mouths relaxed. No zoom, cuts or morphing; faces and outfits match the reference.
```

- **Negative:**

```
text, subtitles, watermark, logo, zoom, push-in, camera shake, morphing, face drift, changed outfit, extra fingers, fused fingers, deformed hands, extra limbs, duplicate people, speaking, lip sync, talking mouth, blood, gore, visible wound, photorealistic, 3d render, cartoon, camera movement, pan, tilt, necklace, chain, ring, earrings, bracelet, any jewelry, splint on LEFT arm, white plaster splint, missing splint
```

### s43_c2  (NEW, start +16.0 s)

- Narration cue: "A black ledger, its band off with my teeth because I only had one hand."
- Attach: KF s43 still as start frame; REF-NICO (approved face); optional: last frame of s43_c1 as start frame if Flow allows, else rely on KF
- Cut in: Glove box open, Nico looking at the notebook  |  Cut out: Open notebook in LEFT hand
- Risk: band in teeth, page text
- **Prompt** (804 chars):

```
Painterly gouache-and-oil illustrated realism, cinematic noir, visible brush texture, film grain, 16:9. Sal's dim private garage, one bare bulb, old gray Lincoln Town Car, dim single bulb, cold concrete, breath fog. Nico: 34, dark wavy hair, stubble, gray eyes, thin white scar through LEFT eyebrow, dark sweater, black plastic splint on RIGHT forearm, three velcro straps, small white cross on wrist strap, only one usable hand. Start: his LEFT hand lifts the black notebook against the dashboard. He lowers his face, catches the elastic band in his teeth, pulls it off, and opens the cover to a page of blurred handwritten columns, no legible text. End: notebook open in his LEFT hand. Camera: close, locked off. Silent, mouths relaxed. No zoom, cuts or morphing; faces and outfits match the reference.
```

- **Negative:**

```
text, subtitles, watermark, logo, zoom, push-in, camera shake, morphing, face drift, changed outfit, extra fingers, fused fingers, deformed hands, extra limbs, duplicate people, speaking, lip sync, talking mouth, blood, gore, visible wound, photorealistic, 3d render, cartoon, camera movement, pan, tilt, necklace, chain, ring, earrings, bracelet, any jewelry, splint on LEFT arm, white plaster splint, missing splint
```

### s43_c3  (NEW, start +29.0 s)

- Narration cue: "In the trunk, a deli receipt for a prepaid phone, and a boy's tan jacket from a discount rack."
- Attach: KF s43 still as start frame; REF-NICO (approved face); optional: last frame of s43_c2 as start frame if Flow allows, else rely on KF
- Cut in: Open notebook in LEFT hand  |  Cut out: Tan jacket in LEFT hand
- Risk: small props
- **Prompt** (759 chars):

```
Painterly gouache-and-oil illustrated realism, cinematic noir, visible brush texture, film grain, 16:9. Sal's dim private garage, one bare bulb, old gray Lincoln Town Car, dim single bulb, cold concrete, breath fog. Nico: 34, dark wavy hair, stubble, gray eyes, thin white scar through LEFT eyebrow, dark sweater, black plastic splint on RIGHT forearm, three velcro straps, small white cross on wrist strap; a small tan jacket from a discount rack, a folded deli receipt. Start: at the open trunk. His LEFT hand lifts a small tan jacket and a folded receipt out of the trunk; he looks at them, jaw working. End: jacket held in his LEFT hand. Camera: medium, locked off. Silent, mouths relaxed. No zoom, cuts or morphing; faces and outfits match the reference.
```

- **Negative:**

```
text, subtitles, watermark, logo, zoom, push-in, camera shake, morphing, face drift, changed outfit, extra fingers, fused fingers, deformed hands, extra limbs, duplicate people, speaking, lip sync, talking mouth, blood, gore, visible wound, photorealistic, 3d render, cartoon, camera movement, pan, tilt, necklace, chain, ring, earrings, bracelet, any jewelry, splint on LEFT arm, white plaster splint, missing splint
```

### s43_c4  (NEW, start +50.0 s)

- Narration cue: "I would rather lose everything my father built than lose the way she looked at me when I didn't lie."
- Attach: KF s43 still as start frame; REF-NICO (approved face); optional: last frame of s43_c3 as start frame if Flow allows, else rely on KF
- Cut in: Tan jacket in LEFT hand  |  Cut out: LEFT hand resting on the closed trunk
- Risk: trunk lid
- **Prompt** (790 chars):

```
Painterly gouache-and-oil illustrated realism, cinematic noir, visible brush texture, film grain, 16:9. Sal's dim private garage, one bare bulb, old gray Lincoln Town Car, dim single bulb, cold concrete, breath fog. Nico: 34, dark wavy hair, stubble, gray eyes, thin white scar through LEFT eyebrow, dark sweater, black plastic splint on RIGHT forearm, three velcro straps, small white cross on wrist strap, at the trunk, jacket in his LEFT hand. Start: Nico lowers his head and closes his eyes for a beat, breath fogging. He lifts his head, lays the jacket in the trunk, and shuts the lid with his LEFT hand, resting the hand on it. End: hand resting on the closed trunk. Camera: medium, locked off. Silent, mouths relaxed. No zoom, cuts or morphing; faces and outfits match the reference.
```

- **Negative:**

```
text, subtitles, watermark, logo, zoom, push-in, camera shake, morphing, face drift, changed outfit, extra fingers, fused fingers, deformed hands, extra limbs, duplicate people, speaking, lip sync, talking mouth, blood, gore, visible wound, photorealistic, 3d render, cartoon, camera movement, pan, tilt, necklace, chain, ring, earrings, bracelet, any jewelry, splint on LEFT arm, white plaster splint, missing splint
```


## s44 (CH12, narration 37.34 s) - 2 clip(s)

**Timing / bridge:** Gaps 11-24 and 32-37 s: bridge with stills (the letter in her hands, the sunrise window).

### s44_c1  (NEW, start +3.0 s)

- Narration cue: "At dawn, Danny Bell let me read his father's last letter."
- Attach: KF s44 still as start frame; REF-IVY (approved face)
- Cut in: keyframe pose  |  Cut out: Ivy lowering the page, eyes lifting to Danny
- Risk: paper, reading eyes
- **Prompt** (712 chars):

```
Painterly gouache-and-oil illustrated realism, cinematic noir, visible brush texture, film grain, 16:9. Park Slope kitchen at dawn, narrow table, mugs, cold dawn window light. Ivy: 28, freckles, red messy bun with a pen through it, square emerald ring (too big) on LEFT ring finger, nothing at neck, gray cardigan; Danny: 17, thin, bald, no eyebrows, gray beanie, port scar at the collarbone. Start: Ivy and Danny at the table. Ivy unfolds a three-page letter and reads silently, her eyes tracking down the page; Danny watches her, hands wrapped around a mug. End: she lowers the page. Camera: medium two-shot, locked off. Silent, mouths relaxed. No zoom, cuts or morphing; faces and outfits match the reference.
```

- **Negative:**

```
text, subtitles, watermark, logo, zoom, push-in, camera shake, morphing, face drift, changed outfit, extra fingers, fused fingers, deformed hands, extra limbs, duplicate people, speaking, lip sync, talking mouth, blood, gore, visible wound, photorealistic, 3d render, cartoon, camera movement, pan, tilt, ring on a chain, necklace, pendant, earrings, bracelet, second ring
```

### s44_c2  (NEW, start +24.0 s)

- Narration cue: "The letter ended: Ivy, say it. Say all of it."
- Attach: KF s44 still as start frame; REF-IVY (approved face); optional: last frame of s44_c1 as start frame if Flow allows, else rely on KF
- Cut in: Ivy lowering the page, eyes lifting to Danny  |  Cut out: Ivy's hand on Danny's
- Risk: hand overlap
- **Prompt** (642 chars):

```
Painterly gouache-and-oil illustrated realism, cinematic noir, visible brush texture, film grain, 16:9. Park Slope kitchen at dawn, narrow table, mugs, cold dawn window light. Ivy: 28, freckles, red messy bun with a pen through it, square emerald ring (too big) on LEFT ring finger, nothing at neck, gray cardigan; Danny: bald, gray beanie, thin. Start: Danny wipes his eye with the back of his sleeve. Ivy reaches across the table and lays her LEFT hand over his; he looks at it, then at her. End: her hand on his. Camera: medium two-shot, locked off. Silent, mouths relaxed. No zoom, cuts or morphing; faces and outfits match the reference.
```

- **Negative:**

```
text, subtitles, watermark, logo, zoom, push-in, camera shake, morphing, face drift, changed outfit, extra fingers, fused fingers, deformed hands, extra limbs, duplicate people, speaking, lip sync, talking mouth, blood, gore, visible wound, photorealistic, 3d render, cartoon, camera movement, pan, tilt, ring on a chain, necklace, pendant, earrings, bracelet, second ring
```


## s46 (CH13, narration 38.64 s) - 2 clip(s)

**Timing / bridge:** Gaps 12-22 and 30-38.6 s: stills of Sal's hands, Lucia and Tommy standing, the lanterns.

### s46_c1  (NEW, start +4.0 s)

- Narration cue: "Sal looked at his hands, then at his nephew."
- Attach: KF s46 still as start frame; REF-NICO (approved face)
- Cut in: keyframe pose  |  Cut out: Sal and Nico, eyes locked
- Risk: two faces, wet eyes
- **Prompt** (831 chars):

```
Painterly gouache-and-oil illustrated realism, cinematic noir, visible brush texture, film grain, 16:9. Carroll Street garden at night, long table, paper lanterns, bare fig tree, black notebook on the cloth, dusk blue, warm lantern glow. Sal: silver hair, warm brown eyes, camel coat. Nico: 34, dark wavy hair, stubble, gray eyes, thin white scar through LEFT eyebrow, dark coat, black plastic splint on RIGHT forearm, three velcro straps, small white cross on wrist strap, left side of body to camera. Start: close two-shot over the notebook. Sal's warm brown eyes fill; he looks down at his own hands on the table, then lifts his eyes to Nico, who stays still, breathing. End: the two men's eyes locked. Camera: close two-shot, locked off. Silent, mouths relaxed. No zoom, cuts or morphing; faces and outfits match the reference.
```

- **Negative:**

```
text, subtitles, watermark, logo, zoom, push-in, camera shake, morphing, face drift, changed outfit, extra fingers, fused fingers, deformed hands, extra limbs, duplicate people, speaking, lip sync, talking mouth, blood, gore, visible wound, photorealistic, 3d render, cartoon, camera movement, pan, tilt, necklace, chain, ring, earrings, bracelet, any jewelry, splint on LEFT arm, white plaster splint, missing splint
```

### s46_c2  (NEW, start +22.0 s)

- Narration cue: "I put my phone on the tablecloth and called Agent Reyes on speaker."
- Attach: KF s46 still as start frame; REF-NICO (approved face); optional: last frame of s46_c1 as start frame if Flow allows, else rely on KF
- Cut in: Sal and Nico, eyes locked  |  Cut out: Phone on the cloth, screen lit
- Risk: phone screen has no legible text
- **Prompt** (686 chars):

```
Painterly gouache-and-oil illustrated realism, cinematic noir, visible brush texture, film grain, 16:9. Carroll Street garden at night, long table, paper lanterns, bare fig tree, black notebook on the cloth, dusk blue, warm lantern glow. Ivy: red messy bun with a pen, gray cardigan, square emerald ring on LEFT ring finger only (no band yet); a phone; white tablecloth. Start: close on the table. Ivy's hand sets her phone face-up on the tablecloth between the men; the screen glows. Sal's eyes go to the phone; Nico does not move. End: phone on the cloth, screen lit. Camera: close, locked off. Silent, mouths relaxed. No zoom, cuts or morphing; faces and outfits match the reference.
```

- **Negative:**

```
text, subtitles, watermark, logo, zoom, push-in, camera shake, morphing, face drift, changed outfit, extra fingers, fused fingers, deformed hands, extra limbs, duplicate people, speaking, lip sync, talking mouth, blood, gore, visible wound, photorealistic, 3d render, cartoon, camera movement, pan, tilt, ring on a chain, necklace, pendant, earrings, bracelet, second ring, splint on LEFT arm, white plaster splint, missing splint
```


## s49 (CH15, narration 43.61 s) - 2 clip(s)

**Timing / bridge:** Gaps 0-8, 16-30, 38-43.6 s: bridge with stills (the chest tube kit, Tommy in the doorway, the clock at 2:00).

### s49_c1  (NEW, start +8.0 s)

- Narration cue: "He came home at 1:40 Sunday morning carried by Tommy, shot under the left arm."
- Attach: KF s49 still as start frame; REF-IVY (approved face); REF-NICO (approved face)
- Cut in: keyframe pose  |  Cut out: Ivy and Priya bent over the sterile field
- Risk: gloved hands; no visible blood
- **Prompt** (897 chars):

```
Painterly gouache-and-oil illustrated realism, cinematic noir, visible brush texture, film grain, 16:9. Carroll Street kitchen at 2 a.m., marble island, sterile drape, lamp, harsh lamp and a phone flashlight. Nico: 34, dark wavy hair, stubble, gray eyes, thin white scar through LEFT eyebrow lying on the marble island, sterile blue drape over his left chest, black plastic splint on RIGHT forearm, three velcro straps, small white cross on wrist strap on his stomach; Ivy: red bun with a pen, cardigan over navy scrubs, blue sterile gloves; Priya: tall, scrubs. No blood visible. Start: Priya raises her phone flashlight over the field; Ivy glances at it and tucks sterile gauze under the drape; Nico's chest rises, gray eyes on Ivy. End: both women bent over the field. Camera: tight overhead, locked off. Silent, mouths relaxed. No zoom, cuts or morphing; faces and outfits match the reference.
```

- **Negative:**

```
text, subtitles, watermark, logo, zoom, push-in, camera shake, morphing, face drift, changed outfit, extra fingers, fused fingers, deformed hands, extra limbs, duplicate people, speaking, lip sync, talking mouth, blood, gore, visible wound, photorealistic, 3d render, cartoon, camera movement, pan, tilt, rings over gloves, necklace, earrings, splint on LEFT arm, white plaster splint, missing splint
```

### s49_c2  (NEW, start +30.0 s)

- Narration cue: "Priya looked at my sterile field."
- Attach: KF s49 still as start frame; REF-IVY (approved face); REF-NICO (approved face); optional: last frame of s49_c1 as start frame if Flow allows, else rely on KF
- Cut in: Ivy and Priya bent over the sterile field  |  Cut out: Priya and Ivy exchanging a look
- Risk: mild
- **Prompt** (666 chars):

```
Painterly gouache-and-oil illustrated realism, cinematic noir, visible brush texture, film grain, 16:9. Carroll Street kitchen at 2 a.m., marble island, sterile drape, lamp, harsh lamp and a phone flashlight. Ivy: red bun with a pen, blue sterile gloves, cardigan over scrubs; Priya: tall, scrubs; Nico partly in frame under a blue drape. No blood visible. Start: Priya looks at Ivy's sterile field, then at Ivy; Priya nods slowly in approval. Ivy lets out a breath and her shoulders drop. End: the two women's eyes meeting over the island. Camera: tight overhead, locked off. Silent, mouths relaxed. No zoom, cuts or morphing; faces and outfits match the reference.
```

- **Negative:**

```
text, subtitles, watermark, logo, zoom, push-in, camera shake, morphing, face drift, changed outfit, extra fingers, fused fingers, deformed hands, extra limbs, duplicate people, speaking, lip sync, talking mouth, blood, gore, visible wound, photorealistic, 3d render, cartoon, camera movement, pan, tilt, rings over gloves, necklace, earrings
```


## s50 (CH15, narration 24.08 s) - 3 clip(s)

**Timing / bridge:** 3 clips = 24 s = shot length 24.08 s, near-contiguous; trim c3's last 0.1 s.

### s50_c1  (NEW, start +0.0 s)

- Narration cue: "At 11:52 on Sunday I heard the bolt slide back."
- Attach: KF s50 still as start frame; REF-IVY (approved face); REF-NICO (approved face)
- Cut in: keyframe pose  |  Cut out: Door ajar, bolt drawn back
- Risk: bolt
- **Prompt** (674 chars):

```
Painterly gouache-and-oil illustrated realism, cinematic noir, visible brush texture, film grain, 16:9. Ivy's third-floor bedroom beside a connecting door with a brass bolt on Ivy's side, low warm lamp. A brass bolt with two crooked screws on a dark wooden connecting door. Ivy's RIGHT hand; her LEFT hand shows a square emerald ring over a thin gold band. Start: extreme close on the bolt. Ivy's RIGHT hand slides it back with a small metallic jerk; the door opens a few inches onto a dark room with a low lamp. End: door ajar, bolt drawn back. Camera: close on the bolt, locked off. Silent, mouths relaxed. No zoom, cuts or morphing; faces and outfits match the reference.
```

- **Negative:**

```
text, subtitles, watermark, logo, zoom, push-in, camera shake, morphing, face drift, changed outfit, extra fingers, fused fingers, deformed hands, extra limbs, duplicate people, speaking, lip sync, talking mouth, blood, gore, visible wound, photorealistic, 3d render, cartoon, camera movement, pan, tilt, ring on a chain, necklace, pendant, earrings, bracelet, extra rings beyond emerald and thin gold band
```

### s50_c2  (NEW, start +8.0 s)

- Narration cue: "She said, 'I love you. I wanted you to hear it once without anyone else in the room.'"
- Attach: KF s50 still as start frame; REF-IVY (approved face); REF-NICO (approved face); optional: last frame of s50_c1 as start frame if Flow allows, else rely on KF
- Cut in: Door ajar, bolt drawn back  |  Cut out: Nico's LEFT hand raised toward Ivy
- Risk: drain on LEFT side, LEFT hand
- **Prompt** (844 chars):

```
Painterly gouache-and-oil illustrated realism, cinematic noir, visible brush texture, film grain, 16:9. Ivy's third-floor bedroom beside a connecting door with a brass bolt on Ivy's side, low warm lamp. Nico: 34, dark wavy hair, stubble, gray eyes, thin white scar through LEFT eyebrow propped on pillows, chest drain bottle on the LEFT side, black plastic splint on RIGHT forearm, three velcro straps, small white cross on wrist strap; Ivy in her late mother's gray cardigan, red hair down, emerald ring over thin gold band on LEFT ring finger. Start: Ivy in the doorway. She crosses to the bedside and stops; Nico's gray eyes follow her; his LEFT hand lifts slowly from the blanket, wincing. End: his hand raised toward her. Camera: medium, locked off. Silent, mouths relaxed. No zoom, cuts or morphing; faces and outfits match the reference.
```

- **Negative:**

```
text, subtitles, watermark, logo, zoom, push-in, camera shake, morphing, face drift, changed outfit, extra fingers, fused fingers, deformed hands, extra limbs, duplicate people, speaking, lip sync, talking mouth, blood, gore, visible wound, photorealistic, 3d render, cartoon, camera movement, pan, tilt, ring on a chain, necklace, pendant, earrings, bracelet, extra rings beyond emerald and thin gold band, splint on LEFT arm, white plaster splint, missing splint
```

### s50_c3  (NEW, start +16.0 s)

- Narration cue: "I took her wrist and kissed the inside of it where her pulse was... her hand on my splint."
- Attach: KF s50 still as start frame; REF-IVY (approved face); REF-NICO (approved face); optional: last frame of s50_c2 as start frame if Flow allows, else rely on KF
- Cut in: Nico's LEFT hand raised toward Ivy  |  Cut out: Ivy's hand resting on the black splint
- Risk: HIGH: wrist grip, which hand is which
- **Prompt** (830 chars):

```
Painterly gouache-and-oil illustrated realism, cinematic noir, visible brush texture, film grain, 16:9. Ivy's third-floor bedroom beside a connecting door with a brass bolt on Ivy's side, low warm lamp. Nico: 34, dark wavy hair, stubble, gray eyes, thin white scar through LEFT eyebrow, black plastic splint on RIGHT forearm, three velcro straps, small white cross on wrist strap, chest drain on LEFT side; Ivy: loose red hair, gray cardigan, emerald ring over gold band on LEFT ring finger. Start: his LEFT hand takes her wrist and he presses his lips to the inside of it. Ivy's face softens. She settles into the chair and rests her hand on the black splint on the blanket. End: her hand on the splint. Camera: close two-shot, locked off. Silent, mouths relaxed. No zoom, cuts or morphing; faces and outfits match the reference.
```

- **Negative:**

```
text, subtitles, watermark, logo, zoom, push-in, camera shake, morphing, face drift, changed outfit, extra fingers, fused fingers, deformed hands, extra limbs, duplicate people, speaking, lip sync, talking mouth, blood, gore, visible wound, photorealistic, 3d render, cartoon, camera movement, pan, tilt, ring on a chain, necklace, pendant, earrings, bracelet, extra rings beyond emerald and thin gold band, splint on LEFT arm, white plaster splint, missing splint
```


## s53 (CH16, narration 44.89 s) - 4 clip(s)

**Timing / bridge:** 4 clips = 32 s over 44.89 s. c4 changes location (car): use the s51 car keyframe. Gaps: stills of Brancato's face, the neon sign, Reyes's team at the front door.

### s53_c1  (NEW, start +0.0 s)

- Narration cue: "I'm not armed, Carmine. My wife doesn't like it." (Lion)
- Attach: KF s53 still as start frame; REF-IVY (approved face); REF-NICO (approved face)
- Cut in: keyframe pose  |  Cut out: Weapons pointed at Nico, Nico still
- Risk: six faces, guns
- **Prompt** (856 chars):

```
Painterly gouache-and-oil illustrated realism, cinematic noir, visible brush texture, film grain, 16:9. Brancato's social club, green back door, linoleum floor, neon sign with a burned-out M, neon green and sodium orange. Nico: 34, dark wavy hair, stubble, gray eyes, thin white scar through LEFT eyebrow, black shirt, gauze bulge on his LEFT side, black plastic splint on RIGHT forearm, three velcro straps, small white cross on wrist strap, pale and swaying; six men in dark clothes at the far side of the room. Start: wide from the back door. Nico steps in through the door, both hands empty and open at his sides. The men in the room turn their heads, then raise their pistols toward him. He stands swaying. End: weapons up, Nico still. Camera: wide, locked off. Silent, mouths relaxed. No zoom, cuts or morphing; faces and outfits match the reference.
```

- **Negative:**

```
text, subtitles, watermark, logo, zoom, push-in, camera shake, morphing, face drift, changed outfit, extra fingers, fused fingers, deformed hands, extra limbs, duplicate people, speaking, lip sync, talking mouth, blood, gore, visible wound, photorealistic, 3d render, cartoon, camera movement, pan, tilt, necklace, chain, ring, earrings, bracelet, any jewelry, splint on LEFT arm, white plaster splint, missing splint, gun in Nico's hand
```

### s53_c2  (NEW, start +9.0 s)

- Narration cue: "Six guns turned. I stepped in front of him. 'Be quiet. It's my turn.'"
- Attach: KF s53 still as start frame; REF-IVY (approved face); REF-NICO (approved face); optional: last frame of s53_c1 as start frame if Flow allows, else rely on KF
- Cut in: Weapons pointed at Nico, Nico still  |  Cut out: Ivy in front of Nico, facing the guns
- Risk: blocking, many people
- **Prompt** (847 chars):

```
Painterly gouache-and-oil illustrated realism, cinematic noir, visible brush texture, film grain, 16:9. Brancato's social club, green back door, linoleum floor, neon sign with a burned-out M, neon green and sodium orange. Ivy: red messy bun with a pen, navy scrubs under a gray cardigan, emerald ring on LEFT hand over gold band; Nico: 34, dark wavy hair, stubble, gray eyes, thin white scar through LEFT eyebrow, black plastic splint on RIGHT forearm, three velcro straps, small white cross on wrist strap, behind her. Start: Nico in the door, weapons raised. Ivy steps quickly across in front of him, turns her back to him, faces the room with arms slightly out and chin up. Nico stays swaying behind her. End: Ivy shielding him. Camera: wide, locked off. Silent, mouths relaxed. No zoom, cuts or morphing; faces and outfits match the reference.
```

- **Negative:**

```
text, subtitles, watermark, logo, zoom, push-in, camera shake, morphing, face drift, changed outfit, extra fingers, fused fingers, deformed hands, extra limbs, duplicate people, speaking, lip sync, talking mouth, blood, gore, visible wound, photorealistic, 3d render, cartoon, camera movement, pan, tilt, ring on a chain, necklace, pendant, earrings, bracelet, extra rings beyond emerald and thin gold band, splint on LEFT arm, white plaster splint, missing splint
```

### s53_c3  (NEW, start +21.0 s)

- Narration cue: "He said, 'In my house, we don't point guns at the doctor.' He told them to put them down."
- Attach: KF s53 still as start frame; REF-IVY (approved face); REF-NICO (approved face); optional: last frame of s53_c2 as start frame if Flow allows, else rely on KF
- Cut in: Ivy in front of Nico, facing the guns  |  Cut out: All pistols pointed down
- Risk: guns lowering together
- **Prompt** (609 chars):

```
Painterly gouache-and-oil illustrated realism, cinematic noir, visible brush texture, film grain, 16:9. Brancato's social club, green back door, linoleum floor, neon sign with a burned-out M, neon green and sodium orange. Brancato: late sixties, white hair, brown cardigan buttoned wrong. Six men in dark clothes with pistols. Start: pistols raised. Brancato lifts one flat palm and pushes it down; the men lower their pistols toward the floor one after another. End: all pistols pointed down. Camera: wide, locked off. Silent, mouths relaxed. No zoom, cuts or morphing; faces and outfits match the reference.
```

- **Negative:**

```
text, subtitles, watermark, logo, zoom, push-in, camera shake, morphing, face drift, changed outfit, extra fingers, fused fingers, deformed hands, extra limbs, duplicate people, speaking, lip sync, talking mouth, blood, gore, visible wound, photorealistic, 3d render, cartoon, camera movement, pan, tilt, necklace, chain, ring, earrings, bracelet, any jewelry
```

### s53_c4  (NEW, start +36.89 s)

- Narration cue: "In the car, Nico was gray, pulse 110. 'I came in with nothing because you were in that room.'"
- Attach: KF s53 still as start frame; REF-IVY (approved face); REF-NICO (approved face); optional: last frame of s53_c3 as start frame if Flow allows, else rely on KF
- Cut in: All pistols pointed down  |  Cut out: Nico's eyes on Ivy, her fingers still on his wrist
- Risk: wrist grip
- **Prompt** (887 chars):

```
Painterly gouache-and-oil illustrated realism, cinematic noir, visible brush texture, film grain, 16:9. Brancato's social club, green back door, linoleum floor, neon sign with a burned-out M, neon green and sodium orange. Inside a black car, wet street, streetlights sliding. Ivy: red bun with a pen, cardigan, emerald ring over gold band on LEFT ring finger; Nico: 34, dark wavy hair, stubble, gray eyes, thin white scar through LEFT eyebrow, gray-faced, black plastic splint on RIGHT forearm, three velcro straps, small white cross on wrist strap. Start: Ivy's two fingers rest on Nico's LEFT wrist, her eyes distant, counting. Nico watches her face, closes his eyes, opens them. Streetlight stripes slide across them. End: his eyes on hers. Camera: medium two-shot in the back seat, locked off. Silent, mouths relaxed. No zoom, cuts or morphing; faces and outfits match the reference.
```

- **Negative:**

```
text, subtitles, watermark, logo, zoom, push-in, camera shake, morphing, face drift, changed outfit, extra fingers, fused fingers, deformed hands, extra limbs, duplicate people, speaking, lip sync, talking mouth, blood, gore, visible wound, photorealistic, 3d render, cartoon, camera movement, pan, tilt, ring on a chain, necklace, pendant, earrings, bracelet, extra rings beyond emerald and thin gold band, splint on LEFT arm, white plaster splint, missing splint
```


## s54 (CH17, narration 31.0 s) - 2 clip(s)

**Timing / bridge:** Gaps 10-15 s and 23-31 s: bridge with stills (Nico's stained gauze, the signature page, the planter with geraniums).

### s54_c1  (NEW, start +2.0 s)

- Narration cue: "In the visiting room I said, I'm sorry I made you carry it."
- Attach: KF s54 still as start frame; REF-NICO (approved face)
- Cut in: keyframe pose  |  Cut out: Brothers' fingertips touching
- Risk: two hands touching
- **Prompt** (824 chars):

```
Painterly gouache-and-oil illustrated realism, cinematic noir, visible brush texture, film grain, 16:9. federal detention visiting room, glass table, gray walls, flat institutional light. Nico: 34, dark wavy hair, stubble, gray eyes, thin white scar through LEFT eyebrow, rumpled white shirt, black plastic splint on RIGHT forearm, three velcro straps, small white cross on wrist strap, faint brown stain on the gauze at his LEFT side; Enzo: 21, gold curls, tan jumpsuit. Start: the brothers face each other across the glass table. Nico leans forward and lays his LEFT hand flat on the table; Enzo looks at the hand, then slowly slides his own hand across to touch Nico's fingers. End: fingertips touching. Camera: medium, locked off. Silent, mouths relaxed. No zoom, cuts or morphing; faces and outfits match the reference.
```

- **Negative:**

```
text, subtitles, watermark, logo, zoom, push-in, camera shake, morphing, face drift, changed outfit, extra fingers, fused fingers, deformed hands, extra limbs, duplicate people, speaking, lip sync, talking mouth, blood, gore, visible wound, photorealistic, 3d render, cartoon, camera movement, pan, tilt, necklace, chain, ring, earrings, bracelet, any jewelry, splint on LEFT arm, white plaster splint, missing splint
```

### s54_c2  (NEW, start +15.0 s)

- Narration cue: "...and I cried in front of a guard."
- Attach: KF s54 still as start frame; REF-NICO (approved face); optional: last frame of s54_c1 as start frame if Flow allows, else rely on KF
- Cut in: Brothers' fingertips touching  |  Cut out: Nico lifting his head
- Risk: mild
- **Prompt** (778 chars):

```
Painterly gouache-and-oil illustrated realism, cinematic noir, visible brush texture, film grain, 16:9. federal detention visiting room, glass table, gray walls, flat institutional light. Nico: 34, dark wavy hair, stubble, gray eyes, thin white scar through LEFT eyebrow, rumpled white shirt, black plastic splint on RIGHT forearm, three velcro straps, small white cross on wrist strap; Enzo: gold curls, tan jumpsuit; a guard blurred in the background. Start: hands touching. Nico's head bows; a tear runs down his cheek and he wipes it with the back of his LEFT hand. Enzo watches him, and the guard behind them shifts his weight. End: Nico lifting his head. Camera: medium, locked off. Silent, mouths relaxed. No zoom, cuts or morphing; faces and outfits match the reference.
```

- **Negative:**

```
text, subtitles, watermark, logo, zoom, push-in, camera shake, morphing, face drift, changed outfit, extra fingers, fused fingers, deformed hands, extra limbs, duplicate people, speaking, lip sync, talking mouth, blood, gore, visible wound, photorealistic, 3d render, cartoon, camera movement, pan, tilt, necklace, chain, ring, earrings, bracelet, any jewelry, splint on LEFT arm, white plaster splint, missing splint
```


## s55 (CH17, narration 38.61 s) - 2 clip(s)

**Timing / bridge:** Gaps 11-20 and 28-38.6 s: stills of the jurors' hands, Ivy's face, the courtroom clock.

### s55_c1  (NEW, start +3.0 s)

- Narration cue: "Thursday, third grand jury. I waived my privilege myself..."
- Attach: KF s55 still as start frame; REF-IVY (approved face)
- Cut in: keyframe pose  |  Cut out: Ivy's hands folded, ring over band visible
- Risk: hand anatomy, ring
- **Prompt** (646 chars):

```
Painterly gouache-and-oil illustrated realism, cinematic noir, visible brush texture, film grain, 16:9. grand jury room, wood-paneled, long table, rail, flat daylight. Ivy: 28, freckles, red messy bun with a pen through it, square emerald ring over a thin plain gold band on LEFT ring finger, nothing at neck, gray cardigan; Holloway: navy suit. Start: Ivy at the witness chair. She raises her RIGHT hand for the oath, steady, holds it, then lowers it and folds her hands on the rail so the ring and band show. End: hands folded. Camera: close, locked off. Silent, mouths relaxed. No zoom, cuts or morphing; faces and outfits match the reference.
```

- **Negative:**

```
text, subtitles, watermark, logo, zoom, push-in, camera shake, morphing, face drift, changed outfit, extra fingers, fused fingers, deformed hands, extra limbs, duplicate people, speaking, lip sync, talking mouth, blood, gore, visible wound, photorealistic, 3d render, cartoon, camera movement, pan, tilt, ring on a chain, necklace, pendant, earrings, bracelet, extra rings beyond emerald and thin gold band
```

### s55_c2  (NEW, start +20.0 s)

- Narration cue: "I told them what I saw. Two shots at 4:10..."
- Attach: KF s55 still as start frame; REF-IVY (approved face); optional: last frame of s55_c1 as start frame if Flow allows, else rely on KF
- Cut in: Ivy's hands folded, ring over band visible  |  Cut out: Holloway and Ivy facing each other
- Risk: mild
- **Prompt** (539 chars):

```
Painterly gouache-and-oil illustrated realism, cinematic noir, visible brush texture, film grain, 16:9. grand jury room, wood-paneled, long table, rail, flat daylight. Holloway: navy suit, neat hair; Ivy: red bun with a pen, gray cardigan. Start: Holloway standing at the lectern. He straightens his cuffs, steps one pace toward her, and holds her gaze; Ivy meets it, chin up, gives one small nod. End: facing each other. Camera: medium, locked off. Silent, mouths relaxed. No zoom, cuts or morphing; faces and outfits match the reference.
```

- **Negative:**

```
text, subtitles, watermark, logo, zoom, push-in, camera shake, morphing, face drift, changed outfit, extra fingers, fused fingers, deformed hands, extra limbs, duplicate people, speaking, lip sync, talking mouth, blood, gore, visible wound, photorealistic, 3d render, cartoon, camera movement, pan, tilt, ring on a chain, necklace, pendant, earrings, bracelet, extra rings beyond emerald and thin gold band
```


## s56 (CH17, narration 33.72 s) - 2 clip(s)

**Timing / bridge:** Gaps 0-10 and 18-22, 30-33.7 s: stills of the hallway, the clock at 2:00 and the discarded splint on the tray.

### s56_c1  (NEW, start +10.0 s)

- Narration cue: "At two o'clock I took off the splint, six weeks less one day."
- Attach: KF s56 still as start frame; REF-IVY (approved face); REF-NICO (approved face)
- Cut in: keyframe pose  |  Cut out: Bare RIGHT forearm with a pink scar, fingers loosely open
- Risk: velcro, hands
- **Prompt** (705 chars):

```
Painterly gouache-and-oil illustrated realism, cinematic noir, visible brush texture, film grain, 16:9. St. Brigid's ER bay 14, curtain, steel tray, cold buzzing fluorescent light. Nico's pale thin RIGHT forearm resting on the bay bed; black plastic splint on RIGHT forearm, three velcro straps, small white cross on wrist strap; Ivy's blue-gloved hands. Start: close on the black splint. Ivy's gloved hands open the three velcro straps one by one, lift the black shell away and set it aside, revealing a long pink scar on the pale forearm. End: bare forearm, scar visible. Camera: close on the forearm, locked off. Silent, mouths relaxed. No zoom, cuts or morphing; faces and outfits match the reference.
```

- **Negative:**

```
text, subtitles, watermark, logo, zoom, push-in, camera shake, morphing, face drift, changed outfit, extra fingers, fused fingers, deformed hands, extra limbs, duplicate people, speaking, lip sync, talking mouth, blood, gore, visible wound, photorealistic, 3d render, cartoon, camera movement, pan, tilt, rings over gloves, necklace, splint on LEFT arm, white plaster splint, missing splint
```

### s56_c2  (NEW, start +22.0 s)

- Narration cue: "His fist closed. All of it, even the ring finger I sewed."
- Attach: KF s56 still as start frame; REF-IVY (approved face); REF-NICO (approved face); optional: last frame of s56_c1 as start frame if Flow allows, else rely on KF
- Cut in: Bare RIGHT forearm with a pink scar, fingers loosely open  |  Cut out: Closed fist, Nico looking up at Ivy
- Risk: HIGH: finger anatomy
- **Prompt** (599 chars):

```
Painterly gouache-and-oil illustrated realism, cinematic noir, visible brush texture, film grain, 16:9. St. Brigid's ER bay 14, curtain, steel tray, cold buzzing fluorescent light. Nico's bare RIGHT hand and forearm with a long pink scar, gloved hands of Ivy at the edge; Nico's gray eyes in the upper frame. Start: the RIGHT hand lies open. The fingers curl slowly into a full fist, the ring finger last; he looks at his own hand, then lifts his eyes to Ivy. End: closed fist held. Camera: close, locked off. Silent, mouths relaxed. No zoom, cuts or morphing; faces and outfits match the reference.
```

- **Negative:**

```
text, subtitles, watermark, logo, zoom, push-in, camera shake, morphing, face drift, changed outfit, extra fingers, fused fingers, deformed hands, extra limbs, duplicate people, speaking, lip sync, talking mouth, blood, gore, visible wound, photorealistic, 3d render, cartoon, camera movement, pan, tilt, rings over gloves, necklace, splint, cast, brace, bandage on forearm
```


## s57 (CH18, narration 19.73 s) - 2 clip(s)

**Timing / bridge:** 2 clips = 16 s over 19.73 s. Gap 8-11.7 s: hold c1's end frame or a still of the signature.

### s57_c1  (NEW, start +0.0 s)

- Narration cue: "That evening there was a cream envelope on the hall table. Term Five."
- Attach: KF s57 still as start frame; REF-IVY (approved face)
- Cut in: keyframe pose  |  Cut out: Pages held at chest height
- Risk: paper, hands, no legible text
- **Prompt** (667 chars):

```
Painterly gouache-and-oil illustrated realism, cinematic noir, visible brush texture, film grain, 16:9. hall table in the Carroll Street brownstone, stair rail behind, evening, warm lamp. Ivy: 28, freckles, red messy bun with a pen through it, square emerald ring over a thin plain gold band on LEFT ring finger, nothing at neck, gray cardigan; a cream envelope on the hall table. Start: Ivy's hands pick up the cream envelope and slide out three stapled pages; her thumb flips to the last page and her eyes scan it. End: pages held at chest height. Camera: medium, locked off. Silent, mouths relaxed. No zoom, cuts or morphing; faces and outfits match the reference.
```

- **Negative:**

```
text, subtitles, watermark, logo, zoom, push-in, camera shake, morphing, face drift, changed outfit, extra fingers, fused fingers, deformed hands, extra limbs, duplicate people, speaking, lip sync, talking mouth, blood, gore, visible wound, photorealistic, 3d render, cartoon, camera movement, pan, tilt, ring on a chain, necklace, pendant, earrings, bracelet, extra rings beyond emerald and thin gold band
```

### s57_c2  (NEW, start +11.73 s)

- Narration cue: "I put the papers down and went upstairs."
- Attach: KF s57 still as start frame; REF-IVY (approved face); optional: last frame of s57_c1 as start frame if Flow allows, else rely on KF
- Cut in: Pages held at chest height  |  Cut out: Empty hall table, the stair rail
- Risk: walking out of frame
- **Prompt** (675 chars):

```
Painterly gouache-and-oil illustrated realism, cinematic noir, visible brush texture, film grain, 16:9. hall table in the Carroll Street brownstone, stair rail behind, evening, warm lamp. Ivy: 28, freckles, red messy bun with a pen through it, square emerald ring over a thin plain gold band on LEFT ring finger, nothing at neck, gray cardigan, lamp on her face. Start: close on Ivy's face, her jaw tight. She sets the papers on the table, squares the stack with her fingertips, turns, and walks up the stairs out of frame. End: empty hall table and stairs. Camera: medium, locked off. Silent, mouths relaxed. No zoom, cuts or morphing; faces and outfits match the reference.
```

- **Negative:**

```
text, subtitles, watermark, logo, zoom, push-in, camera shake, morphing, face drift, changed outfit, extra fingers, fused fingers, deformed hands, extra limbs, duplicate people, speaking, lip sync, talking mouth, blood, gore, visible wound, photorealistic, 3d render, cartoon, camera movement, pan, tilt, ring on a chain, necklace, pendant, earrings, bracelet, extra rings beyond emerald and thin gold band
```


## s58 (CH18, narration 28.19 s) - 3 clip(s)

**Timing / bridge:** 3 clips = 24 s over 28.19 s. Gap 8-9.1 s and the last 2 s: hold end frames; page eleven close-up as a painted still with light drift.

### s58_c1  (NEW, start +0.0 s)

- Narration cue: "I didn't knock. 'Here's the thing about the divorce,' I said. 'I haven't asked.'"
- Attach: KF s58 still as start frame; REF-IVY (approved face); REF-NICO (approved face)
- Cut in: keyframe pose  |  Cut out: Ivy in the doorway, Nico's head turned to her
- Risk: door, 2 people
- **Prompt** (854 chars):

```
Painterly gouache-and-oil illustrated realism, cinematic noir, visible brush texture, film grain, 16:9. Ivy's third-floor bedroom, connecting door, brass bolt undrawn on her side, low warm lamp. Ivy: 28, freckles, red messy bun with a pen through it, square emerald ring over a thin plain gold band on LEFT ring finger, nothing at neck, gray cardigan; Nico: 34, dark wavy hair, stubble, gray eyes, thin white scar through LEFT eyebrow, white shirt, no splint, a long pink scar inside his RIGHT forearm. Start: Ivy opens the connecting door without knocking and steps in. Nico stands at the window, hands open at his sides, the lamp low. He turns his head to her. End: Ivy standing in the doorway, Nico's head turned. Camera: medium wide in the doorway, locked off. Silent, mouths relaxed. No zoom, cuts or morphing; faces and outfits match the reference.
```

- **Negative:**

```
text, subtitles, watermark, logo, zoom, push-in, camera shake, morphing, face drift, changed outfit, extra fingers, fused fingers, deformed hands, extra limbs, duplicate people, speaking, lip sync, talking mouth, blood, gore, visible wound, photorealistic, 3d render, cartoon, camera movement, pan, tilt, ring on a chain, necklace, pendant, earrings, bracelet, extra rings beyond emerald and thin gold band, splint, cast, brace, bandage on forearm
```

### s58_c2  (NEW, start +9.1 s)

- Narration cue: "I emptied my cardigan pockets onto his bed."
- Attach: KF s58 still as start frame; REF-IVY (approved face); REF-NICO (approved face); optional: last frame of s58_c1 as start frame if Flow allows, else rely on KF
- Cut in: Ivy in the doorway, Nico's head turned to her  |  Cut out: Objects scattered on the bed
- Risk: props falling
- **Prompt** (733 chars):

```
Painterly gouache-and-oil illustrated realism, cinematic noir, visible brush texture, film grain, 16:9. Ivy's third-floor bedroom, connecting door, brass bolt undrawn on her side, low warm lamp. Ivy: 28, freckles, red messy bun with a pen through it, square emerald ring over a thin plain gold band on LEFT ring finger, nothing at neck, gray cardigan; a bed with a plain cover. Start: Ivy beside the bed. She turns both cardigan pockets inside out; a foil blister card, a folded form, a small note, a sealed envelope and a white candy twist fall onto the bed. End: objects scattered on the cover. Camera: medium, locked off, bed in foreground. Silent, mouths relaxed. No zoom, cuts or morphing; faces and outfits match the reference.
```

- **Negative:**

```
text, subtitles, watermark, logo, zoom, push-in, camera shake, morphing, face drift, changed outfit, extra fingers, fused fingers, deformed hands, extra limbs, duplicate people, speaking, lip sync, talking mouth, blood, gore, visible wound, photorealistic, 3d render, cartoon, camera movement, pan, tilt, ring on a chain, necklace, pendant, earrings, bracelet, extra rings beyond emerald and thin gold band
```

### s58_c3  (NEW, start +18.19 s)

- Narration cue: "I took the pen out of my hair... I wrote, She does. And under that: Term six."
- Attach: KF s58 still as start frame; REF-IVY (approved face); REF-NICO (approved face); optional: last frame of s58_c2 as start frame if Flow allows, else rely on KF
- Cut in: Objects scattered on the bed  |  Cut out: Pen lifted from the page, hair loose
- Risk: writing hand, no legible text
- **Prompt** (715 chars):

```
Painterly gouache-and-oil illustrated realism, cinematic noir, visible brush texture, film grain, 16:9. Ivy's third-floor bedroom, connecting door, brass bolt undrawn on her side, low warm lamp. Ivy: 28, freckles, red messy bun with a pen through it, square emerald ring over a thin plain gold band on LEFT ring finger, nothing at neck, gray cardigan, red bun with a pen; paper pages on the desk. Start: Ivy pulls the pen out of her bun, red hair falls to her shoulders, and with her RIGHT hand she writes two short lines at the bottom of a page, then lifts the pen. End: pen above the page. Camera: medium close, locked off. Silent, mouths relaxed. No zoom, cuts or morphing; faces and outfits match the reference.
```

- **Negative:**

```
text, subtitles, watermark, logo, zoom, push-in, camera shake, morphing, face drift, changed outfit, extra fingers, fused fingers, deformed hands, extra limbs, duplicate people, speaking, lip sync, talking mouth, blood, gore, visible wound, photorealistic, 3d render, cartoon, camera movement, pan, tilt, ring on a chain, necklace, pendant, earrings, bracelet, extra rings beyond emerald and thin gold band
```


## s59 (CH18, narration 41.91 s) - 2 clip(s)

**Timing / bridge:** Gaps 0-10 and 18-24, 32-41.9 s: stills for Rosaria Amato's story, the open door, and the oven (optional spare clip for Teresa's oven line).

### s59_c1  (NEW, start +10.0 s)

- Narration cue: "I love you, Ivy. I've loved you since you put my money back in my pocket..."
- Attach: KF s59 still as start frame; REF-IVY (approved face); REF-NICO (approved face)
- Cut in: keyframe pose  |  Cut out: Nico's eyes on Ivy's, page held
- Risk: face drift
- **Prompt** (837 chars):

```
Painterly gouache-and-oil illustrated realism, cinematic noir, visible brush texture, film grain, 16:9. Ivy's third-floor bedroom, connecting door open, lamp, warm lamp glow. Nico: 34, dark wavy hair, stubble, gray eyes, thin white scar through LEFT eyebrow, white shirt, no splint, a pink scar on the inside of his RIGHT forearm; Ivy: 28, freckles, red messy bun with a pen through it, square emerald ring over a thin plain gold band on LEFT ring finger, nothing at neck, gray cardigan. Start: close two-shot. Nico holds the last page in his LEFT hand and reads it, his gray eyes moving down, then back up to the top to read it again; Ivy watches his face. He then lifts his gaze to her. End: his eyes on hers. Camera: close two-shot, locked off. Silent, mouths relaxed. No zoom, cuts or morphing; faces and outfits match the reference.
```

- **Negative:**

```
text, subtitles, watermark, logo, zoom, push-in, camera shake, morphing, face drift, changed outfit, extra fingers, fused fingers, deformed hands, extra limbs, duplicate people, speaking, lip sync, talking mouth, blood, gore, visible wound, photorealistic, 3d render, cartoon, camera movement, pan, tilt, ring on a chain, necklace, pendant, earrings, bracelet, extra rings beyond emerald and thin gold band, splint, cast, brace, bandage on forearm
```

### s59_c2  (NEW, start +24.0 s)

- Narration cue: "The door stayed open that night, and I'm not going to tell you the rest."
- Attach: KF s59 still as start frame; REF-IVY (approved face); REF-NICO (approved face); optional: last frame of s59_c1 as start frame if Flow allows, else rely on KF
- Cut in: Nico's eyes on Ivy's, page held  |  Cut out: Nico's faint smile, Ivy watching
- Risk: signing hand
- **Prompt** (831 chars):

```
Painterly gouache-and-oil illustrated realism, cinematic noir, visible brush texture, film grain, 16:9. Ivy's third-floor bedroom, connecting door open, lamp, warm lamp glow. Nico: 34, dark wavy hair, stubble, gray eyes, thin white scar through LEFT eyebrow, white shirt, no splint, scar inside his RIGHT forearm; Ivy: 28, freckles, red messy bun with a pen through it, square emerald ring over a thin plain gold band on LEFT ring finger, nothing at neck. Start: his eyes down on the page. He signs it slowly with his RIGHT hand, careful like a man writing in a foreign language; Ivy watches his face. He lifts his head, the faintest smile. Closed-door ending, no kiss. End: smile, lamp glow between them. Camera: close two-shot, locked off. Silent, mouths relaxed. No zoom, cuts or morphing; faces and outfits match the reference.
```

- **Negative:**

```
text, subtitles, watermark, logo, zoom, push-in, camera shake, morphing, face drift, changed outfit, extra fingers, fused fingers, deformed hands, extra limbs, duplicate people, speaking, lip sync, talking mouth, blood, gore, visible wound, photorealistic, 3d render, cartoon, camera movement, pan, tilt, ring on a chain, necklace, pendant, earrings, bracelet, extra rings beyond emerald and thin gold band, splint, cast, brace, bandage on forearm
```


## s60 (CH19, narration 40.5 s) - 3 clip(s)

**Timing / bridge:** 3 clips = 24 s over 40.5 s. Gaps are covered by painted stills (Theo's laundromat apartment, Enzo's program letter, Danny at school, the garden table) while the narration lists fates.

### s60_c1  (NEW, start +0.0 s)

- Narration cue: "April. The lemon trees came out of their burlap."
- Attach: KF s60 still as start frame; REF-IVY (approved face)
- Cut in: keyframe pose  |  Cut out: Burlap folded over Ivy's arm, tree bare and green
- Risk: burlap shape
- **Prompt** (779 chars):

```
Painterly gouache-and-oil illustrated realism, cinematic noir, visible brush texture, film grain, 16:9. Carroll Street garden in April, burlap being removed from lemon trees and the fig tree, new green leaves, warm April afternoon sun. Ivy: 28, freckles, red messy bun with a pen through it, square emerald ring over a thin plain gold band on LEFT ring finger, nothing at neck, cardigan; Lucia: small, black dress, gold cross, silver-streaked hair. Start: a lemon tree in a clay pot wrapped in burlap. Ivy lifts the burlap off and folds it over her arm; new green leaves and a lemon appear in the light. Lucia stands beside her. End: bare tree in sunlight. Camera: wide garden, locked off. Silent, mouths relaxed. No zoom, cuts or morphing; faces and outfits match the reference.
```

- **Negative:**

```
text, subtitles, watermark, logo, zoom, push-in, camera shake, morphing, face drift, changed outfit, extra fingers, fused fingers, deformed hands, extra limbs, duplicate people, speaking, lip sync, talking mouth, blood, gore, visible wound, photorealistic, 3d render, cartoon, camera movement, pan, tilt, ring on a chain, necklace, pendant, earrings, bracelet, extra rings beyond emerald and thin gold band
```

### s60_c2  (NEW, start +13.0 s)

- Narration cue: "'It's a lemon tree,' Lucia said. 'It's Sicilian. It lives out of spite. Like me.'"
- Attach: KF s60 still as start frame; REF-IVY (approved face); optional: last frame of s60_c1 as start frame if Flow allows, else rely on KF
- Cut in: Burlap folded over Ivy's arm, tree bare and green  |  Cut out: Lucia smiling at the small tree
- Risk: mouth must stay closed
- **Prompt** (616 chars):

```
Painterly gouache-and-oil illustrated realism, cinematic noir, visible brush texture, film grain, 16:9. Carroll Street garden in April, burlap being removed from lemon trees and the fig tree, new green leaves, warm April afternoon sun. Lucia: small, black dress, gold cross, silver hair; a small lemon tree in a clay pot. Start: Lucia beside the small tree. She pats its pot like a stubborn child, shakes her head with a closed-mouth smile, and straightens a branch. End: Lucia smiling at the tree. Camera: medium, locked off. Silent, mouths relaxed. No zoom, cuts or morphing; faces and outfits match the reference.
```

- **Negative:**

```
text, subtitles, watermark, logo, zoom, push-in, camera shake, morphing, face drift, changed outfit, extra fingers, fused fingers, deformed hands, extra limbs, duplicate people, speaking, lip sync, talking mouth, blood, gore, visible wound, photorealistic, 3d render, cartoon, camera movement, pan, tilt, necklace other than the gold cross, rings
```

### s60_c3  (NEW, start +30.0 s)

- Narration cue: "I finish residency in June."
- Attach: KF s60 still as start frame; REF-IVY (approved face); optional: last frame of s60_c2 as start frame if Flow allows, else rely on KF
- Cut in: Lucia smiling at the small tree  |  Cut out: Ivy looking up at the study window
- Risk: mild
- **Prompt** (724 chars):

```
Painterly gouache-and-oil illustrated realism, cinematic noir, visible brush texture, film grain, 16:9. Carroll Street garden in April, burlap being removed from lemon trees and the fig tree, new green leaves, warm April afternoon sun. Ivy: 28, freckles, red messy bun with a pen through it, square emerald ring over a thin plain gold band on LEFT ring finger, nothing at neck, cardigan; a lit study window above. Start: Ivy beside the lemon tree, LEFT hand on the pot. She looks up toward the lit study window and smiles slightly while a breeze moves the leaves. End: she keeps looking at the window. Camera: medium wide, locked off. Silent, mouths relaxed. No zoom, cuts or morphing; faces and outfits match the reference.
```

- **Negative:**

```
text, subtitles, watermark, logo, zoom, push-in, camera shake, morphing, face drift, changed outfit, extra fingers, fused fingers, deformed hands, extra limbs, duplicate people, speaking, lip sync, talking mouth, blood, gore, visible wound, photorealistic, 3d render, cartoon, camera movement, pan, tilt, ring on a chain, necklace, pendant, earrings, bracelet, extra rings beyond emerald and thin gold band
```


## s62 (CH19, narration 43.77 s) - 4 clip(s)

**Timing / bridge:** 4 clips = 32 s over 43.77 s; the last ~12 s (CTA voice) over c4's final frame as a painted still with light drift. The last frame is the film's final image, regenerate until clean.

### s62_c1  (NEW, start +0.0 s)

- Narration cue: "I did not wait. We don't do silence in this house anymore. It's in the contract."
- Attach: KF s62 still as start frame; REF-IVY (approved face); REF-NICO (approved face)
- Cut in: keyframe pose  |  Cut out: Ivy on the fifth stair, hand on the rail
- Risk: stairs count not needed
- **Prompt** (733 chars):

```
Painterly gouache-and-oil illustrated realism, cinematic noir, visible brush texture, film grain, 16:9. Carroll Street brownstone, fourteen stairs up to Nico's study, blinds open, golden afternoon light from the study window. Ivy: 28, freckles, red messy bun with a pen through it, square emerald ring over a thin plain gold band on LEFT ring finger, nothing at neck, gray cardigan, seen mostly from behind. Start: low locked camera at the foot of the stairs. Ivy begins to climb, her LEFT hand sliding up the banister, steady, not rushing. End: Ivy on the fifth stair, hand on the rail. Camera: low wide at the foot of the stairs, locked off. Silent, mouths relaxed. No zoom, cuts or morphing; faces and outfits match the reference.
```

- **Negative:**

```
text, subtitles, watermark, logo, zoom, push-in, camera shake, morphing, face drift, changed outfit, extra fingers, fused fingers, deformed hands, extra limbs, duplicate people, speaking, lip sync, talking mouth, blood, gore, visible wound, photorealistic, 3d render, cartoon, camera movement, pan, tilt, ring on a chain, necklace, pendant, earrings, bracelet, extra rings beyond emerald and thin gold band
```

### s62_c2  (NEW, start +9.0 s)

- Narration cue: "I climbed fourteen stairs, counting every one..."
- Attach: KF s62 still as start frame; REF-IVY (approved face); REF-NICO (approved face); optional: last frame of s62_c1 as start frame if Flow allows, else rely on KF
- Cut in: Ivy on the fifth stair, hand on the rail  |  Cut out: Ivy near the top landing
- Risk: mild
- **Prompt** (690 chars):

```
Painterly gouache-and-oil illustrated realism, cinematic noir, visible brush texture, film grain, 16:9. Carroll Street brownstone, fourteen stairs up to Nico's study, blinds open, golden afternoon light from the study window. Ivy: 28, freckles, red messy bun with a pen through it, square emerald ring over a thin plain gold band on LEFT ring finger, nothing at neck, gray cardigan, seen from behind. Start: Ivy mid-stairs. She continues climbing, passes a pool of golden light, pauses a beat on a stair, looks up, then resumes. End: Ivy near the top landing. Camera: same low wide angle, locked off. Silent, mouths relaxed. No zoom, cuts or morphing; faces and outfits match the reference.
```

- **Negative:**

```
text, subtitles, watermark, logo, zoom, push-in, camera shake, morphing, face drift, changed outfit, extra fingers, fused fingers, deformed hands, extra limbs, duplicate people, speaking, lip sync, talking mouth, blood, gore, visible wound, photorealistic, 3d render, cartoon, camera movement, pan, tilt, ring on a chain, necklace, pendant, earrings, bracelet, extra rings beyond emerald and thin gold band
```

### s62_c3  (NEW, start +18.0 s)

- Narration cue: "...to tell my husband the truth about his father."
- Attach: KF s62 still as start frame; REF-IVY (approved face); REF-NICO (approved face); optional: last frame of s62_c2 as start frame if Flow allows, else rely on KF
- Cut in: Ivy near the top landing  |  Cut out: Nico looking at the door
- Risk: mild
- **Prompt** (720 chars):

```
Painterly gouache-and-oil illustrated realism, cinematic noir, visible brush texture, film grain, 16:9. Carroll Street brownstone, fourteen stairs up to Nico's study, blinds open, golden afternoon light from the study window. Nico: 34, dark wavy hair, stubble, gray eyes, thin white scar through LEFT eyebrow, white shirt, no splint, scar inside RIGHT forearm, seated at the green leather desk; blinds fully open, golden light on the desk. Start: wide on the study, Nico at the desk looking down at papers. He senses her, lifts his head and looks toward the door. End: his eyes on the door, golden light. Camera: wide, locked off. Silent, mouths relaxed. No zoom, cuts or morphing; faces and outfits match the reference.
```

- **Negative:**

```
text, subtitles, watermark, logo, zoom, push-in, camera shake, morphing, face drift, changed outfit, extra fingers, fused fingers, deformed hands, extra limbs, duplicate people, speaking, lip sync, talking mouth, blood, gore, visible wound, photorealistic, 3d render, cartoon, camera movement, pan, tilt, splint, cast, brace, bandage on forearm
```

### s62_c4  (NEW, start +28.0 s)

- Narration cue: "Two shots. That's all it took... One yes, said out loud, is how it ended."
- Attach: KF s62 still as start frame; REF-IVY (approved face); REF-NICO (approved face); optional: last frame of s62_c3 as start frame if Flow allows, else rely on KF
- Cut in: Nico looking at the door  |  Cut out: Final image: both in golden light, file between them
- Risk: file handoff
- **Prompt** (882 chars):

```
Painterly gouache-and-oil illustrated realism, cinematic noir, visible brush texture, film grain, 16:9. Carroll Street brownstone, fourteen stairs up to Nico's study, blinds open, golden afternoon light from the study window. Ivy: 28, freckles, red messy bun with a pen through it, square emerald ring over a thin plain gold band on LEFT ring finger, nothing at neck, gray cardigan, holding a thin file; Nico: 34, dark wavy hair, stubble, gray eyes, thin white scar through LEFT eyebrow, white shirt, no splint, in the golden study; blinds open. Start: Ivy at the doorway with a thin file. Nico rises from the desk and crosses to her; she holds the file out and he takes it with his RIGHT hand. They stand together in golden light, no kiss. End: both standing close. Camera: wide, locked off. Silent, mouths relaxed. No zoom, cuts or morphing; faces and outfits match the reference.
```

- **Negative:**

```
text, subtitles, watermark, logo, zoom, push-in, camera shake, morphing, face drift, changed outfit, extra fingers, fused fingers, deformed hands, extra limbs, duplicate people, speaking, lip sync, talking mouth, blood, gore, visible wound, photorealistic, 3d render, cartoon, camera movement, pan, tilt, ring on a chain, necklace, pendant, earrings, bracelet, extra rings beyond emerald and thin gold band, splint, cast, brace, bandage on forearm
```
