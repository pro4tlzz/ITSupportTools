#!/usr/bin/env python3

import requests
from csv import DictReader

# Set these:
base_url = "https://-admin.okta.com"
api_key = os.environ['okta_api_token']
filename = "/Users/Desktop/okta_rules.csv"

headers = {
    'Authorization': 'SSWS ' + api_key,
    'Accept': 'application/json'
}

session = requests.Session()
session.headers.update(headers)

def eval(rule, user):

    payload=[{"type": "urn:okta:expression:1.0", "value": rule, "targets": {"user": user}, "operation": "CONDITION"}]
    print(payload)
    url = f"{base_url}/api/v1/internal/expression/eval"
    response = session.post(url, json=payload)
    response.raise_for_status()

    eval_result = response.json()
    print(eval_result)

def read_csv():

    with open(filename, 'r', encoding='utf-8-sig') as f:
        reader = DictReader(f)
        for row in reader:
            user = row["user"]
            rule = row["rule"]
            eval(rule, user)


if __name__ == '__main__':

    read_csv()
