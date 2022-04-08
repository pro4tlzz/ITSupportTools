#!/usr/bin/env python3
from urllib import request
import requests
import json
import sys

client_Id=sys.argv[1]
client_Secret=sys.argv[2]
refresh_Token=sys.argv[3]

def generate_Google_Access_Token(client_Id,client_Secret,refresh_Token):

        url = "https://www.googleapis.com/oauth2/v4/token"

        headers = {
        "Accept" : "application/json",
        }

        body = {
        "client_id": client_Id,
        "client_secret": client_Secret,
        "refresh_token": refresh_Token,
        "grant_type": "refresh_token"
        }

        response = requests.request(
        "POST",
        url,
        headers=headers,
        json=body
        )

        response.raise_for_status()

        apiResponse = response.json()
        access_Token = apiResponse["access_token"]

        return access_Token

def list_files(url,headers):

    session = requests.Session()
    session.headers.update(headers)
    response = session.get(url)
    response.raise_for_status()
    apiResponse=response.json()
    nextPageToken=apiResponse["nextPageToken"]
    print(nextPageToken)
    if nextPageToken:
        url=f"https://www.googleapis.com/drive/v3/files&pageToken={nextPageToken}"
        print(url)
        list_files(url,headers)




access_token=generate_Google_Access_Token(client_Id,client_Secret,refresh_Token)

headers = {
    "Accept" : "application/json",
    "Authorization": "Bearer " + access_token,
    "Content-type" :  "application/json"
}
url="https://www.googleapis.com/drive/v3/files"
list_files(url,headers)