import schedule
import time
import smtplib, ssl
import csv
import datetime
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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
            is_birthday = days_between(dob, today)
            ##send email if dob is today
            if is_birthday:
                print(f"Sending email to {name} with  {dob}")
                msgRoot = generate_html_msg(name)
                server.sendmail(sender_email, email, msgRoot.as_string())

    except Exception as e:
        print(e)
    finally:
        server.quit()


## Scheduler & trigger logic  to send email every 10 secs
# Ref https://pypi.org/project/schedule/
# schedule.every(10).seconds.do(job)
##If you wan to send email every day at 8:00 , uncomment below line
def days_between(d1, d2):
    d1 = datetime.datetime.strptime(d1, "%Y-%m-%d").date()
    d1 = str(d1.month) + str(d1.day)
    d2 = datetime.datetime.strptime(d2, '%Y-%m-%d').date()
    d2 = str(d2.month) + str(d2.day)
    if d1 == d2:
        return True
    else:
        return False


def generate_html_msg(name):
    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = ' Happy Birthday'

    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)

    msgText = MIMEText('This is the alternative plain text message.')
    msgAlternative.attach(msgText)

    msgText = MIMEText(
        f'<b> <font face = "Comic sans MS" size =" 4"><h3 style="color:purple;"><br>Dear {name} <br> We are grateful '
        f'test/b>',
        'html')
    msgAlternative.attach(msgText)

    fp = open('bdy.png', 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()

    # Define the image's ID as referenced above
    msgImage.add_header('Content-ID', '<image1>')
    msgRoot.attach(msgImage)
    return msgRoot

schedule.every(10).seconds.do(job)

#schedule.every().day.at("23:13").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)

