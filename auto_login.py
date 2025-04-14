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
    browser.add_cookie({"name": "MUSIC_U = 00EBE8FDC34190931C2F7125036F0918B439B37F966C4D2A9474A0D4AFE64ED502D6830870B9F3AA22AB97E7CACE6B00F5031B346D7AC9783737EF366D857DDADBD0EA48A40CBAEFB93D203BF408C0A24B249FF786EF79A8280F4D06B7A98DAED65A15D2CAA72A6D390E60B86461A0E19D6F284533861CF7E6D469038195F49E587FFF593B55D3DB2839C891CFF8096FDDEB9EEB345D35C82CB055EA4D0EBB1908D2D21336F42EBCD7D1A96E8DF7678CCE12EA589A3B4058D552701206B2B77146323B84CDE9796DE339844A5B218AD48482C9E72A532D5A792113896778BA7152BFC97CBEC3A0E955A97AA982A28A8AB3108A84FC91DE9EB8860BFF92C64E254A93AE1B74DC1E049F7C1AE97582360782537333EFF23564091D95BD31D4762E265EA40C1872A3C15EA45E04348F8EF96E5DD49A0C6CCF5ECC44B5A4C481BFB739CD00892086CC5733B69E92FA4B9ED64C"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()
