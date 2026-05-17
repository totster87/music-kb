---
title: CLAUDE
type: note
permalink: music-kb/claude
---

# music-kb — Claude Instructions

## Basic Memory
- MCP server: `basic-memory` — scoped to `project="music-kb"` only
- **Always pass `project="music-kb"`** to every Basic Memory tool call — never use the default project
- Never write to or read from any other Basic Memory project

### After every practice session
1. Create a session note at `practice/sessions/YYYY-MM-DD-instrument.md` using `write_note`
2. Include: what was practiced, BPMs reached, specific issues observed
3. Add a `## Relations` section using wikilink syntax (see template below)
4. Update the repertoire file for any song worked on — update `current_max_bpm` in frontmatter if it improved
5. Commit and push all changes

### Session note format
See `practice/sessions/2026-05-11-guitar.md` for a canonical example.
Use these relation types in the `## Relations` section:
- `practiced` — points to a repertoire entity (song)
- `practiced_from` — points to a book/method entity
- `revealed_issue` — points to a technique entity (bottleneck)

## ⚠️ CRITICAL — READ FIRST
- **NEVER read, open, or load any `.png`, `.pdf`, or `.html` file. Ever. Under any circumstances.**
- **Do NOT auto-trigger any routines or read any files on session start**
- When showing exercises, songs, or routines: **generate or update an HTML file** and tell the user to open it in Safari. Never output tab or images in chat.
- Use `python docs/viewers/generate_viewer.py` or write a custom HTML file to `docs/viewers/`
- After generating: commit, push, then give the full GitHub Pages URL: `https://totster87.github.io/music-kb/docs/viewers/<filename>.html`
- Always output full https:// links — never local file paths. Links must be tappable on iPhone.

### Session start sequence
1. Call `mcp__basic-memory__recent_activity` with `project="music-kb"` and `timeframe="7d"`
2. If it succeeds: greet the user with a brief summary of what was recently worked on
3. If it fails or tools are unavailable: tell the user immediately — **"Basic Memory could not load — MCP server may not be running"** — then greet normally
4. Do NOT read any other files, generate routines, or do anything else until the user asks

---

## ⚠️ GitHub Pages + Images — What Works and What Does NOT

### Filenames
- ✅ **Use hyphens:** `Drum-Routine-2026-05-04.html`
- ❌ **Do NOT use spaces:** `Drum Routine - 2026-05-04.html` — spaces break GitHub Pages URLs even when URL-encoded

### Images (score pages)
All score PNGs in `docs/rendered/` are stored in **Git LFS**. GitHub Pages serves LFS pointer files, not the actual image content.

- ✅ **Use `media.githubusercontent.com` URLs** — this is GitHub's LFS media CDN and serves actual image content:
  ```
  https://media.githubusercontent.com/media/totster87/music-kb/main/docs/rendered/<slug>/page-XXX.png
  ```
- ❌ **Do NOT use relative paths** like `../rendered/<slug>/page-XXX.png` — GitHub Pages serves the LFS pointer text, showing a broken image
- ❌ **Do NOT use `raw.githubusercontent.com`** — also serves the LFS pointer, not the image

### Template for score images in HTML viewers
```html
<img src="https://media.githubusercontent.com/media/totster87/music-kb/main/docs/rendered/<slug>/page-XXX.png" alt="...">
```

### Swipe carousels for multi-page sections
When a routine block references **2+ pages from the same source**, do NOT stack
them vertically. Wrap them in a swipe carousel so they take the space of a
single page. iPhone Safari handles the swipe natively via CSS scroll-snap.

