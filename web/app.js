const KAPPA = 0.5522847498307936;
let project;
let glyphs = [];
const controls = { weight: 88, counter: 1, construction: 'double' };
let selected = 'H';
const svg = (tag, attributes = {}) => {
  const element = document.createElementNS('http://www.w3.org/2000/svg', tag);
  for (const [name, value] of Object.entries(attributes)) element.setAttribute(name, value);
  return element;
};
const fmt = value => Number(value.toFixed(4)).toString();
const path = contour => contour.map(command => command[0] === 'Z' ? 'Z' : `${command[0]} ${command.slice(1).map(fmt).join(' ')}`).join(' ');
const rectangle = (x0, y0, x1, y1, reverse = false) => {
  const points = [[x0, y0], [x1, y0], [x1, y1], [x0, y1]];
  if (reverse) points.reverse();
  return [['M', ...points[0]], ...points.slice(1).map(point => ['L', ...point]), ['Z']];
};
const oval = (cx, cy, rx, ry, reverse = false) => {
  const k = KAPPA;
  if (!reverse) return [
    ['M', cx + rx, cy],
    ['C', cx + rx, cy + k * ry, cx + k * rx, cy + ry, cx, cy + ry],
    ['C', cx - k * rx, cy + ry, cx - rx, cy + k * ry, cx - rx, cy],
    ['C', cx - rx, cy - k * ry, cx - k * rx, cy - ry, cx, cy - ry],
    ['C', cx + k * rx, cy - ry, cx + rx, cy - k * ry, cx + rx, cy], ['Z'],
  ];
  return [
    ['M', cx + rx, cy],
    ['C', cx + rx, cy - k * ry, cx + k * rx, cy - ry, cx, cy - ry],
    ['C', cx - k * rx, cy - ry, cx - rx, cy - k * ry, cx - rx, cy],
    ['C', cx - rx, cy + k * ry, cx - k * rx, cy + ry, cx, cy + ry],
    ['C', cx + k * rx, cy + ry, cx + rx, cy + k * ry, cx + rx, cy], ['Z'],
  ];
};
const ring = (cx, cy, rx, ry, inset) => [oval(cx, cy, rx, ry), oval(cx, cy, rx - inset, ry - inset, true)];
const singleA = weight => [...ring(255, 245, 185, 245, weight), rectangle(440 - weight, 0, 440, 510), rectangle(310, 0, 440, weight)];
const doubleA = weight => [...ring(250, 185, 175, 185, weight), ...ring(250, 405, 185, 185, weight), rectangle(425 - weight, 0, 425, 520), rectangle(265, 288, 425 - weight / 2, 288 + weight)];
const cyrillicA = weight => [...ring(260, 190, 180, 190, weight), ...ring(260, 400, 180, 180, weight), rectangle(430 - weight, 0, 430, 510), rectangle(270, 285, 430 - weight / 2, 285 + weight)];

function evaluateGlyph(glyph, state = controls) {
  const weight = Number(state.weight);
  let contours; let advance;
  if (glyph.recipe === 'cap-h') { contours = [rectangle(70, 0, 70 + weight, 700), rectangle(610 - weight, 0, 610, 700), rectangle(70 + weight, 318 - weight / 2, 610 - weight, 318 + weight / 2)]; advance = 680; }
  if (glyph.recipe === 'cap-o') { const inset = weight + 24 * (1 - (glyph.name === 'O' ? Number(state.counter) : 1)); contours = ring(340, 350, 270, 360, inset); advance = 680; }
  if (glyph.recipe === 'zero') { contours = ring(340, 350, 235, 350, weight + 8); advance = 680; }
  if (glyph.recipe === 'small-o') { contours = ring(270, 250, 205, 250, weight); advance = 540; }
  if (glyph.recipe === 'latin-a') { contours = state.construction === 'single' ? singleA(weight) : doubleA(weight); advance = 540; }
  if (glyph.recipe === 'cyrillic-a') { contours = cyrillicA(weight); advance = 540; }
  return { ...glyph, advance, contours };
}

function signature(state = controls) {
  return glyphs.map(glyph => {
    const result = evaluateGlyph(glyph, state);
    const points = result.contours.flat().filter(command => ['M', 'L', 'C'].includes(command[0])).map(command => command.slice(-2));
    return { name: result.name, advance: result.advance, contours: result.contours.length, bounds: [Math.min(...points.map(point => point[0])), Math.min(...points.map(point => point[1])), Math.max(...points.map(point => point[0])), Math.max(...points.map(point => point[1]))].map(value => Number(value.toFixed(4))), outline: result.contours.map(path).join('|') };
  });
}

