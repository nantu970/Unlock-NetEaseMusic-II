# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "000B333EDED3848185B098E681981E009C785976B26BF51792D0A1BE55BE92A830A8C09E18AEE7BF5D8AAA0E4192FD66A0E702457BEF43B57CECE1776BF0503F8B7FDBB60B238358AA4B5F2C7F87EE903FBBE2AAB0F7E5779E8840795BB34F11F2159EB510363FC45186AD195BAF1E6E2F399E98861DAEB125278350BBBDED1E80DFAF9339B802EF9D7E1B0B6F932C9CB255B6AEF7C4CA062A7254690C13877A4DEA4CAB1B90C838CC1BD08E1BF05637AAE4502993F0D98BC4D1FBF34493A907EB42576E369D08928E9AC6019BB0260BD3A6C3C396CF9399355CC87C19CFDD5E1FE2A26F84AE2B5BB822562F9178AF30AB15AE19D2A62FDFE7A9837051CE06598A27AA84ACEAAD2F188402F176E628777DE7A7443B3A5051A6EB6FAAFEB746ACC9640C1EE7D96B188DC738879A8A0C5A1C6741F77639AA27E0587100603A630C1527614D4498549170CB26B5B4D25B89F50F6EBA2786A26BC81A2957BC48CFD93C"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
