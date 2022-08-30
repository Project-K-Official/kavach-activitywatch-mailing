import os
import smtplib
import time
from os.path import basename
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from configparser import ConfigParser
from email.mime.image import MIMEImage
import parsing_json

def mail(json):
    configur = ConfigParser()
    configur.read('configurations.ini')

    msg = MIMEMultipart()

    msg['Subject'] = 'Test mail with attachment'
    msg['From'] = configur.get('SMTPlogin', 'sender_address')
    msg['To'] = configur.get('SMTPlogin', 'receiver_address')

    string = "The given time is in minutes"
    for item in json:
        string += item + ':' + str(json[item]/60) + ';\n'

    part1 = MIMEText(string, "plain")
    msg.attach(part1)

    html = """\
    <html>
        <body>
            <img src="cid:Mailtrapimage">
        </body>
    </html>
    """
    part2 = MIMEText(html, "html")
    msg.attach(part2)

    # We assume that the image file is in the same directory that you run your Python script from
    fp = open('plot.png', 'rb')
    image = MIMEImage(fp.read())
    fp.close()

    # Specify the  ID according to the img src in the HTML part
    image.add_header('Content-ID', '<Mailtrapimage>')
    msg.attach(image)

    with smtplib.SMTP("smtp.mailtrap.io", 2525) as server:
        server.login(configur.get('SMTPlogin', 'mailtrap_user'), configur.get('SMTPlogin', 'mailtrap_password'))
        server.sendmail(configur.get('SMTPlogin', 'sender_address'), configur.get('SMTPlogin', 'receiver_address'), msg.as_string())
        print("Successfully sent email")

def saving_json():
    while True:
        print("Deleting old export.json")
        os.system("rm export.json")

        print("Deleting old plot")
        os.system("rm plot.png")

        print("Installing new export.json")
        os.system("wget http://localhost:5600/api/0/export -O export.json")
        print("New export.json installation complete")

        data = parsing_json.parsing()
        parsing_json.plotting(data)
        print("New plot created")
        mail(data)
        time.sleep(600)

if __name__ == "__main__":
    os.system("wget http://localhost:5600/api/0/export -O export.json")
    print("New export.json installation complete")
    data = parsing_json.parsing()
    parsing_json.plotting(data)
    print("New plot created")
    mail(data)
    time.sleep(600)
    saving_json()
