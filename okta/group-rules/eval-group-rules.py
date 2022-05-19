#!/usr/bin/env python3
import requests
import os
from csv import DictReader

api_key=os.environ['okta_api_token']

headers = {
    'Authorization': 'SSWS ' + api_key,
    'Accept': 'application/json'
}

session = requests.Session()
session.headers.update(headers)

base_url="https://-admin.okta.com"
url=f"{base_url}/api/v1/internal/expression/eval"
uid=''

def eval(rule,uid):

    payload=[{"type":"urn:okta:expression:1.0","value":rule,"targets":{"user":uid},"operation":"CONDITION"}]
    print(payload)
    response=session.post(url,json=payload)
    response.raise_for_status

    api_response=response.json()
    print(api_response)

def read_csv(uid):

    filename="okta_rules.csv"
    with open(filename, 'r', encoding='utf-8-sig') as f:
        reader=DictReader(f)
        for row in reader:
            rule=row["rule"]
            eval(rule,uid)


if __name__ == '__main__':

    read_csv(uid)