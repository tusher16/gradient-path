// Domain 1 motion explainers: one short animated diagram per topic, drawn
// above the plain text. Geometry only (boxes, lines, dots, labels); no
// pictures. Each entry: h = viewBox height (width is always 440), steps =
// the captions, svg = inner markup. An element appears at step --t (with an
// optional --o offset) and the matching caption lights up at the same moment.
// At rest everything is visible, so no-JS and reduced-motion readers see the
// finished diagram. Colours come from the page tokens via classes:
//   bx box, ln line, dot, pl flat fill; .m = memory (teal), .s = signal (pink)
//   lb label, hd heading, mid/end = text-anchor;  a = animated, g = grow in, d = draw in

const st = (t, o, more) => `--t:${t}${o ? `;--o:${o}s` : ''}${more ? ';' + more : ''}`;
const box = (x, y, w, h, cls, t, o, r = 10) =>
  `<rect class="a ${cls}" x="${x}" y="${y}" width="${w}" height="${h}" rx="${r}" style="${st(t, o)}"/>`;
const txt = (x, y, s, cls, t, o, more) =>
  `<text class="a ${cls}" x="${x}" y="${y}" style="${st(t, o, more)}">${s}</text>`;
const path = (d, cls, t, o, more) =>
  `<path class="a ${cls}" d="${d}" pathLength="1" style="${st(t, o, more)}"/>`;
const dot = (cx, cy, r, cls, t, o, more) =>
  `<circle class="a ${cls}" cx="${cx}" cy="${cy}" r="${r}" style="${st(t, o, more)}"/>`;
// a labelled box, label centred
const tag = (x, y, w, h, label, cls, lcls, t, o) =>
  box(x, y, w, h, cls, t, o, h / 2) + txt(x + w / 2, y + h / 2 + 5, label, `mid ${lcls}`, t, o);
// a straight arrow: a line plus a drawn head, both fading in together
const arrow = (x1, y1, x2, y2, cls, t, o) => {
  const a = Math.atan2(y2 - y1, x2 - x1), L = 8, w = 0.5;
  const p = (ang) => `${(x2 - L * Math.cos(a + ang)).toFixed(1)} ${(y2 - L * Math.sin(a + ang)).toFixed(1)}`;
  return `<g class="a" style="${st(t, o, '--x:-10px;--y:0px')}"><path class="ln ${cls}" d="M${x1} ${y1} L${x2} ${y2} M${p(w)} L${x2} ${y2} L${p(-w)}"/></g>`;
};
const from = (dx, dy) => `--x:${dx}px;--y:${dy}px`;

