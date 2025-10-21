# eCourts_CauseList_UI
Full project (Requests + Selenium fallback) to fetch cause lists from eCourts and convert to PDF.

## Quick start (Windows + PowerShell)
1. Open PowerShell and `cd` to project folder.
2. Create venv:
   ```powershell
   python -m venv venv
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```
3. Install wkhtmltopdf binary (required for pdfkit):
   - Windows: download installer from https://wkhtmltopdf.org/ and add to PATH.
4. Run the Flask app:
   ```powershell
   python app.py
   ```
5. Open browser at http://127.0.0.1:5000/

## Notes
- Project includes a Selenium fallback in case the site uses JS to render content.
- Update `scraper_core.py` parsing logic if the eCourts DOM changes.
