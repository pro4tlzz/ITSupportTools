#!/usr/bin/env python3
import requests
import json
import urllib
import shutil
import time
import os
import mimetypes

google_cloud_client_id=os.environ['google_cloud_client_id']
google_cloud_client_secret=os.environ['google_cloud_client_secret']
google_cloud_refresh_token=os.environ['google_cloud_refresh_token']

user_list=["CHANGEME"]
admin_users=["CHANGEME"]
root_folder_id="CHANGEME"

matter={
	"user": ""
}

google_oauth_base_url="https://www.googleapis.com"
google_vault_base_url="https://vault.googleapis.com"
google_drive_base_url="https://www.googleapis.com"
google_storage_base_url="https://storage.googleapis.com"

def generate_google_access_token(google_cloud_client_id,google_cloud_client_secret):

        url = f"{google_oauth_base_url}/oauth2/v4/token"

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

def generate_matter(user,matter):

        url = f"{google_vault_base_url}/v1/matters/"

        body = {           
        "state": "OPEN",
        "description": "Generated by Python",
        "name": user + "'s archive"
        }

        response = session.post(url, json=body)
        response.raise_for_status()

        api_response = response.json()
        matter_id=api_response["matterId"]

        matter["user"]=user
        matter["matter_id"]=matter_id
        return matter

def generate_search_query(user,matter):

        user=matter["user"]
        matter_id=matter["matter_id"]

        url = f"{google_vault_base_url}/v1/matters/{matter_id}/savedQueries"

        body = {
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

        response = session.post(url, json=body)
        response.raise_for_status()

        api_response = response.json()
        saved_query_id=api_response["savedQueryId"]

        matter["saved_query_id"]=saved_query_id
        return matter

def generate_export(user,matter):

        user=matter["user"]
        matter_id=matter["matter_id"]

        url = f"{google_vault_base_url}/v1/matters/{matter_id}/exports"

        body = {
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
        
        response = session.post(url, json=body)
        response.raise_for_status()

        api_response=response.json()
        export_id=api_response["id"]

        matter["export_id"]=export_id
        return matter

def set_vault_permissions(admin,matter):

        matter_id=matter["matter_id"]

        url = f"{google_vault_base_url}/v1/matters/{matter_id}:addPermissions"

        body = {
            "matterPermission": 
        {
            "role": "COLLABORATOR",
            "accountId": admin
        },
            "sendEmails": "false",
            "ccMe": "false"
        }

        response = session.post(url, json=body)
        response.raise_for_status()

        api_response=response.json()
        return api_response

def get_export_status(matter):

        matter_id=matter["matter_id"]   

        url = f"{google_vault_base_url}/v1/matters/{matter_id}/exports/"
        
        response = session.get(url)
        response.raise_for_status()

        api_response=response.json()
        status=api_response["exports"][0]["status"]

        while status == "IN_PROGRESS":

                response = session.get(url)
                response.raise_for_status()

                api_response=response.json()
                status=api_response["exports"][0]["status"]
                print("Export is not completed yet. Going to sleep for 30 seconds, then I will check the export status again")
                time.sleep(30)

        if status == "COMPLETED":

            cloud_storage_sink=api_response["exports"][0]["cloudStorageSink"]["files"]

        return cloud_storage_sink

def download_export(object_name,bucket_name,user):
        
        encoded=urllib.parse.quote(object_name,safe='')
        download_url=f"{google_storage_base_url}/storage/v1/b/{bucket_name}/o/{encoded}?alt=media"
        directory=user
        parent_dir="downloads"
        path = os.path.join(parent_dir, directory)
        os.makedirs(path, exist_ok=True)
        last = object_name.split("/")[-1]
        file_name=(path+"/"+last)

        with session.get(download_url, stream=True) as r:
                with open(file_name, 'wb') as f:
                    shutil.copyfileobj(r.raw, f, length=16*1024*1024)
                    r.raise_for_status()

        return file_name

def create_folder(user,root_folder_id,access_token):
            
        folder_metadata = {
        'name' : user,
        'parents' : [root_folder_id],
        'mimeType' : 'application/vnd.google-apps.folder'
        }

        url=f"{google_drive_base_url}/upload/drive/v3/files?uploadType=multipart&supportsAllDrives=true"

        headers={
            "Authorization": "Bearer " + access_token
        }

        files = {
            'data': ('metadata', json.dumps(folder_metadata), "application/json; charset=UTF-8"),
        }

        response = requests.post(url=url, headers=headers, files=files)
        response.raise_for_status()

        api_response=response.json()
        print(api_response)
        archive_user_folder_id=api_response["id"]
        return archive_user_folder_id

def upload_matter(local_file_name,archive_user_folder_id,access_token):

        absolute_file_name=local_file_name.split("/")[-1]

        file_metadata={

            'name': absolute_file_name, 
            "parents": 
                [ archive_user_folder_id ]

            }

        url=f"{google_drive_base_url}/upload/drive/v3/files?uploadType=multipart&supportsAllDrives=true"

        headers={
            "Authorization": "Bearer " + access_token
        }

        with open(local_file_name, 'rb') as file_to_upload:
            type=mimetypes.guess_type(local_file_name,strict=True)
            files = {
            'data': ('metadata', json.dumps(file_metadata), "application/json; charset=UTF-8"),
            'file': ('mimeType', file_to_upload)
                }
            response = requests.post(url=url, headers=headers, files=files)
            response.raise_for_status()

        api_response=response.json()
        print(api_response)
        archive_user_file_id=api_response["id"]
        return archive_user_file_id

def delete_local_folder_file(local_file_name):

        os.remove(local_file_name)
        print(local_file_name+" File Deleted")

def notify_user(archiveUserFolderId):

        url=f"https://drive.google.com/drive/folders/{archiveUserFolderId}"
        return url

for user in user_list:

    access_token=generate_google_access_token(google_cloud_client_id,google_cloud_client_secret)

    headers = {
        "Accept" : "application/json",
        "Content-Type" : "application/json",
        "Authorization": "Bearer " + access_token
    }

    session = requests.Session()
    session.headers.update(headers)

    matter_state_matter_info=generate_matter(user,matter)

    matter_state_saved_query_id=generate_search_query(user,matter)

    matter_state_export_id=generate_export(user,matter)

    archive_user_folder_id=create_folder(user,root_folder_id,access_token)
    
    export_info=get_export_status(matter_state_export_id)

    for export in export_info:

        object_name=export["objectName"]
        bucket_name=export["bucketName"]
        size=export["size"]
        md5_hash=export["md5Hash"]
	
        access_token=generate_google_access_token(google_cloud_client_id,google_cloud_client_secret)
	
        headers = {
		"Accept" : "application/json",
		"Content-Type" : "application/json",
		"Authorization": "Bearer " + access_token
    	}
		
        session.headers.update(headers)

        local_file_name=download_export(object_name,bucket_name,user)

        uploaded_File=upload_matter(local_file_name,archive_user_folder_id,access_token)

        delete_local_folder_file(local_file_name)

    print("Export uploaded to "+notify_user(archive_user_folder_id))

    print(matter)

    for admin in admin_users:

        matterStateAdminPermissions=set_vault_permissions(admin,matter)
