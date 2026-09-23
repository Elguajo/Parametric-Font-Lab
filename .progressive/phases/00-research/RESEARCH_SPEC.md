# ТЗ: Research Phase — Parametric Font Lab для PCK

## 0. Цель этапа

Провести максимально полный исследовательский этап перед разработкой собственного веб-инструмента **Parametric Font Lab** внутри/поверх PCK.

Цель будущего продукта: веб-генератор шрифтов с live-preview и параметрическими осями/ползунками, позволяющий:
- менять Weight, Width, X-height, Contrast, Roundness/Superness, Aperture, Mono amount, Optical/Text↔Display, Tech/Neutral и другие параметры;
- переключать дискретные конструкции глифов (`a`, `g`, `4`, `0`, `Q` и др.);
- поддерживать Latin + Cyrillic;
- сохранять presets;
- сравнивать варианты A/B;
- в перспективе смешивать совместимые стилевые модели;
- экспортировать production-ready font sources и бинарные шрифты (OTF/TTF/Variable TTF/WOFF2).

**На этом этапе НЕ строить production-продукт.**
Нужно провести исследование, reverse-spec, технические спайки, зафиксировать архитектуру и подготовить проект так, чтобы следующий этап разработки можно было начать без дополнительного ручного исследования со стороны пользователя.

---

# 1. Что пользователь предоставляет вручную

Пользователь делает только две вещи:

1. Сохраняет страницу Metaflop Modulator через расширение **SingleFile**.
2. Делает **full-page screenshot** этой же страницы.

После этого пользователь кладёт/передаёт оба файла в проект.

**Всё остальное Codex должен выполнить самостоятельно.**

Не просить пользователя:
- скачивать GitHub-репозитории;
- искать лицензии;
- выписывать параметры;
- описывать layout;
- измерять UI;
- искать технологический стек;
- сравнивать альтернативы;
- собирать ссылки;
- делать архитектурные выводы;
- вручную переносить ассеты;
- готовить структуру проекта.

---

# 2. Принцип исследования

Metaflop используется как:
- UX/reference;
- источник паттернов взаимодействия;
- источник идей параметрической модели.

**Не считать целью прямой порт Metaflop.**

Нужно разделять:

### A. Visual/UX reference
Что в интерфейсе Metaflop удобно и должно быть сохранено или переосмыслено.

### B. Interaction model
Какие состояния, действия, preview-механики и зависимости параметров существуют.

### C. Font-generation engine
Что реально генерирует контуры и какие ограничения есть у текущей архитектуры.

### D. Production font pipeline
Как из параметрической модели получить корректные UFO/Designspace/OTF/TTF/Variable Font/WOFF2.

---

# 3. Обязательное правило перед исследованием

Перед любыми изменениями:

1. Изучить текущий PCK:
   - `AGENTS.md`;
   - project instructions;
   - package manager;
   - monorepo/workspace structure;
   - существующие UI components;
   - существующие dev tooling/scripts;
   - naming conventions;
   - test/lint/build setup;
   - существующие research/reference folders;
   - доступные PCK skills/tools.

2. Не создавать новую архитектуру рядом с существующей, если в PCK уже есть подходящий механизм.

3. Зафиксировать, какие возможности PCK можно переиспользовать.

Создать:
`research/font-lab/pck-integration-audit.md`

В нём:
- найденные reusable-компоненты;
- reusable tooling;
- ограничения PCK;
- рекомендуемое место будущего Font Lab;
- что нельзя дублировать.

---

# 4. Организация research workspace

Создать внутри проекта понятную исследовательскую структуру. Адаптировать путь под реальные conventions PCK, но логически сохранить:

```text
research/font-lab/
├── README.md
├── sources/
├── metaflop/
│   ├── reverse-spec/
│   ├── ui/
│   ├── parameters/
│   └── screenshots/
├── engines/
├── licenses/
├── spikes/
├── architecture/
├── decisions/
└── final/
```

