# Phase 0 Definition of Done audit

Checked against `RESEARCH_SPEC.md` §31 on 2026-09-23. “Complete” means the research artifact/evidence exists; it does not mean the future product works.

| Criterion | Evidence / status |
|---|---|
| Metaflop reverse-spec | `metaflop/reverse-spec/*`, `metaflop/ui/reference-measurements.md`: complete from offline DOM/CSS, screenshot and source; dynamic file-browser observation blocked and identified |
| User SingleFile + screenshot used and preserved | `metaflop/screenshots/README.md` with unchanged SHA-256; complete |
| Official Metaflop source and Bespoke engine | `metaflop/parameters/{engine-analysis,limitations}.md`, pinned commit links; complete |
| Parameters and limitations | 16-parameter table and limitation analysis; complete |
| Alternative engines | `engines/comparison-matrix.md`, 15 resolved HEADs in `sources/repositories.json`; complete, unknown features marked `?` |
| Primary-source licenses | `licenses/license-matrix.md`, direct-file hash manifest; complete with UFO spec document license explicitly unconfirmed after root LICENSE 404 |
| PCK integration audit | `pck-integration-audit.md`; complete |
| Browser outline spike works | `spikes/browser-outline/`: Chromium observed parse, SVG path, live text, control update; complete for tiny original font |
| UFO/Designspace variable build | `spikes/variable-build/`: two UFOs, Designspace, OTF/TTF/VF/WOFF2, instancing check; complete |
| Global/local/switch spike | `spikes/local-axis/`: six cases and topology assertion; complete |
| Data model | `architecture/data-model.md`; complete as proposal |
| Axes model | `architecture/axes-model.md`; complete as proposal |
| Structural switches | `architecture/structural-switches.md`; complete as proposal |
| Latin/Cyrillic architecture | `architecture/script-system.md`; complete as proposal; native quality review remains Phase 1 |
| MVP scope | `final/mvp-scope.md`; complete with reduced V1 scope |
| Risk register | `final/risk-register.md`; complete |
| ADRs | `decisions/ADR-001` through `ADR-010`; complete as Phase 1 proposals |
| Final report and JSON | `final/RESEARCH_REPORT.md` and `final/research-summary.json`; complete |
| Executable next task | Report §9 / `.progressive/phases/01-technical-sans-mvp.md`; complete |

Known evidence limits: SingleFile has no scripts and browser policy denied direct file rendering; static DOM/CSS plus official JS cover behavior with remaining dynamic UX points named. Tiny spikes do not establish whole-font quality or export readiness. These limits do not require the two reference files from the user; both files were present.
