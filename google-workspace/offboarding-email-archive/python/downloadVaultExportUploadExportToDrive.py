#!/usr/bin/env python3
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


client_id=sys.argv[1]
client_secret=sys.argv[2]
refresh_token=sys.argv[3]
matterId=sys.argv[4]
exportId=sys.argv[5]
userName=sys.argv[6]

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

        jsonContent = response.json()
        vaultAccessToken = jsonContent["access_token"]
        return vaultAccessToken
    except:
        print("\033[1m"+"Issue Occured with generating Google Vault Access Token"+"\033[0m")
        sys.exit(1)

def get_Export_Status(access_token,matterId,exportId):

    url = "https://vault.googleapis.com/v1/matters/"+matterId+"/exports/"+exportId
    
    headers = {
        "Accept" : "application/json",
        "Content-Type" : "application/json",
        "Authorization": "Bearer " + access_token
    }

    response = requests.request(
    "GET",
    url,
    headers=headers,
    )

    apiResponse=response.json()

    status=apiResponse["status"]

    while status == "IN_PROGRESS":
            response = requests.request(
            "GET",
            url,
            headers=headers,
            )

            apiResponse=response.json()

            status=apiResponse[status]
            print(status)
            time.sleep(90)

    if status == "COMPLETED":
        fileBucketId=apiResponse["cloudStorageSink"]["files"][0]["bucketName"]
        fileNameId=apiResponse["cloudStorageSink"]["files"][0]["objectName"]
        fileSize=apiResponse["cloudStorageSink"]["files"][0]["size"]
        #print(fileBucketId,fileNameId,fileSize)

    return fileBucketId,fileNameId,fileSize

def actually_Download_Export(exportInfo,userName,access_Token):

    fileBucketId,fileNameId,fileSize=exportInfo

    encoded=urllib.parse.quote(fileNameId,safe='')
    download_url="https://storage.googleapis.com/storage/v1/b/"+fileBucketId+"/o/"+encoded+"?alt=media"
    directory=userName
    parent_dir="downloads"
    path = os.path.join(parent_dir, directory)
    os.makedirs(path, exist_ok=True)
    fileName=(path+"/"+userName+"-gmail_export.zip")

    auth={
        "Authorization": "Bearer " + access_Token
    }


    with requests.get(download_url, stream=True,headers=auth) as r:
            PreparedResponse=requests.get
            with open(fileName, 'wb') as f:
                shutil.copyfileobj(r.raw, f, length=16*1024*1024)
    return fileName

def upload_Matter(access_Token,localFileName,userName,folderId):

    remoteFileName=userName+"-gmail_export.zip"

    file_metadata={

        'name': remoteFileName, 
        "parents": 
            [ folderId ]

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
    archiveUserFileId=apiResponse["id"]
    return archiveUserFileId

def create_Folder(access_Token,userName):

    archiveLeaversFolderId="CHANGEME"
        
    folder_metadata = {
    'name' : userName,
    'parents' : [archiveLeaversFolderId],
    'mimeType' : 'application/vnd.google-apps.folder'
    }

    url="https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart&supportsAllDrives=true"

    headers={
        "Authorization": "Bearer " + access_Token
    }
    files = {
        'data': ('metadata', json.dumps(folder_metadata), "application/json; charset=UTF-8"),
        'file': ('mimeType', open(localFileName, "rb"))
    }

    response = requests.post(
        url=url,
        headers=headers,
        files=files,
    )

    apiResponse=response.json()
    archiveUserFolderId=apiResponse["id"]
    return archiveUserFolderId

def delete_localFolderFile(localFileName):

    os.remove(localFileName)
    print(localFileName+" File Deleted")

def notify_User(archiveUserFolderId):

    url="https://drive.google.com/drive/folders/"+archiveUserFolderId
    return url

access_Token=generate_vault_access_token(client_id,client_secret,refresh_token)
exportInfo=get_Export_Status(access_Token,matterId,exportId)
localFileName=actually_Download_Export(exportInfo,userName,access_Token)
archiveUserFolderId=create_Folder(access_Token,userName)
uploaded_File=upload_Matter(access_Token,localFileName,userName,archiveUserFolderId)
delete_localFolderFile(localFileName)
print("Export downloaded to "+localFileName+" and uploaded to "+notify_User(archiveUserFolderId))