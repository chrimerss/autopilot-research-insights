# published/ — your research history

These files are the **grounding** for each insight's "Connections to My Work" section.
The analyzer reads `_data/publications.yml` (titles/venues/years) **plus** any full-text
markdown placed here, so the richer this folder is, the better the synthesis.

## Convention

- One file per paper: `published/<slug>.md`.
- Front matter: `title`, `authors`, `year`, `venue`, optional `link`.
- Body: the paper's **main text only** (no references, no boilerplate) — convert your PDF
  to markdown and paste the prose.

## Why add these?

`_data/publications.yml` already lists your 20 most-recent Scholar papers, which is enough
for the insight grounding check to pass. Adding full text here lets the model draw *specific*
methodological connections (e.g., "this extends the F-IDF metric you defined…") rather than
title-level ones.

See `example.md` for the shape.
