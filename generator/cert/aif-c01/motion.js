// Domain 1–3 motion explainers: one short animated diagram per topic, drawn
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

// ---------------- Domain 2 · Fundamentals of GenAI ----------------
'tokens-embeddings': { h: 250,
  steps: [
    'A model reads tokens, sub-word pieces, not words. Prices and limits are counted in tokens.',
    'An embedding turns a piece of text into a vector: a point whose position captures its meaning.',
    'Similar meanings land close together, so a search for “money back” finds the refund policy.',
    'Chunking cuts a long document into pieces before embedding, so search returns one paragraph, not a whole manual.'],
  svg:
    txt(220, 26, 'Unbelievable', 'mid hd', 0) +
    tag(116, 40, 56, 28, 'Un', 'bx m', 'lb m', 0, 0.4) +
    tag(180, 40, 80, 28, 'believ', 'bx m', 'lb m', 0, 0.55) +
    tag(268, 40, 60, 28, 'able', 'bx m', 'lb m', 0, 0.7) +
    path('M40 100 V232 H246', 'ln', 1) +
    dot(96, 146, 7, 'dot g', 1, 0.3) + txt(50, 114, 'refund policy', '', 1, 0.3) +
    dot(124, 160, 7, 'dot g', 1, 0.5) + txt(140, 166, 'money back', '', 1, 0.5) +
    dot(226, 212, 7, 'dot g', 1, 0.7) + txt(216, 200, 'holiday rota', 'end', 1, 0.7) +
    dot(110, 153, 30, 'ln m g', 2) + txt(48, 226, 'close = similar', 'lb m', 2, 0.3) +
    box(278, 100, 54, 132, 'bx', 3, 0, 4) +
    path('M286 116 H324 M286 128 H318 M286 140 H324 M286 152 H312 M286 164 H324 M286 176 H320 M286 188 H324 M286 200 H316 M286 212 H322', 'ln', 3) +
    [100, 148, 196].map((y, i) => box(368, y, 60, 36, 'bx m', 3, 0.4 + i * 0.2, 4)).join('') +
    arrow(336, 166, 362, 166, 'm', 3, 0.3) },

'model-types': { h: 300,
  steps: [
    'A transformer reads the whole passage at once and works out which words matter to which. That is attention.',
    'A foundation model is pre-trained once on huge general data, then adapted to many tasks.',
    'A multimodal model takes more than one kind of input or output, like a photo plus a question.',
    'A diffusion model starts from random noise and removes it step by step until a picture appears.'],
  svg:
    txt(12, 22, 'Transformer', 'lb', 0) +
    [[40, 52, 'cat'], [100, 64, 'drank'], [172, 32, 'it'], [212, 44, 'was'], [264, 72, 'thirsty']]
      .map(([x, w, s], i) => tag(x, 62, w, 28, s, i === 2 ? 'bx m' : 'bx', i === 2 ? 'lb m' : 'lb', 0, i * 0.12)).join('') +
    path('M188 62 Q 140 22 66 62', 'ln m d', 0, 0.8) +
    path('M188 62 Q 244 26 300 62', 'ln m d', 0, 1.0) +
    tag(14, 112, 170, 36, 'Foundation model', 'bx m', 'lb m', 1) +
    arrow(188, 130, 214, 130, '', 1, 0.3) +
    [[220, 80, 'summarise'], [306, 52, 'chat'], [364, 60, 'code']]
      .map(([x, w, s], i) => tag(x, 115, w, 30, s, 'bx', '', 1, 0.5 + i * 0.15)).join('') +
    box(14, 170, 44, 34, 'bx', 2, 0, 4) +
    `<polygon class="a pl" points="18,200 30,182 38,192 44,186 54,200" style="${st(2, 0.1)}"/>` +
    txt(70, 193, '+', 'mid lb', 2, 0.2) +
    tag(82, 172, 112, 30, 'what is this?', 'bx', '', 2, 0.3) +
    arrow(198, 187, 236, 187, '', 2, 0.5) +
    tag(242, 172, 128, 30, 'multimodal', 'bx m', 'lb m', 2, 0.6) +
    arrow(374, 187, 386, 187, 'm', 2, 0.8) + txt(390, 192, 'answer', '', 2, 0.9) +
    [0, 1, 2, 3].map((k) => {
      const x = 14 + k * 76, n = [14, 8, 3, 0][k];
      let s = box(x, 228, 52, 52, k === 3 ? 'bx m' : 'bx', 3, k * 0.35, 6);
      for (let j = 0; j < n; j++) s += dot(x + 8 + ((j * 17) % 36), 236 + ((j * 23) % 36), 2.5, 'dot', 3, k * 0.35 + 0.1);
      if (k === 3) s += `<polygon class="a pl" points="${x + 6},${272} ${x + 20},${250} ${x + 30},${262} ${x + 38},${254} ${x + 46},${272}" style="${st(3, 1.2)}"/>`;
      if (k < 3) s += arrow(x + 56, 254, x + 72, 254, '', 3, k * 0.35 + 0.2);
      return s;
    }).join('') +
    txt(434, 259, 'noise → image', 'end lb m', 3, 1.3) },

