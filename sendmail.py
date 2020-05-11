# https://stackoverflow.com/questions/16512592/login-credentials-not-working-with-gmail-smtp
from envelopes import Envelope, GMailSMTP
# https://www.tutorialspoint.com/python/python_multithreading.htm
import threading
from clsData import User, Mail
import time

class SendMail(threading.Thread):
    def __init__(self, objUser : User, objSystem : User, objMail : Mail):
        threading.Thread.__init__(self)
        self.objUser = objUser
        self.objMail = objMail
        self.objSystem = objSystem

        self.envelope = Envelope(
            from_addr=(objSystem.email, objSystem.name),
            to_addr=(objUser.email, objUser.name),
            subject=objMail.subject,
            text_body=objMail.content
        )

    def run(self):
        print ("Starting send to " + self.objUser.email)
        gmail = GMailSMTP(self.objSystem.email, self.objSystem.pw  )
        gmail.send(self.envelope)
        print ("Exiting send to " + self.objUser.email)

if __name__ == "__main__":
    user = User()
    user.name = "vulhjp"
    user.email = "vulhjp0122@hotmail.com"

    sys = User()
    sys.name = "clarck"
    sys.email = "clarck5566@gmail.com"
    sys.pw = "jo4gk6ai7"

    mail_1 = Mail()
    mail_1.subject = "First thread"
    mail_1.content = "test1"
    mail_2 = Mail()
    mail_2.subject = "second thread"
    mail_2.content = "test2"

    thread1 = SendMail(user, sys, mail_1)
    thread2 = SendMail(user, sys, mail_2)

    # Start new Threads
    thread1.start()
    thread2.start()

    # Add threads to thread list
    threads = []
    threads.append(thread1)
    threads.append(thread2)

    # Wait for all threads to complete
    for t in threads:
        t.join()
    print ("Exiting Main Thread")
#envelope.add_attachment('/Users/bilbo/Pictures/helicopter.jpg')

# Send the envelope using an ad-hoc connection...
# envelope.send('smtp.googlemail.com', login='clarck5566@gmail.com', password='jo4gk6ai7', tls=True)

# Or send the envelope using a shared GMail connection...

