#!/usr/bin/env python3
import json
from pydoc import resolve
import requests
import os
from base64 import b64encode
import xml.etree.ElementTree as ET
from json2xml import json2xml
from json2xml.utils import readfromurl, readfromstring, readfromjson
import sys

jamf_api_usermane_test=os.environ['jamf_api_usermane_test']
jamf_api_password_test=os.environ['jamf_api_password_test']
base_url=f"https://changeme.jamfcloud.com"
branch="release"

def make_bearer():

    headers = {
    "Authorization": "Basic {}".format(
        b64encode(bytes(f"{jamf_api_usermane_test}:{jamf_api_password_test}", "utf-8")).decode("ascii")
        )
    }

    url=f"{base_url}/api/v1/auth/token"
    r = requests.post(url,headers=headers)
    r.raise_for_status
    api_response=r.json()

    token=api_response['token']
    expires=api_response['expires']

    return token, expires

def find_installomator_jamf():

    url=f"{base_url}/JSSResource/scripts/name/installomator"
    r=jamf_session.get(url)
    r.raise_for_status
    api_response=r.json()

    try:
        jamf_script_name=api_response['script']['name']
        jamf_script_id=api_response['script']['id']
        jamf_script_content=api_response['script']['script_contents']
    except Exception as e:
        print(f"Couldn't find keys for script.name or script.id ")
        sys.exit(1)

    parent_dir="downloads"
    os.makedirs(parent_dir, exist_ok=True)
    file_name=f"{parent_dir}/installomator-jamf.sh"

    with open(file_name, 'w') as f:
        f.write(jamf_script_content)
    
    return jamf_script_name, jamf_script_id, file_name, api_response

def get_latest_installomator_script_content():

    url="https://raw.githubusercontent.com/Installomator/Installomator/{branch}/Installomator.sh"
    r=requests.get(url)
    r.raise_for_status

    parent_dir="downloads"
    os.makedirs(parent_dir, exist_ok=True)
    file_name=f"{parent_dir}/installomator-github.sh"

    with open(file_name, 'w') as f:
        f.write(r.text)

    return file_name

def get_latest_installomator_release_info():

    url="https://api.github.com/repos/installomator/installomator/releases/latest"
    r=requests.get(url)
    r.raise_for_status
    latest_release_info_version=r.json()['name']
    return latest_release_info_version

def replace_jamf_installomator_script(api_response,github_file_name,jamf_script_id):

    print(github_file_name)
    with open(github_file_name, 'r') as f:
        api_response['script']['script_contents']=f.read()
        del api_response['script']['script_contents_encoded']
        url=f"{base_url}/JSSResource/scripts/id/{jamf_script_id}"
        payload=json2xml.Json2xml(api_response,attr_type=False,root=False).to_xml()
        response=jamf_session.put(url,data=payload.encode('utf-8'))
        print(response.status_code)
        print(payload)
        response.raise_for_status

if __name__ == '__main__':

    token,expires=make_bearer()

    jamf_headers = {
    'Accept': 'application/json' ,
    'Authorization': 'Bearer ' +token
    }

    jamf_session = requests.Session()
    jamf_session.headers.update(jamf_headers)

    jamf_script_name,jamf_script_id,jamf_file_name,api_response=find_installomator_jamf()
    github_file_name=get_latest_installomator_script_content()
    latest_release_info_version=get_latest_installomator_release_info()
    replace_jamf_installomator_script(api_response,github_file_name,jamf_script_id)