module.exports = {

'ai-nesting': { h: 262,
  steps: [
    'AI: any machine doing something we would call smart, even rules a person wrote by hand.',
    'Machine learning sits inside: it learns the rules from examples instead.',
    'Deep learning sits inside that: neural networks with many layers, good at images, speech and language.',
    'Generative AI sits inside deep learning: models that make new text, images or code.',
    'Agentic AI is generative AI put in a loop: it plans, calls tools, checks the result and repeats.'],
  svg:
    box(8, 8, 424, 246, 'bx', 0, 0, 16) + txt(24, 34, 'AI', 'lb', 0) +
    box(28, 46, 386, 198, 'bx', 1, 0, 14) + txt(44, 72, 'Machine learning', 'lb', 1) +
    box(48, 86, 348, 148, 'bx', 2, 0, 12) + txt(64, 112, 'Deep learning', 'lb', 2) +
    box(68, 126, 168, 92, 'bx m', 3, 0, 10) + txt(84, 154, 'Generative AI', 'lb m', 3) +
    txt(84, 178, 'makes new things', '', 3, 0.3) +
    arrow(240, 170, 284, 170, 's', 4) +
    path('M318 140 A30 30 0 1 1 288 170', 'ln s d', 4, 0.2) +
    dot(318, 140, 5, 'dot s g', 4, 0.5) + dot(348, 170, 5, 'dot s g', 4, 0.7) + dot(318, 200, 5, 'dot s g', 4, 0.9) +
    txt(318, 226, 'agentic loop', 'mid lb s', 4, 0.6) },

'learning-types': { h: 246,
  steps: [
    'Supervised: every example arrives with its answer (the coloured tag), and the model learns to give that answer.',
    'Unsupervised: no answers at all; the model finds the groups by itself.',
    'Reinforcement: an agent acts, the world scores it, and it learns what earns points.',
    'RLHF is reinforcement where the points are people’s ratings of answers.'],
  svg:
    txt(74, 26, 'Supervised', 'mid lb', 0) +
    [50, 86, 122].map((y, i) => box(26, y, 52, 26, 'bx', 0, i * 0.15, 6) +
      dot(98, y + 13, 8, `dot ${i % 2 ? 's' : 'm'} g`, 0, 0.3 + i * 0.15)).join('') +
    tag(26, 178, 96, 32, 'model', 'bx m', 'lb m', 0, 0.9) +
    txt(220, 26, 'Unsupervised', 'mid lb', 1) +
    [[176, 76, -30, 60], [194, 70, 40, 90], [184, 94, 10, 110], [248, 104, -70, 40], [266, 110, 20, -30],
     [254, 128, -40, -60], [204, 168, 50, -80], [226, 172, -20, -100], [214, 192, 40, -40]]
      .map(([x, y, dx, dy], i) => dot(x, y, 6, 'dot', 1, i * 0.05, from(dx, dy))).join('') +
    dot(185, 80, 26, 'ln m g', 1, 0.8) + dot(256, 114, 26, 'ln m g', 1, 0.95) + dot(215, 177, 26, 'ln m g', 1, 1.1) +
    txt(366, 26, 'Reinforcement', 'mid lb', 2) +
    dot(330, 84, 20, 'bx m g', 2) + txt(330, 124, 'agent', 'mid', 2, 0.1) +
    box(352, 150, 76, 44, 'bx', 2, 0.3) + txt(390, 177, 'world', 'mid', 2, 0.3) +
    path('M350 92 Q 404 100 396 146', 'ln d', 2, 0.6) +
    path('M352 176 Q 300 178 318 108', 'ln m d', 2, 1.0) +
    txt(300, 164, '+1', 'end lb m', 2, 1.2) +
    txt(366, 226, 'RLHF: people give the +1', 'mid', 3) },

'data-types': { h: 214,
  steps: [
    'Structured data fits a table of rows and columns, like a spreadsheet of orders.',
    'Unstructured data is everything else: text, images, audio and video. Most company data is like this.',
    'Time-series data is a value measured over time, so the order matters.',
    'Labelled data has the answer attached, usually added by a person, which is why labels cost money.'],
  svg:
    txt(79, 26, 'Structured', 'mid lb', 0) +
    box(20, 44, 118, 120, 'bx', 0, 0, 6) +
    path('M20 74 H138 M20 104 H138 M20 134 H138 M60 44 V164 M100 44 V164', 'ln', 0, 0.25) +
    txt(220, 26, 'Unstructured', 'mid lb', 1) +
    box(160, 44, 50, 66, 'bx', 1, 0, 4) +
    path('M168 60 H202 M168 72 H198 M168 84 H202 M168 96 H190', 'ln', 1, 0.1) +
    box(222, 44, 60, 66, 'bx', 1, 0.2, 4) +
    `<polygon class="a pl" points="228,104 246,78 258,92 266,84 278,104" style="${st(1, 0.35)}"/>` +
    dot(268, 58, 5, 'dot', 1, 0.4) +
    path('M160 178 l8 -12 l8 22 l8 -28 l8 32 l8 -20 l8 12 l8 -6 l8 10 l8 -16 l8 18 l8 -8 l8 4 l10 -2 l10 0', 'ln d', 1, 0.5) +
    txt(366, 26, 'Time-series', 'mid lb', 2) +
    path('M300 44 V164 H430', 'ln', 2) +
    path('M304 146 L320 132 L336 138 L352 112 L368 118 L384 94 L400 100 L416 74 L428 68', 'ln m d', 2, 0.3, '--dur:1.4s') +
    path('M252 110 V118', 'ln m', 3) +
    tag(222, 118, 60, 24, 'cat', 'bx m', 'lb m', 3, 0.1) },

'inference-types': { h: 250,
  steps: [
    'Real-time: someone is waiting, so a live endpoint answers in milliseconds.',
    'Batch: a whole dataset is scored offline, and no endpoint stays up.',
    'Asynchronous: big or slow requests wait in a queue, and you are told when each is done.',
    'Serverless: nothing runs between requests. Cheap for rare traffic, but the first call is slow while it wakes up.'],
  svg:
    txt(12, 45, 'Real-time', 'lb', 0) +
    dot(150, 40, 9, 'dot g', 0, 0.1) + arrow(164, 40, 244, 40, '', 0, 0.3) +
    box(250, 26, 50, 28, 'bx m', 0, 0.5, 8) + arrow(306, 40, 376, 40, 'm', 0, 0.8) +
    txt(430, 45, 'ms', 'end lb m', 0, 1.0) +
    txt(12, 105, 'Batch', 'lb', 1) +
    [0, 1, 2, 3].map((i) => box(136 + i * 7, 92 - i * 5, 34, 22, 'bx', 1, i * 0.1, 3)).join('') +
    arrow(196, 100, 244, 100, '', 1, 0.5) + box(250, 86, 50, 28, 'bx m', 1, 0.6, 8) +
    arrow(306, 100, 340, 100, 'm', 1, 0.9) + txt(430, 105, 'overnight', 'end lb m', 1, 1.1) +
    txt(12, 165, 'Async', 'lb', 2) +
    box(136, 146, 42, 30, 'bx', 2, 0, 4) + txt(157, 166, '1 GB', 'mid', 2) +
    arrow(184, 160, 206, 160, '', 2, 0.3) +
    [0, 1, 2].map((i) => box(212 + i * 18, 151, 13, 18, 'bx', 2, 0.4 + i * 0.1, 3)).join('') +
    arrow(268, 160, 284, 160, '', 2, 0.7) + box(290, 146, 50, 28, 'bx m', 2, 0.8, 8) +
    dot(366, 160, 8, 'dot m g', 2, 1.2) + txt(430, 165, 'notify', 'end lb m', 2, 1.3) +
    txt(12, 225, 'Serverless', 'lb', 3) +
    box(250, 206, 50, 28, 'bx off', 3, 0, 8) +
    dot(150, 220, 9, 'dot g', 3, 0.5) + arrow(164, 220, 244, 220, '', 3, 0.7) +
    box(250, 206, 50, 28, 'bx m g', 3, 1.0, 8) +
    txt(430, 225, 'scales to zero', 'end lb m', 3, 0.3) },

'use-cases': { h: 228,
  steps: [
    'The answer is a number, like a house price: regression.',
    'The answer is a category, like fraud or not, or churn yes or no: classification.',
    'You want groups nobody has labelled, like customer segments: clustering.',
    'It must be exact every time, like tax from a fixed rate table: use a plain rule, not ML.'],
  svg:
    [['House price?', 'Regression', 'bx m', 'lb m'], ['Fraud or not?', 'Classification', 'bx m', 'lb m'],
     ['Customer groups?', 'Clustering', 'bx m', 'lb m'], ['Tax from a table?', 'No ML: a rule', 'bx s', 'lb s']]
      .map(([q, a, bc, lc], i) => {
        const y = 32 + i * 56;
        return txt(12, y + 5, q, 'lb', i) + arrow(170, y, 248, y, i === 3 ? 's' : '', i, 0.3) +
          tag(256, y - 18, 172, 36, a, bc, lc, i, 0.6);
      }).join('') },

'aws-ai-services': { h: 340,
  steps: [
    'Speech: Transcribe writes down what is said; Polly reads text aloud.',
    'Documents: Textract reads scanned paper; Comprehend understands text you already have.',
    'Pictures and languages: Rekognition looks at images; Translate converts one language to another.',
    'Conversations and shopping: Lex works out what a user wants; Personalize recommends the next item.'],
  svg:
    [['speech', 'Transcribe', 'text'], ['text', 'Polly', 'speech'],
     ['scanned form', 'Textract', 'fields, tables'], ['text', 'Comprehend', 'sentiment, PII'],
     ['photo', 'Rekognition', 'labels, faces'], ['English', 'Translate', 'German'],
     ['chat message', 'Lex', 'intent'], ['clicks, buys', 'Personalize', 'recommendations']]
      .map(([i, s, o], k) => {
        const y = 22 + k * 40, t = Math.floor(k / 2), d = (k % 2) * 0.5;
        return `<text class="a end" x="138" y="${y + 5}" style="${st(t, d, from(-14, 0))}">${i}</text>` +
          tag(148, y - 15, 142, 30, s, 'bx m', 'lb m', t, d + 0.2) +
          `<text class="a" x="300" y="${y + 5}" style="${st(t, d + 0.4, from(14, 0))}">${o}</text>`;
      }).join('') },

'trad-ml-vs-fm': { h: 256,
  steps: [
    'Two kinds of model, built for two kinds of job.',
    'A neat table, huge volume, and every decision must be explained: a small traditional model.',
    'Messy text or images, many different tasks, few labels: a foundation model.',
    'Or both together: the foundation model pulls fields out of documents, and the traditional model scores them.'],
  svg:
    box(14, 150, 200, 70, 'bx', 0, 0, 12) + txt(114, 180, 'Traditional ML', 'mid lb', 0) +
    txt(114, 204, 'small, cheap, explainable', 'mid', 0, 0.2) +
    box(226, 150, 200, 70, 'bx m', 0, 0.3, 12) + txt(326, 180, 'Foundation model', 'mid lb m', 0, 0.3) +
    txt(326, 204, 'messy input, many tasks', 'mid', 0, 0.5) +
    [[24, 60, 104, 'huge volume'], [24, 102, 92, 'tabular data'], [122, 102, 92, 'must explain']]
      .map(([x, y, w, s], i) => `<g class="a" style="${st(1, i * 0.2, from(0, -40))}">` +
        `<rect class="bx" x="${x}" y="${y}" width="${w}" height="30" rx="15"/><text class="mid" x="${x + w / 2}" y="${y + 20}">${s}</text></g>`).join('') +
    [[236, 60, 150, 'free text, images'], [236, 102, 92, 'many tasks'], [334, 102, 92, 'few labels']]
      .map(([x, y, w, s], i) => `<g class="a" style="${st(2, i * 0.2, from(0, -40))}">` +
        `<rect class="bx m" x="${x}" y="${y}" width="${w}" height="30" rx="15"/><text class="mid" x="${x + w / 2}" y="${y + 20}">${s}</text></g>`).join('') +
    path('M300 222 Q 220 246 140 222', 'ln s d', 3) +
    txt(220, 250, 'or both', 'mid lb s', 3, 0.4) },

'ml-lifecycle': { h: 250,
  steps: [
    'Start with the business goal, then collect the data (Amazon S3, AWS Glue).',
    'Clean it (Glue DataBrew, Data Wrangler) and shape it into features (Feature Store).',
    'Train and tune it (SageMaker AI), then evaluate it on data it never saw.',
    'Deploy it behind an endpoint or a managed API, and monitor it (Model Monitor).',
    'When the world changes, monitoring triggers retraining. It is a loop, not a line.'],
  svg:
    `<ellipse class="a ln d" cx="220" cy="125" rx="170" ry="85" pathLength="1" style="${st(0, 0, '--dur:7s')}"/>` +
    [['Goal', 220, 40], ['Data', 340, 65], ['Clean', 390, 125], ['Features', 340, 185],
     ['Train', 220, 210], ['Evaluate', 100, 185], ['Deploy', 50, 125], ['Monitor', 100, 65]]
      .map(([s, x, y], i) => tag(x - 43, y - 15, 86, 30, s, 'bx', 'lb', Math.floor(i / 2), (i % 2) * 0.6)).join('') +
    tag(57, 50, 86, 30, 'Monitor', 'bx s', 'lb s', 4) +
    txt(220, 120, 'a loop, not a line', 'mid hd', 4, 0.3) +
    txt(220, 146, 'drift → retrain', 'mid lb s', 4, 0.6) },

'mlops': { h: 236,
  steps: [
    'MLOps puts training and deployment in one automated pipeline (SageMaker Pipelines).',
    'Every run repeats the same steps, so any model version can be rebuilt.',
    'In production, Model Monitor watches quality against a threshold.',
    'Customer behaviour shifts and accuracy slides below the line: that is drift.',
    'The drop triggers retraining, and the new model goes back through the same pipeline.'],
  svg:
    ['Code', 'Train', 'Evaluate', 'Register', 'Deploy']
      .map((s, i) => tag(6 + i * 86, 20, 78, 30, s, 'bx m', 'lb m', 0, i * 0.2)).join('') +
    txt(424, 78, 'same steps, every run', 'end', 1) +
    path('M84 35 H92 M170 35 H178 M256 35 H264 M342 35 H350', 'ln m', 1) +
    path('M40 104 V214 H424', 'ln', 2) +
    path('M40 150 H424', 'ln dash', 2, 0.2) + txt(424, 144, 'threshold', 'end', 2, 0.3) +
    txt(48, 118, 'accuracy', '', 2, 0.3) +
    path('M44 126 L110 124 L170 128 L220 134', 'ln d', 2, 0.6) +
    path('M220 134 L250 150 L290 176', 'ln s d', 3) +
    dot(290, 176, 7, 'dot s g', 3, 0.5) + txt(290, 204, 'drift detected', 'mid lb s', 3, 0.6) +
    path('M296 168 C 250 120 140 110 131 54', 'ln m d', 4) +
    path('M290 176 L330 136 L420 128', 'ln m d', 4, 0.8) },

'metrics': { h: 224,
  steps: [
    'Twenty payments, four of them fraud. When one outcome is rare, accuracy misleads.',
    'A model that always says “not fraud” is 80% accurate and catches nothing.',
    'A better model flags five. Precision: 3 of its 5 flags were fraud. Recall: it caught 3 of the 4 frauds.',
    'One fraud slipped through. When a miss is costly, push recall up and accept more false alarms.'],
  svg:
    [36, 76, 116, 156, 196].map((x) => [44, 84, 124, 164].map((y) => {
      const fraud = (x === 76 && y === 44) || (x === 156 && y === 84) || (x === 36 && y === 124) || (x === 196 && y === 164);
      return dot(x, y, 9, `dot ${fraud ? 's' : ''} g`, 0, ((x + y) % 7) * 0.06);
    }).join('')).join('') +
    txt(232, 40, '20 payments, 4 fraud', 'lb', 0, 0.4) +
    txt(232, 76, 'Always “not fraud”:', '', 1) +
    txt(232, 98, 'accuracy 80%, recall 0%', 'lb s', 1, 0.3) +
    [[76, 44], [156, 84], [36, 124], [116, 44], [116, 124]].map(([x, y], i) => dot(x, y, 16, 'ln m g', 2, i * 0.12)).join('') +
    txt(232, 138, 'Model B flags 5:', '', 2, 0.4) +
    txt(232, 160, 'precision 3/5 = 60%', 'lb m', 2, 0.6) +
    txt(232, 182, 'recall 3/4 = 75%', 'lb m', 2, 0.8) +
    dot(196, 164, 16, 'ln s g', 3) + txt(196, 206, 'missed', 'mid lb s', 3, 0.3) },

};
