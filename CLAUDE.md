# music-kb — Claude Instructions

## ⚠️ CRITICAL — READ FIRST
- **NEVER read, open, or load any `.png`, `.pdf`, or `.html` file. Ever. Under any circumstances.**
- **Do NOT auto-trigger any routines or read any files on session start**
- **Wait for user input. Do nothing until the user speaks first.**
- When showing exercises, songs, or routines: **generate or update an HTML file** and tell the user to open it in Safari. Never output tab or images in chat.
- Use `python docs/viewers/generate_viewer.py` or write a custom HTML file to `docs/viewers/`
- After generating: commit, push, then give the full GitHub Pages URL: `https://totster87.github.io/music-kb/docs/viewers/<filename>.html`
- Always output full https:// links — never local file paths. Links must be tappable on iPhone.
- On session init: greet the user, tell them to say `load my session` or a trigger phrase. Stop there.

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
1. Read `practice/Practice Log.md` to see what was last worked on — avoid repeating the same thing
2. Build a balanced session pulling from multiple sources: technique exercises, song excerpts, creative exploration
3. Draw from: Better Lovers (Highly Irresponsible), ABR Truth of a Liar, ABR Treatment, BTBAM Prequel to the Sequel, any relevant technique concepts
4. Generate an HTML file at `docs/viewers/Guitar-Routine-YYYY-MM-DD.html` with the routine written out — include embedded score pages for any referenced exercises/songs
5. Commit, push, output the GitHub Pages URL: `https://totster87.github.io/music-kb/docs/viewers/Guitar-Routine-YYYY-MM-DD.html`
6. After the session ask for BPM + difficulty notes, log to Practice Log, commit and push

### "drum routine" / "make me a drum routine"
Do NOT default to any specific exercise. Generate a fresh varied routine by:
1. Read `practice/Practice Log.md` to see what was last worked on — avoid repeating the same thing
2. Build a balanced session. Draw freely from the full book library — don't default to the same books each time. Good rotation includes:
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
3. Generate an HTML file at `docs/viewers/Drum-Routine-YYYY-MM-DD.html` with the routine written out — include embedded score pages for referenced exercises
4. Commit, push, output the GitHub Pages URL: `https://totster87.github.io/music-kb/docs/viewers/Drum-Routine-YYYY-MM-DD.html`
5. After the session ask for BPM + difficulty notes, log to Practice Log, commit and push

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
- **Tuning:** Standard (E A D G B E)
- **Current section:** Intro — lead melody only (single note lines)
- **Max BPM:** 90 (target 100)
- **Known issues:** Pick accuracy on descending runs — clips wrong string even at slow tempos
- **Repertoire file:** `repertoire/BTBAM - Prequel to the Sequel.md`
- **Viewer:** Not yet generated — say "generate viewer for BTBAM Prequel" when ready

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

| Slug | Title | Author | Pages | Key Pages |
|------|-------|--------|-------|-----------|
| `double-bass-freedom` | Double Bass Drum Freedom | Virgil Donati | 135 | Basic single strokes: p.9 / Hand-foot independence: p.21 / Sextuplet series: p.59 |
| `progressive-independence-rock` | Progressive Independence: Rock | Ron Spagnardi | 162 | Part 3 combos: p.9 |
| `master-studies-morello` | Master Studies | Joe Morello | 97 | Table of Time: p.43 / Groups of Four (fill-ins): p.71 / Accent Studies: p.7 |
| `the-art-of-bop-drumming` | The Art of Bop Drumming | John Riley | 68 | Jazz comping and ride vocabulary |
| `advanced-techniques-modern-drummer` | Advanced Techniques Vol.1 | Jim Chapin | 55 | Coordinated independence, jazz/be-bop |
| `stick-control` | Stick Control | George Lawrence Stone | 50 | Single Beat Combinations: p.5 |
| `advanced-funk-studies` | Advanced Funk Studies | Rick Latham | 51 | Funk patterns throughout |
| `progressive-steps-syncopation` | Progressive Steps to Syncopation | Ted Reed | 61 | Syncopation reading |
| `abr-messengers` | ABR — Messengers (Guitar) | — | 146 | Full guitar transcription / Truth of a Liar is song 1 |
| `abr-messengers-drums` | ABR — Messengers (Drums) | — | 121 | Full drum transcription |
| `better-lovers-highly-irresponsible` | Better Lovers — Highly Irresponsible | — | 122 | Song index: p.4 / Lie Between: p.7 |
| `better-lovers-play-it-properly` | Better Lovers — Play It Properly | — | 1 | 1 page ingested |
| `dep-one-of-us-is-the-killer` | DEP — One Of Us Is The Killer | — | 93 | Guitar transcription / 8 songs auto-indexed |
| `etid-low-teens` | Every Time I Die — Low Teens | — | 90 | Guitar transcription |
| `30-dirty-grooves` | 30 Dirty Grooves | — | 16 | Drum sheet music |
| `20-chops` | 20 Chops | — | 5 | Drum sheet music (scanned) |
| `evolution-of-blast-beats` | The Evolution of Blast Beats | Derek Roddy | ~100 | 4 blast types intro: p.22 / Kick variations (Metal Downbeat/Upbeat, Punk Feel): p.15 / Double Bass Workout: p.79–81+ / Double Bass Workout exercises work well as burnout finishers OR warm-ups / No pages ingested yet — screenshots only |

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
