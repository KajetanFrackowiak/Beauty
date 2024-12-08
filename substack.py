import os
import time
from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from dotenv import load_dotenv

load_dotenv()

SUBSTACK_EMAIL = os.getenv("SUBSTACK_EMAIL")
SUBSTACK_PASSWORD = os.getenv("SUBSTACK_PASSWORD")

class CustomChrome(uc.Chrome):
    def quit(self):
        time.sleep(0.1)
        super().quit()

def read_summary_from_file(filename):
    with open(filename, "r", encoding="utf-8") as file:
        content = file.read().strip().split("\n")
        summary = content[1].replace("Summary: ", "")
    return summary


def post_from_summary_substack():
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://substack.com/home?utm_source=user-menu")

        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Sign in')]"))
        ).click()

        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'or sign in with password')]"))
        ).click()

        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.NAME, "email"))
        )
        input_email = driver.find_element(By.NAME, "email")
        input_email.send_keys(SUBSTACK_EMAIL)

        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.NAME, "password"))
        )
        input_password = driver.find_element(By.NAME, "password")
        input_password.send_keys(SUBSTACK_PASSWORD)

        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button[type='submit']"))
        ).click()

        summaries_files = [
            "substack_summaries_en.txt",
            "substack_summaries_es.txt",
            "substack_summaries_pl.txt",
            "substack_summaries_tr.txt"
        ]

        for file in summaries_files:
            summary = read_summary_from_file(file)

            time.sleep(5)

            # Wait for the editor to become editable
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,
                                                "div.pencraft.pc-display-flex.pc-flexDirection-column.pc-reset._textEditor_1a1ni_1 div._editorContent_1a1ni_37 div.tiptap.ProseMirror._feedCommentBodyInner_1jaic_266"))
            ).click()

            # Enter the article content into the editor
            time.sleep(2)
            input_post = driver.find_element(By.CSS_SELECTOR,
                                             "div.pencraft.pc-display-flex.pc-flexDirection-column.pc-reset._textEditor_1a1ni_1 div._editorContent_1a1ni_37 div.tiptap.ProseMirror._feedCommentBodyInner_1jaic_266")
            input_post.send_keys(summary)

            # Wait for the Post button to be clickable and post the article
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//button[text()='Post']"))
            ).click()
    finally:
        driver.quit()