# Contributing to Akor

Akor exists to support **meaningful interaction between children** without creating a second operational workflow engine. Please keep each change within the published component boundaries in `docs/wiki/Architecture-and-Ownership.md`.

Before opening a change, run `python -m unittest discover -s tests -v` and, where possible, exercise the six-repository integration fixture. Clearly mark any skipped test. Changes handling real children, authentication, permissions, fragment release, or persisted mission state require explicit architectural and safety review.

Do not add unreviewed student content or secrets to the repository. Do not make the read-only preflight perform Orgo writes.