Pattern (drop the CSS into `<style>`, the script before `</body>`):
```html
<div class="swipe-wrap">
  <div class="swipe">
    <div class="slide"><div class="score-label">Book — p.X</div><img class="score-img" src="..."></div>
    <div class="slide"><div class="score-label">Book — p.Y</div><img class="score-img" src="..."></div>
  </div>
  <div class="swipe-counter">1 / 2</div>
  <div class="swipe-hint">← swipe →</div>
</div>
```
Shortcut: write the routine with plain `score-section` blocks containing
multiple `score-img` tags, then run `python docs/viewers/add_swipe_carousels.py`
to retrofit (idempotent — safe to re-run).

### Deployment
- GitHub Pages deploys from `main` branch — all viewer files must be on `main` to be accessible
- Feature branches are NOT served by GitHub Pages
- CDN propagation takes 1–2 minutes after a push before changes are live

---

This is a personal music practice knowledge base.

---

## Who This Is For

The user is a drummer and guitarist:
- **Drums:** Metal + jazz/funk. Working through method books with BPM logging. Has practice pad and full kit.
- **Guitar:** Drop D / metal. Currently learning Better Lovers — Highly Irresponsible.
- **Goal:** Tailored practice routines from owned books, BPM tracking, exercise pages displayed on request.
- **Book familiarity:** Has worked through most books in the library. Feel free to pull from any book — Chapin, Riley, Latham, Reed, Donati, 30 Dirty Grooves, 20 Chops, ABR Messengers, etc. Don't default to the same 2–3 books every session. Vary it.
- **Recording goal:** Occasionally flag one block per routine as a recording target — one take, no editing, just capturing progress. Start small and build the habit.

---

## Trigger Phrases

### "load my session" / "start practice" / "what am I working on"
1. Read `practice/Practice Log.md` — show last 5 entries
2. Read each active guitar repertoire file and show current section + known issues:
   - `repertoire/Better Lovers - Lie Between the Lines.md`
   - `repertoire/ABR - Truth of a Liar.md`
   - `repertoire/ABR - Treatment.md`
   - `repertoire/BTBAM - Prequel to the Sequel.md`
3. Summarise the suggested session structure (do NOT auto-load any images)
4. Ask: "Want me to pull up the current page?"

### "guitar routine" / "make me a guitar routine"
Do NOT default to any specific song. Generate a fresh varied routine by:
1. Read `practice/Practice Log.md` (last 5–10 entries) to see what was last worked on — avoid repeating the same thing
2. Read `repertoire/*.md` for active songs to see current ceilings + bottlenecks
3. Build a balanced session pulling from multiple sources: technique exercises, song excerpts, creative exploration
4. Draw from: Better Lovers (Highly Irresponsible), ABR Truth of a Liar, ABR Treatment, BTBAM Prequel to the Sequel, ETID Low Teens, DEP, any relevant technique concepts
5. Generate an HTML file at `docs/viewers/Guitar-Routine-YYYY-MM-DD.html` with the routine written out — include embedded score pages for any referenced exercises/songs
6. Commit, push, output the GitHub Pages URL: `https://totster87.github.io/music-kb/docs/viewers/Guitar-Routine-YYYY-MM-DD.html`
7. After the session ask for BPM + difficulty notes, log to Practice Log, commit and push

**Warm-up block — always include one of these guitar workout sources:**
Rotate page by page across sessions — don't repeat the same Vai page two routines in a row. Track the last-used page in the routine viewer so the next routine picks the following one. When a source is exhausted, cycle back to page 1.
- **Steve Vai — 10 Hour Guitar Workout** (`vai-10-hour-workout`, 6 pages) — primary warm-up source. Embed the day's page via the swipe carousel, brief BPM target, 5–8 min block.
- **120 Right Hand Studies — Giuliani** (`120-right-hand-studies-giuliani`, 15 pages) — alternate warm-up source when Vai feels stale. Classical right-hand control, transfers to pick-hand independence.
- **Scale Studies for Jazz Guitar — Rick Stone** (`scale-studies-jazz-guitar-stone`, 24 pages) — alternate when scale/legato fluency is the priority.
- The block should always reference the slug and embed the score page via the standard `media.githubusercontent.com` CDN URL.

