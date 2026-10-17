# Testing and Acceptance

Akor must prove **both** that systems coordinate correctly and that children's cooperation is meaningful, fair and safe.

## Test layers

### 1. Pure contract and content tests

Validate scenario/role IDs, dependency DAG, curriculum mapping, source hashes, locale completeness, schema version, unsupported fields and teacher publication status. Reuse Kontexte and kompose validators instead of reimplementing them.

### 2. Permission and confidentiality tests

- Anonymous actors cannot enter a learner or teacher mission.
- Learner A cannot read learner B's role-restricted fragment or academic artifact.
- An unauthorized role switch cannot unlock a different projection.
- Unpublished resources and teacher-only answers never appear in public APIs, HTML, caches or exports.
- Cross-group, cross-world and cross-organization access fails closed.

### 3. Orgo runtime and resilience tests

Verify authoritative transition history, idempotency, conflict rejection, stale clients, failed requests, duplicate events, pause/resume, offline behavior, and recovery after a worker or network disruption. `validate` and `plan` alone are **insufficient** for these tests.

### 4. Collaboration tests

Two browser sessions and independent fictional identities should receive different information and each have a meaningful contribution. Group advancement must depend on authorized exchanges or a documented teacher-approved fallback; one learner must not fake another learner's completed work.

### 5. Pedagogical and accessibility tests

Verify instructions suitable for the age, communication alternatives, keyboard navigation, error feedback, understandable waiting states, and teacher visibility of individual reasoning. Review with educators; involving children requires appropriate permissions and safeguards.

## Minimum vertical acceptance for the bakery

| # | Acceptance criterion | Evidence required |
| --- | --- | --- |
| 1 | Correct, approved multiplication scenario | Traceable reviewed variant linked to `qc-pri-ma-008` |
| 2 | Stable WorldRelease | Pinned immutable release reference |
| 3 | Orgo owns state | Real workflow/Task evidence, no Akor shadow transition |
| 4 | Teacher controls launch | Authenticated launch with approved permissions and audit |
| 5 | Safe learner projections | Cross-role and cross-team denial tests |
| 6 | Two-child interaction | End-to-end scenario where separate contributions are necessary |
| 7 | Absence, pause and reconnect | No deadlock, no false contribution, clear recovery |
| 8 | Correct learning boundaries | Ekole educational evidence distinct from Orgo completion |
| 9 | Accessibility | Keyboard, mobile, readable instructions and communication alternative |
| 10 | Failure/rollback | Reproducible test run, logs without child secrets, safe degradation |

## Current test evidence

The prequalification bridge reported **six local tests passing**, while Kontexte and kompose reported their own isolated test suites. Orgo's Scenario Injector `validate` and `plan` passed for a **synthetic preparation** fixture; no production apply, multi-student session or fully integrated Playwright test was performed. The 11 successful Ekole Playwright checks were for Ekole v4 functionality, not Akor's future collaboration.

Do not mark the table above complete because a static role preview exists.

## Example Playwright cases to build

- Teacher reviews and starts a version-pinned sandbox mission.
- Child A sees only baker's authorized screen.
- Child B sees only farmer's authorized screen.
- Attempts to access another fragment are denied server-side.
- Repeated submit does not double-progress.
- Delayed member is recoverable without humiliation or ranking.
- An authorized group checkpoint updates after a genuine exchange.
- Teacher stops the activity; both screens become non-mutating.
- Ekole records reviewed learner evidence separately.

All examples are **planned tests**, not currently committed passing tests.
