#!/usr/bin/env node
// Validate the AIF-C01 sources, then inline them into ../../../aws-ai-practitioner.html
// and the reels feed ../../../aws-ai-practitioner-reels.html.
// Run from anywhere:  node generator/cert/aif-c01/build.js
// Exit 1 on any validation error; nothing is written in that case.
const fs = require('fs');
const crypto = require('crypto');
const path = require('path');

const HERE = __dirname;
const OUT = path.join(HERE, '..', '..', '..', 'aws-ai-practitioner.html');
const REELS_OUT = path.join(HERE, '..', '..', '..', 'aws-ai-practitioner-reels.html');
const TOPICS = require('./topics.js');
const QUESTIONS = require('./questions.js');
const { DAYS, CONFUSABLES, PROMPTS, DOMAINS } = require('./extras.js');
const MOTION = require('./motion.js');
const { ZONES, GLYPHS, COVERED_ELSEWHERE } = require('./services.js');
const SHEET_OUT = path.join(HERE, '..', '..', '..', 'aws-ai-practitioner-services.html');
const SVC_REELS_OUT = path.join(HERE, '..', '..', '..', 'aws-ai-practitioner-services-reels.html');
const serviceReels = require('./service-reels.js');

// Mock blueprint: 13/16/18/9/9 = 65, the 20/24/28/14/14 weights of 65.
const MOCK_SPLIT = { 1: 13, 2: 16, 3: 18, 4: 9, 5: 9 };

const errors = [];
const err = (m) => errors.push(m);

