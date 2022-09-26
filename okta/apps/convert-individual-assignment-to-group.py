#!/usr/bin/env python3
import requests
import os
import time

okta_api_token_test=os.environ['okta_api_token_test']

headers = {
    'Authorization': 'SSWS ' + okta_api_token_test,
    'Accept': 'application/json'
}

session = requests.Session()
session.headers.update(headers)

base_url="https://-test-admin.okta.com"
apps=['$appidlist']

def convert_assignments(app):

    url=f"{base_url}/api/v1/appAssignments/instance/{app}/async/convertAll"
    response=session.post(url)
    response.raise_for_status

    convert_result=response.json()
    print(convert_result)

    timer=2

    while url:

        response=session.get(url)
        response.raise_for_status

        convert_result=response.json()
        status=convert_result['status']
        print(convert_result)
        print(f"Going to sleep for {timer}")
        time.sleep(timer)
        timer=timer*2
        if status == 'COMPLETED':
            url = None

if __name__ == '__main__':

    for app in apps:
        convert_assignments(app)