# Source-Verified Code Status — October 27, 2026

> **Scope:** local source snapshot dated October 27, 2026, compared with the supplied wiki pages. Tests were not rerun, and the live GitHub Wiki was not checked.

## Verified scope

- Akor has a read-only, synthetic mission preflight (`src/akor/preflight.py`) and explicit Tandem P2 intent generation (`src/akor/tandem_intent.py`). It checks selected sister-repository contracts and produces review artifacts; it does not launch a live session.
- The P3 `akor.tandem-authority-request/1.0` producer (`src/akor/tandem_authority_request.py`) parses an untrusted P2 intent, checks required UUIDs, hashes, duplicate keys/tasks, and rejects requests attempting to set authority flags. The expected state is `AWAITING_SERVER_VERIFICATION`.
- `tests/test_tandem_intent.py` and `tests/test_tandem_authority_request.py` contain targeted tests for those boundaries; tests are *present in the snapshot*, not independently run by this wiki review.

## Not established

A real Orgo admission transaction, trusted teacher authentication, class membership, WorldRelease verification, child identity, operational Case/Task dispatch, authenticated learner UI, pedagogical assessment and classroom synchronization are **not** implemented by these source paths. A P2/P3 JSON document is neither permission nor proof of approval. No student-facing release is claimed.

## Governing source references

`docs/STATUS.md`, `docs/TANDEM_EDUCATION_P2_REVIEW_ONLY.md`, `docs/TANDEM_EDUCATION_P3_AUTHORITY_REQUEST.md`, `src/akor/tandem_intent.py`, `src/akor/tandem_authority_request.py`.
