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



def list_to_string(base_list):
    """
    Convert a list to its string reprensatation
    """

    try:
        _ = float(base_list[0])
        isNumber = True
    except:
        isNumber = False

    result = '['
    for element in base_list:
        if isNumber:
            result += str(element) + ','
        else:
            result += "'" + str(element) + "',"

    return result[:-1] + ']'






def create_arr_graph(x, y):

    return """data = [{
    x: """ + list_to_string(x) + """,
    y: """ + list_to_string(y) + """ }];

    layout = {
    bargap : 0.35,
    font : {
      family: "Raleway",
      size: 10
    },
    hovermode : "closest",
    legend : {
      "x": -0.0228945952895,
      "y": -0.189563896463,
      "orientation": "h",
      "yanchor": "top"
    },
    height : 220,
    width:340,
    margin : {
      "r": 0,
      "t": 20,
      "b": 40,
      "l": 20
    } };

    Plotly.newPlot('arr', data, layout, {staticPlot: true});"""



def create_redemption_graph(x,y):
    return """var data = [
      {
        x: """ + list_to_string(x) + """,
        y: """ + list_to_string(y) + """,
        type: 'bar'
      }
    ];


    var layout = {
      bargap : 0.35,
      font : {
        family: "Raleway",
        size: 10
      },
      hovermode : "closest",
      legend : {
        "x": -0.0228945952895,
        "y": -0.189563896463,
        "orientation": "h",
        "yanchor": "top"
      },
      height : 220,
      width:340,
      margin : {
        "r": 30,
        "t": 20,
        "b": 40,
        "l": 20
      } };

    Plotly.newPlot('early-redemption', data, layout, {staticPlot: true});"""

def create_udl_graph(x, y):

    return """var trace1 = {
    x: """ + list_to_string(x) + """,
    y: """ + list_to_string(y) + """,
    type: 'scatter'};


    var trace2 = {
    x: """ + list_to_string(x) + """,
    y: """ + list_to_string([3,1]) + """,
    type: 'scatter'};


    data = [trace1, trace2];

    layout = {
    bargap : 0.35,
    font : {
      family: "Raleway",
      size: 10
    },
    hovermode : "closest",
    legend : {
      "x": -0.0228945952895,
      "y": -0.189563896463,
      "orientation": "h",
      "yanchor": "top"
    },
    height : 220,
    width:340,
    margin : {
      "r": 0,
      "t": 20,
      "b": 40,
      "l": 20
    } };

    Plotly.newPlot('udl-data', data, layout, {staticPlot: true});"""


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
                                            nbr_backtests = 4356,
                                            script_arr = create_arr_graph([1,2,3],[4,3,7]),
                                            script_redemption = create_redemption_graph(['Period 1', 'Period 2'],
                                                                                        [2,4]),
                                            script_udl = create_udl_graph([1,4], [2,3])))


        with open('create-pdf.sh','w') as f:
            command = '#!/bin/sh\n'
            command += 'google-chrome-stable --headless --disable-gpu'
            command += ' --print-to-pdf=reports/report'+id+'.pdf '
            command += 'reports/report-template'+id+'.html'
            f.write(command)

        # Try to create pdf while the exit code is not success
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