Пользовательские файлы SingleFile + screenshot положить в отдельный read-only reference folder.

Не изменять оригинальные пользовательские reference files.

---

# 5. Metaflop: полный UI/UX reverse-spec

## 5.1 Источники

Codex самостоятельно:

1. Найти официальный сайт Metaflop.
2. Найти официальный `metaflop-www`.
3. Найти репозиторий/источник конкретного metafont, который используется в Modulator (например Bespoke, если это действительно он).
4. Зафиксировать:
   - URL;
   - repository;
   - branch/tag;
   - commit SHA;
   - дата доступа;
   - license file;
   - stack/dependencies.

Не доверять прежним устным предположениям.
Все лицензии проверить непосредственно по `LICENSE`, source headers и официальной документации.

---

## 5.2 Offline reverse-engineering SingleFile

SingleFile использовать как визуальную и DOM/CSS reference-копию.

Автоматически:

- поднять локально;
- открыть через browser automation / Playwright, если доступно;
- снять DOM tree;
- извлечь CSS;
- определить основные UI regions;
- определить интерактивные controls;
- сопоставить DOM с full-page screenshot;
- определить размеры и layout relationships.

Не копировать минифицированный код в будущий продукт.

---

## 5.3 Обязательные reverse-spec документы

Создать:

### `metaflop/reverse-spec/layout.md`
Зафиксировать:
- общую page grid;
- колонки;
- панели;
- sticky/fixed элементы;
- scrolling behavior;
- responsive behavior;
- размеры/пропорции основных областей;
- breakpoint behavior;
- hierarchy.

### `metaflop/reverse-spec/components.md`
Инвентаризация компонентов:
- navigation;
- parameter group;
- numeric field;
- slider/drag control;
- mode switch;
- reset/random/undo;
- glyph preview;
- glyph selector;
- alphabet chart;
- typewriter specimen;
- download/export;
- sharing;
- font selector;
- preset/metafont selector;
- прочие элементы.

Для каждого:
- purpose;
- state;
- input;
- output;
- dependencies;
- UX notes;
- reusable/not reusable.

### `metaflop/reverse-spec/interactions.md`
Зафиксировать:
- как пользователь меняет параметр;
- keyboard/mouse behavior;
- min/max;
- step;
- reset;
- undo;
- randomize;
- переключение glyph;
- typewriter editing;
- размер preview;
- download;
- share;
- loading;
- error/empty states;
- зависимость UI от выбранного metafont.

### `metaflop/reverse-spec/parameters.md`
Для каждого параметра:
- internal name;
- visible label;
- min;
- max;
- default;
- step;
- semantic meaning;
- affected glyph properties;
- expected visual effect;
- зависимости/конфликты;
- global/local classification;
- linear/nonlinear behavior.

### `metaflop/reverse-spec/design-tokens.md`
Извлечь:
- colors;
- background;
- border;
- typography;
- font sizes;
- line heights;
- spacing scale;
- radius;
- control heights;
- panel widths;
- icon sizes;
- focus/hover states.

Цель — получить достаточно данных, чтобы воспроизвести UX без повторного ручного дизайна.

---

# 6. Исследование font-engine архитектуры Metaflop

Codex должен понять не только UI, но и генерацию.

Исследовать:

- как metafont описывает glyph;
- какие параметры глобальные;
- какие параметры локальные;
- где задаются skeleton/components;
- как строятся curves/contours;
- как выполняются optical corrections;
- как решаются overshoot, taper, contrast;
- как задаётся spacing;
- есть ли kerning;
- как строятся accents;
- какие scripts/encodings поддерживаются;
- как происходит export;
- какие ограничения мешают сделать universal generator.

Создать:

`metaflop/parameters/engine-analysis.md`

И отдельно:

`metaflop/parameters/limitations.md`

