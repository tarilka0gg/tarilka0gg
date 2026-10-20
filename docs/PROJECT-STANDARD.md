# One standard for every project

What every repository of this account looks like, so that a person (or I, in a year) knows where things are.

## README

1. `# Name`, then one badge row, then a one-sentence description.
2. The badge row is the same everywhere, with only the badges that apply: **CI** (the repository has a workflow), **License** (it has a licence file),
   **Release** (it has GitHub releases), **Changelog** (it has `CHANGELOG.md`).
3. Screenshots, if the program has a window: a two-column table, a picture with a bold title and a one-line description under it, each picture a link to
   the full-size file. English locale, taken in a throwaway environment (the Simple Linux live session in a VM), no personal data.
4. The body says what it does, how to install and use it, how to build and test it, and, in its own short section, what was tested and what was not.
5. The end is `## Changelog` (one line linking `CHANGELOG.md`) and `## License`.

## CHANGELOG.md

[Keep a Changelog](https://keepachangelog.com/): `# Changelog`, one intro line, `## [Unreleased]`, then `## [x.y.z] - YYYY-MM-DD`, newest first.
Under a version, `### Added`, `### Changed`, `### Fixed` where they help; a plain list is fine for a small release. A repository without releases
(configs, scripts) needs none. The installer's file points to the Simple Linux changelog, whose releases are the images.

## Language

English by default. A program with a translation decides its language by [simple-locale](https://github.com/tarilka0gg/simple-locale):
`SIMPLE_LANG`, the shared `locale.toml`, the system locale.

## CI

A repository with code has `.github/workflows/ci.yml` that builds and tests it the way the README says; formatting is enforced only where the code
is already formatted. Repositories of shell scripts check the syntax (and ShellCheck errors).

## Commits

Author `tarilka0gg <216761460+tarilka0gg@users.noreply.github.com>`, no co-author lines. One topic per commit, a message that says why.
