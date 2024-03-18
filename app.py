# UPAG040914012022
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import streamlit as st 

import time
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from lxml import html
from urllib.request import urlopen
from util import resolve_captcha,click_search
from PIL import Image
import vk_captchasolver as vc
from selenium.common.exceptions import NoSuchElementException

def scrape_data(cnr_number):
    chrome_version = "122.0.6261.111"
    options =  webdriver.ChromeOptions()
    # options.add_argument("headless")
    cService = webdriver.ChromeService(ChromeDriverManager(driver_version=chrome_version).install())
    browser = webdriver.Chrome(service=cService,options=options)
    # browser = webdriver.Chrome(service = cService,options=options)
    URL='https://services.ecourts.gov.in/ecourtindia_v6/'
    browser.get(URL)
    soup = BeautifulSoup(urlopen(URL))
    elem = browser.find_element(By.CLASS_NAME, 'cinumber')  # Find the search box
    elem.send_keys(cnr_number)
    while True:
        try:
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
                    raise("Something went wrong")
                
    browser.quit()

with st.sidebar:
    cnr_number=st.text_input("Enter your CRN number here")
if cnr_number or cnr_number != "":
    scrape_data(cnr_number)
