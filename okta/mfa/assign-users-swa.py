#!/usr/bin/env python3
import requests
from csv import DictReader

api_key=""

headers = {
    'Authorization': 'SSWS ' + api_key,
    'Accept': 'application/json'
}

session = requests.Session()
session.headers.update(headers)

appid=""
base_url="https://.okta.com"
url=f"{base_url}/api/v1/apps/{appid}/users"

def assign_app(userid,userlogin,password):

    body={
        "id": userid,
        "credentials":
            {"userName": userlogin,
            "password": password},
        }
    print(body)
    response=session.post(url,json=body)
    response.raise_for_status()
    print(response.json())

def get_uid(username):

    url=f"{base_url}/api/v1/users/{username}"

    response=session.get(url)
    response.raise_for_status

    api_response=response.json()

    user_id=api_response["id"]
    return user_id

def read_csv():

    filename="test.csv"
    with open(filename, 'r', encoding='utf-8-sig') as f:
        reader=DictReader(f)
        for row in reader:
            user=row["login"]
            password=row["password"]
            substring=user.split("@")[0]
            uid=get_uid(user)
            assign_app(uid,substring,password)

read_csv()