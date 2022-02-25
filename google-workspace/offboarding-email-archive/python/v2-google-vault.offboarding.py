#!/usr/bin/env python3
import requests
import json
import sys
#get the secrets from your Google Cloud project, use the Oauth2 Playground for your refresh token
client_id=sys.argv[1]
client_secret=sys.argv[2]
refresh_token=sys.argv[3]
userList=["user"]

def generate_vault_access_token(client_id,client_secret,refresh_token):
    try:
        url = "https://www.googleapis.com/oauth2/v4/token"

        body = json.dumps({
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token"
        })

        headers = {
        "Accept" : "application/json",
        "Content-Type" : "application/json",
        }

        response = requests.request(
        "POST",
        url,
        headers=headers,
        data=body
        )

        jsonContent = json.loads(response.text)
        vaultAccessToken = jsonContent["access_token"]
        return vaultAccessToken
    except:
        print("\033[1m"+"Issue Occured with generating Google Vault Access Token"+"\033[0m")
        sys.exit(1)

accessToken=generate_vault_access_token(client_id,client_secret,refresh_token)