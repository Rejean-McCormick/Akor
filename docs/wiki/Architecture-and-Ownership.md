# Architecture and Ownership

## Canonical separation

Akor must connect the existing products **without taking ownership of their business state**.

| Responsibility | Canonical owner | What Akor may do |
| --- | --- | --- |
| Scenario intent, role frames, fictional context, fragments | **Kontexte** | Validate references; adapt and project reviewed content |
| Coordination rules and deterministic preview | **kompose** | Consume a compiled plan and explain dependencies; do not execute a parallel lifecycle |
| World, immutable WorldRelease, routing context | **Orgo_Worlds** | Bind a reviewed scenario version and verify release references |
| Cases, Tasks, Signals, WorkflowVersion, transitions, recipients and operational authorization | **Orgo** | Submit explicitly permitted requests; render responses permitted for each viewer |
| Curriculum links, course content, activities, student work and learning evidence | **Ekole** (with Kristal/Spek content workflows) | Forward minimal learning references; never assign academic mastery |
| Actual human identity and access rights | School identity layer + Orgo/Ekole's own authorization | Map trusted sessions to scoped actor references without becoming a second identity provider |
| Media publication and consent | Approved school media/governance service | Display only approved, authorized assets |

## Target architecture

```text
  EDITORIAL / DESIGN SIDE                   AUTHORIZED RUNTIME
 ┌──────────────────────┐           ┌─────────────────────────┐
 │ Kontexte             │           │ Orgo_Worlds             │
 │ missions, role frames│──────────▶│ WorldRelease reference  │
 └────────────┬─────────┘           └────────────┬────────────┘
              │                                  │
 ┌────────────▼─────────┐           ┌────────────▼────────────┐
 │ kompose              │  review   │ Orgo                    │
 │ compile and preview  ├──────────▶│ Cases/Tasks/Signals     │
 │ no live state owner  │  boundary │ authorized transitions  │
 └──────────────────────┘           └────────────┬────────────┘
                                                 │
                                     ┌───────────▼──────────┐
                                     │ Akor server adapters │
                                     │ approval, mapping,   │
                                     │ safe projections     │
                                     └───────────┬──────────┘
                                                 │
                                     ┌───────────▼──────────┐
                                     │ Ekole                │
                                     │ teacher / learner UI │
                                     │ learning evidence    │
                                     └──────────────────────┘
```

Akor itself can be deployed as a service, a library of server-side adapters, or a dedicated sidecar **only after an architecture decision and threat review**. The current bridge is a **local dry-run tool**, not any of these production deployments.

## Operational invariants

1. **Exactly one live mission state owner: Orgo, even for solo missions.**
2. **Only Orgo (via its trusted authorization path) decides which role-specific content is releasable.** Kontexte story data and client-side role selectors are not authorization.
3. **Akor never performs direct database writes to Orgo or Orgo_Worlds.** Use documented controlled interfaces.
4. **WorldRelease is pinned for each running mission.** A later content revision must not silently rewrite a child's active adventure.
5. **kompose live `lifecycle` rules must not compete with Orgo's transitions.** They may inform validation and mock replay.
6. **Ekole learning evidence and Orgo task state are different records.** Do not infer mastery from `Task COMPLETED`.
7. **Teacher-only material never crosses into a learner projection** without approved transformation/publication.
8. **Failure is explicit.** If Orgo is unavailable, disable interactive mission actions rather than silently running a local state machine; ordinary Ekole lessons remain available.

## Integration entry points

- **Teacher review**: compiled mission, curriculum mapping, role demands, group configuration, permissions, WorldRelease and approval.
- **Mission launch**: authenticated teacher action, controlled server-to-server invocation, correlation and idempotency.
- **Learner projection**: only currently authorized instructions, messages, tasks and fragments.
- **Learner action**: validate the actor, mission, step and revision; never trust role names supplied by a browser.
- **Learning evidence**: reference educational artifacts without leaking answers into Orgo or exposing peer records.

For conceptual shapes and non-implemented endpoint examples, see [Integration Contracts](Integration-Contracts). For runtime ordering, see [Mission Lifecycle](Mission-Lifecycle).

## Related source material

- Kontexte: `docs/ekole-orgo/02_ARCHITECTURE_CIBLE.md` and `docs/decisions/ADR-001-ORGO-CANONIQUE.md`.
- kompose: `docs/b6/ARCHITECTURE.md`; `contracts/schemas/kontexte-preview.schema.json`.
- Orgo: `docs/Technical-Reference/SCENARIO_INJECTOR.md`.
- Orgo_Worlds: `docs/Technical-Reference/Worlds/04_DATA_OWNERSHIP_MATRIX.md`.
- Local bridge: `Ekole_Pont_Missions_v4_1/RAPPORT_SIX_DEPOTS.md`.