'fm-lifecycle': { h: 196,
  steps: [
    'Choose the data, then the model design.',
    'Pre-train it on a massive amount of unlabelled data. That costs millions, so few companies ever do it.',
    'Fine-tune it for a narrower job, evaluate it, then deploy it.',
    'Collect feedback (ratings, human review), which feeds the next round of tuning.',
    'Most companies start from an existing model and join at fine-tuning or later.'],
  svg:
    tag(8, 56, 92, 32, 'Data', 'bx', 'lb', 0) + arrow(102, 72, 118, 72, '', 0, 0.3) +
    tag(120, 56, 92, 32, 'Model', 'bx', 'lb', 0, 0.4) + arrow(214, 72, 230, 72, '', 1) +
    tag(232, 56, 92, 32, 'Pre-train', 'bx s', 'lb s', 1, 0.2) + txt(278, 44, 'costs millions', 'mid lb s', 1, 0.5) +
    arrow(326, 72, 342, 72, '', 2) +
    tag(344, 56, 92, 32, 'Fine-tune', 'bx m', 'lb m', 2, 0.1) + arrow(390, 90, 390, 136, '', 2, 0.4) +
    tag(344, 140, 92, 32, 'Evaluate', 'bx', 'lb', 2, 0.5) + arrow(342, 156, 326, 156, '', 2, 0.7) +
    tag(232, 140, 92, 32, 'Deploy', 'bx', 'lb', 2, 0.8) + arrow(230, 156, 214, 156, '', 3) +
    tag(120, 140, 92, 32, 'Feedback', 'bx m', 'lb m', 3, 0.2) +
    path('M166 138 Q 250 104 340 84', 'ln m d', 3, 0.6) +
    txt(390, 24, 'you start here', 'mid lb m', 4) + path('M390 30 V52', 'ln m', 4, 0.2) },

'genai-tradeoffs': { h: 246,
  steps: [
    'Strengths: one model adapts to many jobs, talks naturally and creates new content.',
    'Weakness: it can hallucinate, stating false things confidently.',
    'It is also nondeterministic (the same question can get a different answer), and it cannot explain why it answered as it did.',
    'Choosing a model is a trade-off: modality, latency, cost, context length, compliance and language.'],
  svg:
    txt(14, 24, 'Good at', 'lb m', 0) +
    [[40, 'adaptable'], [80, 'conversational'], [120, 'creates content']]
      .map(([y, s], i) => tag(14, y, 150, 30, s, 'bx m', 'lb m', 0, 0.2 + i * 0.2)).join('') +
    txt(234, 24, 'Watch out for', 'lb s', 1) +
    tag(234, 40, 190, 30, 'hallucinates', 'bx s', 'lb s', 1, 0.2) +
    tag(234, 80, 190, 30, 'changes its answer', 'bx s', 'lb s', 2) +
    tag(234, 120, 190, 30, 'hard to explain', 'bx s', 'lb s', 2, 0.3) +
    txt(14, 186, 'Choose by', 'lb', 3) +
    [[100, 84, 'modality'], [192, 76, 'latency'], [276, 52, 'cost'], [336, 90, 'context']]
      .map(([x, w, s], i) => tag(x, 166, w, 30, s, 'bx', '', 3, 0.2 + i * 0.12)).join('') +
    [[100, 104, 'compliance'], [212, 92, 'language']]
      .map(([x, w, s], i) => tag(x, 206, w, 30, s, 'bx', '', 3, 0.7 + i * 0.12)).join('') },

