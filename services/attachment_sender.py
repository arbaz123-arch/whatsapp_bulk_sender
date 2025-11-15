# services/attachment_sender.py
import time
import pathlib
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver

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

        # Wait for the preview to load
        time.sleep(2.0)
        
        # Try multiple selectors for the send button with retries
        for attempt in range(3):
            try:
                print(f"  [DEBUG] Attempt {attempt + 1} to find and click send button")
                
                # Try multiple selectors for the send button
                send_selectors = [
                    "button[aria-label='Send']",
                    "span[data-icon='send']",
                    "div[role='button'][aria-label='Send']",
                    "div[role='button'] span[data-icon='send']",
                    "button[data-testid='media-send']"  # New WhatsApp Web selector
                ]
                
                for selector in send_selectors:
                    try:
                        send_btn = wait.until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                        )
                        # Scroll into view and click using JavaScript for reliability
                        driver.execute_script("arguments[0].scrollIntoView(true);", send_btn)
                        time.sleep(0.5)
                        driver.execute_script("arguments[0].click();", send_btn)
                        print(f"  [DEBUG] Clicked send button with selector: {selector}")
                        time.sleep(1.0)  # Wait for send to complete
                        return True
                    except Exception as e:
                        print(f"  [DEBUG] Failed with selector {selector}: {str(e)[:100]}...")
                        time.sleep(0.5)
                
                # If we get here, none of the selectors worked
                print("  [DEBUG] Trying to press Enter as fallback")
                from selenium.webdriver.common.keys import Keys
                actions = webdriver.ActionChains(driver)

                actions.send_keys(Keys.ENTER).perform()
                time.sleep(1.0)
                return True
                
            except Exception as e:
                print(f"  [DEBUG] Attempt {attempt + 1} failed: {str(e)[:100]}...")
                time.sleep(1.0)
        
        print("  [ERROR] Could not find or click send button after multiple attempts")
        return False

    except Exception as e:
        print("  [FAIL] Attach + send failed:", e)
        return False
