#!/usr/bin/env python3
import requests
import json
import sys
#get the secrets from your Google Cloud project, use the Oauth2 Playground for your refresh token
client_Id=sys.argv[1]
client_Secret=sys.argv[2]
refresh_Token=sys.argv[3]

userList=[""]
adminUsers=[""]

matter={
	"user": "",
	"matterId": "",
	"savedQueryId": "",
	"exportId": ""
}

def generate_Google_Access_Token(client_Id,client_Secret,refresh_Token):

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

def generate_Matter(user,matter,access_Token):

    url = "https://vault.googleapis.com/v1/matters/"

    headers = {
    "Accept" : "application/json",
    "Content-Type" : "application/json",
    "Authorization": "Bearer " + access_Token
    }

    body = json.dumps ({           
    "state": "OPEN",
    "description": "Generated by Python",
    "name": user + "'s archive"
    })

    response = requests.request(
    "POST",
    url,
    headers=headers,
    data=body
    )

    apiResponse = response.json()
    matterId=apiResponse["matterId"]

    matter["user"]=user
    matter["matterId"]=matterId

    return matter

def generate_Search_Query(user,matter,access_Token):

    user=matter["user"]
    matterId=matter["matterId"]

    url = "https://vault.googleapis.com/v1/matters/"+matterId+"/savedQueries"
    
    headers = {
    "Accept" : "application/json",
    "Content-Type" : "application/json",
    "Authorization": "Bearer " + access_Token
    }

    body=json.dumps({
        "displayName": user + "'s email search query",
        "query": {
            "corpus": "MAIL",
            "dataScope": "ALL_DATA",
            "searchMethod": "ACCOUNT",
            "accountInfo": { "emails": [user]},
            "mailOptions": {"excludeDrafts" : "false"},
            "timeZone": "Atlantic/Canary",
            "method": "ACCOUNT"
    }}
    )

    response = requests.request(
    "POST",
    url,
    headers=headers,
    data=body
    )

    apiResponse = response.json()
    savedQueryId=apiResponse["savedQueryId"]

    matter["savedQueryId"]=savedQueryId

    return matter

def generate_Export(user,matter,access_Token):

    user=matter["user"]
    matterId=matter["matterId"]
    savedQueryId=matter["savedQueryId"]

    url = "https://vault.googleapis.com/v1/matters/"+matterId+"/exports"

    headers = {
    "Accept" : "application/json",
    "Content-Type" : "application/json",
    "Authorization": "Bearer " + access_Token
    }

    body = json.dumps(
        {
            "name": user + "'s Export",
            "query": {
                "corpus": "MAIL",
                "dataScope": "ALL_DATA",
                "searchMethod": "ACCOUNT",
                "accountInfo": { "emails": [user]},
                "mailOptions": {"excludeDrafts" : "false"},
                "timeZone": "Atlantic/Canary",
                "method": "Account",
            },
            "exportOptions": {
                "mailOptions": {
                    "exportFormat": "MBOX",
                    "showConfidentialModeContent": "true"
                },
                "region": "any"
                }
            }
    )
    
    response = requests.request(
    "POST",
    url,
    headers=headers,
    data=body
    )

    apiResponse=response.json()
    matterExportId=apiResponse["id"]

    matter["matterExportId"]=matterExportId

    return matter

def set_Vault_Permissions(admin,matter,access_Token):

    matterId=matter["matterId"]

    url = "https://vault.googleapis.com/v1/matters/"+matterId+":addPermissions"

    headers = {
    "Accept" : "application/json",
    "Content-Type" : "application/json",
    "Authorization": "Bearer " + access_Token
    }

    
    body = json.dumps(
    {
        "matterPermission": 
    {
        "role": "COLLABORATOR",
        "accountId": admin
    },
        "sendEmails": "false",
        "ccMe": "false"
    }
    )

    response = requests.request(
    "POST",
    url,
    headers=headers,
    data=body
    )

    apiResponse=response.json()

    return apiResponse

for user in userList:
    access_Token=generate_Google_Access_Token(client_Id,client_Secret,refresh_Token)
    matterStateMatterInfo=generate_Matter(user,matter,access_Token)
    matterStateSavedQueryId=generate_Search_Query(user,matter,access_Token)
    matterStateExportId=generate_Export(user,matter,access_Token)
    for adminId in adminUsers:
        matterStateAdminPermissions=set_Vault_Permissions(adminId,matter,access_Token)
        print(matterStateAdminPermissions)