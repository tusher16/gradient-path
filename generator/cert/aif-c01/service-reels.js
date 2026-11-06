// Turns every entry in services.js into a reel, in the shape the shared reels player reads:
// topics (id, title, hook), motion (h, steps, svg), segs (what is read aloud). Nothing here is
// new content: job, clue, look-alike and memory line all come from the cheat sheet, so the card
// and its reel cannot disagree.
//
// A scene is three beats on one stage, plus the memory line:
//   step 0  the job: input goes through the machine, output draws itself
//   step 1  the clue: the words a question uses pop in as chips
//   step 2  the look-alike, when there is one: this service, not that one, which gets struck out
//   hook    the place in the town and the machine light up as the memory line lands
const esc = (t) => String(t).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const short = (n) => n.replace(/^(?:Amazon|AWS) /, '').replace(/ \(.*\)$/, '');
const spoken = (n) => n.replace(/ \(.*\)$/, '');
// inside a place the family name is already understood
const inPlace = (n) => (/^(SageMaker|Bedrock|AgentCore|Glue) /.test(n) ? n.replace(/^\w+ /, '') : short(n));
const cap = (t) => t[0].toUpperCase() + t.slice(1);
const WHERE = {
  person: 'part of the person', rental: 'in the rental shop', workshop: 'in the workshop', office: 'in the office',
  warehouse: 'in the warehouse', vault: 'in the vault', audit: 'in the audit office', neighbours: 'one of the neighbours',
};
// the head on the cheat sheet, with the one sense each service is
const HEAD = 'M145 128c0-52 33-88 75-88s75 36 75 88c0 62-33 110-75 110s-75-48-75-110Z';
const EYES = 'M176 96c6-6 14-6 20 0M244 96c6-6 14-6 20 0', MOUTH = 'M196 182c14 12 34 12 48 0';
const SENSE = {
  rekognition: EYES, transcribe: 'M145 112c-12-4-16 8-14 20s8 22 16 18M295 112c12-4 16 8 14 20s-8 22-16 18',
  polly: MOUTH, lex: MOUTH, translate: MOUTH, comprehend: 'M176 58c10-14 28-14 38-4 10-10 32-8 40 6',
  textract: EYES + 'M166 96a20 20 0 1 0 40 0 20 20 0 1 0-40 0M234 96a20 20 0 1 0 40 0 20 20 0 1 0-40 0M206 96h28',
  personalize: 'M220 112l-8 30h14',
};
// a small repeat on the output picture that fits what the picture is
const SIG = {
  bell: 'ring', gear: 'spin', search: 'scan', key: 'turn', shield: 'pop', lock: 'pop', check: 'pop', star: 'pop', dots: 'pop', graph: 'pop',
  wave: 'flow', speaker: 'flow', stream: 'flow', road: 'flow', pipe: 'flow', chart: 'rise', lines: 'rise', doc: 'rise', log: 'rise', table: 'rise',
};

const W = 440, CHIP_H = 28, ROW = 34, CHAR = 9;   // IBM Plex Mono is 0.6em wide, so 15px text is 9px a character

