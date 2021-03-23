import schedule
import time
import smtplib, ssl

port = 465  # For SSL
password = input("Type your password and press enter: ")
sender_email = "youremail@gmail.com"
receiver_email = "youremail+12@gmail.com"
message = """\
Subject: Hi there

This message is sent from Python."""

context = ssl.create_default_context()


def job():
    print("I'm working...")
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        #server.connect("smtp.gmail.com", 587)
        #server.helo()
        server.starttls(context=context)
        server.login("youremail@gmail.com", password)
        server.sendmail(sender_email, receiver_email, message)

    except Exception as e:
        print(e)
    finally:
        server.quit()


schedule.every(10).seconds.do(job)
##
while True:
    schedule.run_pending()
    time.sleep(1)
