import schedule
import time
import smtplib, ssl
import csv
import datetime

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
    print("Start Birthday Email Job..")
    try:

        server = smtplib.SMTP("smtp.gmail.com", 587)

        server.starttls(context=context)
        server.login("youremail@gmail.com", password)
        ## read CSV
        file = open("email_add.csv")
        reader = csv.reader(file)
        next(reader)
        ## Itrate over list
        for name, email, dob in reader:
            print(f"Iterate over email add csv")
            today = datetime.datetime.now().strftime('%Y-%m-%d')
            date_diff = days_between(dob, today)
            print(f"number diff {date_diff}")
            ##send email if dob is today
            if date_diff == 0:
                print(f"Sending email to {name} with  {dob}")
                server.sendmail(sender_email, email, message)

    except Exception as e:
        print(e)
    finally:
        server.quit()


## Scheduler & trigger logic  to send email every 10 secs
# Ref https://pypi.org/project/schedule/
# schedule.every(10).seconds.do(job)
##If you wan to send email every day at 8:00 , uncomment below line

def days_between(d1, d2):
    d1 = datetime.datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)

schedule.every(10).seconds.do(job)

#schedule.every().day.at("23:13").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)