'token-pricing': { h: 288,
  steps: [
    'You pay for input tokens (what you send) and output tokens (what comes back). Output usually costs more.',
    'On-demand is a taxi meter: pay only for the tokens you use. It fits low or spiky traffic.',
    'Provisioned Throughput is a leased car: reserved capacity billed by the hour, used or not.',
    'Batch is a freight train: cheaper per token for big jobs where nobody waits.',
    'Prompt caching: a long prefix sent with every request is read from cache, which is cheaper and faster.'],
  svg:
    tag(14, 20, 124, 32, 'input tokens', 'bx', 'lb', 0) + arrow(142, 36, 170, 36, '', 0, 0.2) +
    tag(176, 20, 70, 32, 'model', 'bx m', 'lb m', 0, 0.3) + arrow(250, 36, 278, 36, '', 0, 0.5) +
    tag(284, 20, 144, 32, 'output tokens', 'bx s', 'lb s', 0, 0.6) +
    txt(356, 72, 'costs more per token', 'mid', 0, 0.8) +
    txt(12, 124, 'On-demand', 'lb', 1) +
    [6, 18, 4, 26, 8, 14, 30, 6, 10, 4, 22, 8].map((h, i) =>
      `<rect class="a bx m" x="${140 + i * 14}" y="${134 - h}" width="10" height="${h}" rx="2" style="${st(1, 0.2 + i * 0.05, from(0, 6))}"/>`).join('') +
    txt(430, 124, 'pay per token', 'end lb m', 1, 0.8) +
    txt(12, 174, 'Provisioned', 'lb', 2) +
    box(140, 152, 164, 28, 'bx', 2, 0.2, 4) + txt(222, 171, 'reserved, every hour', 'mid', 2, 0.4) +
    txt(430, 174, 'fixed hourly', 'end lb', 2, 0.6) +
    txt(12, 224, 'Batch', 'lb', 3) +
    [0, 1, 2, 3].map((i) => box(140 + i * 7, 212 - i * 5, 34, 22, 'bx', 3, i * 0.1, 3)).join('') +
    arrow(200, 218, 250, 218, '', 3, 0.5) + txt(430, 224, 'results later, cheaper', 'end lb m', 3, 0.7) +
    txt(12, 270, 'Caching', 'lb', 4) +
    tag(140, 252, 112, 28, 'same prefix', 'bx m', 'lb m', 4, 0.2) +
    tag(258, 252, 80, 28, 'new ask', 'bx', '', 4, 0.4) +
    txt(430, 271, 'cached', 'end lb m', 4, 0.6) },

'aws-genai-stack': { h: 330,
  steps: [
    'A ready foundation model behind an API, no servers: Amazon Bedrock. Building and hosting your own model: SageMaker AI.',
    'A pre-trained model deployed into your account in a few clicks: SageMaker JumpStart. Amazon’s own models: Nova.',
    'A business analyst working with data: Amazon Quick. A developer building software: Kiro.',
    'Writing an agent in code: Strands Agents. Running agents securely in production: Bedrock AgentCore.'],
  svg:
    [['ready FM, no servers', 'Amazon Bedrock'], ['build your own model', 'SageMaker AI'],
     ['one-click model shelf', 'SageMaker JumpStart'], ['Amazon’s own models', 'Amazon Nova'],
     ['business analyst', 'Amazon Quick'], ['developer’s IDE', 'Kiro'],
     ['agent written in code', 'Strands Agents'], ['agents in production', 'Bedrock AgentCore']]
      .map(([who, what], k) => {
        const y = 24 + k * 40, t = Math.floor(k / 2), d = (k % 2) * 0.5;
        return `<text class="a end" x="196" y="${y + 5}" style="${st(t, d, from(-14, 0))}">${who}</text>` +
          arrow(202, y, 224, y, '', t, d + 0.15) +
          tag(230, y - 15, 200, 30, what, 'bx m', 'lb m', t, d + 0.3);
      }).join('') },

