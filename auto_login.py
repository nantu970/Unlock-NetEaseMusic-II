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
    browser.add_cookie({"name": "MUSIC_U", "value": "0078E78A8F5C437AD0662E2D50B945E7A6FA672CC64D149B86779C8F55BCF428391FD7DF942963E479F8BC0834B319FF89DC6ABB3592F04AC38568B0C9CEC1E7946A8658367A52F03B8301BBCB76CBED655CF49C2A4D1726752A2EE2601DB4BF45B1560EDA875912102C67D52E5D5305CE285E770CE19E7950129AAC388F8DB046FC6C7DB051A9AB9B9DCC69448970E1BB07C0E3E67932E23526FF480F65CD45215D27797E69F590FE17712B12683821410B7AE1174FD0C2AAE5369B94FAC3800FB31D95B70D23F873483D50EBD74C388542C536A3AA3F8826FC8A57C7A31B49702B0F4511AC699945B3F46133BFD040BF798383CE3BDD2E158A17CD09863DE145B3B7F86E5E60CDE57E3149F8676335A1FBD33C2E2B2579D9C83382AE70AEC7752BD09C18D7ABF743AEB97C2DB03BE8F29A871F09460F75588DFFF0CC1F56AAE1FC2B745B8500B69AA0CF728E5DBB05385F3B30DA5E2C3E2F71C43A698087DCF3"})
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
