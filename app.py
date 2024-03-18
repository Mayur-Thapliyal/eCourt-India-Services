# UPAG040914012022
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import streamlit as st 

import time,os
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from lxml import html
from urllib.request import urlopen
from util import resolve_captcha,click_search
from PIL import Image
import vk_captchasolver as vc
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
def scrape_data(cnr_number,browser):
    URL='https://services.ecourts.gov.in/ecourtindia_v6/'
    driver.get(URL)
    
    while True:
        try:
            elem = browser.find_element(By.XPATH, '/html/body/div[1]/div/main/div[2]/div/form/input')  # Find the search box
            elem.clear()
            elem.send_keys(cnr_number)
            print(">>>> itter <<<<<")
            resolve_captcha(driver=browser)
            click_search(driver=browser)
            chief_judicial_magistrate_heading = browser.find_element(By.XPATH, '/html/body/div[1]/div/main/div[3]/h2')  # get hedding
            print("chief ===",chief_judicial_magistrate_heading)
            st.markdown("Case Detail")
            case_detail = browser.find_element(By.XPATH, '/html/body/div[1]/div/main/div[3]/table[1]')  # invalid captcha input
            st.markdown(case_detail.text)
            print(case_detail.text )
            st.markdown("Case Status")
            case_detail = browser.find_element(By.XPATH, '/html/body/div[1]/div/main/div[3]/table[2]')  # invalid captcha input
            st.markdown(case_detail.text)
            return

        except NoSuchElementException as e:
            try:
                is_invalid_captcha = browser.find_element(By.XPATH, '/html/body/div[7]/div/div/div[1]/button')  # invalid captcha input
                is_invalid_captcha.click()
                time.sleep(2)
                back_button = browser.find_element(By.XPATH, '/html/body/div[1]/div/main/p/button')  # captcha input
                back_button.click()
            except Exception as e:
                try:
                    click_to_refresh = browser.find_element(By.XPATH, '/html/body/div/div/a')  # captcha input
                    click_to_refresh.click()
                except Exception as e:
                    browser.quit()
                    raise("Something went wrong")

@st.cache_resource
def create_browser():
    URL='https://services.ecourts.gov.in/ecourtindia_v6/'
    import chromedriver_binary
    chrome_version = "114.0.5735.90"
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument("window-size=1920,1080")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disadriver_version=chrome_versionble-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)
    # cService = webdriver.ChromeService(ChromeDriverManager().install())
    return driver

with st.sidebar:
    cnr_number=st.text_input("Enter your CRN number here")
if cnr_number or cnr_number != "":
    driver = create_browser()
    scrape_data(cnr_number,driver)

