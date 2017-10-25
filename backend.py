import csv, json, smtplib, mimetypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

import os

class form():

        def __init__(self, dictionary, formNum):

            str = ''

            if formNum == 1:
                str = 'medicalform.csv'
            elif formNum == 2:
                str = 'transportationform.csv'
            elif formNum == 3:
                str = 'financialform.csv'
			#******************Add New Form info here*****************
			
			#elif formNum == num: add more form names here with the associated key when the script is ran
			
			#******************Finish New Form info here**************
            else:
                str = 'form.csv'

            filename = dictionary['lastname'] + dictionary['firstname'] + str

            with open(filename, 'w') as f:
                w = csv.writer(f)
                w.writerow(dictionary.keys())
                w.writerow(dictionary.values())
            f.close()
            
            #sends an email with the csv file attached. Uses Gmail Server currently
			#username and password is gmail login
            emailfrom = "smptsohacktest@gmail.com"
            emailto = "bailey.garner15@gmail.com"
            fileToSend = dictionary['lastname'] + dictionary['firstname'] + str
            username = "smptsohacktest"
            password = "Ohackteam14"

            msg = MIMEMultipart()
            msg["From"] = emailfrom
            msg["To"] = emailto
            msg["Subject"] = "Form Submission"
            msg.preamble = ""

            ctype, encoding = mimetypes.guess_type(fileToSend)
            if ctype is None or encoding is not None:
                ctype = "application/octet-stream"

            maintype, subtype = ctype.split("/", 1)

            fp = open(fileToSend, "rb")
            attachment = MIMEBase(maintype, subtype)
            attachment.set_payload(fp.read())
            fp.close()
            encoders.encode_base64(attachment)
            attachment.add_header("Content-Disposition", "attachment", filename=fileToSend)
            msg.attach(attachment)
            server = smtplib.SMTP("smtp.gmail.com:587")
            server.starttls()
            server.login(username,password)
            server.sendmail(emailfrom, emailto, msg.as_string())
            server.quit()

            os.remove(fileToSend)

def start(jsonString, formNum):
    python_object = json.loads(jsonString)
    foo = form(python_object, formNum)

