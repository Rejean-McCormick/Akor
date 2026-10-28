# Akor

**Learning in Concert**

> Children do not need to do the same thing to learn together. Their contributions must matter to one another.

Akor helps children **learn in concert** through shared missions, complementary roles, and meaningful interactions. Its name is inspired by *accord*: harmony between children working toward a common goal, and reliable coordination between the systems that support them.

Akor is intended to connect **Kontexte**, **kompose**, **Orgo**, **Orgo_Worlds**, and **Ekole**. The purpose of that integration is human: to give every learner a reason to participate, communicate, listen, contribute, and make decisions together.

## Why Akor?

Working in the same room is not the same as working together. In a meaningful Akor mission:

- Every child has a role and something useful to contribute.
- Roles provide different but complementary perspectives, information, or actions.
- Progress depends on exchanging ideas, explaining reasoning, and making shared decisions.
- Participation remains accessible, including when a child needs more time, another way to communicate, or a partner is absent.
- The teacher can guide the experience and review individual learning without reducing everyone to one group score.

Collaboration is a learning opportunity, not an obligation for every lesson. Missions should be adaptable to solo, pair, group, and teacher-facilitated formats.

## Responsibilities

Akor is an **integration and interaction layer**, not a replacement for the systems around it.

| System | Responsibility |
| --- | --- |
| **Kontexte** | Designs educational situations, narrative settings, roles, and interaction intentions. |
| **kompose** | Reviews and prepares coordination plans and role-aware previews. |
| **Orgo_Worlds** | Provides versioned worlds and WorldRelease context. |
| **Orgo** | Owns the live operational state: cases, tasks, signals, permissions, and transitions. |
| **Akor** | Validates integration boundaries, connects approved mission definitions to authorized state, and presents role-safe interactions to Ekole. |
| **Ekole** | Provides learner and teacher interfaces, curriculum connections, student work, and learning evidence. |

Akor must **not** become a second workflow engine, identity provider, automatic grading service, or independent publisher of unreviewed educational content.

## How a mission should work

1. **Design:** Kontexte describes a situation, its learning goals, roles, and opportunities for interaction.
2. **Prepare:** kompose checks coordination intentions and produces a deterministic preview.
3. **Review:** An authorized teacher approves the pedagogical content and the intended experience.
4. **Release:** A compatible WorldRelease and Orgo workflow are explicitly selected and verified.
5. **Play:** Orgo maintains the authoritative mission state; Akor exposes only the actions and information permitted for each participant in Ekole.
6. **Reflect:** Ekole stores relevant student work and evidence for teacher review. Completing a mission does not automatically establish mastery.

This is the **target lifecycle**, not a claim that the full runtime has already been implemented.

## Example: The Village Bakery

In a fictional bakery, one child may interpret a customer's order, another may work with supplies, and another may check quantities. The group succeeds by communicating and combining their reasoning, not by completing unrelated worksheets.

The existing bakery prototypes require further review: source materials do not yet agree on the course mapping and multiplication scenario. The original scenarios should remain unchanged until an approved, versioned variant is ready.

## Safety and inclusion by design

- **Teacher governance:** No unreviewed mission is launched or published automatically.
- **Role-scoped information:** Children see only the fragments, tasks, and feedback they are authorized to access.
- **No hidden shortcuts:** All live state changes go through Orgo's authorized operations.
- **Child privacy:** Do not expose peer records, private accommodations, secret answers, or service credentials.
- **Accessibility:** Offer appropriate visual, text, and teacher-assisted alternatives; avoid deadlocks when a participant is absent.
- **Learning integrity:** Distinguish participation, mission completion, and demonstrated subject knowledge.

## Project status

**Status: standalone repository foundation available (read-only preflight); production integration not yet released.**

The existing `Ekole_Pont_Missions_v4_1` precursor is a **read-only prequalification prototype**. It can inspect Kontexte and kompose inputs, generate role-aware review materials, and validate a synthetic preparation scenario through Orgo's injector in `validate` / `plan` mode. It does **not** start a live collaborative session, create operational tasks, or provide authenticated multi-child gameplay.

This repository now includes a working read-only preflight CLI, unit tests, source-boundary checks, a Windows launcher, and an English wiki. Live service interfaces, classroom authentication, mission lifecycle integration, and end-to-end collaborative tests have **not** been implemented or qualified.

## Development roadmap

1. **Foundation (started):** Maintain this standalone `akor` repository, pin source versions, define contracts, and preserve the read-only review flow.
2. **Solo mission:** Run a reviewed, persistent bakery mission in an isolated Orgo environment using fictional learners.
3. **Collaborative mission:** Support complementary roles, authorized information sharing, meaningful hand-offs, and recovery from disconnects or absent partners.
4. **Learning evidence:** Link individual contributions to Ekole for teacher interpretation, without automatic certification.
5. **School readiness:** Validate accessibility, privacy, operational safety, and classroom usability before deployment with real children.

## Getting started

Run Akor in **non-mutating review mode**, with the six repositories as siblings and Python 3.10+ and Node.js 18+ installed:

```text
Ekole/
  akor/
  ekole/
  ekole-quebec/
  Kontexte/
  kompose/
  Orgo/
  Orgo_Worlds/
```

On Windows, double-click `LANCER_REVUE_AKOR.bat`. From a terminal:

```bash
python run_akor.py --root /path/to/Ekole --out /path/to/Ekole/akor/output
python -m unittest discover -s tests -v
```

A successful preflight produces `output/REVUE_ENSEIGNANT.html`, `output/RAPPORT.md`, and non-published JSON review artifacts. It intentionally reports **blockers** to live mission delivery, including the existing source-mapping mismatch between `qc-pri-ma-006` and `qc-pri-ma-008`. It does not create Orgo tasks, publish a child-facing mission, or use real student records.

For the full guide, read [Development and local usage](docs/DEVELOPMENT.md), [Project status](docs/STATUS.md), and the [Akor wiki](docs/wiki/Home.md).

## Guiding principle

**Akor connects systems so children can connect with one another.**

## Tandem 1.0 synthetic handoff (P1)

Akor also offers an **independent read-only integration check** for the reviewed Kontexte -> Kompose -> Ekole synthetic preview, with **Orgo remaining the sole live operational authority**. This is **not** a second compiler or a classroom authorization. The existing bakery preflight remains available as a legacy, non-publishing review workflow.

See [Tandem Akor interop/security P1](docs/TANDEM_AKOR_INTEROP_SECURITY_P1.md) for the Windows command and scope limitations.
