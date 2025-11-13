import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# def init_driver():
#     chrome_opts = Options()
#     chrome_opts.add_argument("--start-maximized")
#     driver = webdriver.Chrome(options=chrome_opts)
#     return driver

def init_driver():
    chrome_opts = Options()
    chrome_opts.add_argument("--disable-blink-features=AutomationControlled")
    chrome_opts.add_argument("--disable-popup-blocking")
    chrome_opts.add_argument("--no-sandbox")
    chrome_opts.add_argument("--disable-dev-shm-usage")
    chrome_opts.add_argument("--disable-gpu")
    chrome_opts.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=chrome_opts)
    return driver


def wait_for_login(driver, timeout=300):
    wait = WebDriverWait(driver, timeout)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='textbox']")))
    return True

def open_chat(driver, phone: str, wait_timeout=45):
    url = f"https://web.whatsapp.com/send/?phone={phone}&text&app_absent=0"
    driver.get(url)
    wait = WebDriverWait(driver, wait_timeout)
    try:
        msg_box = wait.until(
            EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true' and @data-tab='10']"))
        )
        return msg_box
    except Exception:
        return None
