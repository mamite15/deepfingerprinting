from selenium import webdriver
import chromedriver_binary
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import logging

driver = None

def setup(url):
    global driver

    logging.basicConfig(format='%(asctime)s %(message)s',
                        datefmt='%Y/%m/%d %I:%M:%S %p', level=logging.INFO)

    driver = webdriver.Chrome()
    driver.implicitly_wait(2.5)

    driver.get(url)

def switch_frame(name):
    driver.switch_to.frame(name)

def find(name_or_id):
    if name_or_id.startswith('#'):
        return driver.find_element(By.ID, name_or_id[1:])
    else:
        return driver.find_element(By.NAME, name_or_id)

def update_select_value(name_or_id, value):
    Select(find(name_or_id)).select_by_visible_text(value)

def run_script(code):
    driver.execute_script(code)

def iframes():
    return driver.find_elements(By.TAG_NAME, "iframe")