### "drum routine" / "make me a drum routine"
Do NOT default to any specific exercise. Generate a fresh varied routine by:
1. Read `practice/Practice Log.md` (last 5–10 entries) to see what was last worked on — avoid repeating the same thing
2. Read `library/*.md` exercise catalogs — these list every exercise that's been worked on per book, current ceiling, bottlenecks, and untried candidates. **This is the primary picker.** Bias toward `bottlenecked` and `needs-revisit` statuses; rotate `in-rotation`; pull from `## Candidates for Rotation` sections when fresh material is wanted. Add new entries to the relevant catalog after the session.
3. Build a balanced session. Draw freely from the full book library — don't default to the same books each time. Good rotation includes:
   - Warm-up: Stick Control, rudiments, or a Reed syncopation reading exercise
   - Technique: Morello, Chapin, PI Rock, Latham funk, 30 Dirty Grooves, 20 Chops — rotate these
   - Double bass: Donati (any section — single strokes, hand-foot independence, sextuplets)
   - Music application: ABR Messengers, The Roots You Got Me, or any transcription
   - Jazz/bop: Riley Art of Bop, Chapin Advanced Techniques — don't neglect these
   - **Burnout finisher (always last):** Fast double bass, blast beats, doubletime swing, or any high-intensity free-form block. No click, no structure — just push. 5 min max.
     Preferred burnout types (rotate these):
     - Straight 16th endurance — both feet alternating 16ths at max tempo, simple hand groove on top, hold until form breaks
     - Sextuplet sprint — groups of 6 on the feet, push tempo each minute, stop when it blurs
     - Kick + snare unison — feet and snare hit together on every note, build speed until collapse
     - Doubletime bop — take a swing tempo and double it, hold the ride feel as long as possible
     - Trading bursts — 4 bars medium swing / 4 bars full doubletime, alternate
     - Open sprint — no rules, no click, full kit, play as hard and fast as possible for 3 min
     Note: user is NOT interested in gravity blast. Has "The Evolution of Blast Beats" by Derek Roddy — no pages ingested yet, do not reference specific exercises until ingested.
4. Generate an HTML file at `docs/viewers/Drum-Routine-YYYY-MM-DD.html` with the routine written out — include embedded score pages for referenced exercises
5. Commit, push, output the GitHub Pages URL: `https://totster87.github.io/music-kb/docs/viewers/Drum-Routine-YYYY-MM-DD.html`
6. After the session ask for BPM + difficulty notes, log to Practice Log AND update the relevant `library/<slug>.md` catalog (add BPM history entry, update ceiling/status/last_worked), commit and push

### "show me page X of [book]" / "pull up page X"
Read and display the correct PNG. Path format: `docs/rendered/<slug>/page-XXX.png`

Book slugs:
- Better Lovers: `better-lovers-highly-irresponsible`
- Master Studies (Morello): `master-studies-morello`
- Progressive Independence Rock: `progressive-independence-rock`
- Double Bass Freedom (Donati): `double-bass-freedom`
- Stick Control: `stick-control`
- Art of Bop Drumming: `the-art-of-bop-drumming`
- Advanced Techniques (Chapin): `advanced-techniques-modern-drummer`
- Advanced Funk Studies (Latham): `advanced-funk-studies`
- Ted Reed Syncopation: `progressive-steps-syncopation`
- ABR Messengers Drums: `abr-messengers-drums`
- The Roots — You Got Me: `the-roots-you-got-me`
- DEP — One Of Us Is The Killer (guitar): `dep-one-of-us-is-the-killer`
- 30 Dirty Grooves (drums): `30-dirty-grooves`
- 20 Chops (drums): `20-chops`

