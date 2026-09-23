# Reuse policy for Phase 1

1. **Reference only:** Metaflop UI/assets/source, Bespoke glyph algorithms, Fontra/Glyphr/BirdFont editors, FontForge internals and Recursive outlines. Write original geometry and interface code. Do not transplant GPL routines/CSS or trace glyphs from source fonts.
2. **Allowed dependencies subject to pinned notice audit:** fontTools (MIT), fontmake/ufo2ft (Apache family; verify each dependency), opentype.js (MIT), optional HarfBuzz core/WASM under its applicable notices. Keep third-party notices and exact version hashes in release artifacts. Closed-source use of permissive components is feasible under their terms.
3. **Potential fork:** Folent (MIT) code can be forked with notice, but its contour matching is unsuitable for production font interpolation; no reason to fork in V1. Fontc/Coldtype can be evaluated separately; no fork planned.
4. **Fonts/assets:** do not import, morph or redistribute commercial fonts; OFL fonts require their own notices, reserved-name checks, and OFL continuity for modified font software. Keep user-supplied font rights separate from app license. No Metaflop-generated/Bespoke/Recursive outlines enter PFL recipes.
5. **Attribution files when shipping:** `THIRD_PARTY_NOTICES.md` for runtime packages and bundled assets; per-font OFL/notice in any test font package; source-level provenance manifest for generated original glyphs. Recheck transitive licenses when actual dependency graph exists.

This is a conservative implementation policy derived from primary files, not a substitute for legal review of unusual deployment models. Unknown license (UFO spec prose) means no copying, not permission.
