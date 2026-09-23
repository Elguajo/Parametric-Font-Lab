<div align="center">

# Parametric Font Lab

### Build typefaces with sliders — from clean technical sans to expressive display styles.

**Parametric Font Lab** is an experimental web tool for designing fonts as a system of parameters instead of drawing every variation by hand.

![Status](https://img.shields.io/badge/status-research%20%2F%20prototype-6C63FF)
![Focus](https://img.shields.io/badge/v0.1-Technical%20Sans-111111)
![Scripts](https://img.shields.io/badge/scripts-Latin%20%2B%20Cyrillic-0A8F7A)
![UI](https://img.shields.io/badge/interface-slider--based-F2C94C)

</div>

---

## Что это?

Обычный шрифт — это готовый набор букв.

**Parametric Font Lab** рассматривает шрифт как систему, которую можно настраивать:

```text
Weight        Thin  ─────────────●────  Bold
Width         Narrow ─────●────────────  Wide
X-height      Low ─────────────●───────  High
Roundness     Sharp ───────●───────────  Round
Aperture      Closed ───────────●──────  Open
Mono          Proportional ──●─────────  Mono
Optical       Text ─────────────●──────  Display
Tech          Neutral ────────────●────  Engineered
```

Меняешь значение — **весь шрифт перестраивается**, а результат сразу виден в glyph preview, alphabet chart и живом тексте.

> Идея проста: не рисовать вручную десять похожих шрифтов, а описать правила, из которых можно получить целое пространство вариантов.

---

## Для чего этот проект?

Первая версия сосредоточена на **Technical / Geometric Sans** — шрифтах для:

- AV и системной интеграции;
- интерфейсов и dashboards;
- IT / software / hardware брендов;
- технической документации;
- презентаций;
- signage;
- display typography;
- продуктовых названий и wordmarks.

Главный тестовый кейс проекта — разработка семейства **AV Tech Sans**.

---

## Для новичка: как это должно работать

Представь редактор вроде Metaflop, но с более широким design space.

Ты открываешь сайт и видишь:

```text
┌──────────────────┬────────────────────────────┬────────────────────┐
│ PARAMETERS       │ GLYPH / LIVE SPECIMEN      │ CHARACTER SET      │
│                  │                            │                    │
│ Weight      540  │            A               │ A B C D E F ...    │
│ Width       102  │                            │ a b c d e f ...    │
│ X-height     72  │   Network Control          │ А Б В Г Д Е ...    │
│ Aperture     68  │   Сетевые AV решения       │ а б в г д е ...    │
│ Roundness    44  │                            │ 0 1 2 3 4 5 ...    │
│ Tech         63  │   4K60 · H.26x · 10 Gbps  │                    │
│ Mono         18  │                            │                    │
└──────────────────┴────────────────────────────┴────────────────────┘
```

Никакого знания Bézier-кривых для первого эксперимента не требуется.

Двигаешь параметры → сравниваешь варианты → сохраняешь preset → экспортируешь шрифт.

---

## Не просто sliders

Цель проекта — не сделать ещё один фильтр, который растягивает готовые буквы.

Внутри шрифт должен строиться из **типографической грамматики**:

```text
Glyph
 ├─ Stem
 ├─ Bowl
 ├─ Counter
 ├─ Crossbar
 ├─ Diagonal
 ├─ Shoulder
 ├─ Aperture
 ├─ Terminal
 └─ Tail
```

Параметр меняет не картинку целиком, а связанные части конструкции.

Например:

```text
Aperture ↑
    ↓
C / G / e / c / s
становятся более открытыми

Weight ↑
    ↓
stems становятся толще
counters автоматически компенсируются
spacing корректируется

Mono ↑
    ↓
advance widths сближаются
sidebearings перестраиваются
```

---

## Planned controls

| Группа | Параметры |
|---|---|
| **Dimensions** | Width, Cap Height, X-height, Ascender, Descender |
| **Stroke** | Weight, Contrast, Horizontal/Vertical balance |
| **Shape** | Roundness, Superness, Aperture, Taper |
| **Style** | Tech, Soft/Sharp, Text/Display |
| **Spacing** | Tracking, sidebearing logic, Proportional/Mono |
| **Optical** | Overshoot, joins, stroke compensation |
| **Glyph-specific** | R leg, Q tail, G aperture, A crossbar, M vertex |

Некоторые изменения нельзя качественно представить обычным ползунком. Для них будут **structural switches**:

```text
a     single-storey / double-storey
g     single-storey / double-storey
4     open / closed
0     plain / slashed
Q     tail variants
R     leg variants
1     foot / no foot
```

---

## Latin + Cyrillic с самого начала

Первая версия проектируется сразу для двух систем:

```text
Latin
ABCDEFGHIJKLMNOPQRSTUVWXYZ
abcdefghijklmnopqrstuvwxyz

Cyrillic
АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ
абвгдеёжзийклмнопрстуфхцчшщъыьэюя
```

Кириллица здесь не должна быть «дорисована потом».

`Д`, `Ж`, `Л`, `Ф`, `Я`, `б`, `д`, `л`, `т` требуют собственных правил и оптических решений, но должны наследовать общую DNA выбранного стиля.

---

## Style space

Долгосрочная идея — работать не только с Weight и Width, а с **характером шрифта**.

```text
                TECHNICAL

                   ▲
                   │
        Mono       │       Display
                   │
                   │
Humanist ◄─────────┼─────────► Geometric
                   │
                   │
          Text     │       Engineered
                   │
                   ▼

                 SOFT
```

Вместо десятков разрозненных файлов пользователь получает **design space**.

---

## Что значит «смешивать стили»?

Не:

```text
Font A + Font B = магически идеальный Font C
```

а:

```text
Style DNA A
     │
     ├── geometry
     ├── proportions
     ├── aperture
     ├── terminals
     ├── rhythm
     └── glyph variants
                ↓
        compatible design space
                ↑
     ┌── geometry
     ├── proportions
     ├── aperture
     ├── terminals
     ├── rhythm
     └── glyph variants
Style DNA B
```

Совместимые модели можно интерполировать. Несовместимые конструкции переключаются или используют отдельные style engines.

Это позволяет избежать главной проблемы простого vector morphing: технически промежуточная форма может существовать, но типографически быть плохой.

---

# v0.1 — Technical Sans Lab

Первая production-версия намеренно ограничена.

### Цель

Создать качественный параметрический **Technical / Geometric Sans generator**, а не пытаться сразу генерировать любой шрифт в мире.

### Планируемый MVP

```text
✓ Slider-based editor
✓ Numeric values
✓ Live glyph preview
✓ Alphabet chart
✓ Editable typewriter/specimen
✓ Latin
✓ Russian Cyrillic
✓ Presets
✓ A/B comparison
✓ Small-delta randomization
✓ Structural glyph variants
✓ Project save/load

Export targets:
→ OTF
→ TTF
→ Variable TTF
→ WOFF2
```

> Export formats считаются planned до тех пор, пока production pipeline не будет проверен на реальных build-spikes.

---

# Архитектура

Высокоуровневая модель:

```text
┌───────────────────────────────────────────────┐
│                 WEB INTERFACE                 │
│ sliders · presets · specimen · compare · UX  │
└───────────────────────┬───────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────┐
│               PARAMETRIC MODEL                │
│ axes · switches · constraints · style engine │
└───────────────────────┬───────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────┐
│                 GLYPH GRAMMAR                 │
│ stem · bowl · arch · terminal · tail · joins │
└───────────────────────┬───────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────┐
│            METRICS + OPTICAL SYSTEM           │
│ spacing · kerning · overshoot · compensation │
└───────────────────────┬───────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────┐
│               FONT SOURCE LAYER               │
│           UFO masters + Designspace           │
└───────────────────────┬───────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────┐
│                  BUILD PIPELINE               │
│         fontTools / fontmake / WOFF2          │
└───────────────────────────────────────────────┘
```

Архитектура пока находится в исследовании. Конкретные библиотеки становятся частью проекта только после технической проверки и license audit.

---

## Почему не просто форк Metaflop?

Metaflop — один из главных UX-референсов проекта: его модель

```text
parameters → glyph/chart → typewriter
```

очень хорошо подходит для параметрического font tool.

Но Parametric Font Lab исследует более широкий подход:

- несколько style engines;
- global и local axes;
- structural switches;
- Latin + Cyrillic;
- reusable glyph components;
- richer designspace;
- variable-font pipeline;
- A/B comparison;
- presets;
- production-oriented export.

Поэтому Metaflop используется прежде всего как **reference и объект reverse-spec**, а не автоматически как кодовая база.

---

## Технические направления исследования

Проект изучает и проверяет идеи из экосистемы:

**Metaflop** — parametric UX и Metafont-подход  
**Fontra** — designspace, variable editing, components  
**UFO / Designspace** — переносимый font-source слой  
**fontTools / fontmake** — OpenType и variable-font build pipeline  
**opentype.js** — browser font parsing/rendering  
**HarfBuzz** — shaping и glyph positioning  
**Glyphr Studio / FontForge** — editor workflows  
**Recursive** — пример продуманной многомерной variable-font системы

Это не означает, что все эти проекты станут зависимостями.

---

# Текущий статус

> **Research / Architecture**

Репозиторий сейчас находится на раннем этапе: формируется PCK-based project workflow и готовится исследование архитектуры Parametric Font Lab. В production-приложении пока нельзя генерировать или экспортировать шрифты.

Текущий приоритет:

```text
Metaflop reverse-spec
        ↓
engine research
        ↓
license audit
        ↓
technical spikes
        ↓
architecture decision
        ↓
Technical Sans MVP
```

---

# Roadmap

| Phase | Результат |
|---|---|
| **0 — Research** | Reverse-spec, engine comparison, licenses, spikes, architecture |
| **1 — Technical Sans MVP** | Interactive Latin + Cyrillic parametric generator |
| **2 — Production Fonts** | Masters, Designspace, variable/static exports |
| **3 — More Style Engines** | Neo Grotesk, Humanist Sans, Mono |
| **4 — Style Interpolation** | Controlled mixing between compatible design systems |
| **5 — Extensibility** | Additional scripts, plugins, custom engines |

---

# Для разработчиков и AI-агентов

Репозиторий использует **Progressive Context Kit (PCK)** как слой проектного контекста и агентного workflow.

Перед работой:

```text
Read AGENTS.md first.
```

Не нужно заранее загружать весь проектный контекст. Используйте маршрутизацию и правила репозитория, чтобы читать только необходимые для текущей задачи материалы.

Технические решения, которые влияют на архитектуру, совместимость или лицензирование, должны фиксироваться как project decisions / ADR согласно repository workflow.

---

# Principles

**Typography first.**  
Если математически корректная интерполяция выглядит типографически плохо — это плохой результат.

**Parameters should have meaning.**  
Slider должен описывать понятное свойство дизайна, а не случайную трансформацию.

**Beginner-friendly outside, rigorous inside.**  
Пользователь может просто двигать Weight, но engine обязан корректно учитывать counters, spacing и optical compensation.

**Scripts are first-class.**  
Latin и Cyrillic проектируются как части одной системы.

**Open formats where practical.**  
Font source и export pipeline должны по возможности строиться вокруг переносимых industry formats.

**No license-by-assumption.**  
Reference-font, исходный код, UI assets и generated fonts могут иметь разные лицензии. Их права проверяются отдельно.

---

# Inspiration ≠ tracing

Parametric Font Lab может изучать существующие гарнитуры, design systems и типографические подходы как reference.

Цель проекта — строить **собственные parametric glyph recipes**, а не автоматически превращать коммерческие font files в распространяемые производные шрифты.

---

# Repository

## Phase 1b: run locally

The implemented workbench generates original Basic Latin, Russian Cyrillic including `Ё/ё`,
NBSP and acute/dieresis marks from bounded recipes. It provides a browser SVG preview,
script-aware metrics/kerning, controlled Text/Display presets and static export. From a
clean macOS/Linux checkout:

```sh
npm run setup
npm test
npm run export
python3 -m http.server 8765 --bind 127.0.0.1 --directory .
```

Open `http://127.0.0.1:8765/web/` for the browser workbench. Adjust the sliders or numeric
fields, download the resulting project JSON, then compile exactly those settings with:

```sh
npm run export -- --project /path/to/pfl-phase-1b-project.json
```

`requirements.lock` and `package-lock.json` pin the compiler and test dependency graphs.
Each export writes derived UFO, Designspace, TTF, OTF, WOFF2 and a manifest under
`build/<source-hash>/`. Exports leave unrelated files in `build/` untouched.

`fontlab/project.json` selects only the bounded Phase 1b repertoire and controls; the original
contours are deterministically generated locally by `fontlab/recipes.py`. No external font
outlines are imported. See `THIRD_PARTY_NOTICES.md` for compiler/test dependencies.

https://github.com/Elguajo/Parametric-Font-Lab

---

## License

Лицензия самого Parametric Font Lab пока не зафиксирована в репозитории.

До появления явного `LICENSE` не следует предполагать право на копирование, модификацию или распространение исходного кода проекта.

Лицензии сторонних research/reference-проектов рассматриваются отдельно.

---

<div align="center">

### Parametric Font Lab

**Type is not a file. It is a design space.**

`parameters → rules → glyphs → fonts`

</div>