### "ingest inbox" / "process inbox" / "catalog screenshots"
1. Run `python docs/ingest.py --auto` to list what's in `docs/inbox/`
2. For each file, ask the user: what book/source is this from, and what page number?
3. Run `python docs/ingest.py` interactively OR manually move the file: `docs/inbox/<file>` → `docs/rendered/<slug>/page-XXX.png`
4. Update `docs/page-index.json` to include the new page number under the correct slug
5. `git lfs track "docs/rendered/<slug>/*.png"` if new slug
6. `git add` the moved file + `.gitattributes` + `page-index.json`, commit and push
7. Confirm CDN URL: `https://media.githubusercontent.com/media/totster87/music-kb/main/docs/rendered/<slug>/page-XXX.png`

**iPhone upload flow:** GitHub app → `docs/inbox/` → tap + → Upload file → commit to main → say "ingest inbox" in Claude

### "make me a routine" / "build a session"
Ask: pad or kit? How long? Then build a structured session. Display pages only when walking through each exercise.

### "generate viewer for [song/exercise]"
Run: `python docs/viewers/generate_viewer.py <slug> "<title>" <start> <end>` then commit and push.

---

## Active Work

### Guitar — Better Lovers, Lie Between the Lines
- **Tuning:** Drop D
- **Transcription pages:** `docs/rendered/better-lovers-highly-irresponsible/page-007.png` to `page-019.png`
- **Current section:** Section A — Clean Intro (♩=99, let ring, pages 7–8)
- **Known issue:** String skipping on all-downpicking — clips wrong string mid-skip
- **Repertoire file:** `repertoire/Better Lovers - Lie Between the Lines.md`
- **Viewers (open in browser):**
  - `docs/viewers/Better Lovers - Lie Between the Lines (Clean Intro).html`
  - `docs/viewers/Better Lovers - Lie Between the Lines (Full Song).html`

### Guitar — ABR, Truth of a Liar
- **Tuning:** Drop D (confirm)
- **Current section:** Section A
- **Max BPM:** 120 (target 130)
- **Known issues:** String skipping is the bottleneck — single-string tremolo is faster; pick attack inconsistency; unclear how hard to hit strings
- **Approach:** BPM automation from 75, +1 BPM increments. 105 iffy, 118 sloppy, 120 max
- **Repertoire file:** `repertoire/ABR - Truth of a Liar.md`
- **Viewer:** Not yet generated — say "generate viewer for ABR Truth of a Liar" when ready

### Guitar — ABR, Treatment
- **Tuning:** C G C F A D (Drop C)
- **Current section:** Section A — Intro (Guitar 1 only)
- **Max BPM:** ~130 (target 195)
- **Known issues:** Pinch harmonics frequently missed — pick angle and squeeze timing; sloppy above 130
- **Repertoire file:** `repertoire/ABR - Treatment.md`
- **Viewer:** Not yet generated — say "generate viewer for ABR Treatment" when ready

### Guitar — BTBAM, Prequel to the Sequel
- **Tuning:** C# standard — standard down 3 half steps (high→low: C# G# E B F# C#)
- **Tempo:** Section A ♩=100 · Section B ♩=120 (starts at 1:00)
- **Tone:** Distortion w/ delay, palm muted throughout Section A
- **Current section:** Section A intro — lead melody (mm.1–16). Section B (mm.19+) not yet started.
- **Max BPM:** 80 (target 100 = song tempo)
- **Source slug:** `btbam-prequel-to-the-sequel` — single-page stand-in tab from screenshot until full PDF acquired
- **Score path:** `docs/rendered/btbam-prequel-to-the-sequel/page-001.png`
- **Known issues:** Pick accuracy on descending runs — clips wrong string even at slow tempos
- **Repertoire file:** `repertoire/BTBAM - Prequel to the Sequel.md`
- **Viewer:** `docs/viewers/BTBAM-Prequel-to-the-Sequel.html` — auto-shows page-001.png once saved
- **When building a routine block for BTBAM Prequel:** always reference the C# standard tuning, always embed the page-001 score image via the CDN URL, always note distortion+delay tone

