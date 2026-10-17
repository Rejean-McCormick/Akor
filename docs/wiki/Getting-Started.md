# Getting Started

## If you just want to read the wiki

Start with [Home](Home), then [Vision and Name](Vision-and-Name), [Collaborative Learning Principles](Collaborative-Learning-Principles) and [Village Bakery Walkthrough](Village-Bakery-Walkthrough).

This directory is structured for a **GitHub Wiki**, with `Home.md`, `_Sidebar.md` and `_Footer.md`. It can also live as project documentation in a normal Git repository. No web service is needed to read these Markdown files.

## Proposed standalone repository layout

```text
C:\mycode\Ekole\
├── ekole\
├── ekole-quebec\
├── Kontexte\
├── kompose\
├── Orgo\
├── Orgo_Worlds\
└── akor\
    └── docs\
        └── wiki\
            ├── Home.md
            ├── _Sidebar.md
            └── ...
```

This is a **proposed layout**. The `akor` Git repository has not been created by this documentation task.

## Current runnable precursor

`Ekole_Pont_Missions_v4_1` is an independent read-only prequalification bundle. With the six repositories side by side on Windows, it exposes `LANCER_REVUE_MISSIONS.bat` and an optional Python CLI `pont_missions.py`.

The bridge compiles review-only role projections, calls Orgo's injector in `validate` and `plan` mode, and produces a local teacher review HTML page. It does **not** create live tasks or authorize student fragments.

To run a local rehearsal, use the documented commands in that bundle's `README.md`; verify that its checkout paths point to the intended snapshots and use only synthetic material. Do not assume it is a deployed Akor API.

## Publishing as a GitHub Wiki

For a repository with its wiki enabled, its wiki uses a separate Git repository, conventionally named `<repository>.wiki.git`. You can copy these Markdown pages into that wiki checkout and commit them there. For example (replace the placeholder organization and repository URL with your own):

```bash
git clone https://github.com/OWNER/akor.wiki.git
# Copy contents of this Akor.wiki directory into the cloned folder.
cd akor.wiki
git add .
git commit -m "Document Akor collaborative learning vision and contracts"
git push
```

If the wiki does not yet exist or your host disables wiki features, place the files under `docs/wiki/` in the main repository instead. Do not overwrite an existing wiki without comparing its content.

## Next development step

Implement a reviewed **solo** bakery mission on an isolated Orgo test environment using fictional accounts. Do not start with production school data. See [Roadmap](Roadmap), [Integration Contracts](Integration-Contracts) and [Testing and Acceptance](Testing-and-Acceptance).
