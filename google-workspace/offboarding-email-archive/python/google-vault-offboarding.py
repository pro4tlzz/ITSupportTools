#!/usr/bin/env python3
import requests
import json
import sys
#get the secrets from your Google Cloud project, use the Oauth2 Playground for your refresh token
client_id=sys.argv[1]
client_secret=sys.argv[2]
refresh_token=sys.argv[3]
credentials=sys.argv[4]

def get_list_from_file(filename):
    try:
        # open and read the file into list
        with open(filename) as f:
            string_list = f.read().splitlines()
            f.close()
            print(string_list)
            return string_list
    except:
        print("\033[1m"+"Issue Occured with obtaining list from file"+"\033[0m")
        sys.exit(1)

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

def generate_matter(leaver_user,vaultAccessToken):
    try:
        matterList = []
        for user in leaver_user:
            url = "https://vault.googleapis.com/v1/matters/"

            headers = {
            "Accept" : "application/json",
            "Content-Type" : "application/json",
            "Authorization": "Bearer " + vaultAccessToken
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

            jsonContent = json.loads(response.text)
            matterID=jsonContent["matterId"]
            #print("Matter ID for " + user + " is " + matterID)
            print(jsonContent)

            matterList.append({
                "matterInstance": {
                    "user": user,
                    "userInfo": {
                        "matterID": matterID,
                        "savedQueryID": "",
                        "matterExportID": ""
                }
                
                }
            })

        return matterList
    except:
        print("\033[1m"+"Issue Occured with generating Google Vault Matter"+"\033[0m")
        sys.exit(1)

def generate_search_query(matterList,vaultAccessToken):
    try:
        for matter in matterList:
            matterList = []
            for key, value in matter.items():
                user=(matter['matterInstance']['user'])
                matterID=(matter['matterInstance']['userInfo']['matterID'])
                url = "https://vault.googleapis.com/v1/matters/"+matterID+"/savedQueries"
                
                headers = {
                "Accept" : "application/json",
                "Content-Type" : "application/json",
                "Authorization": "Bearer " + vaultAccessToken
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
                jsonContent = json.loads(response.text)
                print(jsonContent)
                savedQueryID=jsonContent["savedQueryId"]
                #print("savedQueryId for " + user + " is " + savedQueryID + " matterID is " + matterID)

                matterList.append({
                    "matterInstance": {
                        "user": user,
                        "userInfo": {
                            "matterID": matterID,
                            "savedQueryID": savedQueryID,
                            "matterExportID": ""
                    }
                    
                    }
                }
                )
        return matterList
    except:
        print("\033[1m"+"Issue Occured with generating Google Vault Matter Search Query"+"\033[0m")
        sys.exit(1)

def generate_export(savedQueryID,matterList,vaultAccessToken):
    try:
        for matter in matterList:
            matterList = []
            for key, value in matter.items():
                user=(matter['matterInstance']['user'])
                matterID=(matter['matterInstance']['userInfo']['matterID'])
                savedQueryID=(matter['matterInstance']['userInfo']['savedQueryID'])
                print(user,matterID,savedQueryID)
                url = "https://vault.googleapis.com/v1/matters/",matterID,"/exports"
                url=''.join(url)
                print(url)
                headers = {
                "Accept" : "application/json",
                "Content-Type" : "application/json",
                "Authorization": "Bearer " + vaultAccessToken
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
                jsonContent = json.loads(response.text)
                matterExportID=jsonContent["id"]
                print(jsonContent)
                #print("matterExportID for " + user + " is " + matterExportID  + " searchQueryID is " + savedQueryID + " matterID is " + matterID)
                matterList.append({
                    "matterInstance": {
                        "user": user,
                        "userInfo": {
                            "matterID": matterID,
                            "savedQueryID": savedQueryID,
                            "matterExportID": matterExportID
                    }
                    
                    }
                }
                )
        return matterList
    except:
        print("\033[1m"+"Issue Occured with generating Google Vault Matter Export"+"\033[0m")
        sys.exit(1)

def set_matter_permissions(adminAccountIDs,matterList,vaultAccessToken):
    try:
        for matter in matterList:
            matterList = []
            for key, value in matter.items():
                for each in adminAccountIDs:
                    print(each)
                    print(matterList)
                    matterID=(matter['matterInstance']['userInfo']['matterID'])
                    url = "https://vault.googleapis.com/v1/matters/",matterID,":addPermissions"
                    print(url)
                    url=''.join(url)
                    print(url)
                    headers = {
                    "Accept" : "application/json",
                    "Content-Type" : "application/json",
                    "Authorization": "Bearer " + vaultAccessToken
                    }

                    body = json.dumps(
                        {
                            "matterPermission": 
                        {
                            "role": "COLLABORATOR",
                            "accountId": each
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
                    jsonContent = (response.text)
                    print(jsonContent)
        return each
    except:
        print("\033[1m"+"Issue Occured with setting Google Vault Matter permissions"+"\033[0m")
        sys.exit(1)

def generate_links_notify(matterList,credentials):
    try:
        for matter in matterList:
            matterList = []
            user=(matter['matterInstance']['user'])
            matterID=(matter['matterInstance']['userInfo']['matterID'])
            savedQueryID=(matter['matterInstance']['userInfo']['savedQueryID'])
            exportID=(matter['matterInstance']['userInfo']['matterExportID'])
            print("************************************************************************************************************************************************************************************************************************************************************")
            print("Export Link for " + user + " https://vault.google.com/matter/"+ matterID + "/exports")
            print("Matter Link for " + user + " https://vault.google.com/matter/"+ matterID)
            print("Search Query Link for " + user + " https://vault.google.com/matter/"+ matterID + "/search")
            print("************************************************************************************************************************************************************************************************************************************************************")
            url=credentials
            body=json.dumps(
                {
                    'text': "Export Link for " + user + " https://vault.google.com/matter/"+ matterID + "/exports"
                }
                )
            headers={
            'Content-type': 'application/json'
            }
            response = requests.request(
            "POST",
            url,
            data=body,
            )
    except:
        print("\033[1m"+"Issue Occured with generating links for notifications"+"\033[0m")
        sys.exit(1)

vaultAccessToken=generate_vault_access_token(client_id,client_secret,refresh_token)
input_filename='.txt'
leaver_user=get_list_from_file(input_filename)
adminAccountIDs='.txt'
admin_users=get_list_from_file(adminAccountIDs)
matter=generate_matter(leaver_user,vaultAccessToken)
savedQueryID=generate_search_query(matter,vaultAccessToken)
matterExportID=generate_export(savedQueryID,matter,vaultAccessToken)
last_admin=set_matter_permissions(admin_users,matter,vaultAccessToken)
generate_links_notify(matter,credentials)