# app.py - Flask backend
from flask import Flask, render_template, request, jsonify, send_file, abort
from scraper_core import fetch_cause_list_page_by_params, extract_and_build_courts_from_rendered_html, find_cause_list_links_for_complex, download_cause_list_pdf
from utils import ensure_dirs, safe_filename
import os

ensure_dirs()
app = Flask(__name__, static_folder="static", template_folder="templates")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/listing_page", methods=["POST"])
def listing_page():
    payload = request.json or {}
    state = payload.get("state", "")
    district = payload.get("district", "")
    court_complex = payload.get("court_complex", "")
    date_str = payload.get("date", "")
    html, url = fetch_cause_list_page_by_params(state, district, court_complex, "", date_str)
    if not html:
        return jsonify({"ok": False, "error": "Could not load cause_list page."}), 500
    parsed = extract_and_build_courts_from_rendered_html(html)
    links = find_cause_list_links_for_complex(html, court_complex or district or state, date_str)
    return jsonify({"ok": True, "parsed_selects": parsed, "candidates": links, "source_url": url})

@app.route("/api/download", methods=["POST"])
def api_download():
    payload = request.json or {}
    state = payload.get("state", "")
    district = payload.get("district", "")
    court_complex = payload.get("court_complex", "")
    court_name = payload.get("court_name", "")
    date_str = payload.get("date", "")
    all_judges = payload.get("all_judges", False)
    html, url = fetch_cause_list_page_by_params(state, district, court_complex, court_name, date_str)
    if not html:
        return jsonify({"ok": False, "error": "Failed to load source page."}), 500
    candidates = find_cause_list_links_for_complex(html, court_complex or court_name or district, date_str)
    if not candidates:
        return jsonify({"ok": False, "error": "No cause list links detected."}), 404
    chosen = []
    if all_judges:
        chosen = candidates
    else:
        if court_name:
            for c in candidates:
                if court_name.lower() in c['title']:
                    chosen.append(c)
        if not chosen:
            chosen = candidates[:1]
    results = []
    for c in chosen:
        title = c.get("title")[:100]
        url_c = c.get("url")
        local = download_cause_list_pdf(url_c, out_filename = f"{court_complex}_{title}_{date_str}"[:120])
        if local:
            results.append({"title": title, "file": local})
    if not results:
        return jsonify({"ok": False, "error": "Failed to download any PDFs."}), 500
    return jsonify({"ok": True, "files": [{"title": r['title'], "path": r['file']} for r in results]})

@app.route("/download_file")
def download_file():
    path = request.args.get("path")
    if not path or not os.path.exists(path):
        abort(404)
    return send_file(path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
