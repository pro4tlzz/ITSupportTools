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

base_url="https://$org.okta.com"
group="$group"
url=f"{base_url}/api/v1/groups/{group}/users"

list_of_rows=["user_id","user_status","username","factor_id","factor_type","factor_created","factor_lastUpdated"]

def list_users(url):

    make_csv(list_of_rows)

    while url:

        response = session.get(url)
        response.raise_for_status
        api_response=response.json()

        for user in api_response:

            user_id=user["id"]
            user_status=user["status"]
            username=user["profile"]["login"]
            data={
                "user_id":  user_id,
                "user_status":  user_status,
                "username":  username
            }
            print(data)
            if user_status == "ACTIVE":

                get_factors(user_id,data)

        next = response.links.get('next')
        url = next['url'] if next else None

def get_factors(user_id,user_data):

    url=f"{base_url}/api/v1/users/{user_id}/factors"
    response = session.get(url)
    response.raise_for_status
    factors=response.json()

    for factor in factors:

                factor_id=factor["id"]
                factor_type=factor["factorType"]
                factor_created=factor["created"]
                factor_lastUpdated=factor["lastUpdated"]

                user_data["factor_id"]=factor_id
                user_data["factor_type"]=factor_type
                user_data["factor_created"]=factor_created
                user_data["factor_lastUpdated"]=factor_lastUpdated

                update_csv(user_data)

                print(user_data)

def make_csv(rows):

    filename="mycsvfile.csv"
    with open(filename, 'w') as f:
        w = csv.writer(f)
        w.writerow(rows)

def update_csv(data):
    
    with open('mycsvfile.csv', 'a') as f:
        w = csv.writer(f)
        w.writerow(data.values())

list_users(url)