module.exports = function serviceReels({ ZONES, GLYPHS }) {
  const errors = [];
  const allServices = ZONES.flatMap((z) => z.services);
  const byId = new Map(allServices.map((x) => [x.id, x]));
  const measured = (m) => GLYPHS[m].replace(/<(path|rect|circle|ellipse) /g, '<$1 pathLength="1" ');
  const outOf = (x) => x.g[x.g.length - 1];
  // a picture that draws itself; the signature repeat sits inside the draw so they cannot fight
  const drawn = (g, x, y, size, cls, t, o, sig) => `<g transform="translate(${x} ${y}) scale(${(size / 24).toFixed(3)})"><g class="gg ${cls} a d" style="--t:${t};--o:${o}s;--dur:.7s">` +
    `<g${sig ? ` class="sig ${SIG[g] || 'bob'}"` : ''}>${measured(g)}</g></g></g>`;
  const token = (g, x, y, cls, o, dx) => `<g transform="translate(${x} ${y}) scale(.92)"><g class="gg ${cls} a tk" style="--t:0;--o:${o}s;--dx:${dx}px">${GLYPHS[g]}</g></g>`;
  const strip = (zi) => ZONES.map((z, i) => `<use href="#g-${z.g}" x="${17.5 + i * 55}" y="2" width="20" height="20" class="gl ${i === zi ? 'here' : 'off'}"/>`).join('');
  // chips wrap by measured width; a chip wider than the stage is a content error, not a clip
  const chips = (words, y0, t, stagger, charW, h, row, size, label) => {
    let x = 0, y = y0, out = '';
    words.forEach((w, i) => {
      const cw = Math.ceil(w.length * charW) + 20;
      if (cw > W) errors.push(`${label}: chip "${w}" is wider than the stage`);
      if (x && x + cw > W) { x = 0; y += row; }
      out += `<g class="a g" style="--t:${t};--o:${(i * stagger).toFixed(2)}s"><rect class="bx" x="${x}" y="${y}" width="${cw}" height="${h}" rx="${h / 2}"/>` +
        `<text class="chip mid" style="font-size:${size}px" x="${x + cw / 2}" y="${y + h / 2 + size * 0.34}">${esc(w)}</text></g>`;
      x += cw + 6;
    });
    return { svg: out, bottom: y + h };
  };

  const topics = [], motion = {}, segs = {};
  let n = 0;
  ZONES.forEach((z, zi) => {
    // the place's own reel: where it sits in the town, then who lives there
    const zid = 'z-' + z.id;
    const grid = ZONES.map((p, i) => {
      const cx = 55 + (i % 4) * 110, y = 2 + Math.floor(i / 4) * 62, here = i === zi;
      return `<g class="a g" style="--t:0;--o:${(i * 0.09).toFixed(2)}s"><use href="#g-${p.g}" x="${cx - 16}" y="${y}" width="32" height="32" class="gl ${here ? 'here big' : 'off'}"/>` +
        `<text class="${here ? 'lb s' : ''} mid" x="${cx}" y="${y + 50}">${esc(cap(p.place.replace(/^The /, '')))}</text></g>`;
    }).join('');
    const who = chips(z.services.map((x) => inPlace(x.name)), 138, 0, 0.14, 7.8, 26, 31, 13, zid);
    topics.push({ id: zid, kind: 'place', z: zi, title: z.place, hook: `${z.services.length} services live here.`, sr: `${z.place}. Services here: ${z.services.map((x) => short(x.name)).join(', ')}.` });
    motion[zid] = { h: who.bottom + 2, steps: [z.say], svg: grid + who.svg };
    segs[zid] = [`${z.place}. ${z.say}`, `${z.services.length} services live here.`];

    z.services.forEach((x) => {
      n++;
      const flow = x.g.length > 1, H = x.not ? 3 : 2, hx = 27.5 + zi * 55;
      let svg = strip(zi) + `<circle class="ln s a g" style="--t:${H}" cx="${hx}" cy="12" r="15"/>`;
      if (flow) {
        const [gi, go] = x.g;
        svg += drawn(gi, 30, 49, 60, 'in', 0, 0) + `<text class="lbx mid a" style="--t:0" x="60" y="133">goes in</text>` +
          `<path class="ln a d" pathLength="1" style="--t:0;--o:.3s" d="M96 79H165"/><path class="ln m a d" pathLength="1" style="--t:0;--o:1.5s" d="M275 79H344"/>` +
          `<rect class="bx m a g" style="--t:0;--o:.2s" x="165" y="34" width="110" height="90" rx="14"/>`;
        if (z.id === 'person') {
          svg += `<g transform="translate(220 79) scale(.37) translate(-220 -139)"><path class="head a" style="--t:0;--o:.3s" d="${HEAD}"/><path class="sense a d" pathLength="1" style="--t:0;--o:1.15s" d="${SENSE[x.id]}"/></g>`;
        } else {
          svg += `<g transform="translate(198 57) scale(1.83)"><g class="gg mach a" style="--t:0;--o:.3s">${GLYPHS[z.g]}</g></g>`;
        }
        svg += token(gi, 96, 68, 'in', 0.5, 47) + `<rect class="pu a" style="--t:0;--o:1.15s" x="165" y="34" width="110" height="90" rx="14"/>` +
          token(go, 275, 68, 'out', 1.45, 47) + drawn(go, 350, 49, 60, 'out', 0, 1.95, true) + `<text class="lbx mid a" style="--t:0;--o:1.95s" x="380" y="133">comes out</text>` +
          `<rect class="hl a g" style="--t:${H}" x="165" y="34" width="110" height="90" rx="14"/>`;
      } else {
        svg += `<circle class="bx m a g" style="--t:0" cx="220" cy="79" r="50"/>` + drawn(x.g[0], 184, 43, 72, 'out', 0, 0.25, true) +
          `<circle class="pu a" style="--t:0;--o:1s" cx="220" cy="79" r="50"/><circle class="hl a g" style="--t:${H}" cx="220" cy="79" r="50"/>`;
      }
      const clue = chips(x.clue.split(/,\s*/), 178, 1, 0.5, CHAR, CHIP_H, ROW, 15, x.id);
      svg += `<text class="lbx a" style="--t:1" x="0" y="168">question says</text>` + clue.svg;
      let bottom = clue.bottom;
      const steps = [x.job + '.', 'Listen for these words in the question.'];
      const said = [`${spoken(x.name)}, ${WHERE[z.id]}. ${x.job}.`, `The question says: ${x.clue}.`];
      if (x.not) {
        const o = byId.get(x.not[0]), y = bottom + 36, mine = short(x.name), theirs = short(o.name);
        for (const nm of [mine, theirs]) if (nm.length > 25) errors.push(`${x.id}: "${nm}" is too long for the look-alike column`);
        svg += `<text class="lbx a" style="--t:2" x="0" y="${y - 12}">not the same as</text>` +
          drawn(outOf(x), 85, y, 36, 'out', 2, 0) + `<text class="lb m mid a" style="--t:2" x="103" y="${y + 55}">${esc(mine)}</text>` +
          `<text class="hd mid a" style="--t:2;--o:.3s" x="220" y="${y + 26}">≠</text>` +
          drawn(outOf(o), 319, y, 36, 'in', 2, 0.4) + `<text class="lb mid a" style="--t:2;--o:.4s" x="337" y="${y + 55}">${esc(theirs)}</text>` +
          `<path class="ln s strike a d" pathLength="1" style="--t:2;--o:1.1s" d="M311 ${y + 40}L363 ${y - 4}"/>`;
        bottom = y + 60;
        steps.push(`Not ${theirs}: ${x.not[1]}`);
        said.push(`Not ${spoken(o.name)}. ${x.not[1]}`);
      }
      said.push('Remember. ' + x.hook);
      topics.push({ id: x.id, kind: 'service', z: zi, n, title: x.name, hook: x.hook,
        sr: `${x.name}. ${x.job}. Question says: ${x.clue}.` });
      motion[x.id] = { h: bottom + 2, steps, svg };
      segs[x.id] = said;
    });
  });
  return { topics, motion, segs, errors };
};
