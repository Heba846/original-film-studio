# Implement the twenty-minute narrated film in the existing Remotion project

The author wants a complete film of about twenty minutes, not a trailer. The approved look is the existing painterly Flow footage. Total remaining Flow generation budget is capped at 1,000 credits. Claude's coding usage does not provide Flow generation credits.

Read Film_20min_Script_EN.md, Production_Plan_AR.md, and edit_decision_list.json first. Preserve src/index.tsx's existing Opening composition and the working development server. Create a separate composition rather than replacing Opening.

## Implementation

1. Read the edit decision list. Reuse the exact existing WAVs for entries with audio_status=existing_unchanged. Entries marked needs_pickup must not silently fall back to the old recording: the text has changed.
2. Measure actual file durations before building the final timeline. Planned times are estimates until the four new recordings exist. Recalculate scene, caption, and chapter positions after any recording changes. Preserve natural voice speed.
3. Keep an explicit media manifest: segment ID, narrative event, source file, in/out points, continuity phase, and permitted reuse. A missing visual is an editor-only placeholder, never disguised as finished footage. Block final export if required audio or visuals are missing.
4. Start by producing one coherent 60–90 second section with complete shot coverage. Do not generate the entire film blindly. The first section must establish geography and who is speaking to whom; narrator voiceover does not require visible lip-sync.
5. Use code for exact evidence lettering, readable contract clauses, short dates, atmosphere layers, restrained parallax, and transitions. Do not turn the whole film into typography, a generic slideshow, or a static talking head.
6. Reuse footage when the story reinterprets it. Do not reuse a character's speaking face under unrelated words. Do not flip footage horizontally: the injured arm is RIGHT and the eyebrow scar is LEFT. Observe ring, clothing, weather, and injury chronology.
7. Import the three existing Flow clips first, but inspect each before approving it. They contain continuity errors. No paid generation is implied by loading the editor.
8. Keep a budget ledger. Plan 700 credits for primary results, 200 for retakes, 100 unspent reserve. Check the actual selected model cost and number of outputs. No automatic upgrade to a more expensive model. If supporting images also cost credits, charge them to the same cap.
9. Preview at 720p and render at source-appropriate resolution. A larger export does not restore missing detail. Export SRT and chapter markers separately.
10. Report actual completed work, missing assets, measured runtime, and remaining budget. Never claim that a script or a placeholder timeline is the completed film.

## Editorial constraints

Keep the ending and the causal evidence chain. Do not add invented dialogue or new plot twists. Four exact pickup paragraphs are provided in Pickup_Lines_EN.md; only these require new narration for this cut. Any further rewriting needs an explicit change list.

The voiceover can bridge a scene while the images show environments, reactions, or objects. An eyeline, a shot of the listener, and correctly placed sound establish a conversation more reliably than laying speech over an unrelated moving face.
