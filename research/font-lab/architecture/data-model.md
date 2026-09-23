# Canonical data model — proposal

Editable source is deterministic UTF-8 JSON (`schemaVersion`, stable IDs, sorted keys). Generated UFO/Designspace and binaries are derived, never the source of truth. Human-readable JSON avoids custom parser/YAML ambiguity; use a JSON Schema and migration functions. Store app state separately from font geometry and retain unknown future fields only through explicit migrations.

| Entity | Responsibility, key fields and references |
|---|---|
| `FontProject` | root ID, schemaVersion, name, engine ID/version, scripts, axis values, glyph map, presets, export profiles, provenance |
| `StyleEngine` | versioned recipe registry and valid parameter domain; references `GlyphRecipe` and grammar version |
| `Glyph` | stable ID, Unicode scalar(s), production name, script, recipe ID, metrics, anchor IDs, local overrides, chosen switch |
| `GlyphRecipe` | construction family, ordered component graph/point IDs, constraints, optical rules; references primitives |
| `Component` | primitive type, local parameters, transform, parent/children and stable contour ID |
| `Axis` | semantic ID, UI range/default, mapping function, optional four-letter OpenType tag, exportability |
| `LocalAxis` | glyph ID + inherited/overridden axis, local domain/default; never implicitly becomes `fvar` |
| `StructuralSwitch` | enum ID, variants, default, recipe family per variant, optional `ssXX`/`zero` mapping |
| `Metrics` | unitsPerEm, vertical zones, advance, sidebearings, anchors and interpolation policy |
| `KerningGroup` | script-qualified side, member glyph IDs and pair exceptions; stable across compatible masters |
| `Preset` | immutable axis/switch/text snapshot, engine version and creation metadata |
| `Master` | generated location, compatible recipe family, source hash, validation report, UFO path |
| `Instance` | named coordinates, optional static export name and metrics profile |
| `ScriptModule` | script ID, repertoire, language forms, glyph groups, marks, specimen tests |
| `ExportProfile` | format(s), switch branch, axes, subset policy, family naming, validation threshold |

Serialization/versioning by owner: `FontProject` is one JSON document with a required top-level `schemaVersion`; `StyleEngine` is a referenced, independently versioned recipe package; `Glyph`, `GlyphRecipe`, `Component`, `Axis`, `LocalAxis`, `StructuralSwitch`, `Metrics`, `KerningGroup`, `Preset`, `ScriptModule` and `ExportProfile` are nested JSON objects with stable IDs and schema-governed fields. Recipe/component and axis/switch schema changes require explicit migrations because they can alter geometry. `Master` and `Instance` are JSON manifest records keyed by source hash and compiler version, with UFO/Designspace as separate generated files; they are regenerated rather than migrated as editable data. Unicode mappings, anchors and kerning references always use stable glyph IDs, never array positions.

Example source fragment:

```json
{
  "schemaVersion": 1,
  "id": "project-demo",
  "styleEngine": { "id": "geometric-technical-sans", "version": "0.1" },
  "scripts": ["Latn", "Cyrl"],
  "axes": { "weight": 0.5, "width": 0.5 },
  "glyphs": {
    "a": { "recipe": "a.double", "switches": { "aForm": "double" }, "localAxes": { "aperture": 0.6 } }
  }
}
```

Serialization contracts: normalized source values 0–1 where useful, explicit units for geometric dimensions, immutable enum identifiers, no raw code or executable expressions in project files. Migrate vN→vN+1 with fixture tests; compiler records its exact version and source hash. `Master` and `Instance` metadata may appear in project manifest but generated contours do not. Preset references must match engine version or pass a migration. Reject unknown switch IDs and out-of-range coordinates with typed diagnostics.
