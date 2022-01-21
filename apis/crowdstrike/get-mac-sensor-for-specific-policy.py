#!/usr/bin/env python3
import requests
import json
import sys
import shutil

client_id=sys.argv[1]
client_secret=sys.argv[2]

def get_token(client_id,client_secret):

    try:

        body="client_id="+client_id+"&client_secret="+client_secret

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        }

        url="https://api.crowdstrike.com/oauth2/token"

        response = requests.request(
            "POST",
            url,
            headers=headers,
            data=body
        )

        jsonContent=json.loads(response.text)
        accessToken=jsonContent["access_token"]
        return accessToken

    except:
        print("\033[1m"+"Issue Occured with authenticating to Crowdstrike Falcon API"+"\033[0m")
        sys.exit(1)
    
def get_sensor_version_policy(accessToken):
    
    try:

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer '+accessToken
        }

        url="https://api.crowdstrike.com/policy/combined/sensor-update/v2?filter=FQLFORYOURPOLICY"
        
        response = requests.request(
            "GET",
            url,
            headers=headers,
        )

        jsonContent=json.loads(response.text)
        sensorVersion=jsonContent["resources"][0]["settings"]["sensor_version"]
        print("Sensor Version from policy is "+sensorVersion)
        return sensorVersion

    except:
        print("\033[1m"+"Issue Occured with getting Policy & Sensor Version from Crowdstrike Falcon API"+"\033[0m")
        sys.exit(1)

def get_sha256(accessToken,sensorVersion):

    try:

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer '+accessToken
        }

        url="https://api.crowdstrike.com/sensors/combined/installers/v1?filter=version:%27"+sensorVersion+"%27"

        response = requests.request(
                "GET",
                url,
                headers=headers,
        )

        jsonContent=json.loads(response.text)
        sha256=jsonContent["resources"][0]["sha256"]
        print("SHA256 of sensor "+sensorVersion+" is "+sha256)
        return sha256

    except:
        print("\033[1m"+"Issue Occured with getting Policy & Sensor Version from Crowdstrike Falcon API"+"\033[0m")
        sys.exit(1)

def download_Sensor(accessToken,sha256,sensorVersion):

    try:

        fileName="/var/tmp/FalconSensorMacOS-"+sensorVersion+".pkg"
        print(sha256)

        headers = {
            'Authorization': 'Bearer '+accessToken
        }

        url="https://api.crowdstrike.com/sensors/entities/download-installer/v1?id="+sha256

        with requests.get(url, stream=True,headers=headers) as r:
            with open(fileName, 'wb') as f:
                shutil.copyfileobj(r.raw, f, length=16*1024*1024)
        print("Downloaded Crowdstrike Falcon Sensor "+sensorVersion+" to "+fileName)
        return fileName

    except:
        print("\033[1m"+"Issue Occured with downloading sensor from Crowdstrike Falcon API"+"\033[0m")
        sys.exit(1)


accessToken=get_token(client_id,client_secret)
sensorVersion=get_sensor_version_policy(accessToken)
sha256=get_sha256(accessToken,sensorVersion)
download_Sensor(accessToken,sha256,sensorVersion)