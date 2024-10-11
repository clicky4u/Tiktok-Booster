import time
import sys
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from colorama import Fore, Style, init
import threading
import keyboard
from PIL import Image
from art import display_banner


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless=new')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--window-size=1920x1080')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--remote-debugging-port=9222')
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])


init(autoreset=True)
display_banner()


driver = webdriver.Chrome(options=chrome_options)
driver = None
captcha_image_path = "captcha_image.png"


def get_video_url():
    print(Fore.CYAN + "Enter the TikTok video URL" + Style.RESET_ALL)
    return input(Fore.GREEN + ">>> " + Style.RESET_ALL)


def get_target_views():
    print(Fore.CYAN + "Enter the number of views you want to send" + Style.RESET_ALL)
    while True:
        try:
            return int(input(Fore.GREEN + ">>> " + Style.RESET_ALL))
        except ValueError:
            print(Fore.RED + "Invalid input, please enter a valid number.")


def styled_input_box(prompt):
    box_width = len(prompt) + 4
    print(Fore.YELLOW + '┌' + '─' * (box_width - 2) + '┐')
    print(Fore.YELLOW + '│ ' + prompt + ' │')
    print(Fore.YELLOW + '└' + '─' * (box_width - 2) + '┘')
    return input(Fore.GREEN + "" + Style.RESET_ALL)


def capture_captcha():
    try:
        captcha_image_xpath = "//img[@class='img-thumbnail card-img-top border-0']"
        captcha_element = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, captcha_image_xpath))
        )
        captcha_element.screenshot(captcha_image_path)
        print(f"Captcha image saved to: {captcha_image_path}")
        Image.open(captcha_image_path).show()
    except Exception as e:
        print(Fore.RED + "Error capturing Captcha:", str(e))


def get_captcha_input():
    return styled_input_box("Please enter the code in the image")


def enter_captcha_code(captcha_code):
    try:
        captcha_input_xpath = "/html/body/div[5]/div[2]/form/div/div/div//input[@type='text' and @placeholder='Enter the word']"
        captcha_input = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, captcha_input_xpath))
        )
        captcha_input.clear()
        captcha_input.send_keys(captcha_code)

        submit_button_xpath = "//button[contains(@class, 'submit-captcha')]"
        submit_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, submit_button_xpath))
        )
        submit_button.click()

        print(Fore.LIGHTGREEN_EX + "Captcha submitted successfully!")
    except Exception as e:
        print(Fore.RED + "Error entering Captcha:", str(e))


def start_automation(video_url, target_views):
    global driver
    service = Service(executable_path=driver)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_window_size(100, 400)
    driver.get('https://zefoy.com')

    capture_captcha()
    captcha_code = get_captcha_input()
    enter_captcha_code(captcha_code)

    print(Fore.LIGHTMAGENTA_EX + "Captcha solved! Continuing with the process...")

    try:
        views_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 't-views-button')]"))
        )
        views_button.click()
    except Exception:
        pass

    try:
        video_url_input = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "/html/body/div[10]/div//input[@type='search' and @placeholder='Enter Video URL']"))
        )
        video_url_input.click()
        video_url_input.clear()
        video_url_input.send_keys(video_url)
    except Exception:
        pass

    total_views_sent = 0
    disable_button_xpath = "/html/body/div[10]/div//button[@type='submit' and contains(@class, 'disableButton')]"
    btn_dark_xpath = "/html/body/div[10]/div//button[contains(@type, 'submit') and contains(@class, 'btn-dark')]"

    retry_attempts = 5
    retry_delay = 5

    while total_views_sent < target_views:
        try:
            disable_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, disable_button_xpath))
            )
            disable_button.click()
        except Exception:
            retry_attempts -= 1
            if retry_attempts == 0:
                break
            time.sleep(retry_delay)
            retry_delay *= 2
            continue

        try:
            btn_dark = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, btn_dark_xpath))
            )
            btn_dark.click()
            print(Fore.LIGHTGREEN_EX + f"☣︎ 1000 views sent to the video. Total: {total_views_sent + 1000}/{target_views} ☣︎")
            total_views_sent += 1000
            retry_attempts = 5
            retry_delay = 5
            time.sleep(10)
        except Exception:
            pass

    driver.quit()


def listen_for_stop():
    keyboard.wait('ctrl+z')
    print(Fore.RED + "\nStopping process and closing the browser...")
    if driver is not None:
        driver.quit()
    sys.exit(0)


if __name__ == "__main__":
    video_url = get_video_url()
    target_views = get_target_views()

    automation_thread = threading.Thread(target=start_automation, args=(video_url, target_views))
    automation_thread.start()

    stop_listener_thread = threading.Thread(target=listen_for_stop)
    stop_listener_thread.start()

    automation_thread.join()

    print(Fore.LIGHTGREEN_EX + "\nProcess completed!")
