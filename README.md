# 🏛️ eCourts Cause List Downloader

A Flask-based web application that allows users to fetch and download **daily cause lists** of Indian district courts in **real-time** directly from the official [eCourts website](https://services.ecourts.gov.in/ecourtindia_v6/?p=cause_list/).

---

## 🚀 Features

- ✅ Real-time cause list scraping from eCourts portal  
- ✅ Dynamic input for **State**, **District**, **Court Complex**, **Court Name**, and **Date**  
- ✅ Option to download **all judges’ cause lists** in one click  
- ✅ Automatic **PDF generation** using `pdfkit` + `wkhtmltopdf`  
- ✅ Modern UI built with **Bootstrap 5**  
- ✅ Clean and responsive interface  

---

## 🧠 Tech Stack

| Component | Technology Used |
|------------|-----------------|
| Frontend   | HTML, CSS, Bootstrap 5, JavaScript |
| Backend    | Python Flask |
| Web Scraping | BeautifulSoup, Requests, Selenium |
| PDF Conversion | pdfkit + wkhtmltopdf |
| Browser Automation | WebDriver Manager |


---

## ⚙️ Installation & Setup

### 1️⃣ Clone this Repository
```bash
git clone https://github.com/<your-username>/eCourts_CauseList_UI.git
cd eCourts_CauseList_UI
 Create and Activate Virtual Environment
python -m venv venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
venv\Scripts\Activate.ps1

Install wkhtmltopdf

Download and install from 👉 https://wkhtmltopdf.org/downloads.html

Then verify:

wkhtmltopdf --version

Run the Application
python app.py


## 🗂️ Project Structure

