# Project Status

## October 27, 2026 — source-verified update

The older sections below are retained for context; read the current code-backed checkpoint: [Source-verified code status — October 27, 2026](Code-Status-2026-10-27).

**P2 synthetic review intents and P3 untrusted authority requests exist in source, but neither grants runtime admission or starts a classroom mission.**


**Historical baseline: October 17, 2026.** Akor now exists as a dedicated repository. The P2/P3 source checkpoint above supersedes this historical table where newer functionality is described; Akor remains not a completed live classroom product.

## Demonstrated in supplied sources or the local prequalification bundle

| Capability | Status | Basis |
| --- | --- | --- |
| Kontexte role/mission catalogue | Existing source | 38 roles, 11 mission records, localization examples |
| Kontexte Grade 3 candidate planning | Existing source | 60 localized overlays; 83 internal objective candidates; 36-week plan |
| Bakery mission skeleton | Existing, **synthetic/unreviewed** | `data/missions/boulangerie.json` |
| kompose deterministic preview | Implemented for simulation | Preview schema; local B6 tests |
| Role preview without private fragment contents | Demonstrated locally | Ekole mission prequalification bundle |
| Orgo operational server | Existing separate product | Work/Case/Task/Signal/Workflow API v3 |
| Orgo scenario validation and planning | Demonstrated | `validate` and `plan` on synthetic preparation fixture |
| Orgo_Worlds WorldRelease ownership | Defined in separate product | Canonical specs and data ownership matrix |
| Ekole v4 teacher/student publication separation | Existing in supplied Ekole baseline | Teacher workspace, published student pilots |
| Akor learner-facing live mission | **Not implemented** | No live adapter / student session path delivered |
| Akor teacher start/pause/finish operations | **Not implemented** | Current teacher view is review-only |
| Authorized peer interaction, fragments and joins | **Not implemented for this pilot** | Source describes intent; runtime not qualified |
| Persistent solo mission with real Orgo state | **Not demonstrated by Akor** | Target next milestone |
| Multi-child collaboration and moderation | **Not implemented** | Target subsequent milestone |
| School identity, privacy and retention controls | **Not demonstrated for Akor** | Production gate |

## Source set

The source review used these ZIP snapshots:

- `znapshot_ekole_10171043.zip`
- `znapshot_ekole-quebec_10171043.zip`
- `znapshot_Kontexte_10171044.zip`
- `znapshot_Kompose_10171044.zip`
- `znapshot_Orgo_10171044.zip`
- `znapshot_Orgo_Worlds_10171044.zip`

The prequalification artifact is `Ekole_Pont_Missions_prequalification_v4_1.zip` and its report `RAPPORT_SIX_DEPOTS.md`. It uses **no network request, token or Orgo write**, and it does not publish student content.

## Known blockers

1. Bakery source references `qc-pri-ma-006` while the desired Grade 3 multiplication pilot is `qc-pri-ma-008`.
2. Bakery status is `scenario_skeleton_requires_pedagogical_review`; human review steps have no qualified runtime implementation.
3. Fragment/role authorization, joins and partner absence need a tested Orgo workflow.
4. No pinned bakery WorldRelease is present in the delivered Worlds examples.
5. No trusted teacher-to-Orgo launch and learner projection bridge has been built.
6. No real student identity, classroom privacy, resumption or educational evidence integration has been proven in this assembly.
7. Cross-browser solo and multi-user end-to-end scenarios have not yet passed as a complete stack.

## Evidence vs aspiration

Previous Ekole Playwright tests passed on Windows, but they covered **the then-current Ekole portal, pilots and teacher editor**, not Akor collaboration. Do not cite them as evidence that a live Akor mission works. Likewise, Orgo injector planning does not certify student fragment authorization.

See [Roadmap](Roadmap), [Testing and Acceptance](Testing-and-Acceptance) and [Open Decisions](Open-Decisions).
