# Privacy, Safety, and Authorization

Akor's target audience includes children. Collaboration introduces risks: seeing another learner's details, disclosing role secrets, unmoderated contact, peer pressure, identity confusion, and publication of work without review. **Privacy and access control must be designed before a classroom deployment.**

## Non-negotiable boundaries

1. Learner browsers receive **only authorized projections** for their authenticated session. Never send every fragment and hide unwanted ones with CSS or JavaScript.
2. A URL parameter, browser role selector or self-declared role is **not** authorization.
3. Teacher prompts, confidential answers, diagnostics, unpublished media and private drafts stay outside the learner API.
4. Avoid persistent direct-message or open chat between minors unless separately justified, moderated and governed.
5. No real-world purchases, contact with strangers, external emails or public posting from a fictional scenario without explicit, separate adult authorization.
6. Separate real identity from synthetic personas and narrative roles.
7. Do not equate World membership with global Orgo permission.
8. Do not store peer ability rankings, behavioral inferences, or unnecessary activity traces.
9. Define retention and deletion controls before retaining student evidence, messages, media, or role history.
10. When trust checks fail, sensitive mission actions and projections **fail closed**.

## Authentication model

Orgo's snapshot supports local authentication and optional OIDC, with federated identity matched by **issuer + subject**, followed by Orgo-local RBAC. Orgo_Worlds provides World membership/context but does not create a second login. Akor should use only trusted school integration/session mappings. It must not automatically link users based on email or accept one product's roles as another's permission.

## Threats to test

| Threat | Expected control |
| --- | --- |
| Child changes a role ID in a URL | Server rejects unauthorized role/projected data |
| Learner guesses another team's mission ID | Tenant/group scoped authorization blocks read and write |
| Old browser replays an earlier task submission | Version/revision and idempotency checks prevent duplicate advancement |
| Cached fragment remains after role reassignment | Refresh/revoke projections, limit stale access, audit where needed |
| Absent partner causes deadlock | Teacher-approved fallback; no false impersonation |
| Public course API exposes answer keys | Publication filtering and regression tests |
| Mission service is unavailable | Explain outage; no local shadow runtime |
| Teacher account accesses wrong school | Organization/world/course scoping |

## Consent and governance

Real learner data requires school policy, privacy review, appropriate consents and jurisdiction-specific compliance checks. The wiki does not claim any legal compliance certification. Avoid using identifiable student data during early pilot testing; use fictional accounts and synthetic artifacts.

## Existing limitations

The current Akor precursor is a read-only, no-token dry-run bundle. It has **not** demonstrated the multi-student identity, access, moderated interaction or retention controls described here. These are release gates, not completed features.