В `limitations.md` обязательно ответить:
- почему текущий Metaflop не может генерировать практически любой стиль;
- какие параметры отсутствуют;
- какие structural switches отсутствуют;
- почему один skeleton не покрывает все семейства;
- где параметры начинают конфликтовать;
- что требуется для Latin + Cyrillic;
- что требуется для Text ↔ Display;
- что требуется для Proportional ↔ Mono;
- что требуется для variable fonts.

---

# 7. Обязательный research внешних решений

Не ограничиваться Metaflop.

Минимум исследовать и сравнить:

- Fontra
- fontTools / varLib
- fontmake
- opentype.js
- UFO / Designspace ecosystem
- HarfBuzz (если релевантен для shaping/preview)
- Glyphr Studio
- FontForge
- BirdFont
- Metaflop
- Recursive как reference variable-font architecture
- Folent / morphing-style tools
- современные parametric/generative font projects на GitHub

Codex должен также самостоятельно найти **дополнительные актуальные проекты**, если они релевантнее списка выше.

Для каждого кандидата зафиксировать:

- назначение;
- current status;
- language/stack;
- browser/server/CLI;
- license;
- variable-font support;
- designspace support;
- interpolation;
- component model;
- local axes;
- glyph editing;
- kerning;
- Latin/Cyrillic;
- export formats;
- suitability for reuse;
- integration complexity with PCK;
- major risks.

Создать:

`engines/comparison-matrix.md`

Не делать ranking вида “best overall” без аргумента.
Дать recommendations по конкретным слоям системы.

---

# 8. License / legal audit

Это обязательный deliverable.

Создать:

`licenses/license-matrix.md`

Для каждого исследованного проекта:

- repository;
- exact license;
- license source path;
- attribution requirements;
- copyleft/permissive;
- можно ли использовать код внутри закрытого продукта;
- можно ли модифицировать;
- можно ли распространять;
- есть ли ограничения на assets/UI/design;
- нужно ли открывать производный код;
- риск для PCK.

Особенно отдельно проверить Metaflop:
- website/source code;
- design/assets;
- metafont source;
- generated font license.

**Не делать юридических выводов на основании README, если есть LICENSE.**

Создать также:

`licenses/reuse-policy.md`

С решениями:
- что разрешено только как reference;
- что можно переиспользовать как dependency;
- что можно fork;
- что нельзя копировать;
- какие attribution файлы потребуются.

---

# 9. Исследование будущей Parametric Font Architecture

Codex должен спроектировать систему не как “30 sliders поверх одного шрифта”, а как расширяемый font designspace.

Обязательно исследовать модель:

```text
STYLE ENGINE
    ↓
GLYPH GRAMMAR
    ↓
GLOBAL AXES
    ↓
LOCAL AXES
    ↓
STRUCTURAL SWITCHES
    ↓
SCRIPT MODULES
    ↓
SPACING/KERNING
    ↓
OPTICAL CORRECTIONS
    ↓
UFO/DESIGNSPACE
    ↓
BUILD PIPELINE
```

---

# 10. Glyph Grammar research

Определить минимальный набор reusable primitives/components.

Исследовать необходимость:

- Stem
- Crossbar
- Bowl
- Counter
- Arch
- Shoulder
- Spine
- Diagonal
- Leg
- Tail
- Terminal
- Aperture
- Join
- Spur
- Overshoot zone

Для каждого:
- параметры;
- constraints;
- optical corrections;
- какие glyphs используют.

Создать:

`architecture/glyph-grammar.md`

---

# 11. Axes model

Спроектировать потенциальные global axes.

Минимально исследовать:

```text
Weight
Width
X-height
Cap-height
Contrast
Roundness
Superness
Aperture
Terminal angle
Taper
Optical/Text↔Display
Mono/Proportional
Tech/Neutral
Soft/Sharp
```

Не утверждать, что все они должны попасть в MVP.

Для каждого axis:
- semantic definition;
- valid range;
- linear/nonlinear;
- affected components;
- conflicts;
- compatibility with OpenType variable axis;
- custom axis tag proposal;
- whether it should be global or style-engine-specific.

