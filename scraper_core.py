# scraper_core.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pdfkit
import os
import logging
from utils import ensure_dirs, safe_filename
from selenium_fallback import render_page_get_source

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ECOURTS_CAUSELIST_BASE = "https://services.ecourts.gov.in/ecourtindia_v6/?p=cause_list/"
DCOURTS_SAMPLE = "https://newdelhi.dcourts.gov.in/cause-list-%e2%81%84-daily-board/"

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; eCourtsScraper/1.0)"}

def fetch_cause_list_page_by_params(state, district, court_complex, court_name, date_str):
    ensure_dirs()
    try:
        r = requests.get(ECOURTS_CAUSELIST_BASE, headers=HEADERS, timeout=15)
        if r.status_code == 200 and ("cause_list" in r.text.lower() or "cause list" in r.text.lower()):
            return r.text, r.url
    except Exception as e:
        logger.debug("requests fetch failed: %s", e)
    try:
        html, final_url = render_page_get_source(ECOURTS_CAUSELIST_BASE, wait=4, headless=True)
        return html, final_url
    except Exception as e:
        logger.exception("selenium fallback failed: %s", e)
        return None, None

def extract_and_build_courts_from_rendered_html(html):
    soup = BeautifulSoup(html, "lxml")
    data = {}
    selects = soup.find_all("select")
    if selects:
        out = {}
        for sel in selects:
            sid = sel.get("id") or sel.get("name") or "select"
            out[sid] = [opt.get_text(strip=True) for opt in sel.find_all("option") if opt.get("value")]
        return out
    scripts = soup.find_all("script")
    for s in scripts:
        txt = s.string
        if not txt:
            continue
        if "state" in txt.lower() and "district" in txt.lower():
            return {"script_data": txt[:4000]}
    return {}

def find_cause_list_links_for_complex(rendered_html, complex_name, date_str):
    soup = BeautifulSoup(rendered_html, "lxml")
    anchors = soup.find_all("a", href=True)
    matches = []
    for a in anchors:
        txt = a.get_text(" ", strip=True).lower()
        href = a['href']
        if complex_name and (complex_name.lower() in txt or complex_name.lower() in href.lower() or date_str in txt):
            url = href
            if url.startswith("/"):
                url = urljoin("https://services.ecourts.gov.in", url)
            matches.append((txt, url))
    seen = set()
    out = []
    for t,u in matches:
        if u not in seen:
            seen.add(u)
            out.append({"title": t, "url": u})
    return out

def html_to_pdf(html_content, out_path):
    ensure_dirs()
    options = { 'enable-local-file-access': None }
    try:
        pdfkit.from_string(html_content, out_path, options=options)
        return out_path
    except Exception as e:
        logger.exception("pdfkit failed: %s", e)
        return None

def download_cause_list_pdf(url, out_filename=None):
    ensure_dirs()
    try:
        resp = requests.get(url, headers=HEADERS, timeout=20, stream=True)
        ctype = resp.headers.get("Content-Type", "").lower()
        if "application/pdf" in ctype or url.lower().endswith(".pdf"):
            if not out_filename:
                out_filename = url.split("/")[-1] or "causelist.pdf"
            out_filename = safe_filename(out_filename)
            local_path = os.path.join("downloads", out_filename)
            with open(local_path, "wb") as f:
                for chunk in resp.iter_content(8192):
                    if chunk:
                        f.write(chunk)
            return local_path
        else:
            html = resp.text
            if not html or len(html.strip()) < 20:
                html, _ = render_page_get_source(url, wait=4, headless=True)
            if not html:
                return None
            if not out_filename:
                out_filename = url.split("/")[-1] or "causelist"
            out_filename = safe_filename(out_filename)
            out_path = os.path.join("downloads", out_filename + ".pdf")
            ok = html_to_pdf(html, out_path)
            return ok
    except Exception as e:
        logger.exception("download_cause_list_pdf failed: %s", e)
        return None