'agentic-ai': { h: 262,
  steps: [
    'An agent gets a goal, reasons about the next step and picks a tool.',
    'It calls the tool, looks at the result and repeats until the goal is met or a stop rule fires.',
    'MCP is a standard plug: any agent can reach any tool or data source the same way.',
    'Memory keeps earlier steps and conversations: short-term for this session, long-term across sessions.',
    'Context engineering decides what fills the model’s limited window each step: instructions, facts, tool results, history.'],
  svg:
    tag(14, 112, 80, 32, 'goal', 'bx', 'lb', 0) + arrow(98, 128, 122, 128, '', 0, 0.2) +
    dot(170, 128, 34, 'bx m g', 0, 0.4) + txt(170, 133, 'agent', 'mid lb m', 0, 0.5) +
    path('M134.8 98.4 A46 46 0 1 1 134.8 157.6', 'ln m d', 1) +
    txt(158, 196, 'act, observe, repeat', 'end', 1, 0.6) +
    arrow(220, 128, 246, 128, 'm', 2) +
    box(252, 44, 34, 176, 'bx m', 2, 0.2, 8) + txt(269, 36, 'MCP', 'mid lb m', 2, 0.2) +
    [['search', 58], ['calendar', 104], ['database', 150], ['payments', 196]]
      .map(([s, y], i) => path(`M286 ${y} H306`, 'ln m', 2, 0.5 + i * 0.12) +
        tag(308, y - 15, 118, 30, s, 'bx', '', 2, 0.5 + i * 0.12)).join('') +
    tag(110, 214, 120, 32, 'memory', 'bx', 'lb', 3) + path('M170 180 V212', 'ln', 3, 0.2) +
    box(14, 26, 210, 46, 'bx', 4, 0, 8) + txt(18, 18, 'context window', 'lb', 4) +
    [['bx m', 0], ['bx m', 1], ['bx', 2], ['bx s', 3]]
      .map(([c, i]) => box(22 + i * 50, 36, 44, 26, c, 4, 0.3 + i * 0.15, 4)).join('') },

// ---------------- Domain 3 · Applications of foundation models ----------------
'fm-selection-params': { h: 252,
  steps: [
    'Pick a model like a vehicle: what it costs, what it can take in, how fast it is, its languages and how much text it holds.',
    'Temperature is a creativity dial. Low gives consistent, predictable wording, good for facts and support.',
    'High gives varied, surprising answers, good for brainstorming slogans.',
    'Neither setting makes an answer true. Accuracy comes from better context, not the dial.',
    'Max tokens caps how long the answer can be, which also caps its cost; a stop sequence says where to stop.'],
  svg:
    [[14, 52, 'cost'], [72, 84, 'modality'], [162, 76, 'latency'], [244, 94, 'languages'], [344, 84, 'context']]
      .map(([x, w, s], i) => tag(x, 14, w, 30, s, 'bx', '', 0, i * 0.12)).join('') +
    txt(40, 88, 'temperature', 'lb', 1) + path('M40 104 H400', 'ln', 1) +
    dot(70, 104, 10, 'dot m g', 1, 0.3) + txt(70, 132, 'low', 'mid lb m', 1, 0.4) +
    path('M40 148 H150 M40 160 H150 M40 172 H150', 'ln m', 1, 0.6) +
    dot(370, 104, 10, 'dot g', 2) + txt(370, 132, 'high', 'mid lb', 2, 0.1) +
    path('M300 148 H420 M300 160 H352 M300 172 H396', 'ln', 2, 0.3) +
    txt(222, 198, 'temperature ≠ truth', 'mid lb s', 3) +
    Array.from({ length: 13 }, (_, i) => box(40 + i * 20, 214, 16, 16, 'bx', 4, i * 0.06, 3)).join('') +
    path('M302 206 V240', 'ln s', 4, 0.8) + txt(310, 236, 'max tokens', 'lb s', 4, 0.9) },

