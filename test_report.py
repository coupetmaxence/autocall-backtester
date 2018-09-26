import subprocess
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

import datetime
import bs4
import requests
import json
import pandas as pd
import numpy as np
import codecs

import platform
import jinja2
import os
import time


sending_email = "finance.newsletter.test@gmail.com"
sending_password = "aqwxszedc"



def create_report(id, autocall, start_date, end_date):
    if platform.system() == 'Linux':

        # Create environment to find templates
        latex_jinja_env = jinja2.Environment(
        	loader = jinja2.FileSystemLoader(os.path.abspath('./reports/')))

        # Base template to fill with backtest data
        template = latex_jinja_env.get_template('report-template.html')

        # Fill the template and create a specific html file
        with open("reports/report-template"+id+".html", "w") as text_file:
            text_file.write(template.render(date=time.strftime("%d/%m/%Y"),
                                            product_description = autocall.get_info(),
                                            backtest_begin = start_date.strftime("%d/%m/%Y"),
                                            backtest_end = end_date.strftime("%d/%m/%Y"),
                                            nbr_backtests = 4356))


        with open('create-pdf.sh','w') as f:
            command = '#!/bin/sh\n'
            command += 'google-chrome-stable --headless --disable-gpu'
            command += ' --print-to-pdf=reports/report'+id+'.pdf '
            command += 'reports/report-template'+id+'.html'
            f.write(command)



        while True:
            exit_code = subprocess.call(['./create-pdf.sh'])

            try:
                exit_code = int(exit_code)

                if exit_code == 0:
                    break
            except:
                pass



def send_mail(list_emails, subject, id):
    global sending_email, sending_password
    """
        Send a mail to a list of emails. The body is an html
        formated file template.
    """

    # Creating the server, and handling all connections steps
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.connect("smtp.gmail.com",587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(sending_email, sending_password)

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sending_email

    # open the file to be sent
    filename = "reports/report"+id+".pdf"
    attachment = open(filename, "rb")

    # instance of MIMEBase and named as p
    p = MIMEBase('application', 'octet-stream')

    # To change the payload into encoded form
    p.set_payload((attachment).read())

    # encode into base64
    encoders.encode_base64(p)

    filename = "backtest-report.pdf"
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    # attach the instance 'p' to instance 'msg'
    msg.attach(p)

    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    for email in list_emails :
        msg['To'] = email
        server.sendmail(sending_email, email, msg.as_string())
    server.quit()