Создать:
`architecture/axes-model.md`

---

# 12. Structural switches

Определить дискретные варианты, которые нельзя качественно решать простым interpolation slider.

Минимум:

```text
a: single / double
g: single / double
4: open / closed
0: plain / slashed / dotted
Q: tail variants
R: leg variants
1: foot / no foot
G: spur variants
terminal: flat / angled / rounded
```

Для Cyrillic дополнительно исследовать варианты:
- Д
- Л
- Ж
- К
- У
- Ф
- Я
- д
- л
- т
- б

Создать:
`architecture/structural-switches.md`

---

# 13. Latin + Cyrillic architecture

Нужно сразу проектировать обе системы.

Не допускать “сначала Latin, а Cyrillic потом просто дорисуем”.

Создать:

`architecture/script-system.md`

В документе:
- shared metrics;
- shared components;
- script-specific components;
- glyph groups;
- composites;
- accents;
- localized forms;
- shared optical rules;
- Cyrillic-specific risks;
- минимум glyph coverage для MVP;
- расширенный coverage после MVP.

---

# 14. Spacing, kerning и metrics

Исследовать и спроектировать:

- sidebearings;
- automatic spacing rules;
- kerning groups/classes;
- weight-dependent spacing;
- width-dependent spacing;
- mono mode;
- proportional → mono transition;
- metrics interpolation;
- cap/x-height effects;
- punctuation spacing.

Создать:
`architecture/spacing-kerning.md`

---

# 15. Production font pipeline

Codex должен проверить реальный production pipeline.

Предпочтительно исследовать:

```text
Parametric model
→ generated outlines
→ UFO masters
→ Designspace
→ fontTools/fontmake
→ OTF/TTF
→ Variable TTF
→ WOFF2
```

Нужно подтвердить это техническим spike, а не только теорией.

Создать:
`architecture/build-pipeline.md`

---

# 16. Обязательные disposable research spikes

Эти спайки НЕ являются production implementation.
Они нужны для проверки гипотез.

## Spike A — Browser outline rendering
Проверить:
- загрузку open-source/OFL TTF/OTF;
- парсинг через подходящую JS-библиотеку;
- отображение Bézier contours;
- live text preview;
- изменение хотя бы одного тестового параметра/transform.

Результат:
`spikes/browser-outline/`

README должен объяснить:
- что проверено;
- latency;
- limitations;
- пригодность для production.

## Spike B — UFO/Designspace build
Создать два минимальных совместимых master-файла тестового glyph set.

Проверить:
- UFO;
- Designspace;
- static font build;
- variable font build;
- TTF;
- WOFF2, если pipeline поддерживает.

Использовать только свободно лицензируемые/собственные тестовые outlines.

Результат:
`spikes/variable-build/`

## Spike C — Local axis / glyph component experiment
Проверить концепцию:
- global weight;
- local parameter конкретного glyph;
- один structural switch.

Можно реализовать только на 3–5 тестовых glyphs:
`A R O a g 4` — выбрать минимально достаточный набор.

Цель — определить, какую модель данных использовать.

---

# 17. UI/UX будущего Font Lab

Metaflop использовать как starting UX language, но не ограничиваться им.

Подготовить:

`architecture/ui-information-architecture.md`

Предлагаемый каркас:

```text
TOP BAR
Project / Preset / Compare / Export

LEFT PANEL
Global
Glyph
Style
Optical
Spacing
Advanced

CENTER
Glyph Inspector
or
Live Specimen

RIGHT
Chart / Glyph set / Metrics / Layers

BOTTOM
Typewriter / Technical specimen / A-B compare
```

Исследовать сохранение сильной Metaflop-модели:

```text
parameters → glyph/chart → typewriter
```

Но расширить её под:
- presets;
- A/B compare;
- multiple axes;
- Latin/Cyrillic;
- local glyph editing;
- structural switches;
- variable font preview;
- export.

