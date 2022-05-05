#!/usr/bin/env python3
import requests
import shutil

client_id=""
client_secret=""

def get_token(client_id,client_secret):

    body="client_id="+client_id+"&client_secret="+client_secret

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }

    url="https://api.crowdstrike.com/oauth2/token"

    response = requests.post(url, headers=headers, data=body)
    response.raise_for_status

    api_response=response.json()
    access_token=api_response["access_token"]

    return access_token

def get_sensor_version_policy():

    url="https://api.crowdstrike.com/policy/combined/sensor-update/v2?filter=created_timestamp:'$somefql'"
    
    response = session.get(url)
    response.raise_for_status

    api_response=response.json()
    sensor_version=api_response["resources"][0]["settings"]["sensor_version"]
    print("Sensor Version from policy is "+sensor_version)
    return sensor_version

def get_sha256(sensor_version):

    url=f"https://api.crowdstrike.com/sensors/combined/installers/v1?filter=version:%27{sensor_version}%27"

    response = session.get(url)
    response.raise_for_status

    api_response=response.json()
    sha256=api_response["resources"][0]["sha256"]
    print(f"SHA256 of sensor {sensor_version} is {sha256}")
    return sha256

def download_Sensor(sha_256,sensorVersion):

    parent_dir="downloads"
    fileName=f"{parent_dir}/{sensorVersion}.pkg"

    url=f"https://api.crowdstrike.com/sensors/entities/download-installer/v1?id={sha_256}"

    with session.get(url, stream=True) as r:
        with open(fileName, 'wb') as f:
            shutil.copyfileobj(r.raw, f, length=16*1024*1024)
            r.raise_for_status

    print(f"Downloaded Crowdstrike Falcon Sensor {sensorVersion} to {fileName}")
    return fileName

access_token=get_token(client_id,client_secret)

headers = {
    "Accept": "application/json",
    "Authorization": "Bearer " + access_token,
    "Content-Type": "application/json"
}

session = requests.Session()
session.headers.update(headers)

sensor_version=get_sensor_version_policy()
sha_256=get_sha256(sensor_version)
download_Sensor(sha_256,sensor_version)