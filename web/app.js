const source = new URL('../fontlab/project.json', import.meta.url);
const fontUrl = new URL('./fonts/PFLSansVariable.woff2', import.meta.url);
const controlText = 'H O A V C S n o b d e | Н О С Д Л Ж К Я и н о п б д л е ь\nbone done | нос сон дно поле дело | AV VA AO АО ДО ДЛ b ь';
const repertoire = [...Array.from({ length: 95 }, (_, index) => String.fromCodePoint(32 + index)), '\u00a0', ...'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ', ...'абвгдеёжзийклмнопрстуфхцчшщъыьэюя', '\u0301', '\u0308'];
const presets = { text: { weight: 400, opticalSize: 14 }, display: { weight: 500, opticalSize: 32 } };
const state = { project: null, loaded: false, selected: 'Д' };
const $ = selector => document.querySelector(selector);
function applyAxes() {
  const { weight, opticalSize } = state.project.axes;
  document.documentElement.style.setProperty('--weight', weight);
  document.documentElement.style.setProperty('--optical-size', opticalSize);
  for (const key of ['weight', 'opticalSize']) {
    $(`#${key}`).value = state.project.axes[key];
    $(`#${key}-value`).textContent = state.project.axes[key];
  }
  $('#preset').value = state.project.activePreset;
}
function choose(char) {
  state.selected = char;
  $('#selected-glyph').textContent = char;
  $('#hero-glyph').textContent = char;
  $('#selected-label').textContent = `${char === ' ' ? 'space' : char} · U+${char.codePointAt(0).toString(16).toUpperCase().padStart(4, '0')}`;
  for (const button of document.querySelectorAll('.glyph-button')) button.setAttribute('aria-pressed', String(button.dataset.character === char));
}
function renderProof() {
  const text = $('#specimen').value || controlText;
  $('#proof-list').replaceChildren(...[10, 14, 24, 72].map(size => {
    const row = document.createElement('div'); row.className = 'proof-row';
    const label = document.createElement('span'); label.className = 'size-label'; label.textContent = `${size} px`;
    const specimen = document.createElement('div'); specimen.className = 'proof-text'; specimen.style.fontSize = `${size}px`; specimen.textContent = text;
    row.append(label, specimen); return row;
  }));
}
function renderChart() {
  const chart = $('#chart'); chart.replaceChildren();
  for (const char of repertoire) {
    if (char === ' ' || char === '\u00a0' || char === '\u0301' || char === '\u0308') continue;
    const button = document.createElement('button'); button.type = 'button'; button.className = 'glyph-button'; button.dataset.character = char;
    button.setAttribute('aria-label', `Show glyph ${char}`); button.setAttribute('aria-pressed', String(char === state.selected));
    const shape = document.createElement('span'); shape.className = 'glyph-shape'; shape.textContent = char;
    const code = document.createElement('small'); code.textContent = char.codePointAt(0).toString(16).toUpperCase().padStart(4, '0');
    button.append(shape, code); button.addEventListener('click', () => choose(char)); chart.append(button);
  }
  $('#coverage').textContent = `${repertoire.length} mapped · ${chart.children.length} visible`;
}
async function init() {
  const response = await fetch(source);
  if (!response.ok) throw new Error(`Project load failed: HTTP ${response.status}`);
  state.project = await response.json();
  if (state.project.schemaVersion !== 3 || state.project.engine.id !== 'inter-derived') throw new Error('This workbench requires a version 3 Inter-derived project.');
  const face = new FontFace('PFLSansPreview', `url("${fontUrl.href}") format("woff2")`, { weight: '100 900' });
  await face.load(); document.fonts.add(face);
  await document.fonts.load('400 14px PFLSansPreview', 'ДЛbь');
  if (!document.fonts.check('400 14px PFLSansPreview', 'ДЛbь')) throw new Error('PFL Sans did not become available to the browser.');
  state.loaded = true; document.body.dataset.fontState = 'ready';
  $('#font-status').textContent = 'PFL Sans loaded · actual font preview';
  applyAxes(); renderChart(); choose('Д'); renderProof();
  $('#preset').addEventListener('change', event => { const value = event.target.value; state.project.activePreset = value; if (presets[value]) state.project.axes = { ...presets[value] }; applyAxes(); });
  for (const key of ['weight', 'opticalSize']) $('#'+key).addEventListener('input', event => { state.project.axes[key] = Number(event.target.value); state.project.activePreset = 'custom'; applyAxes(); });
  $('#specimen').addEventListener('input', renderProof);
  $('#download-project').addEventListener('click', () => { const blob = new Blob([JSON.stringify(state.project, null, 2) + '\n'], { type: 'application/json' }); const url = URL.createObjectURL(blob); const a = document.createElement('a'); a.href = url; a.download = 'pfl-sans-v3-project.json'; a.click(); setTimeout(() => URL.revokeObjectURL(url), 0); });
  window.pfl = { get project() { return structuredClone(state.project); }, get loaded() { return state.loaded; }, repertoire };
}
init().catch(error => { document.body.dataset.fontState = 'error'; $('#font-status').textContent = `Font unavailable: ${error.message}`; });