---

# 18. Design tokens для V1

На основе reverse-spec Metaflop создать neutral reusable token set:

`architecture/ui-tokens-proposal.md`

Не копировать branding Metaflop буквально.

Сохранить полезные характеристики:
- dense professional tool UI;
- high information density;
- minimal decoration;
- parameters grouped by semantics;
- live preview always visible;
- numeric precision + slider interaction.

---

# 19. Data model

Создать:
`architecture/data-model.md`

Нужно описать минимум:

```ts
FontProject
StyleEngine
Glyph
GlyphRecipe
Component
Axis
LocalAxis
StructuralSwitch
Metrics
KerningGroup
Preset
Master
Instance
ScriptModule
ExportProfile
```

Для сущностей зафиксировать:
- responsibility;
- key fields;
- references;
- serialization format;
- versioning needs.

Отдельно предложить human-readable project format:
JSON/YAML + generated UFO/Designspace либо другой justified вариант.

---

# 20. PCK integration proposal

Создать:

`architecture/pck-integration.md`

Ответить:
- frontend placement;
- backend/service placement;
- Python build service;
- job execution;
- temp file handling;
- font export storage;
- dependency isolation;
- tests;
- CI;
- caching;
- security при загрузке font files;
- maximum file sizes;
- sandboxing font processing;
- future agent integration.

---

# 21. MVP scope

Создать:

`final/mvp-scope.md`

MVP должен быть реалистичным.

Базовый кандидат:

### Style engine
Geometric/Technical Sans

### Scripts
Latin + Russian Cyrillic

### Global controls
- Weight
- Width
- X-height
- Contrast
- Roundness/Superness
- Aperture
- Terminal
- Mono amount
- Text↔Display
- Tech amount

### Switches
- a single/double
- g single/double
- 4 open/closed
- 0 plain/slashed
- Q tail
- R leg

### UX
- live glyph
- alphabet chart
- live typewriter
- Latin/Cyrillic toggle
- numeric values + sliders
- reset
- randomize small delta
- presets
- A/B compare

### Export
- project source
- OTF/TTF
- Variable TTF if validated
- WOFF2 if validated

Codex должен критически проверить этот scope и предложить уменьшение, если он слишком большой для V1.

---

# 22. Out of scope для первого production этапа

Если исследование не докажет обратное, НЕ включать в MVP:

- Serif;
- Slab;
- Blackletter;
- Script/calligraphic;
- Arabic;
- CJK;
- arbitrary “mix any two fonts”;
- AI-generated outlines;
- full manual Bezier editor уровня Glyphs/Fontra;
- automatic high-quality kerning для всех случаев;
- arbitrary commercial-font morphing.

Зафиксировать roadmap отдельно.

---

# 23. Roadmap

Создать:
`final/roadmap.md`

Минимум:

### Phase 0
Research — текущий этап.

### Phase 1
Technical Sans MVP.

### Phase 2
Variable axes + masters + production export.

### Phase 3
Additional style engines:
- Neo Grotesk
- Humanist Sans
- Mono

### Phase 4
Compatible style interpolation.

### Phase 5
Advanced script support / plugin architecture.

---

# 24. Risk register

Создать:
`final/risk-register.md`

Минимум оценить:

- geometry complexity;
- outline self-intersections;
- interpolation incompatibility;
- variable font constraints;
- kerning complexity;
- Cyrillic quality;
- browser performance;
- font parsing security;
- GPL/copyleft contamination;
- derivative-font licensing;
- scope explosion;
- preserving typographic quality across extreme sliders.

Для каждого:
- probability;
- impact;
- mitigation;
- validation method.

---

# 25. Decision records

Создать ADR-документы минимум по вопросам:

