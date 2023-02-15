#!/usr/bin/env python3

import requests
import os

# Set these:
okta_api_token = os.environ['okta_api_token']
base_url = "https://changeme.okta.com"
appids = ['changeme']

headers = {
    'Authorization': 'SSWS ' + okta_api_token,
    'Accept': 'application/json'
}
session = requests.Session()
session.headers.update(headers)

def list_assignments(appid):

    url = f"{base_url}/api/v1/apps/{appid}/users"

    while url:

        response = session.get(url)
        response.raise_for_status()

        users = response.json()

        for user in users:
            assignment_type = user['scope']
            uid = user['id']
            if assignment_type == 'GROUP':
                print("we have a group assignment")
                change_assignment(appid, uid, user)
    
        url = response.links.get('next', {}).get('url')

def change_assignment(appid, userid, user):

    url = f"{base_url}/api/v1/apps/{appid}/users/{userid}"
    user['scope'] = 'USER'
    response = session.post(url, json=user)
    response.raise_for_status()
    assignment = response.json()
    print(assignment)


if __name__ == '__main__':

    for appid in appids:
        list_assignments(appid)
