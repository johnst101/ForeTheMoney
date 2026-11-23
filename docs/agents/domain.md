# Domain Docs

How the engineering skills should consume this repo's domain documentation when exploring the codebase.

## Before exploring, read these

- `GLOSSARY.md` at the repo root, or
- `GLOSSARY-MAP.md` at the repo root if it exists; it points at one `GLOSSARY.md` per context.
- `docs/adr/` for repo-wide decisions that touch the area being changed.

If these files do not exist, proceed silently and let the domain-modeling flows create them lazily when the architecture or terminology actually needs to be clarified.

## File structure

This repo is a single-context application, so the default pattern is:

```
/
├── GLOSSARY.md
├── docs/adr/
└── backend/
```

## Use the glossary's vocabulary

When your output names a domain concept, use the terms defined by the repo's glossary rather than inventing synonyms. If a concept is missing, treat that as a signal to clarify terminology before writing substantial code or issue text.

## Flag ADR conflicts

If a proposal contradicts an existing ADR, surface that conflict explicitly rather than silently overriding the prior decision.
