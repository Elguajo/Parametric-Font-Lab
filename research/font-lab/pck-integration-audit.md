# PCK integration audit

Observed 2026-09-23 from tracked tree, `git status`, and `.progressive/` routing. This is a PCK workflow scaffold, not an existing web application: no `src/`, package manifest, Python service, UI component library, CI workflows, product tests, or build scripts. `PROJECT_BRIEF.md` and `ARCHITECTURE.md` are `UNINITIALIZED`. `ROADMAP.md` has one active Phase 0 but its spec link points to `.progressive/project/phases/...`; the actual tracked spec is `.progressive/phases/00-research/RESEARCH_SPEC.md`. Two user references already exist at their requested paths and are not to be changed.

| Reusable PCK capability | Use in Font Lab |
|---|---|
| `AGENTS.md`, `.agents/skills/*`, `.progressive/system/QUALITY_PROTOCOL.md` | Routing, decisions, implementation/verification discipline |
| `.progressive/project/{ROADMAP,NEXT_SESSION,CONTEXT_MANIFEST}.md/json` | Phase state and handoff; keep canonical ownership |
| `.progressive/tools/{context_compile,audit,routing_integrity}.py` | Context and workflow checks |
| `.progressive/templates/{ADR,PHASE_COMPLETION}.template.md` | Decision and phase evidence format |
| `.progressive/integrations/*` | Optional tooling routes; no need to install for Phase 0 |

Future product placement: root `apps/font-lab-web/` and `services/font-build/`, with a shared versioned JSON schema at `packages/font-model/` only once code exists. Keep PCK metadata under `.progressive/` and research under `research/font-lab/`. Do not duplicate PCK phase state, ADR process, or tool registry in product code. No current package manager or monorepo convention exists, so Phase 1 may choose minimal tooling based on its first vertical slice. `.serena/` is local-only navigation configuration. External public repositories were inspected outside the worktree.

Constraints: PCK is project governance, not a runtime, job queue, UI kit, or export store. Any service, storage, caching, CI and upload policy is a future implementation decision. No production implementation is authorized by this phase.
