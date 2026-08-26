# CLAUDE.md — oblinux-brand-master

**AGENTS.md is the authoritative repository operating guide. CLAUDE.md
supplements it for Claude Code and must not establish competing repository
policy.**

## Before doing anything in this repository

1. Read `AGENTS.md` at the repository root, in full, before performing any
   repository work.
2. Treat it as the authoritative source for this repository's role,
   architecture, canonical/generated/reference/integration asset boundaries,
   ownership rules, validation scope, Git safety, and release/promotion
   process. Follow those rules exactly as written there — they are not
   restated here.
3. Consult the relevant docs referenced by AGENTS.md (e.g. `docs/RELEASING.md`,
   `docs/INTEGRATION.md`, `docs/SURFACES.md`) before modifying the associated
   subsystem, rather than assuming how it works.
4. Preserve this repository's own architecture. Do not carry over assumptions,
   structure, or conventions from another OBLinux repository (`oblinux-debian-iso`,
   `oblinux-arch-iso`, their `-dev` variants, or the legacy `oblinux` repo).

## Hard constraints (per AGENTS.md)

- Never claim validation, build, runtime, or visual testing that was not
  actually performed — state plainly what was run and what was not.
- Respect the boundaries between stable, development, Brand Master, and
  legacy repositories exactly as AGENTS.md defines them. Do not modify
  sibling repositories from here.
- Never force-push or rewrite published Git history (including tagged
  releases) unless the owner explicitly authorizes it for a specific
  recovery situation.
- Never promote development changes into a stable repository, or bump
  versions/create tags, without explicit owner approval.
- When it's unclear whether a change belongs here or downstream, or whether
  locked canonical artwork may be touched, stop and ask the owner rather than
  guessing.

## Git Commit Policy

This policy applies to every Git commit Claude Code creates in this
repository:

- Use only the repository's configured Git author identity. Do not modify
  Git author or committer identity to represent Claude or Anthropic.
- Do not add `Co-Authored-By` trailers for Claude, Anthropic, or any AI
  system.
- Do not add `Generated-By`, `Assisted-By`, `AI-Generated`, or similar AI
  attribution trailers.
- Do not mention Claude, Anthropic, Claude Code, AI assistance, or automated
  generation anywhere in the commit message.
- Do not add Claude or Anthropic as a contributor, or add any attribution
  trailer, unless the owner explicitly requests one for a specific commit.
- Write normal, professional commit messages that describe the actual
  repository change — nothing more.

Example — correct:

```
Integrate Brand Master v1.0.2
```

Example — incorrect:

```
Integrate Brand Master v1.0.2

Co-Authored-By: Claude Sonnet <noreply@anthropic.com>
```

The repository's configured human Git identity remains the sole commit
attribution unless the owner explicitly instructs otherwise.
