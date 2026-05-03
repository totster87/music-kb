# music-kb — Claude Instructions

## ⚠️ CRITICAL — READ FIRST
- **NEVER read, open, or load any `.png`, `.pdf`, or `.html` file. Ever. Under any circumstances.**
- **Do NOT auto-trigger any routines or read any files on session start**
- **Wait for user input. Do nothing until the user speaks first.**
- When showing exercises, songs, or routines: **generate or update an HTML file** and tell the user to open it in Safari. Never output tab or images in chat.
- Use `python docs/viewers/generate_viewer.py` or write a custom HTML file to `docs/viewers/`
- After generating: commit, push, then tell the user the filename to open in Safari via GitHub app
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
2. Read `repertoire/Better Lovers - Lie Between the Lines.md` — show current section and known issues
3. Summarise the suggested session structure (do NOT auto-load any images)
4. Ask: "Want me to pull up the current page?"

### "guitar routine" / "guitar session"
1. Read `repertoire/Better Lovers - Lie Between the Lines.md`
2. Walk through the routine step by step
3. Only display a page image if the user asks for it
4. At the end ask for BPM + difficulty notes, log to Practice Log, commit and push

### "drum routine" / "drum session"
1. Read `practice/Practice Log.md` for last drum entries
2. Describe the three core exercises with book/page references
3. Only display images on request
4. At the end ask for BPM + difficulty notes, log to Practice Log, commit and push

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
- **Routine file:** `repertoire/Better Lovers - Lie Between the Lines.md`
- **Viewers (open in browser):**
  - `docs/viewers/Better Lovers - Lie Between the Lines (Clean Intro).html`
  - `docs/viewers/Better Lovers - Lie Between the Lines (Full Song).html`

### Drums
- **Morello Groups of Four** (double bass): 70 BPM — just starting double bass
- **Morello Table of Time:** 53 BPM halftime — rushes on subdivision transitions
- **PI Rock Part 3, exercises 1–4:** hands/feet independence — recommended starting point

### Suggested Session Structure
1. Morello Groups of Four (double bass, 70 BPM)
2. PI Rock Part 3 exercises 1–4
3. Morello Table of Time (53 BPM halftime)

---

## Book Library

All PDFs in `docs/`, all pages pre-rendered in `docs/rendered/<slug>/`. Only read images when explicitly requested.

| Slug | Title | Author | Pages | Key Pages |
|------|-------|--------|-------|-----------|
| `double-bass-freedom` | Double Bass Drum Freedom | Virgil Donati | 135 | First exercises: p.9 / Sextuplets: p.59 |
| `progressive-independence-rock` | Progressive Independence: Rock | Ron Spagnardi | 162 | Part 3 combos: p.9 |
| `master-studies-morello` | Master Studies | Joe Morello | 97 | Table of Time: p.8 / Groups of Four: p.9 |
| `the-art-of-bop-drumming` | The Art of Bop Drumming | John Riley | 68 | Jazz comping and ride vocabulary |
| `advanced-techniques-modern-drummer` | Advanced Techniques Vol.1 | Jim Chapin | 55 | Coordinated independence, jazz/be-bop |
| `stick-control` | Stick Control | George Lawrence Stone | 50 | Single Beat Combinations: p.5 |
| `advanced-funk-studies` | Advanced Funk Studies | Rick Latham | 51 | Funk patterns throughout |
| `progressive-steps-syncopation` | Progressive Steps to Syncopation | Ted Reed | 61 | Syncopation reading |
| `abr-messengers-drums` | ABR — Messengers (Drums) | — | 121 | Full drum transcription |
| `better-lovers-highly-irresponsible` | Better Lovers — Highly Irresponsible | — | 122 | Song index: p.4 / Lie Between: p.7 |

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
