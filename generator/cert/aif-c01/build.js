#!/usr/bin/env node
// Validate the AIF-C01 sources, then inline them into ../../../aws-ai-practitioner.html
// and the reels feed ../../../aws-ai-practitioner-reels.html.
// Run from anywhere:  node generator/cert/aif-c01/build.js
// Exit 1 on any validation error; nothing is written in that case.
const fs = require('fs');
const path = require('path');

const HERE = __dirname;
const OUT = path.join(HERE, '..', '..', '..', 'aws-ai-practitioner.html');
const REELS_OUT = path.join(HERE, '..', '..', '..', 'aws-ai-practitioner-reels.html');
const TOPICS = require('./topics.js');
const QUESTIONS = require('./questions.js');
const { DAYS, CONFUSABLES, PROMPTS, DOMAINS } = require('./extras.js');
const MOTION = require('./motion.js');

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
const block = (name) => {
  const m = tpl.match(new RegExp(`/\\*@${name}\\*/([\\s\\S]*?)/\\*@/${name}\\*/`));
  if (!m) { console.error(`page.html has no /*@${name}*/ block`); process.exit(1); }
  return m[1].trim();
};
const rtpl = fs.readFileSync(path.join(HERE, 'reels.html'), 'utf8');
for (const slot of ['/*__TOKENS__*/', '/*__MOTION__*/', '/*__DATA__*/null'])
  if (rtpl.split(slot).length !== 2) { console.error(`reels.html needs exactly one ${slot}`); process.exit(1); }
const rdata = { topics: TOPICS.map(({ id, d, title, hook }) => ({ id, d, title, hook })), motion: MOTION, domains: DOMAINS };
const reels = rtpl.replace('/*__TOKENS__*/', () => block('tokens')).replace('/*__MOTION__*/', () => block('motion'))
  .replace('/*__DATA__*/null', () => JSON.stringify(rdata).replace(/</g, '\\u003c'));
fs.writeFileSync(REELS_OUT, reels);

const fmt = (o) => [1, 2, 3, 4, 5].map((d) => o[d] || 0).join('/');
console.log(`aif-c01: ${TOPICS.length} topics | motion ${Object.keys(MOTION).length} | practice ${QUESTIONS.filter((q) => q.set === 'P').length} | ` +
  `Mock A ${fmt(counts.A)} | Mock B ${fmt(counts.B)} | ${(html.length / 1024).toFixed(0)} KB → ${path.relative(process.cwd(), OUT)}`);
console.log(`reels: ${TOPICS.length} reels | ${(reels.length / 1024).toFixed(0)} KB → ${path.relative(process.cwd(), REELS_OUT)}`);
