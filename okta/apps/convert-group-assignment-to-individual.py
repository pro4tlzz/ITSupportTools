#!/usr/bin/env python3
import requests
import os

okta_api_token_test=os.environ['okta_api_token_test']

headers = {
    'Authorization': 'SSWS ' + okta_api_token_test,
    'Accept': 'application/json'
}

session = requests.Session()
session.headers.update(headers)

base_url="https://changeme.okta.com"
apps=['changeme']

def list_assignments(app):

    url=f"{base_url}/api/v1/apps/{app}/users"

    while url:

        response=session.get(url)
        response.raise_for_status

        api_response=response.json()

        for user in api_response:
            assignment_type=user['scope']
            uid=user['id']
            if assignment_type == 'GROUP':
                print(f"we have a group assignment")
                change_assignment(app,uid,user)
    
        next = response.links.get('next')
        url = next['url'] if next else None

def change_assignment(app,user,profile):

    url=f"{base_url}/api/v1/apps/{app}/users/{user}"
    profile['scope']='USER'
    payload=profile
    response=session.post(url,json=payload)
    response.raise_for_status
    api_response=response.json()
    print(api_response)


if __name__ == '__main__':

    for app in apps:
        list_assignments(app)