function glyphSvg(result, className = 'glyph') {
  const svgElement = svg('svg', { class: className, viewBox: `0 0 ${result.advance} 800`, 'aria-hidden': 'true', 'data-glyph-id': result.id });
  const group = svg('g', { transform: 'translate(0 720) scale(1 -1)' });
  group.append(svg('path', { d: result.contours.map(path).join(' '), 'fill-rule': 'nonzero' }));
  svgElement.append(group);
  return svgElement;
}

function render() {
  try {
    const selectedGlyph = evaluateGlyph(glyphs.find(glyph => glyph.name === selected));
    document.querySelector('#weight').value = controls.weight;
    document.querySelector('#weight-number').value = controls.weight;
    document.querySelector('#counter').value = controls.counter;
    document.querySelector('#counter-number').value = controls.counter;
    document.querySelector('#construction').value = controls.construction;
    document.querySelector('#selected-name').textContent = selectedGlyph.char;
    const outline = document.querySelector('#outline'); outline.replaceChildren(glyphSvg(selectedGlyph, 'outline-glyph').querySelector('g'));
    const chart = document.querySelector('#chart'); chart.replaceChildren();
    for (const glyph of glyphs) {
      const button = document.createElement('button'); button.type = 'button'; button.className = 'glyph-button'; button.dataset.glyph = glyph.name; button.setAttribute('aria-pressed', String(glyph.name === selected)); button.setAttribute('aria-label', `Select ${glyph.char}`);
      button.append(glyphSvg(evaluateGlyph(glyph))); const label = document.createElement('span'); label.textContent = glyph.char; button.append(label);
      button.addEventListener('click', () => { selected = glyph.name; render(); }); chart.append(button);
    }
    const specimen = document.querySelector('#specimen-preview'); specimen.replaceChildren();
    const unsupported = new Set();
    for (const character of document.querySelector('#specimen').value) {
      const glyph = glyphs.find(item => item.char === character);
      if (glyph) specimen.append(glyphSvg(evaluateGlyph(glyph)));
      else if (/\s/.test(character)) { const space = document.createElement('span'); space.className = 'glyph space'; specimen.append(space); }
      else unsupported.add(character);
    }
    document.querySelector('#preview-error').textContent = unsupported.size ? `Outside the Phase 1a repertoire: ${[...unsupported].join(' ')}` : '';
    document.querySelector('#download-project').disabled = false;
  } catch (error) { document.querySelector('#preview-error').textContent = error.message; }
}

for (const key of ['weight', 'counter']) {
  document.querySelector(`#${key}`).addEventListener('input', event => { controls[key] = Number(event.target.value); render(); });
  const numberInput = document.querySelector(`#${key}-number`);
  numberInput.addEventListener('input', () => {
    if (numberInput.validity.valid && numberInput.value !== '' && Number.isFinite(numberInput.valueAsNumber)) {
      controls[key] = numberInput.valueAsNumber;
      render();
    } else {
      document.querySelector('#preview-error').textContent = `${key} is outside the allowed range`;
      document.querySelector('#download-project').disabled = true;
    }
  });
  numberInput.addEventListener('blur', () => { if (!numberInput.validity.valid) render(); });
}
document.querySelector('#construction').addEventListener('input', event => { controls.construction = event.target.value; render(); });
document.querySelector('#specimen').addEventListener('input', render);

function currentProject() {
  return {
    ...project,
    axes: { ...project.axes, weight: controls.weight },
    localOverrides: { ...project.localOverrides, O: { ...project.localOverrides.O, counter: controls.counter } },
    switches: { ...project.switches, aConstruction: controls.construction },
  };
}

document.querySelector('#download-project').addEventListener('click', () => {
  const content = JSON.stringify(currentProject(), null, 2) + '\n';
  const url = URL.createObjectURL(new Blob([content], { type: 'application/json' }));
  const link = document.createElement('a');
  link.href = url;
  link.download = 'pfl-phase-1a-project.json';
  link.click();
  setTimeout(() => URL.revokeObjectURL(url), 0);
});

async function initialize() {
  const response = await fetch(new URL('../fontlab/project.json', import.meta.url));
  if (!response.ok) throw new Error(`Cannot load project JSON (${response.status})`);
  project = await response.json();
  if (project.schemaVersion !== 1 || !Array.isArray(project.glyphs) || project.glyphs.length !== 8) {
    throw new Error('Unsupported Phase 1a project source');
  }
  glyphs = project.glyphs.map(glyph => ({ ...glyph, char: String.fromCodePoint(glyph.unicode) }));
  controls.weight = project.axes.weight;
  controls.counter = project.localOverrides.O.counter;
  controls.construction = project.switches.aConstruction;
  window.pfl = { evaluateGlyph, glyphs, signature, currentProject, get controls() { return { ...controls }; } };
  render();
}

initialize().catch(error => { document.querySelector('#preview-error').textContent = error.message; });
