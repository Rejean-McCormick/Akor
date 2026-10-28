# Implementation status

**Implemented in this repository:** read-only preflight of a **synthetic** Kontexte mission against the exact sister-repository source contracts; kompose planning and role-safe previews; Orgo's `validate` and `plan` commands; Orgo_Worlds' architecture check; static teacher review; automated unit and optional integration tests.

**Additional source implementation (Tandem Education, synthetic only):** P2 review-intent generation (`src/akor/tandem_intent.py`; `tests/test_tandem_intent.py`) and P3 untrusted authority-request envelope (`src/akor/tandem_authority_request.py`; `tests/test_tandem_authority_request.py`) are present. P3 returns `AWAITING_SERVER_VERIFICATION` with authorization flags `false`. See [P2](TANDEM_EDUCATION_P2_REVIEW_ONLY.md) and [P3](TANDEM_EDUCATION_P3_AUTHORITY_REQUEST.md). Their existence is not proof of an admitted workflow or completed cross-repository qualification.

**Not implemented:** live Orgo Case/Task/Signal creation, teacher approval workflow, validated bakery WorldRelease, student identity, role-based fragment release, authenticated collaborative learner interface, classroom synchronization, assessed learning evidence, or integration into Ekole's live student/teacher UI.

**Safety boundaries:** The Akor preflight never calls `inject --apply`, never creates real learner sessions, never enables publishing, and never assigns grades. The preview is **not authorization**. Orgo remains the only canonical operational state manager. No output may be written inside a source repository.

**Historical source baseline for the initial preflight:** the six sister repositories supplied on 2026-10-17: `ekole`, `ekole-quebec`, `Kontexte`, `kompose`, `Orgo`, and `Orgo_Worlds`. Akor does not vendor their source trees.

See [Roadmap](wiki/Roadmap.md) and [Integration Contracts](wiki/Integration-Contracts.md).
