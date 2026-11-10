# Final-system education boundary — Akor

**Scope:** `FC-10` / review-only collaborative mission preparation, not live educational identity or Orgo task state.

## Implemented conformance sequence

1. Read the explicit Kontexte mission `data/missions/<scenario>.json` from its checked-out owner root; refuse out-of-root paths and unsafe JSON.
2. Load the actual Kompose `src/kompose/tandem_handoff.py` and Ékole `tandem/projection.py` validators to check an `ekole.tandem-teacher-preview/1.0` file.
3. Validate expected tenant/World/WorldRelease against **caller-declared synthetic fixture UUIDs**, then invoke Kompose's `verify_initial_design_preview` to ensure no fabricated task progress, reordered source steps or released fragments.
4. Keep the existing `akor.tandem-handoff-check/1.0`, `akor.tandem-execution-intent/1.0` and `akor.tandem-authority-request/1.0` outputs **non-authoritative** with permission and dispatch flags false.

This process never establishes a legitimate teacher, student, WorldRelease or Orgo runtime approval. A real owner and a separate online, authenticated operation would need to make those decisions.

## Tests and remaining gates

Run `PYTHONPATH=src python -m unittest discover -s tests -v`. Several unit tests intentionally use stubbed partner validators; **the branch-level integration runner** separately exercises the actual source owner implementations and negative tampered previews. Do not confuse mock tests with deployed integration. An adopted Akor→Orgo command and grade/learner privacy governance are still needed from their owners.
