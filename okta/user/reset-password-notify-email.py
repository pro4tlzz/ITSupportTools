#!/usr/bin/env python3

import requests
import os
import smtplib, ssl
from csv import DictReader
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Set these:
base_url = "https://domain.okta.com"
api_key = os.environ['okta_api_token']
filename = "users.csv"
gmail_smtp_username = os.environ['gmail_smtp_username']
gmail_smtp_password = os.environ['gmail_smtp_password']

headers = {
    'Authorization': 'SSWS ' + api_key,
    'Accept': 'application/json'
}
session = requests.Session()
session.headers.update(headers)

def reset_password(username):

    url = f"{base_url}/api/v1/users/{username}/lifecycle/expire_password?tempPassword=true"
    response=session.post(url)
    response.raise_for_status()

    reset_password_result = response.json()
    print(reset_password_result)
    temp_password = reset_password_result['tempPassword']

    return temp_password

def send_email(username, temp_password):

    context = ssl.create_default_context()
    oubtbound_host = 'smtp.gmail.com'
    message = MIMEMultipart("alternative")
    message["Subject"] = "multipart test"
    message["From"] = gmail_smtp_username
    message["To"] = username

    # Create the plain-text and HTML version of your message
    text = f"""\
    Hi {username},

    Your Okta password has been reset to {temp_password}
    Please change it at {base_url}

    Thanks
    """
    html = f"""\
    <html>
    <body>
        <p>Hi {username},<br>
        <br>
        Your Okta password has been reset to {temp_password}<br>
        Please change it at {base_url}<br>
        <br>
        Thanks<br>
        </p>
    </body>
    </html>
    """

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    with smtplib.SMTP(oubtbound_host, 587) as server:
        server.debuglevel=1
        server.ehlo()
        server.connect(oubtbound_host, 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_smtp_username, gmail_smtp_password)
        server.sendmail(gmail_smtp_username, username, message.as_string())
    
    server.close

def read_csv():

    with open(filename, 'r', encoding='utf-8-sig') as f:
        users = DictReader(f)
        for user in users:
            username = user["username"]
            temp_password = reset_password(username)
            send_email(username, temp_password)


if __name__ == '__main__':

    read_csv()
