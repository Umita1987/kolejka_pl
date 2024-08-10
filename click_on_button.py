import time
import os

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from dotenv import load_dotenv

def click_on_button():
    options = webdriver.ChromeOptions()
    options.binary_location =  os.environ.get("GOOGLE_CHROME_BIN")
    options.add_argument("--disable-gpu")
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(service=Service(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=options))
    try:
        driver.get("https://kolejka.gdansk.uw.gov.pl/branch/5")
    except Exception as e:
        print(e)
        click_on_button()
    driver.implicitly_wait(10)
    try:
        elem = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[1]/div/div[2]/button/div')
        time.sleep(1)
        elem.click()
        time.sleep(5)

    except NoSuchElementException:
        driver.close()
        click_on_button()

    try:

        elem1 = driver.find_element(By.XPATH,
                                    '/html/body/div[2]/div/main/div/div/div/div[2]/div[1]/'
                                    'div[3]/div/div[2]/ul/li[1]/div[1]/div[2]')
        time.sleep(2)
        elem1.click()
        time.sleep(10)

    except NoSuchElementException:
        driver.close()
        click_on_button()

    try:
        hours = driver.find_element(By.XPATH,
                                    '//form[@novalidate="novalidate" and @class="v-form"]'
                                    '//div[@id="timeloader"]//div[@class="v-btn__content"]').text

        days = driver.find_element(By.XPATH,
                                   "//button[@class='v-btn v-btn--active v-btn--icon v-btn--floating theme--light']"
                                   "//div[@class='v-btn__content']").text

        month = driver.find_element(By.XPATH,
                                    '/html/body/div[2]/div/main/div/div/div/div[2]/div[1]/div[4]/'
                                    'form/div/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div/div/button').text

        return f'{days} {month} {hours}'
    except NoSuchElementException:
        print("NoSuchElementException")
        try:
            elem2 = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[1]/div/div[2]/button/div')
        except Exception as e:
            print(e)
            driver.close()
            click_on_button()
        elem3_text = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[1]/div/div[1]').text
        time.sleep(1)
        elem2.click()
        time.sleep(5)

        print(elem3_text)
        return elem3_text

