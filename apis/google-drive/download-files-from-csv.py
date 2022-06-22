#!/usr/bin/env python3
import requests
from csv import DictReader
import shutil
import os

google_cloud_client_id=os.environ.get["google_cloud_client_id"]
google_cloud_client_secret=os.environ.get["google_cloud_client_secret"]
google_cloud_refresh_token=os.environ.get["google_cloud_refresh_token"]

google_api_base_url="https://www.googleapis.com"

path=os.path.abspath(os.path.dirname(__file__))
csv_file="files-to-download.csv"
filename=os.path.join(path,csv_file)

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

def read_csv():

    with open(filename, 'r', encoding='utf-8-sig') as f:
        reader=DictReader(f)
        for row in reader:
            id=row["id"]
            name=row["name"]
            file=id,name
            download_file_name=download_file(file)
            print(f"{download_file_name} with id {id} has been downloaded")

def download_file(file):

    id,name=file
    url=f"{google_api_base_url}/drive/v2/files/{id}?alt=media"
    with google_drive_session.get(url, stream=True) as r:
        download_file_name=os.path.join(path,name)
        with open(download_file_name, 'wb') as f:
            shutil.copyfileobj(r.raw, f, length=16*1024*1024)
            r.raise_for_status()

    return download_file_name

access_token=generate_google_access_token(google_cloud_client_id,google_cloud_client_secret,google_cloud_refresh_token)


headers = {
    "Accept" : "application/json",
    "Authorization": "Bearer " + access_token,
    "Content-type" :  "application/json"
}

google_drive_session = requests.Session()
google_drive_session.headers.update(headers)

read_csv()