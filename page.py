"""The whole frontend: one HTML page with plain JavaScript. Kept in a Python string so Vercel always finds it."""

PAGE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Rubric-Based Assessment Agent</title>
<style>
  :root { --bg:#f6f7f9; --card:#fff; --ink:#1d2330; --muted:#5f6b7a; --line:#dfe3e8;
          --accent:#2f5bd3; --ok:#1f8a4c; --warn:#b26a00; --bad:#b3261e; --soft:#eef2fb; }
  * { box-sizing:border-box; }
  body { margin:0; font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif; background:var(--bg); color:var(--ink); line-height:1.45; }
  header { background:var(--ink); color:#fff; padding:18px 16px; }
  header h1 { margin:0; font-size:20px; }
  header p { margin:4px 0 0; color:#c9d1dc; font-size:14px; }
  main { max-width:980px; margin:0 auto; padding:16px; }
  .card { background:var(--card); border:1px solid var(--line); border-radius:10px; padding:16px; margin-bottom:16px; }
  .card h2 { margin:0 0 4px; font-size:17px; }
  .step { display:inline-block; background:var(--accent); color:#fff; border-radius:12px; padding:0 9px; font-size:13px; margin-right:6px; }
  .hint { color:var(--muted); font-size:13px; margin:0 0 12px; }
  textarea, input[type=text], input[type=number] { width:100%; border:1px solid var(--line); border-radius:6px; padding:8px; font:inherit; font-size:14px; }
  textarea { min-height:90px; }
  input[type=number] { width:90px; }
  button { background:var(--accent); color:#fff; border:0; border-radius:6px; padding:8px 14px; font:inherit; font-size:14px; cursor:pointer; margin:4px 6px 4px 0; }
  button.secondary { background:#fff; color:var(--accent); border:1px solid var(--accent); }
  button:disabled { opacity:.45; cursor:not-allowed; }
  .tabs button { background:#fff; color:var(--ink); border:1px solid var(--line); }
  .tabs button.active { background:var(--accent); color:#fff; border-color:var(--accent); }
  .row { display:flex; gap:12px; flex-wrap:wrap; }
  .row > div { flex:1 1 300px; }
  .doc { border:1px solid var(--line); border-radius:8px; padding:10px; margin:8px 0; background:#fff; }
  .doc .meta { font-size:12px; color:var(--muted); margin-bottom:4px; }
  .doc pre { white-space:pre-wrap; margin:0; font:inherit; font-size:14px; }
  .doc img { max-width:220px; border:1px solid var(--line); border-radius:4px; float:right; margin-left:10px; }
  .pill { display:inline-block; font-size:12px; border-radius:10px; padding:1px 8px; margin-right:4px; background:var(--soft); }
  .pill.warn { background:#fff1dc; color:var(--warn); }
  .pill.ok { background:#e4f4ea; color:var(--ok); }
  .pill.bad { background:#fde7e5; color:var(--bad); }
  .msg { padding:10px; border-radius:6px; margin:8px 0; font-size:14px; }
  .msg.ok { background:#e4f4ea; } .msg.warn { background:#fff1dc; } .msg.bad { background:#fde7e5; }
  table { border-collapse:collapse; width:100%; font-size:14px; }
  th, td { border-bottom:1px solid var(--line); padding:6px; text-align:left; vertical-align:top; }
  details summary { cursor:pointer; color:var(--accent); font-size:14px; margin-top:6px; }
  .approved { border-color:var(--ok); background:#f3fbf6; }
  .hidden { display:none; }
  footer { position:sticky; bottom:0; background:#fff; border-top:1px solid var(--line); padding:8px 16px; font-size:13px; color:var(--muted); }
  label.inline { font-size:14px; display:inline-flex; align-items:center; gap:6px; }
  .spinner { display:inline-block; width:12px; height:12px; border:2px solid var(--line); border-top-color:var(--accent); border-radius:50%; animation:spin 1s linear infinite; vertical-align:middle; }
  @keyframes spin { to { transform:rotate(360deg); } }
</style>
</head>
<body>
<header>
  <h1>Rubric-Based Assessment Agent</h1>
  <p>The reviewer scores a sample first &rarr; the agent learns her rules &rarr; the agent scores the rest &rarr; the reviewer approves every result. Demo uses synthetic data only.</p>
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
</div>

<!-- STEP 1: task + rubric -->
<div class="card">
  <h2><span class="step">1</span>Task and rubric</h2>
  <p class="hint">Paste the question paper (or job description) and the rubric, or load the demo set.</p>
  <button class="secondary" onclick="loadDemo()">Load demo data</button>
  <div class="row">
    <div><b id="task-label">Question paper</b><textarea id="task"></textarea></div>
    <div><b>Rubric</b><textarea id="rubric"></textarea></div>
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
  $('task').value = ''; $('rubric').value = '';
  ['sample','learnout','queue','results'].forEach(id => $(id).innerHTML='');
  $('rulesbox').classList.add('hidden'); $('learnbtn').classList.add('hidden');
  renderDocs();
}

async function loadDemo() {
  const d = await api('/api/demo/' + S.mode);
  $('task').value = d.task; $('rubric').value = d.rubric;
  S.docs = d.documents; renderDocs();
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

function docHTML(d, extra='') {
  const pills = [];
  if (d.label) pills.push(`<span class="pill">${esc(d.label)}</span>`);
  if (d.redacted) pills.push(`<span class="pill ok">${d.redacted} personal detail(s) removed</span>`);
  if (d.legibility && d.legibility!=='clear') pills.push(`<span class="pill ${d.legibility==='unreadable'?'bad':'warn'}">handwriting: ${esc(d.legibility)}</span>`);
  if (d.route==='send_to_reviewer') pills.push(`<span class="pill bad">unreadable &rarr; reviewer marks this one by hand</span>`);
  return `<div class="doc" id="doc-${d.id}">${d.image?`<img src="${d.image}" alt="scan">`:''}
    <div class="meta"><b>${esc(d.id)}</b> &middot; ${esc(d.source)} ${pills.join('')}</div>
    ${d.pending?'<span class="spinner"></span> reading handwriting...':''}${d.error?`<div class="msg bad">${esc(d.error)}</div>`:''}
    <pre>${esc(d.text)}</pre>${extra}<div style="clear:both"></div></div>`;
}
function renderDocs() {
  $('doccount').textContent = `Documents added: ${S.docs.length} (click to show/hide)`;
  $('docs').innerHTML = S.docs.map(d => docHTML(d, `<button class="secondary" onclick="removeDoc('${d.id}')">Remove</button>`)).join('');
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
    const r = await api('/api/learn', { mode:S.mode, task:$('task').value, rubric:$('rubric').value, examples:ex });
    S.learned = r;
    let html = `<div class="msg ${r.decision==='ready'?'ok':'warn'}">${esc(r.message)}</div>`;
    if (r.self_test) html += '<table><tr><th>Held-out document</th><th>Your score</th><th>Agent score</th><th></th></tr>' +
      r.self_test.held_out.map(h => `<tr><td>${esc(h.id)}</td><td>${h.reviewer}</td><td>${h.agent}</td><td>${h.agree?'<span class="pill ok">agree</span>':'<span class="pill bad">differs</span>'}</td></tr>`).join('') + '</table>';
    if (r.decision!=='ready') html += `<button onclick="pickSample(2); $('learnout').innerHTML='Score the 2 new sample documents above, then click learn again.'">Add 2 more documents to my sample</button>`;
    if (r.notes) html += `<p class="hint">Agent note: ${esc(r.notes)}</p>`;
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
      try {
        const r = await api('/api/score', { mode:S.mode, task:$('task').value, rubric:$('rubric').value, rules, text:d.text, legibility:d.legibility||'clear' });
        S.results[d.id] = { ...r, final:r.suggested, approved:false, opened:false };
      } catch(e) { S.results[d.id] = { error:e.message }; }
      renderCard(d.id); renderResults();
    }
  }
  await Promise.all([worker()]);   // one at a time: stays inside the free-tier rate limit
}
function renderCard(id) {
  const d = S.docs.find(x => x.id===id), r = S.results[id];
  if (r.error) { $('q-'+id).innerHTML = docHTML(d, `<div class="msg bad">${esc(r.error)}</div>`); return; }
  const flagged = r.flags.length > 0;
  const crit = r.criteria.map(c => `<tr><td>${esc(c.criterion)}</td><td>${c.score}/${c.max}</td><td>${esc(c.reason)}<br><i>"${esc(c.evidence)}"</i></td></tr>`).join('');
  const flagsHTML = flagged ? r.flags.map(f => `<span class="pill warn">${esc(f)}</span>`).join('') : '<span class="pill ok">stable across 3 runs</span>';
  const canApprove = !flagged || r.opened;
  $('q-'+id).innerHTML = `<div class="doc ${r.approved?'approved':''}">${d.image?`<img src="${d.image}" alt="scan">`:''}
    <div class="meta"><b>${esc(id)}</b> ${d.label?`<span class="pill">${esc(d.label)}</span>`:''} ${flagsHTML}</div>
    <div>Agent suggests <b>${r.suggested} / ${r.max_total}</b> <span class="hint">(runs: ${r.runs.join(', ')})</span> &middot; ${esc(r.summary)}</div>
    <details ${r.opened?'open':''} ontoggle="if(this.open){S.results['${id}'].opened=true; refreshApprove('${id}')}">
      <summary>Open: document, reasons per criterion${flagged?' (required before approval)':''}</summary>
      <pre style="margin:8px 0">${esc(d.text)}</pre><table><tr><th>Criterion</th><th>Score</th><th>Reason and evidence</th></tr>${crit}</table>
    </details>
    <div style="margin-top:8px">Final score <input type="number" step="0.5" id="fs-${id}" value="${r.final}" onchange="S.results['${id}'].final=+this.value; renderResults()" ${r.approved?'disabled':''}>
      <button id="ap-${id}" ${canApprove&&!r.approved?'':'disabled'} onclick="approve('${id}')">${r.approved?'Approved':'Approve'}</button>
      ${r.approved?`<button class="secondary" onclick="S.results['${id}'].approved=false; renderCard('${id}'); renderResults()">Undo</button>`:''}</div>
    <div style="clear:both"></div></div>`;
}
function refreshApprove(id) { const b = $('ap-'+id); if (b && !S.results[id].approved) b.disabled = false; }
function approve(id) { const r = S.results[id]; r.final = +$('fs-'+id).value; r.approved = true; renderCard(id); renderResults(); }

// ---------- step 6 ----------
function rows() {
  const out = [];
  for (const id of S.sample) out.push({ id, source:'reviewer sample', reviewer:S.reviewer[id]?.score, runs:'', suggested:'', final:S.reviewer[id]?.score, flags:'', approved:'yes (reviewer)' });
  for (const d of S.docs) { const r = S.results[d.id]; if (!r || r.error) continue;
    out.push({ id:d.id, source:'agent', reviewer:'', runs:r.runs.join('|'), suggested:r.suggested, final:r.final, flags:r.flags.join('; '), approved:r.approved?'yes':'no' }); }
  for (const d of S.docs) if (d.route==='send_to_reviewer') out.push({ id:d.id, source:'unreadable - mark by hand', reviewer:'', runs:'', suggested:'', final:'', flags:'unreadable', approved:'no' });
  return out;
}
function renderResults() {
  const rs = rows(); if (!rs.length) { $('results').innerHTML=''; return; }
  const agentRows = rs.filter(r => r.source==='agent'), done = agentRows.filter(r => r.approved==='yes').length;
  const changed = agentRows.filter(r => r.approved==='yes' && +r.final !== +r.suggested).length;
  let html = `<p>${done} of ${agentRows.length} agent scores approved &middot; reviewer changed ${changed} of them &middot; AI cost so far (paid-tier price; free tier = $0): $${S.usage.cost.toFixed(4)}</p>`;
  html += '<table><tr><th>ID</th><th>Source</th><th>Agent (3 runs)</th><th>Final</th><th>Approved</th><th>Flags</th></tr>' +
    rs.map(r => `<tr><td>${esc(r.id)}</td><td>${esc(r.source)}</td><td>${esc(r.runs)}</td><td>${esc(r.final)}</td><td>${esc(r.approved)}</td><td>${esc(r.flags)}</td></tr>`).join('') + '</table>';
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

fetch('/api/health').then(r => r.json()).then(h => {
  $('health').textContent = h.key_set ? `Connected to ${h.provider} (${h.model})${h.mock?' - MOCK MODE':''}` : 'AI key is not set on the server yet (add GEMINI_API_KEY in Vercel settings).';
});
</script>
</body>
</html>
"""
