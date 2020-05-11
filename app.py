import threading
from clsData import User, Mail
from sendmail import SendMail
from fillform import FillForm
import configparser
import os


def main():
	config = configparser.ConfigParser()
	config.read('Startup.ini')
	id_li = config['Common']['User'].split(",")

	objSys = User()
	objSys.name = "clarck"
	objSys.email = os.environ['SendMail_email']
	objSys.pw = os.environ['SendMail_pw']

	user_li = []
	for user_id in id_li:
		user = User()
		user.id = user_id
		user.name = config[user.id]['name']
		user.pw = config[user.id]['pw']
		user.email = config[user.id]['email']
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
