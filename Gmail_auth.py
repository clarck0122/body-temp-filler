# https://accounts.google.com/b/0/DisplayUnlockCaptcha
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

import os
# for local run
driver = webdriver.Chrome()

# # for Heroku run
# # https://stackoverflow.com/questions/41059144/running-chromedriver-with-python-selenium-on-heroku
# # https://www.youtube.com/watch?v=Ven-pqwk3ec
# chrome_options = webdriver.ChromeOptions()
# chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--disable-dev-shm-usage")
# chrome_options.add_argument("--no-sandbox")
# driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

URL = "https://accounts.google.com/b/0/DisplayUnlockCaptcha"
driver.get(URL)

element = driver.find_element_by_xpath("//input[@id='submitChallenge']")
element.click()
