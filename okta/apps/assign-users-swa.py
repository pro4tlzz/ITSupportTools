#!/usr/bin/env python3

import requests
from csv import DictReader

# Set these:
base_url = "https://.okta.com"
api_key = ""
appid = ""
filename = "users.csv"

headers = {
    'Authorization': 'SSWS ' + api_key,
    'Accept': 'application/json'
}
session = requests.Session()
session.headers.update(headers)

url = f"{base_url}/api/v1/apps/{appid}/users"

def assign_app(userid, username, password):
    body = {
        "id": userid,
        "credentials":
            {"userName": username,
            "password": password}
    }
    print(body)
    response = session.post(url, json=body)
    response.raise_for_status()
    print(response.json())

def get_uid(username):
    url = f'{base_url}/api/v1/users/{username}'

    response = session.get(url)
    response.raise_for_status()

    user = response.json()
    user_id = user["id"]
    return user_id

def read_csv():
    with open(filename, 'r', encoding='utf-8-sig') as f:
        users = DictReader(f)
        for user in users:
            login = user['login']
            password = user['password']
            username = login.split("@")[0]
            uid = get_uid(login)
            assign_app(uid, username, password)

read_csv()