### Drums
- **Morello Groups of Four with Fill-Ins** (p.71): 72 BPM — left foot unstable at higher tempos, speeds up/flutters; focus on evenness not speed
- **Morello Table of Time** (p.43): 53 BPM halftime — rushes on subdivision transitions. NOTE: p.43, not p.8
- **PI Rock Part 3, exercises 1–4** (p.9): ~75 BPM — losing control on 16th note alternating hats when right hand hits snare; groups of 3 in second measure are the problem point
- **You Got Me (The Roots)**: 83 BPM — steady, feels elementary but internal clock not 100% solid

### Suggested Session Structure
1. Stick Control p.5 — warm up hands
2. Morello Groups of Four with Fill-Ins (p.71) — double bass, focus on left foot evenness
3. PI Rock Part 3 exercises 1–4 (p.9) — independence, isolate the groups-of-3 snare problem
4. Morello Table of Time (p.43) — subdivision transitions
5. You Got Me — music application

---

## Book Library

All PDFs in `docs/`, all pages pre-rendered in `docs/rendered/<slug>/`. Only read images when explicitly requested.

**Page selection rule:** When embedding score pages in routines, favour pages from the middle of the book. Early pages (covers, TOC, forewords, bios, introductions) and late pages (indices, afterwords) are often text-heavy and useless as exercises. Pages with minimal words and mostly notation are the target — if a page has more prose than staves, skip it and go deeper into the book.

