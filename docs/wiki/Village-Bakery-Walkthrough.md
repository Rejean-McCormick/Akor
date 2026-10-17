# Village Bakery Walkthrough

**Scenario:** *La boulangerie du village* / *Village Bakery*.

This page deliberately separates the **actual October 2026 scenario skeleton** from a **proposed child-facing, collaborative variant**. It is a design walkthrough, not a running multi-user product.

## 1. What the source actually contains

The Kontexte file `data/missions/boulangerie.json` states:

| Field | Current value |
| --- | --- |
| Format | `kontexte.mission/1` |
| Scenario ID | `boulangerie` |
| Version | `0.1.0` |
| Status | `scenario_skeleton_requires_pedagogical_review` |
| Synthetic | `true` |
| Roles | `boulanger`, `fermier`, `comptable` |
| Steps | `phase-1` (flour order), `phase-2` (prepare 12 loaves), `phase-3` (accounts) |
| Dependencies | phase-2 depends on phase-1; phase-3 depends on phase-2 |
| Fragments | `indice-un` (baker) and `indice-deux` (farmer) |
| Join | `jointure-infos` intends to unlock phase-3 |
| Review | every step: `human_review` |
| Curriculum IDs | all three currently `qc-pri-ma-006` (addition) |

The description of an Orgo-authorized fragment **is not equivalent to a working Orgo permission or join**. Existing tooling exports only preparation/review plans, not a complete student mission.

## 2. A multiplication adaptation worth developing

For the Grade 3 course `qc-pri-ma-008`, the pedagogical team may approve an **additional version**, leaving the original addition scenario untouched.

### The challenge

The bakery needs **12 loaves**, arranged in **3 trays of 4**. The group must explain why `3 × 4 = 12`, reconcile the quantities and produce a joint order sheet.

### Three meaningful contributions

- **Baker:** proposes the tray arrangement and explains equal groups.
- **Farmer:** provides a checked quantity and asks how it matches the plan.
- **Accountant:** brings both contributions together, checks the reasoning and helps finalize the shared order.

These assignments are **proposed story mechanics**; the source JSON does not yet describe their executable scoring, teacher checks or release conditions.

### A possible learner exchange

> **Baker:** “I made three trays with four loaves each. How many do we have?”
>
> **Farmer:** “I counted twelve loaves. Does that match your trays?”
>
> **Accountant:** “Let's count the groups together and write the reason.”

The educational value is **explanation plus reconciliation**, not the mere fact that three different users clicked Submit.

## 3. Proposed operational sequence

1. Teacher reviews the scenario, learning target, accessibility and safety.
2. A reviewed WorldRelease and Orgo workflow are pinned in a test world.
3. Teacher launches; trusted session identities and role assignments are established.
4. Each learner receives **only** their Orgo-authorized task projection.
5. Children exchange information through approved channels, on-screen or in person.
6. Orgo verifies required submissions, human reviews and joins; duplicates and missing partners are handled.
7. Group sees its outcome. Ekole stores individual learning evidence for teacher review.

## 4. Essential fallback modes

- **Solo:** the same Orgo runtime uses a reviewed solo branch, without fictional “peer” activity being mistaken for classmates.
- **Pair:** one child may take more than one role with teacher approval, or the teacher mediates the missing role.
- **Partner absence:** pause, reassign, or introduce an explicitly labeled authorized synthetic helper.
- **Connection lost:** recover the authoritative Orgo state before allowing more actions.

## 5. What must pass before calling this integrated

- Approved mapping to `qc-pri-ma-008` and a reviewed scenario version.
- Orgo-enforced fragment release, role-specific projections, join and replay behavior.
- WorldRelease pinned and validated; test-world mutation only with authorization.
- Authenticated teacher launch; fictional student identities in initial tests.
- Functional learner and teacher screens using actual Orgo state.
- Evidence stored in Ekole without treating completion as mastery.
- Cross-browser tests for solo and multi-child sessions, disconnections, absent partners and privacy.

See [Testing and Acceptance](Testing-and-Acceptance) and [Project Status](Project-Status).
