# Development and local usage

## Source tree

- `src/akor/preflight.py`: non-mutating adapter/compiler, derived from the previously reviewed `pont_missions.py`.
- `run_akor.py`: convenient CLI without an editable installation.
- `tests/`: local safety tests and optional six-repository integration tests.
- `docs/wiki/`: the English Akor wiki.
- `examples/sample_review/`: generated-example snapshots, **not** a published student page.
- `output/`: ignored local preflight output.

## Prerequisites

Python 3.10 or later and Node.js 18 or later, plus six sister repositories with their current contracts. There are no third-party Python dependencies for the preflight. Node is used only to run the official Orgo and Orgo_Worlds validation scripts.

```
Ekole/
  akor/
  ekole/
  ekole-quebec/
  Kontexte/
  kompose/
  Orgo/
  Orgo_Worlds/
```

On Windows, launch `LANCER_REVUE_AKOR.bat`. On any OS:

```sh
python run_akor.py --root /path/to/Ekole --out /path/to/Ekole/akor/output
```

Override individual locations using `--ekole`, `--ekole-quebec`, `--kontexte`, `--kompose`, `--orgo`, and `--orgo-worlds` when repositories are not siblings.

## Tests

```sh
python -m unittest discover -s tests -v
```

To test against all six external source repos, set `AKOR_TEST_SIBLINGS` to their common parent (or install Akor alongside them). The integration tests are skipped without the sources, **not** silently treated as passing.

## Security

Never commit `output/`, tokens, teacher session keys, learner records, or private role clues. Run the sample mission only as a synthetic review; do not attach it to real student identities. Outputs are intentionally teacher-oriented and must not be publicly hosted as an operational student experience.