| Slug | Title | Author | Pages | Key Pages |
|------|-------|--------|-------|-----------|
| `double-bass-freedom` | Double Bass Drum Freedom | Virgil Donati | 135 | Ch.1 Getting Started: p.6–27 / Ch.2 Left Foot Technique: p.28–36 / Ch.3 Developing Single Strokes: p.37–47 / Ch.4 Creative Single Strokes: p.48–59 / Ch.5 16th Note Triplet Series: p.60–73 / Ch.6 16th Note Series: p.74–82 / Ch.7 Double Stroke Rolls: p.83–100 / Ch.8 Paradiddles: p.101–108 / Ch.9 Bass Drum Flams: p.109–118 / Ch.10 Recorded Works: p.119–135 |
| `progressive-independence-rock` | Progressive Independence: Rock | Ron Spagnardi | 162 | S1 Right Hand 8th Notes: p.3–29 / S2 Right Hand Quarter Notes: p.30–56 / S3 Right Hand Up-Beats: p.57–83 / S4 Right Hand Sixteenth Notes: p.84–109 / S5 16th Note 1E&: p.110–136 / S6: p.137–162 / Note: "Part 3 combos p.9" = S1 Snare/Bass Drum Combination |
| `master-studies-morello` | Master Studies | Joe Morello | 97 | Accent Studies: p.7–19 / Buzz Roll Studies: p.20–29 / Stroke Combination Studies: p.30–39 / Control Studies (Table of Time p.43, Stone Killer p.54): p.40–65 / Fill-In Studies (Groups of Three p.66, Groups of Four p.70): p.66–76 / Ostinato Studies: p.77–81 / Flam Studies: p.82–93 |
| `the-art-of-bop-drumming` | The Art of Bop Drumming | John Riley | 68 | Time Playing: p.6–14 / Comping: p.16–32 / Soloing: p.34–45 / Brushes: p.47–53 / Jazz Essentials (Shuffle, Waltz, Samba, Mambo): p.55–60 / Charts: p.63–68 |
| `advanced-techniques-modern-drummer` | Advanced Techniques Vol.1 | Jim Chapin | 55 | Coordinated independence, jazz/be-bop / p.6 confirmed text — do NOT use p.1–13 / Dotted 8ths+16ths: p.9–14 / Eighths: p.16–20 / Triplet: p.25–29 / Sixteenths: p.30–33 / Solo Exercises: p.41–55 |
| `stick-control` | Stick Control | George Lawrence Stone | 50 | Single Beat Combinations: p.5–7 / Triplets: p.8–9 / Short Roll Combinations: p.10–15 / Flams: p.16–23 / Short Rolls in 6/8: p.24–29 / Combinations in 3/8: p.30–32 / Flam Triplets: p.34–37 / Short Roll Progressions: p.38–46 |
| `advanced-funk-studies` | Advanced Funk Studies | Rick Latham | 51 | p.5 = author bio — do NOT use / Introductory Exercises: p.10 / Fixed Hi-hat Patterns: p.11–15 / Combination Exercises: p.16–18 / Fill Patterns: p.19 / Funk Patterns: p.20–24 / Transcriptions (Gadd, Garibaldi, Mason, Erskine etc.): p.26–33 / Solos: p.34–51 |
| `progressive-steps-syncopation` | Progressive Steps to Syncopation | Ted Reed | 61 | Foundation (quarter/eighth/dotted/triplet/16th notes): p.3–27 / Syncopated Eighth Notes: p.28–35 / Syncopation Exercises 1–9: p.36–44 / Accents: p.45–59 |
| `abr-messengers` | ABR — Messengers (Guitar) | — | 146 | NOT YET CHAPTERIZED — do not use in routines |
| `abr-messengers-drums` | ABR — Messengers (Drums) | — | 121 | Truth of a Liar: p.7–17 / Up Against the Ropes: p.18–30 / Back Burner: p.31–38 / The Blinding Light: p.39–60 / Vital Signs: p.61–69 / The Eleventh Hour: p.70–80 / The Balance: p.81–89 / Black Sheep: p.90–97 / An American Dream: p.98–120 |
| `better-lovers-highly-irresponsible` | Better Lovers — Highly Irresponsible | — | 122 | Lie Between The Lines: p.7–19 / Your Misplaced Self: p.20–24 / A White Horse Covered In Blood: p.25–35 / Future Myopia: p.36–47 / Deliver Us From Life: p.48–58 / Drowning In A Burning World: p.59–67 / Everything Was Put Here For Me: p.68–78 / Superman Died Paralyzed: p.79–93 / At All Times: p.94–106 / Love As An Act Of Rebellion: p.107–122 |
| `better-lovers-play-it-properly` | Better Lovers — Play It Properly | — | 1 | 1 page ingested |
| `dep-one-of-us-is-the-killer` | DEP — One Of Us Is The Killer | — | 93 | Prancer: p.6–16 / When I Lost My Bet: p.17–27 / One Of Us Is the Killer: p.28–35 / Hero of the Soviet Union: p.36–42 / Nothing's Funny: p.43–50 / Understanding Decay: p.51–62 / Paranoia Shields: p.63–70 / Crossburner: p.76–82 / The Threat Posed by Nuclear Weapons: p.83–92 |
| `etid-low-teens` | Every Time I Die — Low Teens | — | 90 | Fear And Trembling: p.4–12 / C++ (Love Will Get You Killed): p.13–17 / Two Summers: p.18–22 / Awful Lot: p.23–27 / I Didn't Want To Join Your Stupid Cult Anyway: p.28–32 / It Remembers: p.33–45 / The Coin Has A Say: p.46–50 / Religion Of Speed: p.51–58 / Just As Real But Not As Brightly Lit: p.59–69 / Map Change: p.70–80 / Skin Without Bones: p.81–84 / Nothing Visible; Ocean Empty: p.85–90 |
| `30-dirty-grooves` | 30 Dirty Grooves | — | 16 | Grooves: p.4–15 |
| `20-chops` | 20 Chops | — | 5 | p.1 = cover / p.2–3 = intro / Chops content: p.4 |
| `btbam-prequel-to-the-sequel` | BTBAM — Prequel to the Sequel | Paul Waggoner | 1+ | Single-page tab screenshot stand-in (C# standard tuning). Section A ♩=100 mm.1–16, Section B ♩=120 mm.19+. Replace with full PDF when acquired. |
| `vai-10-hour-workout` | 10 Hour Guitar Workout | Steve Vai | 6 | Page-by-page rotation. Cycle pp.2→6 only (skip p.1 intro). |
| `evolution-of-blast-beats` | The Evolution of Blast Beats | Derek Roddy | ~100 | NOT YET CHAPTERIZED — do not use in routines / No pages ingested yet — screenshots only / Known from screenshots: 4 blast types intro p.22 / Kick variations p.15 / Double Bass Workout p.79–81+ |
| `rod-morgenstein-drum-set-warm-ups` | Drum Set Warm-Ups | Rod Morgenstein | ? | NOT YET CHAPTERIZED — pages not yet rendered |
| `jungle-drum-n-bass` | Jungle / Drum n Bass | — | ? | NOT YET CHAPTERIZED — pages not yet rendered |
| `120-right-hand-studies-giuliani` | 120 Right Hand Studies | Mauro Giuliani | 15 | Page-by-page rotation. Cycle pp.3→14 only (skip pp.1–2 intro and p.15). |
| `scale-studies-jazz-guitar-stone` | Scale Studies for Jazz Guitar | Rick Stone | 24 | Page-by-page rotation — no chapter map. Embed one page per warm-up, cycle p.1→p.24. |
| `converge-axe-to-fall` | Converge — Axe to Fall | — | ? | Guitar tab — pages not yet rendered |
| `converge-concubine` | Converge — Concubine | — | ? | Guitar tab — pages not yet rendered |
| `converge-dark-horse` | Converge — Dark Horse | — | ? | Guitar tab — pages not yet rendered |
| `converge-drop-out` | Converge — Drop Out | — | ? | Guitar tab — pages not yet rendered |
| `converge-first-light` | Converge — First Light | — | ? | Guitar tab — pages not yet rendered |
| `converge-hum-of-hurt` | Converge — Hum of Hurt | — | ? | Guitar tab — pages not yet rendered |
| `converge-to-feel-something` | Converge — To Feel Something | — | ? | Guitar tab — pages not yet rendered |
| `converge-under-duress` | Converge — Under Duress | — | ? | Guitar tab — pages not yet rendered |
| `converge-versus` | Converge — Versus | — | ? | Guitar tab — pages not yet rendered |
| `converge-worms-will-feed` | Converge — Worms Will Feed | — | ? | Guitar tab — pages not yet rendered |

---

## After Every Session

Ask:
1. What BPM felt comfortable?
2. Any specific difficulties?

Log to `practice/Practice Log.md`, commit and push.

---

## Setup on a New Machine

```bash
git clone https://github.com/totster87/music-kb.git
cd music-kb
git lfs pull
```
Open in Claude Code — this file loads automatically. Say `load my session` to begin.

## GitHub Pages (iPhone Viewer Access)

If GitHub Pages is enabled, all HTML viewers are accessible directly in Safari — no downloading needed.

**Status:** Needs to be enabled. Requires either:
- GitHub Pro ($4/month) for private repo, OR
- Make repo public (free)

**To enable:** github.com/totster87/music-kb → Settings → Pages → Source: Deploy from branch → Branch: main → Folder: / (root)

**Base URL once enabled:** `https://totster87.github.io/music-kb/`

**Viewer URLs (once Pages is live):**
- Clean Intro: `https://totster87.github.io/music-kb/docs/viewers/Better%20Lovers%20-%20Lie%20Between%20the%20Lines%20(Clean%20Intro).html`
- Full Song: `https://totster87.github.io/music-kb/docs/viewers/Better%20Lovers%20-%20Lie%20Between%20the%20Lines%20(Full%20Song).html`

**When generating new viewers:** Always remind the user of the Pages URL pattern so they can tap it directly on iPhone.

**If Pages is not yet enabled:** Tell the user to open the HTML file from the GitHub app → download → open in Safari.