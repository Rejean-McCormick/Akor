# Integration Contracts

**Status: contract-design guide, not a published Akor HTTP API.** Names and JSON sketches below are **proposals**. Implementations must first check actual versions, routes, ownership and permission models in all neighboring repositories.

## Inputs that exist in the supplied sources

| Source | Artifact or contract | Use |
| --- | --- | --- |
| Kontexte | `kontexte.mission/1` | Role/step/fragment/join intentions |
| kompose | `kompose.kontexte-preview/1` | Deterministic, safe, non-dispatchable preview |
| Orgo | `orgo.scenario.v1` | Controlled scenario injector format |
| Orgo_Worlds | World/WorldRelease docs | Versioned release context and memberships |
| Ekole | v3/v4 publication separation | Course content/teacher access/learning evidence boundary |

**Source snapshot:** six archives dated October 17, 2026, as listed in [Project Status](Project-Status).

kompose's preview schema explicitly requires `preview_only=true`, `dispatch_allowed=false`, `canonical_runtime="orgo"`, and marks joins as `orgo_not_implemented`. A preview must not be silently reinterpreted as an authorization to start a session.

## Required contract families (proposed)

### A. Reviewed mission manifest

Record stable content references, source hashes, approved objective mapping, review decision, WorldRelease and the compatible Orgo workflow version.

```json
{
  "contract": "akor.review-manifest/0-DRAFT",
  "scenario": {"id": "boulangerie", "source_version": "0.1.0"},
  "reviewed_variant": "boulangerie-multiplication-DRAFT",
  "curriculum": {"course_id": "qc-pri-ma-008", "status": "PENDING_HUMAN_REVIEW"},
  "world_release_ref": null,
  "orgo_workflow_ref": null,
  "launch_eligible": false
}
```

This is an **illustrative non-operational record**, not an accepted payload for Orgo or Ekole. It deliberately cannot launch anything.

### B. Trusted launch request

Akor's server-side adapter must receive trusted teacher identity and session context, inspect approved content and permissions, and invoke only a reviewed Orgo contract. Define tenant/world/group scopes, expected revision, expiration, correlation ID and idempotency key. **Do not invent endpoint paths and assume they exist.**

### C. Learner-safe projection

The response should include only a learner's permitted task, role vocabulary, currently released information, allowed actions, accessible supports and a state revision. It must exclude:

- other groups' records;
- unreleased fragments and answers;
- teacher-only constraints and private review notes;
- raw Orgo service credentials;
- information about a peer's health, supports or scores.

### D. Contribution submission

Treat every submission as a **command**, not an assumed success. Verify identity, authority, mission/session binding, expected revision, payload size/type and idempotency. A valid receipt means that a contribution was recorded, not automatically evaluated.

### E. Learning evidence reference

Use a minimal pseudonymous reference to connect an operational event to an Ekole-owned artifact where authorized. Include source version, objective, conditions, time and review status. The **full pupil work and interpretation** should stay in its educational owner.

### F. Failure and recovery

Return a clear outcome for unauthorized, stale state, unavailable partner, paused session, service outage, invalid revision and duplicate submission. Never fall back to local mission progression without explicit architecture approval.

## Compatibility and evolution

- Record schema versions and rejected unknown/unsafe payloads.
- Use a per-repo adapter and contract tests, rather than copying internal database types across products.
- Pin WorldRelease and mission revisions for active sessions.
- Support idempotent retries at both transport and business-operation boundaries.
- Avoid exposing sensitive payloads in logs or generated reports.
- Document which errors are retryable, which need human intervention, and which are forbidden.

## Orgo Scenario Injector boundary

Orgo's existing injector defaults to **dry-run** and supports `validate` / `plan`. `--apply` is mutating and requires an explicitly authorized, isolated test environment. It does not accept arbitrary HTTP routes or raw SQL. Current bakery fixtures validate a **preparation case and task**, not a complete collaborative classroom workflow.

See [Architecture and Ownership](Architecture-and-Ownership), [Information Sharing and Joins](Information-Sharing-and-Joins), and [Testing and Acceptance](Testing-and-Acceptance).
