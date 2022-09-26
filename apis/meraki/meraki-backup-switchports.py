#!/usr/bin/env python
import requests
import os
import json

meraki_api_key=os.environ['meraki_api_key']
meraki_snmp_reporting_key=os.environ['meraki_snmp_reporting_key']

meraki_headers = {
    'X-Cisco-Meraki-API-Key': meraki_api_key,
    'Accept': 'application/json'
}

meraki_session = requests.Session()
meraki_session.headers.update(meraki_headers)

meraki_base_url="https://api.meraki.com"
meraki_organisation=""
url=f"{meraki_base_url}/api/v1/organizations/{meraki_organisation}/networks"

def get_networks(url):

    response = meraki_session.get(url)
    response.raise_for_status
    networks=response.json()

    for network in networks:
        network_id=network['id']
        name=network['name']
        get_devices(network_id)

def get_devices(network_id):

    url=f"{meraki_base_url}/api/v1/networks/{network_id}/devices"
    response = meraki_session.get(url)
    response.raise_for_status
    devices=response.json()

    for device in devices:
        serial=device['serial']
        model=device['model']   
        name=device['name']
        if "MS" in model:
            print(serial,model)
            data=get_device_switch_ports(serial)
            write_file(name,data)

def get_device_switch_ports(serial):

    url=f"{meraki_base_url}/api/v1/devices/{serial}/switch/ports"
    response = meraki_session.get(url)
    response.raise_for_status
    switch_ports=response.json()
    print(switch_ports,response.status_code)
    return switch_ports

def write_file(name,data):

  with open(f"{name}.json", 'w') as f:
    json.dump(data, f, ensure_ascii=False)

if __name__ == '__main__':

    get_networks(url)