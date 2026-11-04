# Retention audit of `script.md` (proposals only; `script.md` is untouched)

**Status: proposals.** Nothing here has been applied, recorded, or measured. Every time below is an **estimate** from `word_count.json` (150 wpm + the script's `{p=}` pauses). In-chapter times (marked ≈) come from re-running that same model line by line and can drift ±2 s from the JSON. Real timing exists only after narration is recorded. The retention rules used (30-second check, 60-90 s re-hook, minutes 3-7 guard, stacked chapter exits, peak-end) are creator rules of thumb from the loaded retention skill, not guarantees. No channel data, no CTR, no benchmarks were available (`market_brief.md` is still blocked), and none are claimed.

Constraints I held: Ivy's plain dry voice; no new plot; `canon_ledger.md` holds (Ivy never claims to have seen who fired; the injured right hand is never offered as proof; no ring/chain before the wedding; ring on chain only on shift).

## 0. Runtime reality check (affects everything below)
| wpm | est. runtime | source |
|---|---|---|
| 140 | 36:20 | `word_count.json` |
| 150 | 34:01 | `word_count.json` |
| 160 | 31:58 | `word_count.json` |

The "~32 min" target is only met at about 160 wpm, which is brisk for a dry, quiet narrator. At 150 wpm the film is ~34 min. If 32:00 matters, cut ~100-150 words (README already lists candidates) rather than rushing the read. The last two chapters (CH18 93 s, CH19 102 s) are not among the shortest, so the ending has room. Shortest are CH10 (53 s) and CH15 (72 s).

## 1. The first 30 seconds (estimated, 150 wpm)
| Est. time | Shot | What the viewer gets | Verdict |
|---|---|---|---|
| 0:00-0:03 | s01 | "Two shots. That's all it took." Cold, no music | Strong. Keep. |
| 0:03-0:13 | s01 | Garage, 4:10, bumper, "what a life ending sounds like in concrete" | Slightly writerly; 25 words. Owner re-voice (see §4). |
| 0:13-0:38 | s02 | Fallen man, two guns, Nico, left-hand gun, her splint (59 words) | Content is right, but it is the longest unbroken block in the opening. |
| **0:30** | s02 | **The 30-second mark lands mid-sentence in the splint line.** | Nico has not yet spoken. |
| 0:38-0:43 | s03 | **Lion: "Go back inside, Dr. Marlowe. You were never here."** | The title's scene and the first second voice arrive *after* 30 s. |
| 0:43-1:05 | s04 | "Three days later I married him..." + promise | Good promise, but see swap #3 (the promise says "to the end" and pays at 20:14). |

**Fix:** trim ~7 s from s01-line 2 and s02 so Lion's line starts at about 0:31 (swaps #1 and #2). That is an estimate; confirm with the real read. Keep the 1.8 s silence before the line; the script's note already calls for it.

## 2. Chapter openings and closings (every chapter)
Times = chapter start from `word_count.json` (estimate). "Exit loop" = what is still open when the chapter ends (the chapter break is where viewers leave).

| Ch | Est. start | Opening line | Closing line | Exit-loop verdict |
|---|---|---|---|---|
| CH00 Two Shots | 0:00 | "Two shots. That's all it took." | "...Stay to the end and you'll hear one sentence I swore to under oath, the one I had never said to him." | Strong promise. Wording problem (swap #3). |
| CH01 3:05 | 1:05 | "It started at 3:05 that morning, with a man walking into my ER holding his own arm closed." | L: "It's a title. Thank you, Dr. Marlowe." | Warm button, **no open question** at the exit. (Intentional callback: this line returns at the end of CH17; do not change it.) Add one stacked line (swap #5). |
| CH02 4:10 | 3:16 | "Level two, spot 2-14. At 4:08 I found the charger in the cup holder." | "I had a name on my tongue. I didn't say it. I'm not proud of that." | Strong. |
| CH03 | 5:00 | "Saturday at eight, a woman in a rain jacket and a man in a navy suit sat on my couch." | "'I'll tell them,' I said. 'But I'm doing it as myself.'" | Opening is stage-setting (dip, swap #6). Closing is fine. |
| CH04 | 6:21 | "At seven that night I carried groceries up three flights and found my door unlocked and my lamp off." | "'I have conditions,' I said." | Best exit in the first half. Keep. |
| CH05 Terms | 8:50 | "His lawyer wrote it down in blue ink. One. I keep my residency, every shift." | L: "I said, I know." | Funny close, but the live question ("What's the other one?") was left 6 lines earlier. Re-seed (swap #7). |
| CH06 The Code | 10:30 | L: "I lasted three days before I tried to make a fist." | L: "...she had said my name to a computer." | Voice change at the right moment. Exit closes its own question; acceptable because CH07 opens on a ticking clock (8:52 a.m.). |
| CH07 I Do | 12:27 | "Monday, 8:52 a.m., eight minutes before I married a man I'd seen standing over a body..." | "Not a denial. A door closing. I tied the knot." | Strong both ends. |
| CH08 Leak | 14:17 | "Tuesday, the ER. At work I couldn't wear a ring under gloves..." | "...Nico's eyes dropped to the top drawer of his desk, for as long as it takes to read a clock." | Strong exit (plants Sal). Chapter is the longest (3:01); see dip D3. |
| CH09 Enzo | 17:18 | "Sunday lunch under the fig. Enzo excused himself and didn't come back." | L: "...I had to tell her she was never here." | Closes the film's biggest question (who fired) at ~51%. The closing line is the best callback in the script. Next chapter opens a new threat, good. |
| CH10 Lot 4471-B | 19:21 | "Then Theo was arrested." | "...an old man in a gray Lincoln that smelled of licorice." | Good exit. Middle is procedural (D4). |
| CH11 Yes | 20:14 | "Monday, Courtroom 6B. Holloway wanted the judge to call it a sham marriage." | "It smelled of anise." | Strong. Pays the CH00 oath line at 20:14 (see swap #3). |
| CH12 The Glove Box | 21:42 | L: "One-ten in the morning, in my uncle's garage." | "'Somebody else gets to tell you first,' I said." | Strong. |
| CH13 Uncle | 23:27 | "Tuesday, seven p.m. Sal arrived exactly on time with a box of pastry." | "He left for the airport that night, on an Italian passport he bought in September." | Villain exits, **nothing stacked**, with ~10 minutes still to run (swap #11). |
| CH14 Lemon Trees | 24:47 | "At one that morning Bianca Moretti texted me her dinner video, three question marks, and Don't tell my father." | "Paulie also told Reyes who had stood at the top of the ramp that morning in October, and saw who fired. She wouldn't tell me." | Opening asks the viewer to care about a dinner the film never showed (D5). Exit loop is real but the viewer already knows the answer; tie it to the cost planted in CH09 (swap #12). |
| CH15 Kitchen Island | 26:12 | "Saturday night someone lured Nico to the port with a hurt watchman." | L: "...She slept in the chair with her hand on my splint." | Good. "I couldn't say it" opens the loop that CH18 pays. |
| CH16 Bath Avenue | 27:24 | "Monday night Lucia found Enzo's room empty." | L: "I came in with nothing because you were in that room. That's the truth, Ivy." | Strong. |
| CH17 Second Oath | 28:58 | L: "Enzo turned himself in at two-fourteen Tuesday morning." | "He hadn't called me that since the first night. I did not like it at all." | Strong exit. Opening is a dense 150-word block (D6). |
| CH18 Term Six | 30:45 | "That evening there was a cream envelope on the hall table. Term Five." | "The next morning Teresa put the divorce papers in the oven." | Good payoff button. **Teresa is never introduced** (see §5). |
| CH19 April | 32:18 | "April. The lemon trees came out of their burlap." | "...One yes, said out loud, is how it ended." (+ optional CTA) | The loop closes on the film's first line. Keep. |

## 3. Where attention is most likely to dip (editorial judgment, not measured)
| # | Est. window | Chapter | Why | Mitigation |
|---|---|---|---|---|
| D1 | 5:00-6:21 | CH03 | First scene with no physical danger; two official names, a canal, an informant fact, a subpoena, in 80 s. Falls right after the garage payoff, inside the "minutes 3-7" guard zone. | Swap #6 (stake first). The stakes raise follows at 6:21 (the proposal) and the supply-room attack, so this is a short dip. |
| D2 | 10:30-12:27 | CH06 | Longest stretch with no scene conflict: Nico alone, then Enzo and Sal introduced in monologue. | Keep (it is the voice change and plants Enzo/Sal). Direct Lion to shorter breaths; his first line (the failing fist) is a good physical hook. |
| D3 | 15:15-16:15 | CH08 | "A week later I set a trap..." compresses trap, ambush, note-pinning and FBI steps into one 70-word line. Summary tone. | Add a pause after "leave through level two" and after "waited at the exit". No text change needed. |
| D4 | 19:21-20:14 | CH10 | Forms, lots, dates, a pharmacy director. The lowest-energy 53 s in the film. | Swap #10. |
| D5 | 24:47-25:40 | CH14 | The Moretti dinner was cut from the film; viewer meets Bianca, Aldo, Paulie, Lucia's guilt cold. | Optional one-line plant (§5 item A), or accept it and let the owner's description/CTA point to the book. |
| D6 | 28:58-30:00 | CH17 | Lion's visiting-room paragraph is 7 logistics in one breath (surrender, gun, planter, lawyer, divorce). | Add pauses; keep the text. |
| D7 | 32:18-33:30 | CH19 | The epilogue is a list of eight fates in one 198-word block, after the emotional peak. | Swap #13 (reorder so it ends on Nico's smile). |

**Open-question coverage:** the big loops are (1) who fired (named at 0:43, paid at ~19:00), (2) the oath sentence (named at 1:05, paid at 20:14), (3) the other reason (CH05 8:50, paid at CH18 ~32:00), (4) "once without them" (planted 20:14 in CH11, paid in CH15 ~26:50 and CH18). Loop (3) and (4) carry the last third. They are the film's best structure; do not cut them.

## 4. Re-hook line swaps (table)
"Shot" = shot id in `script.md`. "Proposed" keeps Ivy's flat, plain voice and uses only facts already in the script or ledger. Word deltas are approximate.

| # | Shot (est. time) | Current line | Proposed line | Why |
|---|---|---|---|---|
| 1 | s01 (0:03) | "Ten past four that Friday morning, crouched behind my own bumper in a hospital garage, I learned what a life ending sounds like in concrete." | "Ten past four that Friday morning. I was crouched behind my own bumper in a hospital garage." *(owner may add her own plain sentence about the sound)* | Cuts ~9 words (~3.6 s) so Nico's line moves toward 0:30. Drops a writerly image; see §4a. |
| 2 | s02 (0:13) | "I looked over the hood. A man was sliding down the side of a silver sedan, a gun a foot from his open hand. The man standing over him held a different gun, in his left hand. His right arm was in the plaster splint I had built thirty minutes earlier, in bay fourteen, with my own two hands." | "I looked over the hood. A man was sliding down a silver sedan, a gun a foot from his open hand. The man standing over him held a different gun, in his left hand. His right arm was in the splint I had built thirty minutes earlier. With my own two hands." | Same facts (left-hand gun, second gun, her splint), 8 fewer words (~3 s). Keeps "with my own two hands". "Bay fourteen" is re-established in CH01. |
| 3 | s04 (0:43) | "...Stay to the end and you'll hear one sentence I swore to under oath, the one I had never said to him." | "...Stay for both. I swore two sentences under oath in this story. One of them I had never said to him." | The current promise says "to the end" but "Yes. I love him" is sworn at ~20:14 (59% in): a mild promise gap. Two oaths are canon (CH11 "Yes", CH17 "No. I heard two shots"). The second pays at ~29:20 and echoes the opening "Two shots". Check against your intent; if you keep one sentence, change "Stay to the end" to "Stay and you'll hear". |
| 4 | s05 (1:05) | "It started at 3:05 that morning, with a man walking into my ER holding his own arm closed." | No change. | Concrete image and a clean re-hook after the promise; listed so nobody "improves" it. |
| 5 | s08 end (≈3:10) | L: "It's a title. Thank you, Dr. Marlowe." {p=0.8} | Keep the line (it returns at the end of CH17). **Add after it:** H: "I thought that was the strangest part of the night." {p=0.6} | Stacks a micro-loop on a warm exit; the CH00 viewer already knows the night is about to turn. ~10 words, ~4 s. |
| 6 | s13 (5:00) | "Saturday at eight, a woman in a rain jacket and a man in a navy suit sat on my couch. Special Agent Reyes. Prosecutor Holloway. A city crew had pulled a man out of the Gowanus Canal." | "Saturday at eight, an FBI agent and a prosecutor sat on my couch. A city crew had pulled a man out of the Gowanus Canal. Special Agent Reyes. Prosecutor Holloway." | Stake before names. Same facts. Rain jacket / navy suit remain in the image. |
| 7 | s20 end (≈10:25) | L: "I said, I know." {p=0.8} | Keep. **Add after it:** H: "He still hadn't told me the other reason." {p=0.6} | The unanswered "What's the other one?" is the loop that pays at CH18. Re-seed it right before the Lion voice change, when viewers decide whether to stay. |
| 8 | s31 (≈15:15) | "A week later I set a trap: I told Bell I had a secret night shift Wednesday and would leave through level two. At 10:55 a man with a bandaged right hand waited at the exit..." | No text change. Add `{p=0.6}` after "leave through level two." and after "waited at the exit." | Dip D3: gives the trap room to be a scene, not a summary. |
| 9 | s32 (≈16:05) | "I gave him until noon to call the FBI. He asked for one more night. I said yes. I have thought about that yes every day since." | **Owner decides.** The last sentence is an adaptation addition (ledger §7). See §4a. | It is the film's only sentence that puts a regret on Ivy, and it is the one the owner must be able to say as her own. |
| 10 | s39 (19:21) | "I had my own evidence. The sticker on Enzo's card said Lot 4471-B. So did the pills in Theo's car. I cornered the hospital pharmacy director with an old committee letter. Forty-two cards of that lot had been 'destroyed' on a form dated September twenty-ninth, co-signed by Dr. Marcus Bell. The tech said nobody counted. The signing doctor carried the bag out himself, past the garage." | "I had my own evidence. The sticker on Enzo's card said Lot 4471-B. So did the pills in Theo's car. Forty-two cards of that lot had been 'destroyed' on September twenty-ninth, on a form co-signed by Dr. Marcus Bell. I'd cornered the pharmacy director with an old committee letter to see it. The tech said nobody counted. The signing doctor carried the bag out himself, past the garage." | Lead with the answer (curiosity), then show how she got it. Same facts, same length. |
| 11 | s46 end (≈24:45) | "He left for the airport that night, on an Italian passport he bought in September." {p=0.8} | Keep. **Add after it:** H: "Sal was gone. Carmine Brancato wasn't." {p=0.6} | The villain exits with 9+ minutes left. Brancato is the open threat (arrested in CH16); this stacks the next question without new plot. |
| 12 | s48 end (≈26:05) | "Paulie also told Reyes who had stood at the top of the ramp that morning in October, and saw who fired. She wouldn't tell me." {p=0.8} | "Paulie also told Reyes who he had watched fire from the top of that ramp. She wouldn't tell me what he said. I already knew whose name it would be." {p=0.8} | Fixes a loop the viewer can already answer by making the question "what will it cost Enzo?", which CH09 planted ("I didn't know yet what it would cost"). No new fact. |
| 13 | s60 (32:18) | Order: Lucia, Theo, Enzo, Sal, Danny (+donor), Nico "I'm not going to answer that, and smiled", "I finish residency in June." | Same sentences, reordered: Lucia, Theo, "I finish residency in June.", Enzo, Sal, Danny (+donor), Nico "I'm not going to answer that," and smiled. | Ends the list on a callback and a smile instead of a logistics line, right before Reyes arrives at the gate. Add `{p=0.5}` after each fate. |
| 14 | s55 (≈29:10) | "I waived my privilege myself, that morning at six, for October third and nothing else. Reyes's first text on my wedding night was true: it was mine." | "I waived my privilege myself, that morning at six, for October third and nothing else. Nico had told me once that the privilege belonged to the wife. So did the choice to use it." | "Reyes's first text on my wedding night" is never shown, so a first-time viewer can't parse it. This pays off Nico's CH04 line ("The privilege belongs to the wife") and the tagline ("the choice to speak belongs to the wife"). Check against the novel's wedding-night text before accepting. |

### 4a. The 6 lines the owner should re-voice herself
I flag, I do not write replacements. These are the lines carrying the most feeling or a claim only the author can own. Keep the beat in each; use her own words.

1. **s01, CH00 (0:03), "I learned what a life ending sounds like in concrete."** The first sentence anyone hears in her voice after the hook. "Sounds like in concrete" is the most writerly phrase in the script. Plain version wanted.
2. **s11, CH02 (≈4:35), "...while other people decided I should stay out of the way, I was fourteen."** The only glimpse of her wound. The script gives one clause; only she knows how much of it she wants to say. Keep it short.
3. **s32, CH08 (≈16:05), "I have thought about that yes every day since."** Listed in ledger §7 as an adaptation addition, not canon. She should say it, change it, or cut it.
4. **s40, CH11 (≈20:25), "I decided in that second I'd rather be in danger in my own life than safe in somebody else's." and "Yes. I love him..."** The thesis of the film and the first oath. Also named in the README's list.
5. **s50, CH15 (≈26:50), Ivy's "I love you. I wanted you to hear it once without anyone else in the room."** In `script.md` this sits inside a Lion (`L:`) line, so Nico's voice would read Ivy's declaration. Production note: under the voice rule (Heba = Ivy, Lion = Nico), split it so Heba says this sentence and Lion says the rest. That is a script edit; flagged, not made.
6. **s62, CH19 (≈33:30), the last paragraph ("...Two shots. That's all it took... One yes, said out loud, is how it ended.")** Peak-end line. It must sound like the author, not the adapter.

*Honorable mentions (also in the README list):* "Go back inside, Dr. Marlowe." (Lion), "It's my uncle." (Lion), "I'm not armed, Carmine." (Lion), "She does." (Heba).

## 5. Dangling or unclear items found while auditing (owner decisions; I did not change them)
A. **Aldo's dinner (CH14) has no setup.** The film never shows the welcome dinner (ledger timeline: Wed Oct 8, "Aldo's shrimp poisoning; Paulie flees"). An optional one-sentence plant could sit at the end of Joey's paragraph in CH08 (~+30 words, +12 s). I did not write it because the exact event (poisoning vs. allergy) should be checked against the novel pp.69-79, which I cannot see; the source text is not in the repo.
B. **"I said it too hard. He couldn't know why." (s08, CH01).** The script never says why. If the reason is in the novel, one line pays it; otherwise cut those last two sentences. Dangling reasons read as unpaid promises.
C. **"Everybody knew a rule about this man. Nobody had told me." (s05).** The rule is never named. It pays implicitly, but a half-line in CH04 or CH05 could close it.
D. **"A pack of gum" (s48, CH14):** "I chained a deli receipt and a pack of gum to Paulie Ferraro." The gum is not set up anywhere in `script.md`. I could not confirm what it refers to from the ledger.
E. **"Teresa" (s58, CH18):** the closing joke depends on a person the film never introduced. The ledger only mentions "Teresa's small white cross" [p.236] and cut "Teresa-sheets testimony", so I could not confirm her role. A five-word tag the first time she is named would fix it. **"Mr. Feld" (s42)** has the same issue (the lawyer in CH05 is unnamed).
F. **Optional CTA (last 54 words):** it lists "the night on the kitchen island" as a scene the film had no room for, but CH15 is titled "The Kitchen Island" and shows that night. A viewer will notice. Ledger §7 lists real cut material (the gala, most of the welcome dinner, the mock cross-examination); swapping one of those in is safer. Check with the novel.
G. **Ending is not a cliffhanger.** s61 raises Nico's father as an FBI informant, but s62 closes the film emotionally (she climbs the stairs to tell him; "We don't do silence in this house anymore"). I read that as a closed arc with a forward-looking note, consistent with the brief. If the owner thinks it could read as a sequel hook, the fix is a new closing beat, which would be new plot, so I did not propose one.
H. **Stale README numbers.** `README.md` still says 4885 words and lists CH07 289 / CH08 407; `word_count.json` says 4892 total, CH07 262, CH08 441. The README's chapter markers are 1 s off in places. I used the JSON everywhere and did not edit the README.

## 6. Checklist result (retention skill)
| Check | Result |
|---|---|
| First line states the title's scene | Yes |
| Big question named in first minute | Yes (0:43-1:05) |
| Plant ≥5 min before each major reveal | Yes (Enzo planted 10:30, revealed 17:18; Sal planted at CH06/CH08, revealed 23:27) |
| Minutes ~3-7 stakes raise + place/voice/time change | Place changes at 3:16 and 5:00; stakes raise at 6:21; **no voice change until 10:30** |
| No recap | One deliberate echo in CH17 (the oath); not a recap |
| Last two chapters not the shortest | Pass |
| Every promise paid | Mostly; see §5 B-E and swap #3 |
| Session link after payoff | Plan in `packaging_v2.md` |
| Runtime measured | **No, estimated only** |
