#!/usr/bin/env python3
import requests
import csv
import sys
import os

google_cloud_client_id=os.environ.get("google_cloud_client_id")
google_cloud_client_secret=os.environ.get("google_cloud_client_secret")
google_cloud_refresh_token=os.environ.get("google_cloud_refresh_token")

google_api_base_url="https://www.googleapis.com"

path=os.path.abspath(os.path.dirname(__file__))

filename=f"{path}/google-drive-files.csv"

data={
    "id": None,
    "name": None,
    "size": None
}

def generate_google_access_token(google_cloud_client_id,google_cloud_client_secret,google_cloud_refresh_token):

        url = f"{google_api_base_url}/oauth2/v4/token"

        headers = {
        "Accept" : "application/json",
        }

        body = {
        "client_id": google_cloud_client_id,
        "client_secret": google_cloud_client_secret,
        "refresh_token": google_cloud_refresh_token,
        "grant_type": "refresh_token"
        }

        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()

        api_response = response.json()
        access_token = api_response["access_token"]

        return access_token

def list_files(url):

    while url :
        response = google_drive_session.get(url)
        response.raise_for_status()
        api_response=response.json()
        print(response.status_code)
        files=api_response["files"]

        for file in files:

            id=file["id"]
            name=file["name"]
            try:
                size=file["size"]
            except:
                size=None
            data["id"]=id
            data["name"]=name
            data["size"]=size

            update_csv(data)

        try:
            next_page_token=api_response["nextPageToken"]
        except Exception as e:
            print(f"Key nextPageToken not found, last request url was {url}")
            sys.exit(1)
        if next_page_token:
            url=f"{google_api_base_url}/drive/v3/files?q=trashed=true&fields=nextPageToken,files(*)&pageToken={next_page_token}"
            list_files(url)
        else:
            None

def make_csv(rows):

    with open(filename, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(rows)

def update_csv(data):
    
    with open(filename, 'a', newline='') as f:
        w = csv.writer(f)
        w.writerow(data.values())

access_token=generate_google_access_token(google_cloud_client_id,google_cloud_client_secret,google_cloud_refresh_token)

headers = {
    "Accept" : "application/json",
    "Authorization": "Bearer " + access_token,
    "Content-type" :  "application/json"
}

google_drive_session = requests.Session()
google_drive_session.headers.update(headers)

url=f"{google_api_base_url}/drive/v3/files?q=trashed=true&fields=nextPageToken,files(*)"

make_csv(data)
list_files(url)