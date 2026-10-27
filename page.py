"""The whole frontend: one HTML page with plain JavaScript. Kept in a Python string so Vercel always finds it."""

PAGE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Rubric-Based Assessment Agent</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,700&family=Nunito+Sans:wght@400;600;700&family=Caveat:wght@600&display=swap" rel="stylesheet">
<style>
  :root { --bg:#f7f3ea; --card:#fffdf8; --ink:#1f2a37; --muted:#667085; --line:#e6dfd0;
          --board:#1f3b34; --board2:#2a4d44; --chalk:#f3efe4;
          --accent:#0f766e; --accent-soft:#e3f2ef; --ok:#16794a; --warn:#b45309; --bad:#b42318; --soft:#efe9dc;
          --amber:#d97706; --amber-soft:#fff4e0; }
  * { box-sizing:border-box; }
  body { margin:0; font-family:"Nunito Sans", system-ui, -apple-system, "Segoe UI", sans-serif; background:var(--bg); color:var(--ink); line-height:1.5; font-size:15px; }
  h1, h2, h3 { font-family:"Fraunces", Georgia, serif; font-weight:700; letter-spacing:-0.01em; }

  /* chalkboard header */
  header { background: radial-gradient(1200px 300px at 20% -20%, var(--board2), var(--board)); color:var(--chalk); padding:28px 16px 22px; border-bottom:6px solid #8b5e34; }
  .hero { max-width:1000px; margin:0 auto; display:flex; gap:24px; align-items:center; flex-wrap:wrap; }
  .hero svg { flex:0 0 auto; width:96px; height:96px; }
  .hero-text { flex:1 1 420px; }
  header h1 { margin:0; font-size:30px; line-height:1.15; }
  header .tag { font-family:"Caveat", cursive; font-size:24px; color:#ffd88a; margin:2px 0 6px; }
  header p { margin:0; color:#d6e2dc; font-size:15px; max-width:640px; }
  .how { max-width:1000px; margin:18px auto 0; display:grid; grid-template-columns:repeat(auto-fit, minmax(200px,1fr)); gap:10px; }
  .how div { background:rgba(255,255,255,.07); border:1px dashed rgba(243,239,228,.35); border-radius:10px; padding:10px 12px; font-size:14px; color:#e9efe9; }
  .how b { display:block; font-family:"Fraunces", serif; font-size:16px; color:#fff; }

  main { max-width:1000px; margin:0 auto; padding:20px 16px 40px; }
  .card { background:var(--card); border:1px solid var(--line); border-radius:14px; padding:20px; margin-bottom:18px; box-shadow:0 1px 0 rgba(31,42,55,.04), 0 6px 18px rgba(31,42,55,.04); }
  .card h2 { margin:0 0 6px; font-size:21px; display:flex; align-items:center; gap:10px; }
  .step { display:inline-grid; place-items:center; width:30px; height:30px; background:var(--accent); color:#fff; border-radius:50%; font-family:"Nunito Sans", sans-serif; font-size:15px; font-weight:700; }
  .hint { color:var(--muted); font-size:14px; margin:0 0 12px; }
  .learn { background:var(--accent-soft); border-left:4px solid var(--accent); border-radius:8px; padding:10px 14px; margin:0 0 14px; font-size:14px; }
  .learn b { color:var(--accent); }
  textarea, input[type=text], input[type=number] { width:100%; border:1px solid var(--line); border-radius:8px; padding:9px 10px; font:inherit; font-size:14px; background:#fff; }
  textarea:focus, input:focus { outline:2px solid var(--accent-soft); border-color:var(--accent); }
  textarea { min-height:90px; }
  input[type=number] { width:90px; }
  button { background:var(--accent); color:#fff; border:0; border-radius:8px; padding:9px 16px; font:inherit; font-size:14px; font-weight:700; cursor:pointer; margin:4px 6px 4px 0; transition:transform .05s, filter .15s; }
  button:hover { filter:brightness(1.08); } button:active { transform:translateY(1px); }
  button.secondary { background:#fff; color:var(--accent); border:1.5px solid var(--accent); }
  button.override { background:var(--amber); }
  button:disabled { opacity:.45; cursor:not-allowed; }
  .tabs button { background:#fff; color:var(--ink); border:1.5px solid var(--line); }
  .tabs button.active { background:var(--ink); color:#fff; border-color:var(--ink); }
  .row { display:flex; gap:14px; flex-wrap:wrap; }
  .row > div { flex:1 1 300px; }
  .doc { border:1px solid var(--line); border-radius:10px; padding:12px 14px; margin:10px 0; background:#fff; }
  .doc .meta { font-size:13px; color:var(--muted); margin-bottom:6px; }
  .doc pre { white-space:pre-wrap; margin:0; font:inherit; font-size:14px; }
  .doc img { max-width:220px; border:1px solid var(--line); border-radius:6px; float:right; margin-left:10px; }
  .pill { display:inline-block; font-size:12px; font-weight:600; border-radius:999px; padding:2px 9px; margin-right:4px; background:var(--soft); }
  .pill.warn { background:#fff1dc; color:var(--warn); }
  .pill.ok { background:#e3f4ea; color:var(--ok); }
  .pill.bad { background:#fde7e5; color:var(--bad); }
  .pill.amber { background:var(--amber-soft); color:var(--amber); border:1px solid #f5c77e; }
  .msg { padding:11px 14px; border-radius:8px; margin:8px 0; font-size:14px; }
  .msg.ok { background:#e3f4ea; } .msg.warn { background:#fff1dc; } .msg.bad { background:#fde7e5; }
  .msg.amber { background:var(--amber-soft); border-left:4px solid var(--amber); }
  table { border-collapse:collapse; width:100%; font-size:14px; }
  th { font-size:12px; text-transform:uppercase; letter-spacing:.04em; color:var(--muted); }
  th, td { border-bottom:1px solid var(--line); padding:8px 6px; text-align:left; vertical-align:top; }
  tr.ovr td { background:var(--amber-soft); }
  details summary { cursor:pointer; color:var(--accent); font-size:14px; font-weight:600; margin-top:8px; }
  .approved { border-color:#9fd3b5; background:#f4fbf7; }
  .overridden { border:2px solid var(--amber); background:#fffaf0; }
  .hidden { display:none; }
  .stats { display:flex; gap:10px; flex-wrap:wrap; margin:0 0 10px; }
  .stat { background:#fff; border:1px solid var(--line); border-radius:10px; padding:8px 14px; font-size:13px; color:var(--muted); }
  .stat b { display:block; font-size:20px; color:var(--ink); font-family:"Fraunces", serif; }
  .stat.amber b { color:var(--amber); }
  footer { position:sticky; bottom:0; background:rgba(255,253,248,.96); backdrop-filter:blur(4px); border-top:1px solid var(--line); padding:8px 16px; font-size:13px; color:var(--muted); }
  label.inline { font-size:14px; display:inline-flex; align-items:center; gap:6px; }
  .spinner { display:inline-block; width:12px; height:12px; border:2px solid var(--line); border-top-color:var(--accent); border-radius:50%; animation:spin 1s linear infinite; vertical-align:middle; }
  @keyframes spin { to { transform:rotate(360deg); } }
  .about { font-size:14px; }
  .about ul { margin:6px 0 0 18px; padding:0; }
  @media (max-width:600px) { header h1 { font-size:24px; } .hero svg { width:64px; height:64px; } }
</style>
</head>
<body>
<header>
  <div class="hero">
    <svg viewBox="0 0 96 96" aria-hidden="true">
      <rect x="6" y="20" width="40" height="56" rx="4" fill="#f3efe4"/>
      <rect x="50" y="20" width="40" height="56" rx="4" fill="#e9e2d0"/>
      <path d="M46 22 v54 M50 22 v54" stroke="#8b5e34" stroke-width="3"/>
      <g stroke="#9aa6a0" stroke-width="2"><path d="M13 34h26M13 42h26M13 50h20M57 34h26M57 42h26M57 50h18"/></g>
      <circle cx="70" cy="64" r="13" fill="#0f766e"/>
      <path d="M63 64l5 5 9-10" fill="none" stroke="#fff" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="M16 70 L34 52 l5 5 -18 18 -7 2z" fill="#ffd88a" stroke="#8b5e34" stroke-width="1.5"/>
    </svg>
    <div class="hero-text">
      <h1>Rubric-Based Assessment Agent</h1>
      <div class="tag">Mark fairly. Mark faster. Keep the teacher in charge.</div>
      <p>An AI assistant that learns how <i>you</i> apply a rubric, then suggests marks and feedback for the rest of the class, while you approve every single mark. Works for exam scripts (typed or handwritten) and for resume screening. Demo uses synthetic data only.</p>
    </div>
  </div>
  <div class="how">
    <div><b>1 &middot; You mark first</b>A random 15% of the papers, with short comments.</div>
    <div><b>2 &middot; Agent learns</b>It turns your marking into Do's &amp; Don'ts and tests itself.</div>
    <div><b>3 &middot; Agent suggests</b>Marks each remaining paper 3 times and flags doubts.</div>
    <div><b>4 &middot; You decide</b>Confirm or override every mark. Overrides are highlighted.</div>
  </div>
</header>
<main>

<!-- STEP 0: choose use case -->
<div class="card">
  <h2><span class="step">0</span>Choose a use case</h2>
  <div class="tabs">
    <button id="tab-exam" class="active" onclick="setMode('exam')">Exam grading</button>
    <button id="tab-resume" onclick="setMode('resume')">Resume screening</button>
  </div>
  <p class="hint" id="health"></p>
  <details class="about"><summary>Why rubric-based marking with a human in the loop?</summary>
    <ul>
      <li><b>Consistency (inter-rater reliability):</b> two examiners often give different marks to the same answer. A shared rubric and comment bank make marking more uniform across sections.</li>
      <li><b>Assessment for learning:</b> specific, criterion-linked feedback helps students improve more than a bare number.</li>
      <li><b>Teacher time:</b> the agent does the first pass; the teacher reviews instead of marking from scratch.</li>
      <li><b>Accountability:</b> AI only suggests. Every final mark is confirmed by a teacher, and every override is recorded.</li>
    </ul>
  </details>
</div>

<!-- STEP 1: task + rubric -->
<div class="card">
  <h2><span class="step">1</span>Task and rubric</h2>
  <p class="hint">Paste the question paper (or job description) and the rubric, or load the demo set.</p>
  <div class="learn"><b>Tip from assessment practice:</b> a good rubric names each criterion, the marks for it, and what a full, partial and zero answer looks like. The comment bank below is where you write that down.</div>
  <button class="secondary" onclick="loadDemo()">Load demo data</button>
  <div class="row">
    <div><b id="task-label">Question paper</b><textarea id="task"></textarea></div>
    <div><b>Rubric</b><textarea id="rubric"></textarea></div>
  </div>
  <b>Comment bank</b> <span class="hint">- your standard comments: what earns or loses marks, common mistakes, and feedback you usually write. The agent learns from this and reuses the wording.</span>
  <textarea id="bank" style="min-height:160px" placeholder="C1 - 2 marks: ...&#10;Common mistake: ...&#10;Feedback: ..."></textarea>
  <div style="margin-top:6px">
    <button class="secondary" onclick="saveSetup()">Save setup to a file</button>
    <label class="inline">Load setup file: <input type="file" accept=".json" onchange="loadSetup(this.files[0])"></label>
  </div>
</div>

<!-- STEP 2: documents -->
<div class="card">
  <h2><span class="step">2</span>Add documents</h2>
  <p class="hint">Typed text, a scanned image (handwriting), or a PDF/TXT file. Personal details are removed before anything is sent to the AI model.</p>
  <textarea id="newtext" placeholder="Paste one answer / resume here"></textarea>
  <button onclick="addTyped()">Add typed document</button>
  <div style="margin-top:8px">
    <label class="inline">Scans: <input type="file" id="imgs" accept="image/*" multiple onchange="uploadImages(this.files)"></label>
    <label class="inline">Hide top <input type="number" id="maskpct" value="12" min="0" max="40">% of each scan (name/roll no. area)</label>
  </div>
  <div style="margin-top:6px"><label class="inline">PDF / TXT: <input type="file" id="files" accept=".pdf,.txt" multiple onchange="uploadFiles(this.files)"></label></div>
  <details open><summary id="doccount">Documents</summary><div id="docs"></div></details>
</div>

<!-- STEP 3: reviewer scores sample -->
<div class="card">
  <h2><span class="step">3</span>Reviewer scores a random 15% sample</h2>
  <p class="hint">You assess these first. The agent learns how you apply the rubric from your scores and comments.</p>
  <div class="learn"><b>Like moderation:</b> exam boards ask markers to mark a few "standardisation" scripts first. Write comments that name the criterion and the reason, e.g. <i>"C3 = 0: no link to Grade 3"</i>.</div>
  <button onclick="pickSample()">Pick random sample</button>
  <div id="sample"></div>
  <button id="learnbtn" class="hidden" onclick="learn()">Agent: learn my rules</button>
</div>

<!-- STEP 4: rules -->
<div class="card">
  <h2><span class="step">4</span>Approve the learned rules</h2>
  <p class="hint">The agent drafts Do's and Don'ts from your scoring and tests itself on sample documents it did not learn from.</p>
  <div id="learnout"></div>
  <div id="rulesbox" class="hidden">
    <textarea id="rules" style="min-height:140px"></textarea>
    <label class="inline"><input type="checkbox" id="approverules" onchange="document.getElementById('scorebtn').disabled=!this.checked"> <span id="approvelabel">I have checked these rules and approve them</span></label><br>
    <button id="scorebtn" disabled onclick="scoreRest()">Agent: score the remaining documents</button>
  </div>
</div>

<!-- STEP 5: review queue -->
<div class="card">
  <h2><span class="step">5</span>Review and approve</h2>
  <p class="hint">Every score needs your approval. Flagged items must be opened before they can be approved. There is no "approve all".</p>
  <div class="learn"><b>To disagree:</b> type your own mark in <i>Final score</i>, give a short reason, and click <i>Override &amp; approve</i>. Overridden papers are highlighted in amber here and in the results.</div>
  <div id="queuestats" class="stats"></div>
  <div id="queue"></div>
</div>

<!-- STEP 6: results -->
<div class="card">
  <h2><span class="step">6</span>Results and cost</h2>
  <div id="results"></div>
  <button class="secondary" onclick="downloadCSV()">Download results (CSV)</button>
</div>
</main>
<footer id="usage">AI calls: 0 &middot; tokens in 0 / out 0 &middot; estimated cost $0.0000</footer>

<script>
const S = { mode:'exam', docs:[], sample:[], reviewer:{}, learned:null, results:{}, usage:{in:0,out:0,calls:0,cost:0} };
const $ = id => document.getElementById(id);
const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));

async function api(path, body, isForm) {
  const opts = body ? { method:'POST', body: isForm ? body : JSON.stringify(body),
                        headers: isForm ? {} : {'Content-Type':'application/json'} } : {};
  const r = await fetch(path, opts);
  let data; try { data = await r.json(); } catch { throw new Error('Server error (' + r.status + ')'); }
  if (!r.ok) throw new Error(data.error || data.detail || ('Error ' + r.status));
  if (data.usage) addUsage(data.usage, data.cost_usd || 0);
  return data;
}
function addUsage(u, cost) {
  S.usage.in += u.input_tokens||0; S.usage.out += u.output_tokens||0; S.usage.calls += u.calls||1; S.usage.cost += cost;
  $('usage').innerHTML = `AI calls: ${S.usage.calls} &middot; tokens in ${S.usage.in.toLocaleString()} / out ${S.usage.out.toLocaleString()} &middot; estimated cost $${S.usage.cost.toFixed(4)}`;
}

function setMode(m) {
  S.mode = m; S.docs = []; S.sample = []; S.reviewer = {}; S.learned = null; S.results = {};
  $('tab-exam').classList.toggle('active', m==='exam'); $('tab-resume').classList.toggle('active', m==='resume');
  $('task-label').textContent = m==='exam' ? 'Question paper' : 'Job description';
  $('task').value = ''; $('rubric').value = ''; $('bank').value = '';
  restore();
  ['sample','learnout','queue','results','queuestats'].forEach(id => $(id).innerHTML='');
  $('rulesbox').classList.add('hidden'); $('learnbtn').classList.add('hidden');
  renderDocs();
}

async function loadDemo() {
  const d = await api('/api/demo/' + S.mode);
  $('task').value = d.task; $('rubric').value = d.rubric; $('bank').value = d.bank || '';
  S.docs = d.documents; renderDocs(); autosave();
}

async function addTyped() {
  const t = $('newtext').value.trim(); if (!t) return;
  const r = await api('/api/redact', {text:t});
  S.docs.push({ id: nextId(), text: r.text, redacted: r.redacted, source:'typed' });
  $('newtext').value=''; renderDocs();
}
function nextId() { return (S.mode==='exam'?'S':'R') + String(S.docs.length+1).padStart(2,'0') + 'x'; }

// shrink the image and paint over the top band (name / roll number) BEFORE upload
function prepImage(file, maskPct) {
  return new Promise((res, rej) => {
    const img = new Image(); const url = URL.createObjectURL(file);
    img.onload = () => {
      const scale = Math.min(1, 1600 / Math.max(img.width, img.height));
      const c = document.createElement('canvas'); c.width = img.width*scale; c.height = img.height*scale;
      const g = c.getContext('2d'); g.drawImage(img, 0, 0, c.width, c.height);
      g.fillStyle = '#000'; g.fillRect(0, 0, c.width, c.height*maskPct/100);
      res(c.toDataURL('image/jpeg', 0.8));
    };
    img.onerror = rej; img.src = url;
  });
}
async function uploadImages(files) {
  for (const f of files) {
    const id = nextId();
    const doc = { id, text:'', source:'scan', pending:true }; S.docs.push(doc); renderDocs();
    try {
      const dataUrl = await prepImage(f, +$('maskpct').value || 0);
      doc.image = dataUrl;
      const r = await api('/api/transcribe', { image_b64: dataUrl.split(',')[1], media_type:'image/jpeg' });
      Object.assign(doc, { text:r.text, legibility:r.legibility, route:r.route, redacted:r.redacted, pending:false });
    } catch(e) { doc.pending=false; doc.error = e.message; }
    renderDocs();
  }
  $('imgs').value='';
}
async function uploadFiles(files) {
  for (const f of files) {
    const fd = new FormData(); fd.append('file', f);
    try { const r = await api('/api/extract', fd, true);
          S.docs.push({ id: nextId(), text:r.text, redacted:r.redacted, source:'file: '+f.name }); }
    catch(e) { alert(f.name + ': ' + e.message); }
  }
  $('files').value=''; renderDocs();
}
function removeDoc(id) { S.docs = S.docs.filter(d => d.id!==id); renderDocs(); }

function docHTML(d, extra='', editable=false) {
  const pills = [];
  if (d.label) pills.push(`<span class="pill">${esc(d.label)}</span>`);
  if (d.redacted) pills.push(`<span class="pill ok">${d.redacted} personal detail(s) removed</span>`);
  if (d.legibility && d.legibility!=='clear') pills.push(`<span class="pill ${d.legibility==='unreadable'?'bad':'warn'}">handwriting: ${esc(d.legibility)}</span>`);
  if (d.route==='send_to_reviewer') pills.push(`<span class="pill bad">unreadable &rarr; reviewer marks this one by hand</span>`);
  return `<div class="doc" id="doc-${d.id}">${d.image?`<img src="${d.image}" alt="scan">`:''}
    <div class="meta"><b>${esc(d.id)}</b> &middot; ${esc(d.source)} ${pills.join('')}</div>
    ${d.pending?'<span class="spinner"></span> reading handwriting...':''}${d.error?`<div class="msg bad">${esc(d.error)}</div>`:''}
    ${editable ? `<textarea style="min-height:70px" onchange="editDoc('${d.id}', this.value)">${esc(d.text)}</textarea>
      <button class="secondary" onclick="removeDoc('${d.id}')">Remove</button>` : `<pre>${esc(d.text)}</pre>`}${extra}<div style="clear:both"></div></div>`;
}
function editDoc(id, v) { const d = S.docs.find(x => x.id===id); if (d) d.text = v; }
function renderDocs() {
  $('doccount').textContent = `Documents added: ${S.docs.length} (click to show/hide)`;
  $('docs').innerHTML = S.docs.map(d => docHTML(d, '', true) ).join('');
}

// ---------- step 3 ----------
function usable() { return S.docs.filter(d => !d.pending && d.text && d.route!=='send_to_reviewer'); }
function pickSample(extra=0) {
  const pool = usable().filter(d => !S.sample.includes(d.id));
  const want = extra || Math.max(3, Math.ceil(0.15 * usable().length));
  for (let i=pool.length-1; i>0; i--) { const j = Math.floor(Math.random()*(i+1)); [pool[i],pool[j]]=[pool[j],pool[i]]; }
  if (!extra) S.sample = [];
  S.sample.push(...pool.slice(0, want).map(d => d.id));
  renderSample();
}
function renderSample() {
  $('sample').innerHTML = `<p class="hint">${S.sample.length} of ${usable().length} documents chosen at random.</p>` +
    S.sample.map(id => { const d = S.docs.find(x => x.id===id); const r = S.reviewer[id]||{};
      return docHTML(d, `<div class="row" style="margin-top:8px"><div style="flex:0 0 120px">Your score<br><input type="number" step="0.5" id="rs-${id}" value="${r.score??''}"></div>
        <div>Your comment (why this score?)<input type="text" id="rc-${id}" value="${esc(r.comment||'')}"></div></div>`); }).join('');
  $('learnbtn').classList.toggle('hidden', !S.sample.length);
}
function readReviewer() {
  for (const id of S.sample) {
    const v = $('rs-'+id).value; if (v==='') throw new Error('Please give a score for ' + id);
    S.reviewer[id] = { score: +v, comment: $('rc-'+id).value };
  }
}

// ---------- step 4 ----------
async function learn() {
  try { readReviewer(); } catch(e) { alert(e.message); return; }
  $('learnout').innerHTML = '<span class="spinner"></span> learning from your scores and testing itself...';
  try {
    const ex = S.sample.map(id => ({ id, text: S.docs.find(d=>d.id===id).text, score:S.reviewer[id].score, comment:S.reviewer[id].comment }));
    const r = await api('/api/learn', { mode:S.mode, task:$('task').value, rubric:$('rubric').value, examples:ex, bank:$('bank').value });
    S.learned = r;
    let html = `<div class="msg ${r.decision==='ready'?'ok':'warn'}">${esc(r.message)}</div>`;
    if (r.self_test) html += '<table><tr><th>Held-out document</th><th>Your score</th><th>Agent score</th><th></th></tr>' +
      r.self_test.held_out.map(h => `<tr><td>${esc(h.id)}</td><td>${h.reviewer}</td><td>${h.agent}</td><td>${h.agree?'<span class="pill ok">agree</span>':'<span class="pill bad">differs</span>'}</td></tr>`).join('') + '</table>';
    if (r.decision!=='ready') html += `<button onclick="pickSample(2); $('learnout').innerHTML='Score the 2 new sample documents above, then click learn again.'">Add 2 more documents to my sample</button>`;
    if (r.notes) html += `<p class="hint">Agent note: ${esc(r.notes)}</p>`;
    $('learnout').innerHTML = html;
    html += `<button class="secondary" onclick="addRulesToBank()">Add these rules to my comment bank</button>`;
    $('learnout').innerHTML = html;
    $('rules').value = r.rules; $('approverules').checked = false;
    $('approvelabel').textContent = r.decision==='ready' ? 'I have checked these rules and approve them' : 'Continue anyway with these rules (not recommended - the agent asked for more examples)'; $('scorebtn').disabled = true;
    $('rulesbox').classList.remove('hidden');
  } catch(e) { $('learnout').innerHTML = `<div class="msg bad">${esc(e.message)}</div>`; }
}

// ---------- step 5 ----------
async function scoreRest() {
  const todo = usable().filter(d => !S.sample.includes(d.id));
  $('queue').innerHTML = todo.map(d => `<div id="q-${d.id}">${docHTML(d, '<p><span class="spinner"></span> scoring 3 times...</p>')}</div>`).join('');
  const rules = $('rules').value;
  let i = 0;
  async function worker() {
    while (i < todo.length) {
      const d = todo[i++];
      await scoreOne(d, rules);
      if (i < todo.length) await new Promise(r => setTimeout(r, 4000));  // pause: free-tier limit
    }
  }
  await Promise.all([worker()]);   // one at a time: stays inside the free-tier rate limit
}
async function scoreOne(d, rules) {
  try {
    const r = await api('/api/score', { mode:S.mode, task:$('task').value, rubric:$('rubric').value, rules: rules ?? $('rules').value,
                                        text:d.text, legibility:d.legibility||'clear', bank:$('bank').value });
    S.results[d.id] = { ...r, final:r.suggested, approved:false, opened:false };
  } catch(e) { S.results[d.id] = { error:e.message }; }
  renderCard(d.id); renderResults();
}
async function retry(id) {
  $('q-'+id).innerHTML = docHTML(S.docs.find(x => x.id===id), '<p><span class="spinner"></span> scoring 3 times...</p>');
  await scoreOne(S.docs.find(x => x.id===id));
}
function renderCard(id) {
  const d = S.docs.find(x => x.id===id), r = S.results[id];
  if (r.error) { $('q-'+id).innerHTML = docHTML(d, `<div class="msg bad">${esc(r.error)}</div><button onclick="retry('${id}')">Retry</button>`); renderStats(); return; }
  const flagged = r.flags.length > 0;
  const crit = r.criteria.map(c => `<tr><td>${esc(c.criterion)}</td><td>${c.score}/${c.max}</td><td>${esc(c.reason)}<br><i>"${esc(c.evidence)}"</i></td></tr>`).join('');
  const flagsHTML = flagged ? r.flags.map(f => `<span class="pill warn">${esc(f)}</span>`).join('') : '<span class="pill ok">stable across 3 runs</span>';
  const canApprove = !flagged || r.opened;
  const differs = +r.final !== +r.suggested;
  let status = '';
  if (r.approved && r.overridden) status = `<div class="msg amber"><b>Reviewer override:</b> agent ${r.suggested} &rarr; reviewer ${r.final}${r.reason?` &middot; Reason: ${esc(r.reason)}`:''}</div>`;
  else if (r.approved) status = `<div class="msg ok"><b>Approved:</b> agent mark confirmed by reviewer.</div>`;
  $('q-'+id).innerHTML = `<div class="doc ${r.approved ? (r.overridden ? 'overridden' : 'approved') : ''}">${d.image?`<img src="${d.image}" alt="scan">`:''}
    <div class="meta"><b>${esc(id)}</b> ${d.label?`<span class="pill">${esc(d.label)}</span>`:''} ${flagsHTML} ${r.approved && r.overridden ? '<span class="pill amber">overridden</span>' : ''}</div>
    <div>Agent suggests <b>${r.suggested} / ${r.max_total}</b> <span class="hint">(3 separate scoring runs: ${r.runs.join(', ')} - matching numbers mean the agent is confident)</span> &middot; ${esc(r.summary)}</div>
    ${r.feedback ? `<div class="hint" style="margin-top:4px"><b>Feedback for the student:</b> ${esc(r.feedback)}</div>` : ''}
    <details ${r.opened?'open':''} ontoggle="if(this.open){S.results['${id}'].opened=true; refreshApprove('${id}')}">
      <summary>Open: document, reasons per criterion${flagged?' (required before approval)':''}</summary>
      <pre style="margin:8px 0">${esc(d.text)}</pre><table><tr><th>Criterion</th><th>Score</th><th>Reason and evidence</th></tr>${crit}</table>
    </details>
    ${status}
    ${r.approved ? `<button class="secondary" onclick="undo('${id}')">Undo</button>` : `
    <div style="margin-top:10px">Final score <input type="number" step="0.5" id="fs-${id}" value="${r.final}" oninput="onFinal('${id}', this.value)">
      <button id="ap-${id}" class="${differs?'override':''}" ${canApprove?'':'disabled'} onclick="approve('${id}')">${differs?'Override &amp; approve':'Approve'}</button></div>
    <div id="rbox-${id}" class="${differs?'':'hidden'}" style="margin-top:6px"><input type="text" id="rr-${id}" placeholder="Reason for your change (e.g. C3 = 0: no link to Grade 3)" value="${esc(r.reason||'')}" oninput="S.results['${id}'].reason=this.value"></div>`}
    <div style="clear:both"></div></div>`;
  renderStats();
}
function onFinal(id, v) {
  const r = S.results[id]; r.final = v === '' ? r.suggested : +v;
  const differs = +r.final !== +r.suggested, b = $('ap-'+id);
  b.textContent = differs ? 'Override & approve' : 'Approve'; b.className = differs ? 'override' : '';
  $('rbox-'+id).classList.toggle('hidden', !differs);
  renderResults();
}
function refreshApprove(id) { const b = $('ap-'+id); if (b && !S.results[id].approved) b.disabled = false; }
function approve(id) {
  const r = S.results[id]; r.final = +$('fs-'+id).value;
  r.overridden = +r.final !== +r.suggested;
  r.reason = r.overridden ? ($('rr-'+id).value || '').trim() : '';
  if (r.overridden && !r.reason && !confirm('Approve this override without a reason? A reason helps the agent learn.')) return;
  r.approved = true; renderCard(id); renderResults();
}
function undo(id) { const r = S.results[id]; r.approved = false; renderCard(id); renderResults(); }
function renderStats() {
  const vals = Object.values(S.results).filter(r => !r.error);
  if (!vals.length) { $('queuestats').innerHTML=''; return; }
  const appr = vals.filter(r => r.approved).length, ovr = vals.filter(r => r.approved && r.overridden).length, fl = vals.filter(r => r.flags.length).length;
  $('queuestats').innerHTML = `<div class="stat"><b>${appr}/${vals.length}</b>approved</div><div class="stat amber"><b>${ovr}</b>overridden by reviewer</div><div class="stat"><b>${fl}</b>flagged by agent</div>`;
}

// ---------- step 6 ----------
function rows() {
  const out = [];
  for (const id of S.sample) out.push({ id, source:'reviewer sample', reviewer:S.reviewer[id]?.score, runs:'', suggested:'', final:S.reviewer[id]?.score, flags:'', approved:'yes (reviewer)', action:'marked by reviewer', reason:S.reviewer[id]?.comment||'', feedback:'' });
  for (const d of S.docs) { const r = S.results[d.id]; if (!r || r.error) continue;
    out.push({ id:d.id, source:'agent', reviewer:'', runs:r.runs.join('|'), suggested:r.suggested, final:r.final, flags:r.flags.join('; '), approved:r.approved?'yes':'no',
      action: !r.approved ? 'pending' : (r.overridden ? `overridden (${r.suggested} -> ${r.final})` : 'confirmed'), reason:r.reason||'', feedback:r.feedback||'' }); }
  for (const d of S.docs) if (d.route==='send_to_reviewer') out.push({ id:d.id, source:'unreadable - mark by hand', reviewer:'', runs:'', suggested:'', final:'', flags:'unreadable', approved:'no', action:'pending', reason:'', feedback:'' });
  return out;
}
function renderResults() {
  const rs = rows(); if (!rs.length) { $('results').innerHTML=''; return; }
  const agentRows = rs.filter(r => r.source==='agent'), done = agentRows.filter(r => r.approved==='yes').length;
  const changed = agentRows.filter(r => r.approved==='yes' && +r.final !== +r.suggested).length;
  const appr = agentRows.filter(r => r.approved==='yes');
  const exact = appr.filter(r => +r.final === +r.suggested).length, near = appr.filter(r => Math.abs(r.final - r.suggested) <= 1).length;
  let html = appr.length ? `<div class="msg ok"><b>Accuracy on unseen documents (agent vs. your approved mark):</b> exact match ${exact}/${appr.length} (${Math.round(100*exact/appr.length)}%) &middot; within 1 mark ${near}/${appr.length} (${Math.round(100*near/appr.length)}%)</div>` : '';
  html += `<p>${done} of ${agentRows.length} agent scores approved &middot; reviewer changed ${changed} of them &middot; AI cost so far (paid-tier price; free tier = $0): $${S.usage.cost.toFixed(4)}</p>`;
  const ovrRows = rs.filter(r => String(r.action).startsWith('overridden'));
  if (ovrRows.length) html += `<div class="msg amber"><b>${ovrRows.length} paper(s) where the reviewer disagreed with the agent:</b> ${ovrRows.map(r => esc(r.id)).join(', ')} (highlighted below). <button class="secondary" onclick="overridesToBank()">Add override reasons to my comment bank</button></div>`;
  html += `<label class="inline" style="margin:6px 0"><input type="checkbox" id="onlyovr" ${S.onlyOvr?'checked':''} onchange="S.onlyOvr=this.checked; renderResults()"> Show only overridden papers</label>`;
  const shown = S.onlyOvr ? ovrRows : rs;
  html += '<table><tr><th>ID</th><th>Source</th><th>Agent (3 runs)</th><th>Final</th><th>Reviewer action</th><th>Reason / comment</th><th>Flags</th></tr>' +
    shown.map(r => `<tr class="${String(r.action).startsWith('overridden')?'ovr':''}"><td>${esc(r.id)}</td><td>${esc(r.source)}</td><td>${esc(r.runs)}</td><td><b>${esc(r.final)}</b></td><td>${esc(r.action)}</td><td>${esc(r.reason)}</td><td>${esc(r.flags)}</td></tr>`).join('') + '</table>';
  if (S.mode==='resume') {
    const ranked = rs.filter(r => r.approved.startsWith('yes')).sort((a,b) => b.final - a.final).slice(0,5);
    html += `<p><b>Approved shortlist (top 5):</b> ${ranked.map(r => esc(r.id)+' ('+r.final+')').join(', ') || 'approve scores first'}</p>`;
  }
  $('results').innerHTML = html;
}
function downloadCSV() {
  const rs = rows(); if (!rs.length) return;
  const keys = Object.keys(rs[0]);
  const csv = [keys.join(',')].concat(rs.map(r => keys.map(k => '"' + String(r[k] ?? '').replace(/"/g,'""') + '"').join(','))).join('\n');
  const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([csv], {type:'text/csv'}));
  a.download = `results_${S.mode}.csv`; a.click();
}

// ---------- comment bank, save / load ----------
function overridesToBank() {
  const lines = rows().filter(r => String(r.action).startsWith('overridden') && r.reason).map(r => `- ${r.id}: ${r.reason}`);
  if (!lines.length) { alert('No override reasons to add yet.'); return; }
  const b = $('bank'); b.value = (b.value.trim() + '\n\nLessons from my overrides:\n' + lines.join('\n')).trim(); autosave();
  alert('Added ' + lines.length + ' override reason(s) to the comment bank (Step 1).');
}
function addRulesToBank() {
  const b = $('bank'); b.value = (b.value.trim() + '\n\nLearned from my sample (approved):\n' + $('rules').value).trim(); autosave();
}
function setupData() { return { mode:S.mode, task:$('task').value, rubric:$('rubric').value, bank:$('bank').value, rules:$('rules').value }; }
function saveSetup() {
  const a = document.createElement('a');
  a.href = URL.createObjectURL(new Blob([JSON.stringify(setupData(), null, 2)], {type:'application/json'}));
  a.download = `setup_${S.mode}.json`; a.click();
}
async function loadSetup(file) {
  if (!file) return;
  const d = JSON.parse(await file.text());
  if (d.mode && d.mode !== S.mode) setMode(d.mode);
  $('task').value = d.task||''; $('rubric').value = d.rubric||''; $('bank').value = d.bank||''; $('rules').value = d.rules||'';
  autosave();
}
// remember task / rubric / comment bank in this browser (convenience only)
function autosave() { try { localStorage.setItem('setup_'+S.mode, JSON.stringify(setupData())); } catch(e) {} }
function restore() {
  try { const d = JSON.parse(localStorage.getItem('setup_'+S.mode) || 'null');
        if (d) { $('task').value = d.task||''; $('rubric').value = d.rubric||''; $('bank').value = d.bank||''; } } catch(e) {}
}
['task','rubric','bank'].forEach(id => $(id).addEventListener('change', autosave));
restore();

fetch('/api/health').then(r => r.json()).then(h => {
  $('health').textContent = h.key_set ? `Connected to ${h.provider} (${h.model})${h.mock?' - MOCK MODE':''}` : 'AI key is not set on the server yet (add GEMINI_API_KEY in Vercel settings).';
});
</script>
</body>
</html>
"""