const topicById = new Map();
for (const t of TOPICS) {
  if (topicById.has(t.id)) err(`duplicate topic id ${t.id}`);
  if (!(t.d >= 1 && t.d <= 5)) err(`topic ${t.id}: bad domain ${t.d}`);
  for (const k of ['title', 'hook', 'trap']) if (!t[k]) err(`topic ${t.id}: missing ${k}`);
  if (!t.simple?.length || !t.detail?.length) err(`topic ${t.id}: needs simple and detail`);
  if (t.simple?.some((p) => /<|\\\(|\$/.test(p))) err(`topic ${t.id}: simple layer must be plain text`);
  topicById.set(t.id, t);
}

const qids = new Set();
const counts = { P: {}, A: {}, B: {} };
const stems = new Set();
for (const q of QUESTIONS) {
  if (qids.has(q.id)) err(`duplicate question id ${q.id}`);
  qids.add(q.id);
  const t = topicById.get(q.t);
  if (!t) { err(`${q.id}: unknown topic ${q.t}`); continue; }
  q.d = t.d;
  if (!counts[q.set]) { err(`${q.id}: bad set ${q.set}`); continue; }
  counts[q.set][q.d] = (counts[q.set][q.d] || 0) + 1;
  const opts = [...q.right, ...q.wrong];
  if (new Set(opts).size !== opts.length) err(`${q.id}: duplicate options`);
  const multi = q.right.length > 1;
  if (multi && !/Select (TWO|THREE)/.test(q.q)) err(`${q.id}: multi-response stem must say Select TWO/THREE`);
  if (!multi && /Select (TWO|THREE)/.test(q.q)) err(`${q.id}: stem says Select but has one answer`);
  if (multi && opts.length < 5) err(`${q.id}: multiple response needs 5+ options`);
  if (!multi && opts.length !== 4) err(`${q.id}: multiple choice needs exactly 4 options`);
  if (/all of the above|none of the above/i.test(opts.join('|'))) err(`${q.id}: no all/none of the above`);
  if (!q.x || q.x.length < 40) err(`${q.id}: explanation too thin`);
  if (stems.has(q.q)) err(`${q.id}: duplicate stem`);
  stems.add(q.q);
}
for (const set of ['A', 'B']) {
  for (const [d, n] of Object.entries(MOCK_SPLIT)) {
    if ((counts[set][d] || 0) !== n) err(`Mock ${set}: domain ${d} has ${counts[set][d] || 0}, needs ${n}`);
  }
}
for (const t of TOPICS) {
  if (!QUESTIONS.some((q) => q.set === 'P' && q.t === t.id)) err(`topic ${t.id}: no practice question`);
}
const allDayTopics = new Set();
for (const d of DAYS) for (const id of d.topics) {
  if (!topicById.has(id)) err(`day ${d.n}: unknown topic ${id}`);
  if (d.kind === 'learn') allDayTopics.add(id);
}
for (const t of TOPICS) if (!allDayTopics.has(t.id)) err(`topic ${t.id} is never taught in week 1`);
if (DAYS.length !== 14) err(`plan has ${DAYS.length} days, needs 14`);
for (const t of TOPICS) if (!MOTION[t.id]) err(`topic ${t.id}: no motion diagram`);
for (const [id, m] of Object.entries(MOTION)) {
  if (!topicById.has(id)) err(`motion ${id}: unknown topic`);
  if (!(m.h > 0) || !m.steps?.length || !m.svg) err(`motion ${id}: needs h, steps and svg`);
  if (/<script|on\w+=|href=/i.test(m.svg)) err(`motion ${id}: svg must be plain geometry`);
  const ts = [...m.svg.matchAll(/--t:(\d+)/g)].map((x) => +x[1]);
  if (Math.max(...ts) >= m.steps.length) err(`motion ${id}: an element appears at step ${Math.max(...ts)} but there are ${m.steps.length} captions`);
  for (let i = 0; i < m.steps.length; i++) if (!ts.includes(i)) err(`motion ${id}: caption ${i + 1} has nothing appearing with it`);
}

// Cheat sheet: every id resolves, every glyph exists, the job and clue never give the name
// away (they are the question in Hide names mode), and no service in the exam data is missing.
const sheetIds = new Set();
for (const z of ZONES) for (const x of z.services) {
  if (sheetIds.has(x.id)) err(`service ${x.id}: duplicate id`);
  sheetIds.add(x.id);
  for (const k of ['name', 'job', 'clue', 'hook']) if (!x[k]) err(`service ${x.id}: missing ${k}`);
  for (const g of x.g) if (!GLYPHS[g]) err(`service ${x.id}: unknown glyph ${g}`);
  if (x.job.length > 38) err(`service ${x.id}: job is over 38 characters`);
  const own = x.name.replace(/^(Amazon|AWS|SageMaker|Bedrock|AgentCore|Glue) /, '').replace(/ \(.*\)$/, '').toLowerCase();
  for (const k of ['job', 'clue']) if (x[k]?.toLowerCase().includes(own)) err(`service ${x.id}: ${k} gives away the name`);
}
for (const z of ZONES) { if (!GLYPHS[z.g]) err(`zone ${z.id}: unknown glyph ${z.g}`);
  for (const x of z.services) if (x.not && !sheetIds.has(x.not[0])) err(`service ${x.id}: not points at unknown ${x.not[0]}`); }
const examText = JSON.stringify([TOPICS, QUESTIONS, CONFUSABLES]).replace(/<[^>]+>/g, '');
const sheetNames = ZONES.flatMap((z) => z.services.map((x) => x.name));
const named = new Set([...examText.matchAll(/\b(?:Amazon|AWS|SageMaker|Bedrock|AgentCore|Glue) [A-Z][A-Za-z0-9-]*(?: [A-Z][A-Za-z0-9-]*){0,2}/g)].map((x) => x[0]));
const bare = (n) => n.replace(/^(?:Amazon|AWS) /, '').replace(/ \(.*\)$/, '');
for (const n of named) {
  const known = sheetNames.some((x) => bare(x) === bare(n) || bare(n).startsWith(bare(x) + ' '));
  if (!known && !COVERED_ELSEWHERE.some((c) => n.startsWith(c))) err(`cheat sheet is missing "${n}", named in the exam data`);
}

if (errors.length) {
  console.error(errors.map((e) => '  ✗ ' + e).join('\n'));
  console.error(`${errors.length} error(s); nothing written.`);
  process.exit(1);
}

const data = { topics: TOPICS, questions: QUESTIONS, days: DAYS, confusables: CONFUSABLES, prompts: PROMPTS, motion: MOTION, domains: DOMAINS };
const json = JSON.stringify(data).replace(/</g, '\\u003c');
const tpl = fs.readFileSync(path.join(HERE, 'page.html'), 'utf8');
if (!tpl.includes('/*__DATA__*/')) { console.error('page.html has no /*__DATA__*/ slot'); process.exit(1); }
// a function replacer, so "$" in the data is never read as a replace pattern
const html = tpl.replace('/*__DATA__*/null', () => json);
fs.writeFileSync(OUT, html);

// the reels feed shares the study page's tokens and diagram CSS: copied from page.html's
// marked blocks on every build, so the two pages cannot drift apart
const block = (name, src = tpl) => {
  const m = src.match(new RegExp(`/\\*@${name}\\*/([\\s\\S]*?)/\\*@/${name}\\*/`));
  if (!m) { console.error(`template has no /*@${name}*/ block`); process.exit(1); }
  return m[1].trim();
};
const rtpl = fs.readFileSync(path.join(HERE, 'reels.html'), 'utf8');
for (const slot of ['/*__TOKENS__*/', '/*__MOTION__*/', '/*__DATA__*/null'])
  if (rtpl.split(slot).length !== 2) { console.error(`reels.html needs exactly one ${slot}`); process.exit(1); }
// Narration: each reel is read as segments (title + step 1, each later step, then the hook).
// tts/narrate.py records them with Kokoro into audio/aif-c01/<topic>-<n>-<hash>.mp3; the hash
// covers the voice and the text, so an edited caption simply has no file yet and that segment
// falls back to the browser's own voice. The export below is what narrate.py reads.
const VOICE = 'af_heart';
const AUDIO_DIR = path.join(HERE, '..', '..', '..', 'audio', 'aif-c01');
const segs = TOPICS.map((t) => [...MOTION[t.id].steps.map((s, k) => (k === 0 ? t.title + '. ' : '') + s), 'Remember. ' + t.hook]);
const key = (text) => crypto.createHash('sha1').update(VOICE + '|' + text).digest('hex').slice(0, 10);
const script = TOPICS.flatMap((t, i) => segs[i].map((text, k) => ({ file: `${t.id}-${k}-${key(text)}.mp3`, text })));
// Service reels: one per cheat sheet entry, sharing the voice folder under an svc- prefix.
const SVC = serviceReels({ ZONES, GLYPHS });
if (SVC.errors.length) { console.error(SVC.errors.map((e) => '  ✗ ' + e).join('\n')); process.exit(1); }
const svcFile = (id, k, text) => `svc-${id}-${k}-${key(text)}.mp3`;
for (const t of SVC.topics) SVC.segs[t.id].forEach((text, k) => script.push({ file: svcFile(t.id, k, text), text }));
fs.writeFileSync(path.join(HERE, 'tts', 'script.json'), JSON.stringify({ voice: VOICE, segments: script }, null, 1));
const have = new Set(fs.existsSync(AUDIO_DIR) ? fs.readdirSync(AUDIO_DIR) : []);
const audio = {}; let recorded = 0;
TOPICS.forEach((t, i) => { audio[t.id] = segs[i].map((text, k) => { const f = `${t.id}-${k}-${key(text)}.mp3`; if (have.has(f)) { recorded++; return '/audio/aif-c01/' + f; } return null; }); });
const rdata = { topics: TOPICS.map(({ id, d, title, hook }) => ({ id, d, title, hook })), motion: MOTION, domains: DOMAINS, segs, audio, voice: VOICE };
const reels = rtpl.replace('/*__TOKENS__*/', () => block('tokens')).replace('/*__MOTION__*/', () => block('motion'))
  .replace('/*__DATA__*/null', () => JSON.stringify(rdata).replace(/</g, '\\u003c'));
fs.writeFileSync(REELS_OUT, reels);

// The service reels run the same player as the topic reels, copied from reels.html's marked
// blocks, so a fix to one feed reaches both.
const svcAudio = {}; let svcRecorded = 0, svcTotal = 0;
for (const t of SVC.topics) svcAudio[t.id] = SVC.segs[t.id].map((text, k) => { svcTotal++; const f = svcFile(t.id, k, text); if (have.has(f)) { svcRecorded++; return '/audio/aif-c01/' + f; } return null; });
const svcData = { topics: SVC.topics, motion: SVC.motion, segs: SVC.topics.map((t) => SVC.segs[t.id]), audio: svcAudio, voice: VOICE,
  zones: ZONES.map((z) => ({ id: z.id, place: z.place, n: z.services.length })) };
const svcReels = fs.readFileSync(path.join(HERE, 'service-reels.html'), 'utf8')
  .replace('/*__TOKENS__*/', () => block('tokens')).replace('/*__MOTION__*/', () => block('motion'))
  .replace('/*__REELCSS__*/', () => block('reelcss', rtpl))
  .replace('<!--__SYMBOLS__-->', () => Object.entries(GLYPHS).map(([id, m]) => `<symbol id="g-${id}" viewBox="0 0 24 24">${m}</symbol>`).join(''))
  .replace('/*__HELPERS__*/', () => block('helpers', rtpl))
  .replace('/*__PLAYER__*/', () => block('player', rtpl))
  .replace('/*__DATA__*/null', () => JSON.stringify(svcData).replace(/</g, '\\u003c'));
fs.writeFileSync(SVC_REELS_OUT, svcReels);

// The service cheat sheet is static markup, so it works without JavaScript and prints whole.
const escHtml = (t) => t.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const glyph = (id, cls) => `<svg class="g ${cls}" aria-hidden="true"><use href="#g-${id}"/></svg>`;
const allServices = ZONES.flatMap((z) => z.services);
const serviceById = new Map(allServices.map((x) => [x.id, x]));
const card = (x) => {
  const gs = x.g.length > 1 ? `${glyph(x.g[0], 'in')}<span class="to" aria-hidden="true">&rarr;</span>${glyph(x.g[1], 'out')}` : glyph(x.g[0], 'out');
  const not = x.not ? `<p class="not">Not <a href="#s-${x.not[0]}">${escHtml(serviceById.get(x.not[0]).name)}</a>: ${escHtml(x.not[1])}</p>` : '';
  const find = [x.name, x.job, x.clue, x.hook].join(' ').toLowerCase();
  return `<article class="c" id="s-${x.id}" data-s="${escHtml(find)}"><div class="gs">${gs}</div><h3 class="nm">${escHtml(x.name)}</h3>` +
    `<p class="job">${escHtml(x.job)}</p><p class="clue"><span class="lbl">Question says</span>${escHtml(x.clue)}</p><p class="hook">${escHtml(x.hook)}</p>${not}` +
    `<a class="watch" href="/aws-ai-practitioner-services-reels#r-${x.id}">Watch the reel</a>` +
    `<button class="rev" type="button">Show the service</button></article>`;
};
// The person zone opens with a face: each sense is one service, so a question's verb points at it.
const FACE = [
  ['rekognition', 'Rekognition', 'sees', 60, 186, 96, 'start'], ['transcribe', 'Transcribe', 'hears', 122, 150, 128, 'start'],
  ['polly', 'Polly', 'speaks', 184, 196, 182, 'start'], ['lex', 'Lex', 'holds the talk', 246, 208, 196, 'start'],
  ['comprehend', 'Comprehend', 'understands', 40, 220, 58, 'end'], ['textract', 'Textract', 'reads paper', 102, 254, 96, 'end'],
  ['personalize', 'Personalize', 'sniffs your taste', 164, 226, 142, 'end'], ['translate', 'Translate', 'changes language', 226, 236, 182, 'end'],
];
const faceSvg = `<div class="figure"><svg viewBox="0 0 440 290" role="img" aria-label="A face. Eyes: Rekognition sees and Textract reads paper. Ear: Transcribe hears. Mouth: Polly speaks, Lex holds the talk, Translate changes language. Brain: Comprehend understands. Nose: Personalize sniffs your taste.">` +
  `<path class="hd" d="M145 128c0-52 33-88 75-88s75 36 75 88c0 62-33 110-75 110s-75-48-75-110Z"/><path class="hd" d="M145 112c-12-4-16 8-14 20s8 22 16 18M295 112c12-4 16 8 14 20s-8 22-16 18"/>` +
  `<path class="hd" d="M176 58c10-14 28-14 38-4 10-10 32-8 40 6"/><path class="hd" d="M176 96c6-6 14-6 20 0M244 96c6-6 14-6 20 0"/><path class="hd" d="M220 112l-8 30h14"/><path class="hd" d="M196 182c14 12 34 12 48 0"/>` +
  FACE.map(([id, n, v, y, px, py, side]) => {
    const left = side === 'start', tx = left ? 8 : 432, lx = left ? 104 : 336;
    return `<path class="lead" d="M${lx} ${y - 4}L${px} ${py}"/><circle class="pt" cx="${px}" cy="${py}" r="3.5"/><a href="#s-${id}"><text x="${tx}" y="${y - 4}" text-anchor="${side}" class="n">${n}</text><text x="${tx}" y="${y + 12}" text-anchor="${side}" class="v">${v}</text></a>`;
  }).join('') + '</svg></div>';
const sheet = fs.readFileSync(path.join(HERE, 'services.html'), 'utf8')
  .replace('/*__TOKENS__*/', () => block('tokens'))
  .replace('<!--__SYMBOLS__-->', () => Object.entries(GLYPHS).map(([id, m]) => `<symbol id="g-${id}" viewBox="0 0 24 24">${m}</symbol>`).join(''))
  .replace('<!--__COUNT__-->', () => String(allServices.length))
  .replace('<!--__TOWN__-->', () => ZONES.map((z) => `<a href="#${z.id}">${glyph(z.g, '')}<b>${z.place}<i>${z.services.length}</i></b><span>${z.say}</span></a>`).join(''))
  .replace('<!--__ZONES__-->', () => ZONES.map((z) => `<section class="zone" id="${z.id}"><div class="zhead"><h2>${z.place}</h2><p>${z.say}</p></div>` +
    (z.id === 'person' ? faceSvg : '') + `<div class="cards">${z.services.map(card).join('')}</div></section>`).join('\n'));
fs.writeFileSync(SHEET_OUT, sheet);

const fmt = (o) => [1, 2, 3, 4, 5].map((d) => o[d] || 0).join('/');
console.log(`aif-c01: ${TOPICS.length} topics | motion ${Object.keys(MOTION).length} | practice ${QUESTIONS.filter((q) => q.set === 'P').length} | ` +
  `Mock A ${fmt(counts.A)} | Mock B ${fmt(counts.B)} | ${(html.length / 1024).toFixed(0)} KB → ${path.relative(process.cwd(), OUT)}`);
console.log(`services: ${allServices.length} services in ${ZONES.length} places | ${(sheet.length / 1024).toFixed(0)} KB → ${path.relative(process.cwd(), SHEET_OUT)}`);
console.log(`reels: ${TOPICS.length} reels | narration ${recorded}/${script.length - svcTotal} recorded (${VOICE}) | ${(reels.length / 1024).toFixed(0)} KB → ${path.relative(process.cwd(), REELS_OUT)}`);
console.log(`service reels: ${SVC.topics.length} reels | narration ${svcRecorded}/${svcTotal} recorded (${VOICE}) | ${(svcReels.length / 1024).toFixed(0)} KB → ${path.relative(process.cwd(), SVC_REELS_OUT)}`);
