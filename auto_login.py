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
    browser.add_cookie({"name": "MUSIC_U", "value": "007A768F0A58FFF8BFF712C1636F09B712B741EB3BC42962C8FE842576C1C4A28556B1A63E9F6ED84A78AAD5CE87D63DE889364F02B1DE5F0CB3C4B3D7C64E344BA1466ECCED8CE0050120D91B1401C0A885B56F3D97EC812C416EC0E356A42C95EAA8141A57E979CA63087ABEE2A66197CF63D9BE32E695DC037B01BFD0D97021E641484A0369A0836CB2A8FCFCC8833726DF061084618F1A8F56E69D1BE8478CC8D1E9CB3DF3B6043B6737F96E0B7E441BC664DF9A0F1F3BC9002C4BCF632920F836CA92D893F22F1F6E94E63CF77564AF114DF895008748FB478C6C8B15F105A06D8CDB2AF86552AA4D81C4508D9E03F52FF54B6DB610AE60F45AFACFDA6A77828059876CE896F2DAE63A2BAA121625480E1EDA33CB0E2C43B9645F0BEBD06D053548BB5EBCAE8E96BB4EED209C6F83A601D8AE9D25560874AB472CF816098787A3F0E6C73F18066ACC30A45D3139C4"})
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
