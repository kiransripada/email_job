import schedule
import time
import smtplib, ssl
import csv


port = 465  # For SSL
password = input("Type your password and press enter: ")
sender_email = "youremail@gmail.com"
receiver_email = "youremail+1@gmail.com"
message = """\
Subject: Happy Birthday 121 !

This message is sent from mycompany.com."""

context = ssl.create_default_context()


##  Job function  to send email .You can write your logi to fetch email ids from csv in a separate function or here it self
def job():
    print("Start Email Job..")
    try:

        server = smtplib.SMTP("smtp.gmail.com", 587)

        server.starttls(context=context)
        server.login("youremail@gmail.com", password)
        ## read CSV
        file= open("email_add.csv")
        reader = csv.reader(file)
        next(reader)
        ## Itrate over list
        for name, email in reader:
            print(f"Sending email to {name}")
            server.sendmail(sender_email, email, message)

    except Exception as e:
        print(e)
    finally:
        server.quit()


## Scheduler & trigger logic  to send email every 10 secs
#Ref https://pypi.org/project/schedule/
#schedule.every(10).seconds.do(job)
##If you wan to send email every day at 8:00 , uncomment below line


schedule.every().day.at("8:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