'rag': { h: 248,
  steps: [
    'Before any question: documents are cut into chunks, embedded, and stored in a vector database.',
    'A question arrives and is embedded the same way.',
    'The nearest chunks are retrieved and added to the prompt.',
    'The model answers from your documents and cites them.',
    'When documents change, sync the knowledge base so the index updates. No retraining.'],
  svg:
    [0, 1, 2].map((i) => box(14 + i * 6, 38 - i * 5, 40, 30, 'bx', 0, i * 0.1, 3)).join('') +
    arrow(70, 46, 92, 46, '', 0, 0.3) + tag(96, 30, 74, 32, 'chunks', 'bx', '', 0, 0.4) +
    arrow(174, 46, 196, 46, '', 0, 0.6) + tag(200, 30, 70, 32, 'embed', 'bx', '', 0, 0.7) +
    arrow(274, 46, 296, 46, '', 0, 0.9) + tag(300, 30, 128, 32, 'vector store', 'bx m', 'lb m', 0, 1.0) +
    tag(14, 120, 92, 32, 'question', 'bx', 'lb', 1) + arrow(110, 136, 132, 136, '', 1, 0.3) +
    tag(136, 120, 70, 32, 'embed', 'bx', '', 1, 0.4) +
    arrow(364, 66, 364, 116, 'm', 2) + arrow(210, 136, 296, 136, 'm', 2, 0.2) +
    txt(252, 128, 'nearest', 'mid', 2, 0.2) +
    tag(300, 120, 128, 32, 'top chunks', 'bx m', 'lb m', 2, 0.4) +
    arrow(364, 156, 364, 196, '', 2, 0.7) + tag(300, 200, 128, 32, 'prompt', 'bx', 'lb', 2, 0.8) +
    arrow(296, 216, 252, 216, '', 3) + tag(178, 200, 70, 32, 'FM', 'bx m', 'lb m', 3, 0.2) +
    arrow(174, 216, 152, 216, 'm', 3, 0.4) + tag(14, 200, 134, 32, 'answer + sources', 'bx m', 'lb m', 3, 0.5) +
    dot(66, 30, 6, 'dot s g', 4) + txt(14, 96, 'docs changed? sync, no retraining', 'lb m', 4, 0.2) },

'customization-ladder': { h: 262,
  steps: [
    'The bottom rungs change no weights: better prompts, then RAG with your documents.',
    'Fine-tuning retrains the model a little on labelled prompt and response pairs.',
    'Continued pre-training feeds it a mountain of unlabelled text from your field.',
    'Pre-training from scratch builds your own model. Each rung up costs more time, money and data, so climb only as far as you must.',
    'Distillation is a side door: a large teacher model’s answers train a small, cheap student.'],
  svg:
    [['Prompting', 'no training', 0, 0], ['RAG', 'add your docs', 0, 0.5], ['Fine-tune', 'labelled pairs', 1, 0],
     ['Cont. pre-train', 'unlabelled text', 2, 0], ['Pre-train', 'from scratch', 3, 0]]
      .map(([s, n, t, o], i) => {
        const y = 222 - i * 44;
        return tag(14, y, 150, 32, s, i < 2 ? 'bx m' : i === 4 ? 'bx s' : 'bx', i < 2 ? 'lb m' : i === 4 ? 'lb s' : 'lb', t, o) +
          txt(176, y + 21, n, '', t, o + 0.2);
      }).join('') +
    arrow(426, 252, 426, 48, 's', 3, 0.4) + txt(416, 30, 'more cost, data, time', 'end lb s', 3, 0.6) +
    txt(356, 128, 'Distillation', 'mid lb m', 4) +
    dot(326, 170, 22, 'bx m g', 4, 0.2) + arrow(352, 170, 370, 170, 'm', 4, 0.5) +
    dot(386, 170, 12, 'bx m g', 4, 0.6) +
    txt(326, 212, 'teacher', 'mid', 4, 0.3) + txt(392, 212, 'student', 'mid', 4, 0.7) },

