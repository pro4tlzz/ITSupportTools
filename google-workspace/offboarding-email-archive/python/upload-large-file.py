#!/usr/bin/env python3
from pydoc import cli
from urllib import request
import requests
import json
import sys
import os


#get the secrets from your Google Cloud project, use the Oauth2 Playground for your refresh token
client_Id="123"
client_Secret="123"
refresh_Token="123"

def generate_Google_Access_Token(client_Id,client_Secret,refresh_Token):

    try:

        url = "https://www.googleapis.com/oauth2/v4/token"

        headers = {
        "Accept" : "application/json",
        "Content-Type" : "application/json",
        }

        body = json.dumps({
        "client_id": client_Id,
        "client_secret": client_Secret,
        "refresh_token": refresh_Token,
        "grant_type": "refresh_token"
        })

        response = requests.request(
        "POST",
        url,
        headers=headers,
        data=body
        )

        apiResponse = response.json()
        access_Token = apiResponse["access_token"]
        return access_Token

    except:

        print("\033[1m"+"Issue Occured with generating Google Vault Access Token"+"\033[0m")
        sys.exit(1)

def upload(access_token):

 localFileName="test.mkv"

 
 with open(localFileName, 'rb') as file_to_upload:
            size = os.path.getsize(localFileName)
            headers = {
                "Content-Type" : "video/mkv",
                "Authorization" : "Bearer " +  access_token,
                "Content-length": str(size)
            }
            url = "https://www.googleapis.com/upload/drive/v3/files?uploadType=media"
            r = requests.post(
                url=url,
                headers=headers,
                data=file_to_upload,
            )
            print(r.content)
            id=r.json()["id"]
            print(id)
            url=f"https://www.googleapis.com/drive/v3/files/{id}?addParents=123"
            print(url)
            headers = {
                "Authorization" : "Bearer " +  access_token,
            }
            body={
                "name" : "test.mkv"
            }
            r = requests.patch(
                url=url,
                headers=headers,
                json=body
            )
            print(r.content)


access_token=generate_Google_Access_Token(client_Id,client_Secret,refresh_Token)
upload(access_token)
