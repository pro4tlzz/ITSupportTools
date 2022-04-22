#!/usr/bin/env python3
import requests
import csv

api_key=""

headers = {
    'Authorization': 'SSWS ' + api_key,
    'Accept': 'application/json'
}

session = requests.Session()
session.headers.update(headers)

base_url="https://.okta.com"
url=f"{base_url}/api/v1/users?filter%3Dstatus%20eq%20%22ACTIVE%22%0A"

data={
    "user_id": None,
    "user_status": None,
    "username": None,
    "factor_id": None,
    "factor_type": None,
    "factor_created": None,
    "factor_lastUpdated": None,
    "factor_lastVerified": None
}

def list_users(url,data):

    make_csv(data)

    while url:

        response = session.get(url)
        response.raise_for_status
        api_response=response.json()

        for user in api_response:

            user_id=user["id"]
            user_status=user["status"]
            username=user["profile"]["login"]

            data["user_id"]=user_id
            data["user_status"]=user_status
            data["username"]=username

            print(data)
            if user_status == "ACTIVE":

                get_factors(user_id,data)

        next = response.links.get('next')
        url = next['url'] if next else None

def get_factors(user_id,data):

    url=f"{base_url}/api/v1/users/{user_id}/factors"
    response = session.get(url)
    response.raise_for_status
    factors=response.json()

    for factor in factors:

        factor_id=factor["id"]
        factor_type=factor["factorType"]
        factor_created=factor["created"]
        factor_lastUpdated=factor["lastUpdated"]

        try:
            factor_lastVerified=factor["lastVerified"]
        except:
            factor_lastVerified=""

        data["factor_id"]=factor_id
        data["factor_type"]=factor_type
        data["factor_created"]=factor_created
        data["factor_lastUpdated"]=factor_lastUpdated
        data["factor_lastVerified"]=factor_lastVerified

        update_csv(data)

        print(data)

def make_csv(rows):

    filename="mycsvfile.csv"
    with open(filename, 'w') as f:
        w = csv.writer(f)
        w.writerow(rows)

def update_csv(data):
    
    with open('mycsvfile.csv', 'a') as f:
        w = csv.writer(f)
        w.writerow(data.values())

list_users(url,data)
