import os
from dotenv import load_dotenv
from selenium import webdriver
from httpcore import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import undetected_chromedriver as uc
from tiktok_captcha_solver import SeleniumSolver

load_dotenv()

TIKTOK_EMAIL = os.getenv("TIKTOK_EMAIL")
TIKTOK_PASSWORD = os.getenv("TIKTOK_PASSWORD")
CAPTCHA_KEY = os.getenv("CAPTCHA_KEY")


class CustomChrome(uc.Chrome):
    def quit(self):
        time.sleep(0.1)
        super().quit()


def upload_files_on_tiktok():
    options = webdriver.ChromeOptions()

    # Add arguments to Chrome options
    # options.add_argument("--headless")

    driver = webdriver.Chrome(options=options)
    try:
        # Initialize the CAPTCHA solver
        sadcaptcha = SeleniumSolver(
            driver,
            CAPTCHA_KEY,
            mouse_step_size=1,  # Adjust mouse movement speed
            mouse_step_delay_ms=10  # Adjust delay between mouse steps
        )

        driver.get("https://www.tiktok.com/login/phone-or-email/email")

        # Wait for the email input field
        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Email or username']"))
            )
        except TimeoutException:
            print("Email input field not found, retrying...")
            time.sleep(5)
            driver.refresh()  # Optionally refresh the page

        input_email = driver.find_element(By.XPATH, "//input[@placeholder='Email or username']")
        input_email.send_keys(TIKTOK_EMAIL)

        # Wait for the password input field
        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Password']"))
            )
        except TimeoutException:
            print("Password input field not found within the timeout period.")
            driver.quit()
            return

        input_password = driver.find_element(By.XPATH, "//input[@placeholder='Password']")
        input_password.send_keys(TIKTOK_PASSWORD)

        # Click login button
        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//button[@data-e2e='login-button']"))
            ).click()
        except TimeoutException:
            print("Login button not found within the timeout period.")
            driver.quit()
            return

        # Now check for CAPTCHA presence
        sadcaptcha.solve_captcha_if_present()

        time.sleep(10)

        video_files = [
            "beauty_summary_in_en.mp4",
            "beauty_summary_in_es.mp4",
            "beauty_summary_in_pl.mp4",
            "beauty_summary_in_tr.mp4"
        ]

        for video_file in video_files:
            driver.get("https://www.tiktok.com/tiktokstudio/upload")
            # Wait for the file input to be present
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
            )
            file_input = driver.find_element(By.XPATH, "//input[@type='file']")


            video_path = os.path.join(os.getcwd(), video_file)
            file_input.send_keys(video_path)


            time.sleep(3)
            driver.execute_script("window.scrollBy(0, 10000);")


            wait = WebDriverWait(driver, 20)
            post_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@data-e2e='post_video_button']")))


            post_button.click()


            time.sleep(10)

    finally:
        driver.quit()


upload_files_on_tiktok()
