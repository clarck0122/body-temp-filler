import threading
from clsData import User, Mail
from sendmail import SendMail

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
import random
import os

import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger(os.path.basename(__file__))
logging.basicConfig(
        handlers=[RotatingFileHandler('./' + os.path.basename(__file__) + '.log', maxBytes=100000, backupCount=10)],
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
        datefmt='%Y-%m-%dT%H:%M:%S')
logging.getLogger().addHandler(logging.StreamHandler())

class FillForm(threading.Thread):
	def __init__(self, objUser : User, objSystem : User):
		threading.Thread.__init__(self)
		self.objUser = objUser
		self.objSystem = objSystem
		self.Teamperature = str(random.randint(355,365)/10)
		logger.info("objUser, id={}, name={}, pw={}, email={}".format(self.objUser.id, self.objUser.name, self.objUser.pw, self.objUser.email) )
		logger.info("objSystem, id={}, name={}, pw={}, email={}".format(self.objSystem.id, self.objSystem.name, self.objSystem.pw, self.objSystem.email) )

	def run(self):
		delay = random.randint(60,120)
		logger.info ("Starting " + self.objUser.name + ", delay=" + str(delay) + ", Teamperature=" + self.Teamperature)
		time.sleep(delay)

		# # for local run
		# driver = webdriver.Chrome()

		# for Heroku run
		# https://stackoverflow.com/questions/41059144/running-chromedriver-with-python-selenium-on-heroku
		# https://www.youtube.com/watch?v=Ven-pqwk3ec
		chrome_options = webdriver.ChromeOptions()
		chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
		chrome_options.add_argument("--headless")
		chrome_options.add_argument("--disable-dev-shm-usage")
		chrome_options.add_argument("--no-sandbox")
		driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

		URL = "https://" + self.objUser.id + ":" + self.objUser.pw + "@mobile01.umc.com/udtrs.nsf"
		driver.get(URL)

		# wait response
		wait = WebDriverWait(driver, 30)
		try:
			wait.until(lambda driver: driver.current_url != URL)
		except Exception as e:
			logger.info(e)

		# redirect to new page
		URL = "https://mobile01.umc.com/udtrs.nsf/DTRF?open&"
		driver.get(URL)

		# click radio buttuom
		element = driver.find_elements_by_xpath("//input[@type='radio'][@value='No']")
		# view element
		element
		for e in element:
			driver.execute_script("arguments[0].click();", e)
			time.sleep(1)

		# input teamperature
		element = driver.find_element_by_xpath("//input[@id='Temperature']")
		element.send_keys(self.Teamperature)

		# submit
		element = driver.find_element_by_xpath("//a[@role='button'][contains(text(), '呈報 Submit')]")
		element.click()

		# confirm
		wait = WebDriverWait(driver, 30)
		try:
			wait.until(lambda driver: driver.current_url != URL)
		except Exception as e:
			logger.info(e)
		element = driver.find_elements_by_xpath("//h1")
		res = False
		for e in element:
			logger.info(e.text)
			if "Normal" in e.text:
				res = True

		# content = Mail()
		# if res:
		# 	logger.info("pass")
		# 	content.subject = "Sucess: Fill Body Teamperature"
		# 	content.content = "Today teamperature is " + self.Teamperature
		# else:
		# 	logger.info("fail")
		# 	content.subject = "Fail: Fill Body Teamperature"
		# 	content.content = "please check system "

		# mail = SendMail(self.objUser, self.objSystem, content)
		# mail.start()
		driver.close()
		logger.info ("Exiting " + self.objUser.name)


# if __name__ == "__main__":
# 	user = User()
# 	user.id = "00045217"
# 	user.pw = "123938619"
# 	user.name = "vulhjp"
# 	user.email = "vulhjp0122@hotmail.com"

# 	sys = User()
# 	sys.name = "clarck"
# 	sys.email = os.environ['SendMail_email']
# 	sys.pw = os.environ['SendMail_pw']

# 	thread1 = FillForm(user, sys)
# 	thread1.start()
