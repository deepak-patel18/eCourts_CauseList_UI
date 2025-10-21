// static/main.js
async function postJson(url, data) {
  const res = await fetch(url, {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify(data)
  });
  return await res.json();
}

document.getElementById('check').onclick = async () => {
  const state = document.getElementById('state').value;
  const district = document.getElementById('district').value;
  const complex = document.getElementById('complex').value;
  const date = document.getElementById('date').value;
  const resDiv = document.getElementById('result');
  resDiv.innerText = 'Loading candidates...';
  const resp = await postJson('/api/listing_page', {state, district, court_complex: complex, date});
  if (!resp.ok) {
    resDiv.innerText = 'Error: ' + (resp.error || 'unknown');
    return;
  }
  let html = '<h4>Candidates</h4>';
  if (resp.candidates && resp.candidates.length) {
    html += '<ul class="list-group">';
    resp.candidates.forEach(c => {
      html += `<li class="list-group-item">${c.title} - <a href="${c.url}" target="_blank">Open</a></li>`;
    });
    html += '</ul>';
  } else {
    html += '<p>No direct links found. Check parsed selects below.</p>';
  }
  html += '<h4 class="mt-3">Parsed Selects / Data (debug)</h4><pre>' + JSON.stringify(resp.parsed_selects, null, 2) + '</pre>';
  resDiv.innerHTML = html;
};

document.getElementById('download').onclick = async () => {
  const state = document.getElementById('state').value;
  const district = document.getElementById('district').value;
  const complex = document.getElementById('complex').value;
  const court_name = document.getElementById('court_name').value;
  const date = document.getElementById('date').value;
  const all_judges = document.getElementById('all_judges').checked;

  const resDiv = document.getElementById('result');
  resDiv.innerText = 'Starting download... (this may take a few seconds)';

  const resp = await postJson('/api/download', {
    state, district, court_complex: complex, court_name, date, all_judges
  });
  if (!resp.ok) {
    resDiv.innerText = 'Error: ' + (resp.error || 'unknown');
    return;
  }
  let html = '<h4>Files</h4><ul class="list-group">';
  resp.files.forEach(f => {
    const url = '/download_file?path=' + encodeURIComponent(f.path);
    html += `<li class="list-group-item">${f.title} - <a href="${url}" target="_blank">Download</a></li>`;
  });
  html += '</ul>';
  resDiv.innerHTML = html;
};