'fine-tuning-data': { h: 236,
  steps: [
    'Instruction tuning: many “request, then a great answer” pairs teach the model to follow instructions.',
    'Domain adaptation and transfer learning reuse what a model already knows and adjust it for a new field.',
    'Good training data is curated, labelled, big enough, representative of real users, and allowed to be used.',
    'A small, clean, representative set beats a big noisy one.'],
  svg:
    [30, 70, 110].map((y, i) => tag(14, y, 84, 28, 'request', 'bx', '', 0, i * 0.2) +
      arrow(102, y + 14, 120, y + 14, '', 0, i * 0.2 + 0.1) +
      tag(124, y, 76, 28, 'answer', 'bx m', 'lb m', 0, i * 0.2 + 0.2)).join('') +
    tag(14, 168, 96, 32, 'base model', 'bx', 'lb', 1) + arrow(114, 184, 136, 184, 'm', 1, 0.3) +
    tag(140, 168, 96, 32, 'adapted', 'bx m', 'lb m', 1, 0.5) +
    txt(14, 224, 'reuse, then adjust', '', 1, 0.7) +
    txt(262, 24, 'Good data', 'lb', 2) +
    ['curated', 'labelled', 'enough', 'representative', 'permitted'].map((s, i) => {
      const y = 54 + i * 30;
      return path(`M262 ${y - 5} l5 5 l9 -10`, 'ln m d', 2, 0.2 + i * 0.15) + txt(284, y + 1, s, '', 2, 0.25 + i * 0.15);
    }).join('') +
    txt(262, 224, 'clean beats big', 'lb m', 3) },

'prompt-techniques': { h: 290,
  steps: [
    'A good prompt has parts: the instruction, the context, the input data and the output format.',
    'Zero-shot: just ask. One-shot: show one example first. Few-shot: show several.',
    'Chain-of-thought: ask the model to reason step by step before it answers.',
    'Examples in the prompt are in-context learning: nothing is retrained, and the weights do not change.',
    'Prompt Management keeps prompts as versions: edit the draft, ship a tested version, roll back if it gets worse.'],
  svg:
    box(14, 18, 196, 150, 'bx', 0, 0, 12) +
    ['instruction', 'context', 'input', 'output format'].map((s, i) =>
      tag(24, 28 + i * 34, 176, 28, s, i === 0 ? 'bx m' : 'bx', i === 0 ? 'lb m' : '', 0, 0.2 + i * 0.15)).join('') +
    [['zero-shot', 0], ['one-shot', 1], ['few-shot', 3]].map(([s, n], i) => {
      const y = 36 + i * 34;
      return txt(230, y + 5, s, 'lb', 1, i * 0.3) +
        (n ? Array.from({ length: n }, (_, j) => box(330 + j * 22, y - 8, 16, 16, 'bx m', 1, i * 0.3 + 0.1 + j * 0.08, 3)).join('')
           : txt(330, y + 5, 'just ask', '', 1, 0.1));
    }).join('') +
    tag(230, 136, 60, 28, 'step 1', 'bx', '', 2) + arrow(294, 150, 306, 150, '', 2, 0.2) +
    tag(310, 136, 60, 28, 'step 2', 'bx', '', 2, 0.3) + arrow(374, 150, 384, 150, '', 2, 0.5) +
    tag(388, 136, 46, 28, 'end', 'bx m', 'lb m', 2, 0.6) +
    txt(230, 194, 'weights unchanged', 'lb m', 3) +
    path('M40 248 H340', 'ln', 4) +
    [['v1', 70], ['v2', 160], ['v3', 250]].map(([s, x], i) =>
      dot(x, 248, 8, 'dot m g', 4, 0.2 + i * 0.2) + txt(x, 274, s, 'mid', 4, 0.2 + i * 0.2)).join('') +
    dot(330, 248, 9, 'bx off g', 4, 0.9) + txt(330, 274, 'draft', 'mid', 4, 0.9) +
    txt(160, 226, 'production', 'mid lb m', 4, 1.1) },

