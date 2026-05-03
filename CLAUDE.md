# music-kb — Claude Instructions

This is a personal music practice knowledge base. Read this file fully before responding to any prompt. It contains everything needed to assist with practice sessions, routines, and book references.

---

## Who This Is For

The user is a drummer and guitarist:
- **Drums:** Metal + jazz/funk influences. Working through method books with BPM logging. Has a practice pad and a full kit.
- **Guitar:** Drop D / metal. Currently learning Better Lovers — Highly Irresponsible.
- **Goal:** Build tailored practice routines from owned books, track BPM progress, display exercise pages directly in chat.

---

## Trigger Phrases

When the user says any of these, follow the instructions below exactly:

### "load my session" / "start practice" / "what am I working on"
Respond with a summary of current active work:
1. Read `practice/Practice Log.md` — show last 5 entries
2. Read `repertoire/Better Lovers - Lie Between the Lines.md` — show current section and known issues
3. Display the current section's viewer page: Read `docs/rendered/better-lovers-highly-irresponsible/page-007.png`
4. Suggest today's session structure based on what's in the log

### "guitar routine" / "guitar session"
1. Read `repertoire/Better Lovers - Lie Between the Lines.md`
2. Display the clean intro pages: Read `docs/rendered/better-lovers-highly-irresponsible/page-007.png` and `page-008.png`
3. Walk through the routine step by step
4. At the end, ask for BPM and difficulty notes and log to Practice Log

### "drum routine" / "drum session"
1. Read `practice/Practice Log.md` for last drum entries
2. Display the three core exercises:
   - Morello Groups of Four: Read `docs/rendered/master-studies-morello/page-009.png`
   - PI Rock Part 3: Read `docs/rendered/progressive-independence-rock/page-009.png`
   - Morello Table of Time: Read `docs/rendered/master-studies-morello/page-008.png`
3. Walk through the session in order
4. At the end, ask for BPM and difficulty notes and log to Practice Log

### "show me page X of [book]" / "pull up page X"
Read the correct rendered PNG directly. Book slug reference:
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

Path format: `docs/rendered/<slug>/page-XXX.png`

### "make me a routine" / "build a session"
Ask: pad or kit? How long? Then build a structured session pulling exercises from the books below, display each page as you explain it.

### "generate viewer for [song/exercise]"
Run `docs/viewers/generate_viewer.py` with the correct slug and page range. Commit and push.

---

## Active Work

### Guitar — Better Lovers, Lie Between the Lines
- **Tuning:** Drop D
- **Transcription:** `docs/rendered/better-lovers-highly-irresponsible/page-007.png` → `page-019.png`
- **Current section:** Section A — Clean Intro (♩=99, let ring, pages 7–8)
- **Known issue:** String skipping on all-downpicking — clips wrong string
- **Routine:** `repertoire/Better Lovers - Lie Between the Lines.md`
- **Viewers:**
  - Clean intro: `docs/viewers/Better Lovers - Lie Between the Lines (Clean Intro).html`
  - Full song: `docs/viewers/Better Lovers - Lie Between the Lines (Full Song).html`

### Drums
- **Morello Groups of Four** (double bass): 70 BPM baseline — just starting double bass
- **Morello Table of Time:** 53 BPM halftime — rushes on subdivision transitions
- **PI Rock Part 3, exercises 1–4:** hands/feet independence — recommended starting point

---

## Book Library

All PDFs in `docs/`, all pages pre-rendered as PNGs in `docs/rendered/<slug>/`.

| Slug | Title | Author | Pages | Key Pages |
|------|-------|--------|-------|-----------|
| `double-bass-freedom` | Double Bass Drum Freedom | Virgil Donati | 135 | First exercises: p.9 / Sextuplets: p.59 |
| `progressive-independence-rock` | Progressive Independence: Rock | Ron Spagnardi | 162 | Part 3 combos (start here): p.9 |
| `master-studies-morello` | Master Studies | Joe Morello | 97 | Table of Time: p.8 / Groups of Four: p.9 |
| `the-art-of-bop-drumming` | The Art of Bop Drumming | John Riley | 68 | Jazz comping and ride vocabulary |
| `advanced-techniques-modern-drummer` | Advanced Techniques Vol.1 | Jim Chapin | 55 | Coordinated independence, jazz/be-bop |
| `stick-control` | Stick Control | George Lawrence Stone | 50 | Single Beat Combinations: p.5 |
| `advanced-funk-studies` | Advanced Funk Studies | Rick Latham | 51 | Funk patterns throughout |
| `progressive-steps-syncopation` | Progressive Steps to Syncopation | Ted Reed | 61 | Syncopation reading |
| `abr-messengers-drums` | ABR — Messengers (Drums) | — | 121 | Full drum transcription |
| `abr-messengers` | ABR — Messengers (Full) | — | 146 | Full band transcription |
| `better-lovers-highly-irresponsible` | Better Lovers — Highly Irresponsible | — | 122 | Song index: p.4 / Lie Between: p.7 |

---

## Always Do After Any Exercise

After any practice session or exercise discussion, ask:
1. What BPM felt comfortable?
2. Any specific difficulties? (e.g. "rushing left foot above 80", "string skip breaks at 95")

Then log to `practice/Practice Log.md`:
```
| YYYY-MM-DD | Exercise name | Instrument | BPM | Notes |
```
Commit and push after logging.

---

## Displaying Pages in Chat

Use the `Read` tool directly on the PNG path. Always display the image before describing it. Example:
```
Read: docs/rendered/better-lovers-highly-irresponsible/page-007.png
```

---

## Generating New Viewers

```bash
python docs/viewers/generate_viewer.py <slug> "<Title>" <start_page> <end_page>
```
Then `git add docs/viewers/ && git commit && git push`.

---

## Setup on a New Machine

```bash
git clone https://github.com/totster87/music-kb.git
cd music-kb
git lfs pull
```
All rendered pages and PDFs will download. Open any `.html` in `docs/viewers/` in a browser to scroll through songs/exercises. On iPhone: GitHub app → `docs/viewers/` → download and open in Safari.
