# selenium_fallback.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def render_page_get_source(url, wait=5, headless=True):
    opts = Options()
    if headless:
        opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    prefs = {"profile.managed_default_content_settings.images": 2}
    opts.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=opts)
    try:
        driver.get(url)
        time.sleep(wait)
        html = driver.page_source
        current_url = driver.current_url
        return html, current_url
    finally:
        try:
            driver.quit()
        except:
            pass
