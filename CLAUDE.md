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

This is a personal music practice knowledge base.

---

## Who This Is For

The user is a drummer and guitarist:
- **Drums:** Metal + jazz/funk. Working through method books with BPM logging. Has practice pad and full kit.
- **Guitar:** Drop D / metal. Currently learning Better Lovers — Highly Irresponsible.
- **Goal:** Tailored practice routines from owned books, BPM tracking, exercise pages displayed on request.

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
2. Build a balanced session: warm-up (Stick Control/rudiments), technique (Morello/Chapin/PI Rock), double bass (Donati), music application (ABR or other transcription)
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
- **Morello Groups of Four with Fill-Ins** (p.71): 70 BPM — just starting double bass
- **Morello Table of Time** (p.43): 53 BPM halftime — rushes on subdivision transitions
- **PI Rock Part 3, exercises 1–4** (p.49+): hands/feet independence — recommended starting point

### Suggested Session Structure
1. Morello Groups of Four with Fill-Ins (p.71, 70 BPM)
2. PI Rock Part 3 exercises 1–4 (p.49+)
3. Morello Table of Time (p.43, 53 BPM halftime)

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
| `abr-messengers-drums` | ABR — Messengers (Drums) | — | 121 | Full drum transcription |
| `better-lovers-highly-irresponsible` | Better Lovers — Highly Irresponsible | — | 122 | Song index: p.4 / Lie Between: p.7 |
| `dep-one-of-us-is-the-killer` | DEP — One Of Us Is The Killer | — | 93 | Guitar transcription / 8 songs auto-indexed |
| `30-dirty-grooves` | 30 Dirty Grooves | — | 16 | Drum sheet music |
| `20-chops` | 20 Chops | — | 5 | Drum sheet music (scanned) |

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
