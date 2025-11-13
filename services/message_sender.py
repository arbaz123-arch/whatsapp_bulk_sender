import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def type_message(msg_box, text: str):
    msg_box.click()
    for line in text.split("\n"):
        msg_box.send_keys(line)
        msg_box.send_keys(Keys.SHIFT, Keys.ENTER)
    msg_box.send_keys(Keys.BACK_SPACE)

def click_send(driver, wait_timeout=20):
    try:
        msg_box = driver.find_element(By.XPATH, "//div[@contenteditable='true' and @data-tab='10']")
        msg_box.send_keys(Keys.ENTER)
        return True
    except Exception as e:
        print("Failed to send message:", e)
        return False

def bounded_sleep(min_sec: int, max_sec: int):
    time.sleep(random.uniform(min_sec, max_sec))
