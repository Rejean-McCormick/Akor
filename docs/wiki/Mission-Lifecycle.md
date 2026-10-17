# Mission Lifecycle

This is the **proposed Akor integration lifecycle**. Orgo owns actual operational transitions. Akor adapts approved intent and presents authorized views.

## Phases

| Phase | Primary actor | Meaning |
| --- | --- | --- |
| Draft | Scenario editor / Kontexte | Write mission, roles, story, learning links and optional fragments |
| Preview | kompose + Akor | Validate references, compile deterministic projections, detect mismatches |
| Review | Teacher/editor | Verify content, accessibility, target course, dependencies and release rules |
| Release | Orgo_Worlds and authorized publisher | Pin reviewed WorldRelease and approved content versions |
| Launch | Teacher → Akor → Orgo | Open the mission through approved server-side contracts |
| Participate | Children and teachers → Orgo | Receive tasks, cooperate, request help, submit work |
| Observe | Teacher and Ekole | Monitor activity and capture evidence without public ranking |
| Pause/recover | Orgo | Suspend, reconnect, reassign/fallback or resume safely |
| Close | Orgo | Close operational mission state and produce minimal completion receipts |
| Review learning | Ekole/teacher | Evaluate learning evidence separately from operational completion |

## Important conditions

- **Draft and preview are not authorization.** A passing local test does not publish content to children.
- **Human approval is not a JSON boolean controlled by a student.** It requires a trusted actor and an auditable action.
- **A running mission must not drift.** Pin scenario/WorldRelease/contract versions.
- **Orgo must own operational time and state**, including solo missions; no second local scheduler in Akor or Ekole.
- **Academic mastery stays in Ekole**, and completion is never sufficient proof on its own.

## Conceptual events (NOT established API event names)

| Event intent | Purpose |
| --- | --- |
| `mission_requested` | Teacher requests start of a reviewed mission |
| `role_projection_available` | Authorized role view can be rendered |
| `contribution_submitted` | Learner contributed a document, answer or decision |
| `assistance_requested` | Learner asks for a hint or human support |
| `group_checkpoint_satisfied` | Orgo verifies a necessary collaboration condition |
| `mission_paused` / `mission_resumed` | Orgo reports operational suspension and recovery |
| `mission_closed` | Orgo reports closure |
| `learning_evidence_recorded` | Ekole records separate educational evidence |

**These labels are documentation placeholders.** Before implementation, map each one to actual reviewed Orgo routes, schemas, permissions and revision/idempotency semantics. See [Integration Contracts](Integration-Contracts).
