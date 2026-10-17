# Information Sharing and Joins

One way to make children interact is to distribute **complementary fictional information** and help them combine it through discussion. However, controlling information is a **security-sensitive runtime function**, not just a visual trick.

## Existing Kontexte source

The bakery draft contains:

- `indice-un`: held by role `boulanger`, released when `orgo_authorized`.
- `indice-deux`: held by role `fermier`, released when `orgo_authorized`.
- `jointure-infos`: combines those references before unlocking `phase-3`.

The source *describes an intention*. It does not prove that Orgo already enforces the fragment join in a school session. kompose's current preview explicitly marks such enforcement as **not implemented in Orgo for this pilot**.

## Proposed safe release flow

```text
Teacher approves a reviewed mission version
    ↓
Orgo creates/advances a mission session and authenticates actors
    ↓
Orgo decides that fragment A is available to participant 1
    ↓
Akor receives only the authorized recipient projection
    ↓
Child 1 discusses or shares an approved fact with child 2
    ↓
Orgo validates required receipt, join or checkpoint
    ↓
Akor updates both role views from authoritative state
```

**Never** download the whole mission JSON to all learners and hide private fragments with CSS, client-side filters or a role dropdown.

## Interaction must not become a trap

A partner may be absent, refuse, need more time or disconnect. A safe mission needs a teacher-approved fallback with traceable origin, and must never simulate another child's contribution as genuine evidence.

Disclosure rules should cover membership changes, late joins, reassignments, stale tabs, reconnects and repeated submissions. Every operation should be idempotent where appropriate, and sensitive projections should fail closed when permission checks cannot be completed.

## Join guarantees to qualify with Orgo

- Deterministic workflow version and pinned WorldRelease.
- Authorized recipient and trusted actor identities.
- Replay/duplicate event handling and revision conflict detection.
- Server-side verification of required contributions and human review.
- Explicit override/fallback path and corresponding audit event.
- Content release history without unnecessary personal details.
- No peer-owned secret or teacher answer in a public learner endpoint.

These guarantees are acceptance criteria, **not claims of completed Akor functionality**.
