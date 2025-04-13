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
    browser.add_cookie({"name": "MUSIC_U", "value": "009963D9F7C28AE9C25E08065CE8D8337BB8C8954C429CB4023E1F4749C4C374ADFC811A3C15EADCCF1F051145E67B3441B72ED5F4CEF5C84D274BE2251DAA2B2A2E93D1594A9FDDBC6EAA233810A3A932A5886E4C8289F041AE7F2B49A87FC0D92AB4D9BBAB6B6791DD58683570923FB1BB2D620A6B00C8437B6E7077CB1A645004D15A636333F347CDEC047F7DA05A71F45CBDEF9A6802D87257A870F4D1FF2742E1E5D21F0C2BB69BB80CF4B9C68396435C54FCF54041A908B69CF1D77A6CF64046B4286C4705E0EC391B91E9658B58B42D439C60AD7DDAB86AF2BDC41CA7D033362A6ADF03969A2AAA860FB9A539BDA81CA73DFD4B1EB0B6E934A372B98FACE7FBCD37C1BCC0D23FC8E5D3A54BBA7315EE3AB402D602D718148787924E6E3883D34FF7BDE99D7DA46B7A4DC6309C0A08A5DB19EF5E2DE375026C353280660013ADF9163C99B7B1142585AE8C5A3E77F07FC97B474468D268B6BBCAB2546C81"})
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
