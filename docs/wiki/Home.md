# Akor — Learning in Concert

**Code snapshot status (October 27, 2026):** P2 synthetic review intents and P3 untrusted authority requests exist in source, but neither grants runtime admission or starts a classroom mission. See [Source-verified code status — October 27, 2026](Code-Status-2026-10-27) for source evidence and limitations.


> **Akor brings children into accord through shared missions: different roles, meaningful interactions, a common purpose.**

Akor is the proposed collaboration and integration layer connecting **Kontexte**, **kompose**, **Orgo**, **Orgo_Worlds**, and **Ekole**. Its name evokes *accord*: not just agreement between software components, but the way children listen, exchange information, negotiate, help one another, and create something together.

**Akor is not a new learning management system or a second workflow engine.** It exists so that a mission designed elsewhere can become a safe, accessible, cooperative experience in Ekole—with real interdependence between learners, not merely several children viewing the same screen.

## The human purpose

Imagine three children running a fictional village bakery. The baker understands the order, the farmer has information about supplies, and the accountant checks the quantities. None is simply a spectator or a button-clicking assistant. Each has something meaningful to discover or contribute. They must **talk, compare, explain, ask, decide, and act together**.

That is Akor's product ambition: **participation through interaction**. The technology should support the learning conversation, not replace it.

## Start here

| You want to… | Read |
| --- | --- |
| Understand the name and educational promise | [Vision and Name](Vision-and-Name) |
| See the full system and what each repository owns | [Architecture and Ownership](Architecture-and-Ownership) |
| Design meaningful cooperation instead of parallel solo tasks | [Collaborative Learning Principles](Collaborative-Learning-Principles) |
| Understand roles, exchanges, and joint decisions | [Roles and Social Interactions](Roles-and-Social-Interactions) |
| Walk through a classroom mission | [Village Bakery Walkthrough](Village-Bakery-Walkthrough) |
| Design learner- and teacher-facing experiences | [Learner Experience](Learner-Experience) · [Teacher Experience](Teacher-Experience) |
| Review access, safety, privacy, fairness, and accommodations | [Privacy and Safety](Privacy-and-Safety) · [Accessibility and Inclusion](Accessibility-and-Inclusion) |
| Integrate without duplicating Orgo | [Integration Contracts](Integration-Contracts) · [Mission Lifecycle](Mission-Lifecycle) |
| See what is real today and what is proposed | [Project Status](Project-Status) · [Roadmap](Roadmap) |
| Qualify the first classroom-ready implementation | [Testing and Acceptance](Testing-and-Acceptance) |

## The five-system relationship

```text
Kontexte ──────── roles, stories, situations, interaction intentions
     │
kompose ───────── deterministic review, coordination design, safe role previews
     │
Orgo_Worlds ───── versioned World / WorldRelease context
     │
Orgo ──────────── authorized operational state: Cases, Tasks, Signals, workflows
     │
Akor ──────────── reviewed adapters, role-safe projections, interaction bridge
     │
Ekole ────────── learner/teacher interfaces, curriculum and learning evidence
```

This diagram describes **target responsibilities**, not a production deployment. Akor must neither bypass Orgo authorization nor invent its own competing mission state.

## What Akor should make possible

- **A role with purpose:** every participant knows why they matter.
- **A reason to talk:** learners have different, appropriately shared information or capabilities.
- **A shared decision:** progress depends on a meaningful exchange, not only independent checkboxes.
- **A safe way to participate:** speech, text, visual supports, and teacher facilitation where suitable.
- **A graceful alternative:** solo mode, absent partners, different pacing, and recovery do not punish learners.
- **Separate evidence:** mission completion is not automatically subject mastery.

## Historical context (October 17, 2026)

At that checkpoint, Akor was **named and documented, but not implemented as a standalone production product**. The separate source repository and its P2/P3 synthetic capabilities are described in the [October 27 code status](Code-Status-2026-10-27). The existing `Ekole_Pont_Missions_v4_1` prototype qualifies real Kontexte/kompose inputs and validates a synthetic Orgo preparation fixture **without writing to Orgo**. No authenticated multi-child experience has been delivered by this bridge. The bakery scenario remains a synthetic draft needing pedagogical review.

See [Project Status](Project-Status) for a strictly separated *implemented / demonstrated / proposed* inventory.

---

**Akor principle:** *Children do not need to do the same thing to learn together. Their contributions must matter to one another.*

## Contrôle des intégrations (27 octobre 2026)

Voir [[Integration-Verification-2026-10-27]] pour les versions et frontières des dépôts satellites, avec preuves et limites.
