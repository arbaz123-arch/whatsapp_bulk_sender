# services/attachment_sender.py
import time
import pathlib
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def attach_and_send(driver, file_path: str) -> bool:
    try:
        wait = WebDriverWait(driver, 20)
        time.sleep(1.5)  # give UI a moment

        # Prefer the new in-composer "Add file" button
        try:
            attach_btn = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Add file']"))
            )
        except:
            attach_btn = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div[aria-label='Attach']"))
            )

        attach_btn.click()
        time.sleep(0.8)

        file_input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
        )
        file_input.send_keys(str(pathlib.Path(file_path).resolve()))
        time.sleep(1.5)  # allow preview to load

        # Click the Send button for the attached file (new UI prefers button[aria-label='Send'])
        try:
            send_btn = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Send']"))
            )
        except:
            send_btn = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "span[data-icon='send']"))
            )

        send_btn.click()
        time.sleep(1.0)
        return True

    except Exception as e:
        print("  [FAIL] Attach + send failed:", e)
        return False
