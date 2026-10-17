# Roles and Social Interactions

## Role ≠ account ≠ permission

A **narrative role** describes how a learner participates in a fictional situation: baker, farmer, accountant, inventor, explorer. It does not determine authenticated access rights merely because a client requests a matching role name.

Akor must distinguish:

- **Identity**: a trusted, authenticated learner or teacher reference.
- **Membership**: the participant belongs to a particular mission session.
- **Narrative role**: the story perspective, tasks, resources and vocabulary.
- **Authorized projection**: what the participant may actually view or act on at this moment, derived from trusted Orgo decisions.

## Four dimensions of a meaningful role

| Dimension | Question |
| --- | --- |
| Purpose | What important outcome is this person helping the group achieve? |
| Contribution | What can this child create, discover, explain, verify, or decide? |
| Dependency | Whose input do they need, and who needs theirs? |
| Interaction | What conversation, hand-off, comparison, or joint action results? |

Role skins (character, colors, icons, language) may vary. They must not reveal private support needs or create academic inequality.

## Example: the bakery

The existing Kontexte source `data/missions/boulangerie.json` defines three roles: `boulanger` (baker), `fermier` (farmer), and `comptable` (accountant). It has three review-only steps, two role-specific fragments and a proposed join. All are synthetic and await pedagogical review.

A future Akor interaction might ask:

- The **baker** to plan a set of equal trays.
- The **farmer** to verify available quantities.
- The **accountant** to reconcile the order and explain the calculation.

This *interaction design* is a proposal; it is not the exact executable behavior of the existing JSON skeleton.

## Role selection and assignment

Proposed teacher options include: child preference, a teacher-selected role, fair rotation across activities, or a supported assignment. Any automated recommendation must be inspectable, overridable and must not expose inferred disability or ability labels.

In small groups, avoid roles that are purely ceremonial. With a missing partner, use an explicitly authorized fallback: role combination, teacher acting as a partner, or marked fictional helper—never an invisible claim that another child completed the work.

## Channels of interaction

- Face-to-face talk and manipulatives in the classroom.
- Structured short messages inside the mission (only if moderated and authorized).
- Shared artifacts with attribution suitable for the age group.
- Teacher-facilitated hand-offs and decisions.

An open, unmoderated social network is **outside scope**. Akor should transmit only the minimum information needed for the learning action.

See [Information Sharing and Joins](Information-Sharing-and-Joins), [Teacher Experience](Teacher-Experience), and [Privacy and Safety](Privacy-and-Safety).
