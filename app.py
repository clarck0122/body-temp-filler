import threading
from clsData import User, Mail
from sendmail import SendMail
from fillform import FillForm
import configparser
import os


def main():
	config = configparser.ConfigParser()
	config.read('Startup.ini')

	name_li = os.environ['UserNames'].split(",")

	objSys = User()
	objSys.name = "clarck"
	objSys.email = os.environ['SendMail_email']
	objSys.pw = os.environ['SendMail_pw']

	user_li = []
	for name in name_li:
		user = User()
		user.name = name
		user.id = os.environ[user.name + '_id']
		user.pw = os.environ[user.name + '_pw']
		print("id={}, name={}, pw={}, email={}".format(user.id, user.name, user.pw, user.email) )
		user_li.append(user)

	threads = []
	for user in user_li:
		thread = FillForm(user, objSys)
		thread.start()
		threads.append(thread)

	for t in threads:
		t.join()
		print ("Exiting Main Thread")



if __name__ == "__main__":
	main()
