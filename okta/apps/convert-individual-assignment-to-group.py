#!/usr/bin/env python3

import requests
import os
import time

# Set these:
okta_api_token = os.environ['okta_api_token']
base_url = "https://-test-admin.okta.com"
appids = ['$appidlist']

headers = {
    'Authorization': 'SSWS ' + okta_api_token,
    'Accept': 'application/json'
}
session = requests.Session()
session.headers.update(headers)

def convert_assignments(appid):

    url = f"{base_url}/api/v1/appAssignments/instance/{appid}/async/convertAll"
    response = session.post(url)
    response.raise_for_status()

    convert_result = response.json()
    print(convert_result)

    timer = 2
    status = None
    while status != 'COMPLETED':

        response = session.get(url)
        response.raise_for_status()

        convert_result = response.json()
        status = convert_result['status']
        print(convert_result)
        print(f"Going to sleep for {timer}")
        time.sleep(timer)
        timer = timer*2

if __name__ == '__main__':

    for appid in appids:
        convert_assignments(appid)
