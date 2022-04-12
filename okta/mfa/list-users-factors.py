#!/usr/bin/env python3
import requests

api_key=""

headers = {
    'Authorization': 'SSWS ' + api_key,
    'Accept': 'application/json'
}

session = requests.Session()
session.headers.update(headers)

base_url="https://.okta.com"
group=""
url=f"{base_url}/api/v1/groups/{group}/users"

def list_users(url):

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

                get_factors(user_id)

        next = response.links.get('next')
        url = next['url'] if next else None

def get_factors(user_id):

    url=f"{base_url}/api/v1/users/{user_id}/factors"
    response = session.get(url)
    response.raise_for_status
    factors=response.json()

    for factor in factors:

        factor_id=factor["id"]
        factor_type=factor["factorType"]
        factor_created=factor["created"]
        factor_lastUpdated=factor["lastUpdated"]

        data={
            "factor_id":  factor_id,
            "factor_type":  factor_type,
            "factor_created":  factor_created,
            "factor_lastUpdated":  factor_lastUpdated
        }

        print(data)

list_users(url)