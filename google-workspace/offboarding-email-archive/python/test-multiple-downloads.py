k#!/usr/bin/env python3
from ctypes import sizeof
from email import header
from hashlib import md5
from urllib import request
import requests
import json
import sys
from requests.utils import requote_uri
from urllib.parse import urlencode, quote_plus
import urllib
import shutil
import time
import os


#get the secrets from your Google Cloud project, use the Oauth2 Playground for your refresh token
client_Id=""
client_Secret=""
refresh_Token=""

userList=[""]
adminUsers=[""]
rootFolderId=""

matter={
	"user": "",
	"matterId": "",
	"savedQueryId": "",
	"exportId": ""
}

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


def get_Export_Status(matterId,headers):

    try:

        url = "https://vault.googleapis.com/v1/matters/"+matterId+"/exports/"
        
        response = requests.request(
        "GET",
        url,
        headers=headers,
        )

        apiResponse=response.json()
        status=apiResponse["exports"][0]["status"]

        while status == "IN_PROGRESS":

                response = requests.request(
                "GET",
                url,
                headers=headers,
                )

                apiResponse=response.json()
                status=apiResponse["exports"][0]["status"]
                print("Export is not completed yet. Going to sleep for 30 seconds, then I will check the export status again")
                time.sleep(30)

        if status == "COMPLETED":
            cloudStorageSink=apiResponse["exports"][0]["cloudStorageSink"]["files"]
        return cloudStorageSink

    except:

        print("\033[1m"+"Issue Occured with status of Google Vault Export"+"\033[0m")
        sys.exit(1)

def download_Export(objectName,bucketName,size,md5Hash,header,user):

    try:

        encoded=urllib.parse.quote(objectName,safe='')
        download_url="https://storage.googleapis.com/storage/v1/b/"+bucketName+"/o/"+encoded+"?alt=media"
        directory=user
        parent_dir="downloads"
        path = os.path.join(parent_dir, directory)
        os.makedirs(path, exist_ok=True)
        last = objectName.split("/")[-1]
        print(last)
        fileName=(path+"/"+last)

        with requests.get(download_url, stream=True,headers=headers) as r:
                PreparedResponse=requests.get
                with open(fileName, 'wb') as f:
                    shutil.copyfileobj(r.raw, f, length=16*1024*1024)

        return fileName

    except:

        print("\033[1m"+"Issue Occured with downloading Google Vault Export"+"\033[0m")
        sys.exit(1)


def create_Folder(user,rootFolderId,access_Token):

    try:
            
        folder_metadata = {
        'name' : user,
        'parents' : [rootFolderId],
        'mimeType' : 'application/vnd.google-apps.folder'
        }

        url="https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart&supportsAllDrives=true"

        headers={
            "Authorization": "Bearer " + access_Token
        }

        files = {
            'data': ('metadata', json.dumps(folder_metadata), "application/json; charset=UTF-8"),

        }

        response = requests.post(
            url=url,
            headers=headers,
            files=files,
        )

        apiResponse=response.json()
        print(apiResponse)
        archiveUserFolderId=apiResponse["id"]
        return archiveUserFolderId

    except:

        print("\033[1m"+"Issue Occured with creating Google Drive folder"+"\033[0m")
        sys.exit(1)    

def upload_Matter(user,localFileName,archiveUserFolderId,access_Token):

    try:

        l=localFileName.split("/")[-1]
        print(l)

        file_metadata={

            'name': l, 
            "parents": 
                [ archiveUserFolderId ]

            }

        url="https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart&supportsAllDrives=true"

        headers={
            "Authorization": "Bearer " + access_Token
        }

        files = {
            'data': ('metadata', json.dumps(file_metadata), "application/json; charset=UTF-8"),
            'file': ('mimeType', open(localFileName, "rb"))
        }

        response = requests.post(
            url=url,
            headers=headers,
            files=files,
        )

        apiResponse=response.json()
        print(apiResponse)
        archiveUserFileId=apiResponse["id"]
        return archiveUserFileId

    except:

        print("\033[1m"+"Issue Occured with uploading Google Vault export to Google Drive"+"\033[0m")
        sys.exit(1)    

def delete_localFolderFile(localFileName):

    try:

        os.remove(localFileName)
        print(localFileName+" File Deleted")

    except:

        print("\033[1m"+"Issue Occured with deleting local file"+"\033[0m")
        sys.exit(1)    

def notify_User(archiveUserFolderId):

    try:

        url="https://drive.google.com/drive/folders/"+archiveUserFolderId
        return url

    except:

        print("\033[1m"+"Issue Occured with composing URL Notification for Export in Google Drive"+"\033[0m")
        sys.exit(1)    


access_Token=generate_Google_Access_Token(client_Id,client_Secret,refresh_Token)
headers = {
    "Accept" : "application/json",
    "Content-Type" : "application/json",
    "Authorization": "Bearer " + access_Token
}
exportList=get_Export_Status("exportid",headers)
archiveUserFolderId=create_Folder("user",rootFolderId,access_Token)


count=0
for each in exportList:
    count+=1
    objectName=each["objectName"]
    bucketName=each["bucketName"]
    size=each["size"]
    md5Hash=each["md5Hash"]
    #print(objectName,bucketName,size,md5Hash)
    localFileName=download_Export(objectName,bucketName,size,md5Hash,header,"user")
    print(localFileName)
    uploaded_File=upload_Matter("user@domain.com",localFileName,archiveUserFolderId,access_Token)
    delete_localFolderFile(localFileName)
    print("Export downloaded to "+localFileName+" and uploaded to "+notify_User(archiveUserFolderId))
    print(matter)
