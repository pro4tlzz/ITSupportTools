#!/usr/bin/env python3
import requests
import sys

client_id=""
client_secret=""
refresh_token=""

domain="domain.com"
url=f"https://admin.googleapis.com/admin/directory/v1/users?domain={domain}&query=isSuspended=false"

def generate_google_access_token(client_id,client_secret,refresh_token):

        url = "https://www.googleapis.com/oauth2/v4/token"

        data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token"
        }

        headers = {
        "Accept" : "application/json",
        "Content-Type" : "application/json",
        }

        response = requests.post(url, headers=headers, json=data)

        api_response = response.json()
        access_token = api_response["access_token"]
        return access_token

def paginate(url):

    while url:
        
        response = session.get(url)
        response.raise_for_status
        api_response=response.json()

        users=api_response["users"]
        for user in users:
            primary_email=user["primaryEmail"]
            get_user_id(primary_email)

        try:
            nextpagetoken=api_response["nextPageToken"]
        except:
            print("nextPageToken is null so exiting, goodbye")
            sys.exit(0)

        next_page=url.split("&pageToken=")[0]
        next_url=f"{next_page}&pageToken={nextpagetoken}"
        print(next_page,next_url)

        paginate(next_url)

def get_user_id(primaryEmail):

    url = f"https://admin.googleapis.com/admin/directory/v1/users/{primaryEmail}"
    response = session.get(url)
    response.raise_for_status
    api_response=response.json()
    id=api_response["id"]
    print(id,primaryEmail)

access_token=generate_google_access_token(client_id,client_secret,refresh_token)

session = requests.Session()
headers = {
        "Accept" : "application/json",
        "Content-Type" : "application/json",
        "Authorization": "Bearer "+access_token
}
session.headers.update(headers)

paginate(url)