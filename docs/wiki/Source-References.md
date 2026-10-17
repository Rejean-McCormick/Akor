# Source References and Evidence Boundaries

The Akor wiki was prepared against the following **local snapshot archives** provided for the October 17, 2026 review. It documents existing behavior when confirmed by source and explicitly labels proposed Akor features as not yet implemented.

## Primary files by repository

| Repository | Paths | What they support |
| --- | --- | --- |
| `Kontexte` | `data/missions/boulangerie.json`, `docs/ekole-orgo/02_ARCHITECTURE_CIBLE.md`, `docs/decisions/ADR-001-ORGO-CANONIQUE.md` | Three roles/steps/two fragments/one join; Orgo state owner; scenario still synthetic |
| `Kontexte` | `Kontexte.wiki/Adaptive-Participation.md`, `Kontexte.wiki/Orgo-Integration.md` | Private supports, simulation-only export and gaps |
| `kompose` | `docs/b6/ARCHITECTURE.md`, `contracts/schemas/kontexte-preview.schema.json` | Preview contract, canonical-runtime marker, non-dispatchable status and unenforced joins |
| `Orgo` | `docs/Technical-Reference/SCENARIO_INJECTOR.md`, `docs/Technical-Reference/COMMON_IDENTITY.md` | Injector dry-run and identity boundaries |
| `Orgo_Worlds` | `docs/Technical-Reference/Worlds/04_DATA_OWNERSHIP_MATRIX.md`, `08_IDENTITY_MEMBERSHIP_PERSONAS.md` | World/release ownership and scoped membership |
| `Ekole` / `ekole-quebec` | Teacher interface, publication layer and 202-course corpus in supplied snapshots | Separate teacher/student content and baseline educational source |
| Integration precursor | `Ekole_Pont_Missions_v4_1/README.md`, `RAPPORT_SIX_DEPOTS.md` | What the dry-run bridge actually validated or did not validate |

## Archive names

```text
znapshot_ekole_10171043.zip
znapshot_ekole-quebec_10171043.zip
znapshot_Kontexte_10171044.zip
znapshot_Kompose_10171044.zip
znapshot_Orgo_10171044.zip
znapshot_Orgo_Worlds_10171044.zip
Ekole_Pont_Missions_prequalification_v4_1.zip
```

## A claim checklist for future updates

When a new behavior is documented, state:

1. **Owner** (which product is the source of truth).
2. **Version and evidence** (commit or snapshot; test command/results).
3. **Level** (concept, static mock, test-world implementation, fully integrated, classroom approved).
4. **Security scope** (whose permissions and data are involved).
5. **Pedagogical scope** (draft, approved, or validated with learning evidence).

Do not promote simulation test results or static previews into claims about live learner collaboration.