1. Используем ли Metaflop code или только reference.
2. Browser geometry vs server geometry.
3. Core source format: custom JSON vs UFO-first.
4. Build pipeline.
5. Browser preview library.
6. Variable font strategy.
7. Latin/Cyrillic architecture.
8. Mono axis strategy.
9. Local axes strategy.
10. Structural switches representation.

Путь:
`decisions/ADR-XXX-*.md`

---

# 26. Final research report

Создать:

`final/RESEARCH_REPORT.md`

Это главный документ, который пользователь сможет открыть первым.

Структура:

1. Executive summary.
2. Что найдено в Metaflop.
3. Что стоит сохранить из UX.
4. Что нельзя/не стоит переносить.
5. Ограничения Metaflop engine.
6. Лучшие reusable technologies по слоям.
7. License conclusions.
8. Proposed architecture.
9. Recommended MVP.
10. PCK integration.
11. Risks.
12. Open questions.
13. Exact next implementation task.

---

# 27. Machine-readable research summary

Дополнительно создать:

`final/research-summary.json`

Минимум:

```json
{
  "sources": [],
  "repositories": [],
  "licenses": [],
  "uiComponents": [],
  "metaflopParameters": [],
  "candidateEngines": [],
  "recommendedStack": {},
  "axes": [],
  "structuralSwitches": [],
  "mvp": {},
  "risks": [],
  "decisions": []
}
```

Это пригодится дальнейшим Codex/agent-задачам без повторного чтения всех Markdown-файлов.

---

# 28. Требования к источникам

Для каждого внешнего технического утверждения:

- использовать первичный источник по возможности;
- фиксировать URL;
- commit SHA/tag/version;
- дату доступа;
- не опираться на случайные статьи, если есть official docs/source;
- source code считать более сильным доказательством поведения, чем маркетинговую страницу.

---

# 29. Требования к Git hygiene

Research не должен загрязнять production tree.

- Использовать отдельную branch, если workflow PCK это предусматривает.
- Не коммитить огромные cloned repositories внутрь основного repo без необходимости.
- Лучше фиксировать manifest:
  - repo URL;
  - commit SHA;
  - license;
  - local research path.
- Не добавлять node_modules, build artifacts, caches.
- Disposable spikes держать изолированно.

---

# 30. Запреты на этом этапе

Не делать:

- полноценный production frontend;
- редизайн PCK;
- массовое копирование Metaflop CSS/JS;
- перенос GPL-кода без отдельного ADR;
- импорт/морфинг коммерческих шрифтов;
- создание финального AV Tech Sans;
- преждевременное добавление десятков style engines;
- выбор технологии “потому что она знакома”.

---

# 31. Definition of Done

Research Phase считается завершённым только когда:

- Metaflop полностью reverse-specified;
- пользовательские SingleFile + screenshot использованы и сохранены как reference;
- официальный Metaflop source изучен;
- engine Metaflop разобран;
- параметры и ограничения задокументированы;
- альтернативные engines исследованы;
- лицензии проверены по первичным источникам;
- PCK integration audit выполнен;
- browser outline spike работает;
- UFO/Designspace variable build spike работает или документирован конкретный blocker;
- data model определён;
- axes model определён;
- structural switches определены;
- Latin/Cyrillic architecture определена;
- MVP scope зафиксирован;
- risk register готов;
- ADR готовы;
- `RESEARCH_REPORT.md` готов;
- `research-summary.json` готов;
- следующий implementation task сформулирован так, чтобы пользователь мог сразу передать его Codex.

---

# 32. Формат финального ответа Codex пользователю

После выполнения Codex должен вернуть только:

1. Короткий итог исследования — 5–10 пунктов.
2. Главные архитектурные решения.
3. Найденные критические риски.
4. Ссылку/путь на `final/RESEARCH_REPORT.md`.
5. Ссылку/путь на `final/research-summary.json`.
6. Предлагаемый следующий этап.
7. Список файлов, созданных/изменённых в repo.

Не пересказывать весь research в сообщении — подробности должны быть в документах.
