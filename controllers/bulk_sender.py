import time
import pandas as pd

from config.settings import (
    DEFAULT_MESSAGE_TEMPLATE,
    SLEEP_BETWEEN_MESSAGES_SEC,
    BATCH_SIZE_BEFORE_BREAK,
    BATCH_BREAK_SEC,
    DRY_RUN,
    START_FROM_INDEX,
    MAX_TO_SEND
)

from utils.loader import load_contacts
from services.whatsapp_driver import init_driver, wait_for_login, open_chat
from services.message_sender import type_message, click_send, bounded_sleep
from services.attachment_sender import attach_and_send


def run_bulk_sender():
    contacts_path = "data/contacts.csv"
    out_log = []

    df = load_contacts(contacts_path)
    total = len(df)
    print(f"Loaded {total} contacts.")

    start = max(0, START_FROM_INDEX)
    end = total if MAX_TO_SEND is None else min(total, start + MAX_TO_SEND)
    chunk = df.iloc[start:end].copy()

    driver = init_driver()
    driver.get("https://web.whatsapp.com")
    print("Please scan the QR code in the browser...")
    wait_for_login(driver)
    print("Logged in.")

    sent_count = 0

    for idx, row in chunk.iterrows():
        name = row.get("name", "").strip()
        phone = row.get("phone", "").strip()

        message = row.get("message", "").strip() or DEFAULT_MESSAGE_TEMPLATE
        message = message.replace("{name}", name or "there")

        attachment = row.get("attachment", "").strip()

        # Open chat
        msg_box = open_chat(driver, phone)
        if msg_box is None:
            print(f"[FAIL] Could not open chat for {phone}")
            out_log.append({"name": name, "phone": phone, "status": "failed_open_chat"})
            continue

        # ==============================
        #   CASE 1: ATTACHMENT + TEXT 
        # ==============================
        if attachment:
            if DRY_RUN:
                print(f"[DRY RUN] Would send attachment + message to {phone}")
                out_log.append({"name": name, "phone": phone, "status": "dry_run"})
                bounded_sleep(*SLEEP_BETWEEN_MESSAGES_SEC)
                continue

            # STEP 1 — Send attachment WITHOUT caption
            ok = attach_and_send(driver, attachment)

            if ok:
                print(f"[OK] Sent attachment to {phone}")

                # STEP 2 — Now send the message normally after the file
                try:
                    # Re-find message box (DOM changes after sending file)
                    from selenium.webdriver.support.ui import WebDriverWait
                    from selenium.webdriver.support import expected_conditions as EC
                    from selenium.webdriver.common.by import By

                    msg_box = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located(
                            (By.XPATH, "//div[@contenteditable='true' and @data-tab='10']")
                        )
                    )

                    type_message(msg_box, message)

                    if click_send(driver):
                        print(f"[OK] Sent message to {phone}")
                        out_log.append({"name": name, "phone": phone, "status": "sent"})
                        sent_count += 1
                    else:
                        print(f"[FAIL] Could not send message to {phone}")
                        out_log.append({"name": name, "phone": phone, "status": "failed_send"})

                except Exception as e:
                    print(f"[FAIL] Could not type/send text after attachment for {phone}: {e}")
                    out_log.append({"name": name, "phone": phone, "status": "failed_send"})

            else:
                print(f"[FAIL] Could not send attachment to {phone}")
                out_log.append({"name": name, "phone": phone, "status": "failed_send"})

            bounded_sleep(*SLEEP_BETWEEN_MESSAGES_SEC)
            continue  # Move to next contact — IMPORTANT

        # =======================
        #   CASE 2: TEXT ONLY
        # =======================
        try:
            type_message(msg_box, message)
        except Exception:
            print(f"[WARN] Could not type message for {phone}")

        if DRY_RUN:
            print(f"[DRY RUN] Would send message to {phone}")
            out_log.append({"name": name, "phone": phone, "status": "dry_run"})
        else:
            if click_send(driver):
                print(f"[OK] Sent message to {phone}")
                out_log.append({"name": name, "phone": phone, "status": "sent"})
                sent_count += 1
            else:
                print(f"[FAIL] Could not send message to {phone}")
                out_log.append({"name": name, "phone": phone, "status": "failed_send"})

        bounded_sleep(*SLEEP_BETWEEN_MESSAGES_SEC)

        # Batch break
        if sent_count and (sent_count % BATCH_SIZE_BEFORE_BREAK == 0):
            print(f"Taking a {BATCH_BREAK_SEC}s break...")
            time.sleep(BATCH_BREAK_SEC)

    # Save CSV log
    pd.DataFrame(out_log).to_csv("logs/send_log.csv", index=False)
    print("\nDone. Log saved to logs/send_log.csv")
    driver.quit()
