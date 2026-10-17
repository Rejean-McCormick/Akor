# Test results — Akor v0.1.0

Source baseline: six archive snapshots supplied on 2026-10-17.

## Executed in the build environment

- `AKOR_TEST_SIBLINGS=<six-sibling-source-root> python -m unittest discover -s tests -v`: **13 passed / 0 failed / 0 skipped**.
- `python run_akor.py --root <six-sibling-source-root> --out <scratch-output>`: successful. Source verification, Orgo injector `validate`, injector `plan`, and Orgo_Worlds architecture check all completed without writes to Orgo.
- `python -m compileall -q src run_akor.py tests`: successful.
- Standalone tests without sister repos: **6 passed / 7 skipped**, explicitly. They are not equivalent to the integration tests.
- Source checks: original source bytes preserved in tests, private clue text absent from generated review files, and output inside a sister repo refused.

## Known blockers (not failures hidden by the tests)

- Kontexte bakery mission still maps to `qc-pri-ma-006` whereas the proposed Grade 3 multiplication course is `qc-pri-ma-008`.
- No approved and pinned bakery WorldRelease, no full Orgo role-guarded join workflow, no classroom identity, and no authenticated multi-child learner UI.
- No live Orgo backend, database, Ekole UI integration, or Windows BAT execution was tested end to end by this build.

The preflight's `validate` and `plan` operations are checks **only**. Neither passing tests nor static review authorizes publishing a mission to children.