'prompt-risks': { h: 258,
  steps: [
    'Prompt injection hides orders in the input or in a document the model reads. If it works, the model is hijacked and serves the attacker.',
    'Jailbreaking talks the model past its safety rules, often through role-play.',
    'Poisoning taints the training or retrieval data, so the model learns or repeats something wrong.',
    'Exposure, or leaking: the model reveals its hidden instructions or private data.',
    'Defences: Bedrock Guardrails, input checks, least-privilege tools, and keeping instructions separate from data.'],
  svg:
    txt(14, 22, 'Injection', 'lb s', 0) +
    box(14, 34, 44, 56, 'bx', 0, 0, 4) + path('M22 48 H50 M22 60 H46 M22 84 H48', 'ln', 0, 0.1) +
    path('M22 72 H50', 'ln s', 0, 0.3) +
    arrow(62, 62, 98, 62, '', 0, 0.5) + tag(102, 47, 70, 30, 'model', 'bx', '', 0, 0.6) +
    txt(137, 100, 'hijacked', 'mid lb s', 0, 0.9) +
    txt(234, 22, 'Jailbreaking', 'lb s', 1) +
    tag(234, 40, 126, 28, 'role-play trick', 'bx s', 'lb s', 1, 0.2) +
    path('M392 34 V96', 'ln', 1, 0.1) + txt(392, 110, 'rules', 'mid', 1, 0.1) +
    arrow(364, 54, 426, 54, 's', 1, 0.6) +
    txt(14, 136, 'Poisoning', 'lb s', 2) +
    [0, 1, 2, 3, 4].map((i) => box(14, 148 + i * 12, 80, 9, i === 2 ? 'bx s' : 'bx', 2, i * 0.08, 2)).join('') +
    arrow(100, 176, 128, 176, '', 2, 0.5) + tag(132, 161, 70, 30, 'model', 'bx', '', 2, 0.6) +
    txt(234, 136, 'Exposure', 'lb s', 3) +
    tag(234, 152, 70, 30, 'model', 'bx', '', 3) + arrow(308, 167, 334, 167, 's', 3, 0.3) +
    tag(338, 152, 90, 30, 'secrets', 'bx s', 'lb s', 3, 0.5) +
    txt(220, 244, 'Defend: Guardrails, input checks, least privilege', 'mid lb m', 4) },

'fm-evaluation': { h: 262,
  steps: [
    'Three ways to grade a model: people review the answers, a benchmark test set, or another model acting as judge.',
    'ROUGE asks how much of the reference the output covered. It is the summary metric.',
    'BLEU asks how much of the output matches the reference wording. It is the translation metric.',
    'BERTScore compares meaning rather than exact words, so a good paraphrase still scores well.',
    'Then the business asks: is the task done, are users happy, and what does each interaction cost?'],
  svg:
    [[14, 118, 'human review'], [140, 104, 'benchmark'], [252, 150, 'LLM-as-a-judge']]
      .map(([x, w, s], i) => tag(x, 16, w, 30, s, 'bx m', 'lb m', 0, i * 0.2)).join('') +
    [['ROUGE', 'covers it?', 'summaries', 4], ['BLEU', 'matches it?', 'translation', 3]].map(([n, q, u, k], r) => {
      const y = 86 + r * 46, t = r + 1;
      return txt(14, y + 5, n, 'lb', t) +
        [0, 1, 2, 3, 4].map((j) => box(110 + j * 20, y - 8, 16, 16, j < k ? 'bx m' : 'bx', t, 0.2 + j * 0.08, 3)).join('') +
        txt(222, y + 5, q, '', t, 0.6) + txt(430, y + 5, u, 'end lb m', t, 0.8);
    }).join('') +
    txt(14, 183, 'BERTScore', 'lb', 3) + dot(124, 178, 7, 'dot m g', 3, 0.2) + dot(142, 182, 7, 'dot m g', 3, 0.3) +
    txt(222, 183, 'same meaning?', '', 3, 0.5) + txt(430, 183, 'paraphrases', 'end lb m', 3, 0.7) +
    [[14, 102, 'task done?'], [124, 116, 'users happy?'], [248, 124, 'cost per chat?']]
      .map(([x, w, s], i) => tag(x, 218, w, 30, s, 'bx', '', 4, i * 0.2)).join('') },


};
