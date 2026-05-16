---
title: Library — Exercise Catalogs
type: note
permalink: music-kb/library/readme
tags:
- catalog
- index
---

# Library — Exercise Catalogs

Per-book exercise catalogs to support autonomous routine generation.
Each book that has been touched in practice gets its own file; new books are
added the first time an exercise from them is logged or referenced in a routine.

## Purpose
- `repertoire/` = songs being learned (per-song notes)
- `library/` = method-book exercises (per-book catalogs of individual exercises)
- `practice/Practice Log.md` = chronological session history
- `CLAUDE.md` = high-level book chapter map

When generating a routine, scan `library/*.md` instead of cold-picking from chapter ranges. Each catalog answers: what's been tried, what's the ceiling, what's worth pulling next.

## Per-Exercise Schema

Each exercise entry uses this shape:

```
### p.X — <Exercise Name>
- **Chapter:** <chapter from CLAUDE.md book map>
- **Focus:** <one-line description of what it trains>
- **Tags:** comma, separated, technique, tags
- **Status:** in-rotation | attempted | needs-revisit | bottlenecked | untried
- **Current ceiling:** <BPM or qualitative>
- **Last worked:** YYYY-MM-DD
- **BPM History:**
  - YYYY-MM-DD: BPM, brief note
- **Bottlenecks:** specific issues observed
- **Notes:** anything else worth remembering
```

A `## Candidates for Rotation` section lists untried pages worth pulling next, with a one-liner reason.

## Tag Vocabulary

Reusable across catalogs so routines can pick by intent:

**Hand technique:** single-strokes, double-strokes, paradiddle, flam, drag, rolls, accents, dynamics
**Foot technique:** double-bass, left-foot, hand-foot-independence, bass-flam
**Subdivisions:** quarter, eighth, sixteenth, triplet, sextuplet, subdivisions
**Coordination:** independence, ostinato, comping
**Style:** jazz, bop, funk, rock, metal, latin
**Time:** 6-8, 3-4, time-signature, rubato
**Reading:** reading, syncopation
**Application:** kit-incorporation, soloing, brushes, fills, warm-up
**Internal clock:** internal-clock, click-discipline

## Routine Generation Hook

When asked for a routine, the picker should:
1. Read this README + every `library/*.md` for the target instrument
2. Filter by intent (warm-up, technique, double-bass, music application, burnout)
3. Bias toward **needs-revisit** and **bottlenecked** statuses; rotate **in-rotation**
4. Pull from `## Candidates for Rotation` sections when the user wants new material
5. Avoid repeating exercises from the most recent 2 sessions in the Practice Log
