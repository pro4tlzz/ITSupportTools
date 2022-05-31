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
meraki_organisation="$someorg"
url=f"{meraki_base_url}/api/v1/organizations/{meraki_organisation}/networks"

def get_networks(url):

    response = meraki_session.get(url)
    response.raise_for_status
    api_response=response.json()

    for network in api_response:
        id=network['id']
        name=network['name']
        current_snmp_settings=get_snmp_setting(id)
        if 'errors' in current_snmp_settings:
            print(f"No SNMP Config Possible for network {id} {name}")
        else:
            write_file(name,current_snmp_settings)
            set_snmp_settings(id)

def get_snmp_setting(network_id):

    url=f"{meraki_base_url}/api/v1/networks/{network_id}/snmp"
    response = meraki_session.get(url)
    response.raise_for_status
    api_response=response.json()
    print(api_response)
    return api_response

def write_file(name,data):

  with open(f"{name}.json", 'w') as f:
    json.dump(data, f, ensure_ascii=False)

def set_snmp_settings(id):

    payload={"access": "community", "communityString": meraki_snmp_reporting_key}
    url=f"{meraki_base_url}/api/v1/networks/{id}/snmp"
    response = meraki_session.put(url,json=payload)
    response.raise_for_status
    api_response=response.json()
    print(api_response)


if __name__ == '__main__':

    get_networks(url)