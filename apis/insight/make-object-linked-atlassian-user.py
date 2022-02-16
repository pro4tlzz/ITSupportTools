#!/usr/bin/env python3
from json import tool
from re import T
from urllib.parse import uses_relative
import requests
import json
import sys
from requests.auth import HTTPBasicAuth

user_Email=sys.argv[1]
api_User=sys.argv[2]
api_Password=sys.argv[3]

def check_if_user_exists(user_Email,api_User,api_Password):

        url = "https://api.atlassian.com/jsm/insight/workspace/$SCHEMAID/v1/iql/objects?objectSchemaId=8&iql=Email="+user_Email

        headers = {
        "Accept" : "application/json",
        "Content-Type" : "application/json",
        "X-ExperimentalApi": "opt-in"
        }

        response = requests.request(
        "GET",
        url,
        headers=headers,
        auth = HTTPBasicAuth(api_User, api_Password)
        )

        apiResponse=response.json()
        toIndex=apiResponse["toIndex"]
        
        if toIndex == 1:
                userObjectKey=apiResponse["objectEntries"][0]["objectKey"]
                print("Insight User exists {}".format(userObjectKey))
                return userObjectKey
        else: 
                print("No matching Insight user found")
                return False

def search_User(user_Email,api_User,api_Password):

        url = "https://yourdomain.atlassian.net/rest/api/3/user/search?query="+user_Email

        headers = {
        "Accept" : "application/json",
        "Content-Type" : "application/json",
        "X-ExperimentalApi": "opt-in"
        }

        response = requests.request(
        "GET",
        url,
        headers=headers,
        auth = HTTPBasicAuth(api_User, api_Password)
        )
    
        apiResponse=response.json()
        accountID=apiResponse[0]['accountId']
        return accountID

def make_User(user_Email,api_User,api_Password,accountID):

        url = "https://yourdomain.atlassian.net/rest/api/3/user/search?query="+user_Email

        headers = {
        "Accept" : "application/json",
        "Content-Type" : "application/json",
        "X-ExperimentalApi": "opt-in"
        }

        response = requests.request(
        "GET",
        url,
        headers=headers,
        auth = HTTPBasicAuth(api_User, api_Password)
        )
    
        apiResponse=response.json()
        accountID=apiResponse[0]['accountId']
        displayName=apiResponse[0]['displayName']
        firstName,lastName=displayName.split()

        print(displayName,firstName,lastName,accountID)
        null=None
        body=json.dumps(
{

	"attributes":

		[{
				"objectTypeAttributeId": "$ID",
				"objectAttributeValues": [{
					"value": displayName
				}]
			},

			{
				"objectTypeAttributeId": "$ID",
				"objectAttributeValues": [{
					"value": firstName
				}]
			},

			{
				"objectTypeAttributeId": "$ID",
				"objectAttributeValues": [{
					"value": lastName
				}]
			},

			{
				"objectTypeAttributeId": "$ID",
				"objectAttributeValues": [{
					"value": user_Email
				}]
			},

			{
				"objectTypeAttributeId": "$ID",
				"objectAttributeValues": [{
					"value": null
				}]
			},

			{
				"objectTypeAttributeId": "$ID",
				"objectAttributeValues": [{
					"value": null
				}]
			},

			{
				"objectTypeAttributeId": "$ID",
				"objectAttributeValues": [{
					"value": "2"
				}]
			},

			{
				"objectTypeAttributeId": "$ID",
				"objectAttributeValues": [{
					"value": null
				}]
			},

			{
				"objectTypeAttributeId": "$ID",
				"objectAttributeValues": [{
					"value": accountID
				}]
			}
		],

	"objectTypeId": $VAR,

	"avatarUUID": "",

	"hasAvatar": "false"

}
        )

        postURL="https://api.atlassian.com/jsm/insight/workspace/$SCHEMAID/v1/object/create/"

        response = requests.request(
        "POST",
        postURL,
        headers=headers,
        auth = HTTPBasicAuth(api_User, api_Password),
        data=body
        )

        print(body)
        apiResponse=response.json()
        print(apiResponse)
        return apiResponse

userObjectKey=check_if_user_exists(user_Email,api_User,api_Password)
accountID=search_User(user_Email,api_User,api_Password)

if userObjectKey is False:
        print("Insight User Does not exist")
        make_User(user_Email,api_User,api_Password,accountID)
