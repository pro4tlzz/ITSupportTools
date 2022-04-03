# v2-google-vault-offboarding.py

## Script Workflow

This script performs the following:

- Generates Google Bearer Token using Oauth2 method
- Generates a Google Vault Matter
- Generates a Google Vault Matter saved search query
- Generates a Google Vault Matter export
- Gets the info of the Google Vault Export
- Downloads the Google Vault Export (only first file - gmail export) to downloads folder from the same dir
- Makes a folder in Google Drive nested under the folder you specify
- Uploads the Google Vault Export to that folder
- Deletes the Google Vault Export file from where it was downloaded to
- Notifies you that it is complete and provides a link to the Google Drive folder
- Sets permissions on the Google Vault Matter so all your admins have access to it

## Required Changes and credential setup

Supply the variables (sys.arg[X])

Use a Google Cloud Project with the following APIs enabled :
- Drive 
- Vault
- Cloud Storage APIs

Create an Oauth2 Client Credential Set in your project

Using the Oauth2 Developer Playground set your Client Id and Client Secret from your Oauth2 Credential Set

Grant Access to : 
- https://www.googleapis.com/auth/drive 
- https://www.googleapis.com/auth/ediscovery 
- https://www.googleapis.com/auth/devstorage.read_only

Within the script change the variables with value == CHANGEME to values which confirm with a list for userList & adminUsers

For archiveLeaversFolderId set a folderId from Google Drive

## Optional Changes

For debugging you can just print the apiResponse and matter instances

#  Google Matter, Search Query & Export Generator for leaver users  - DEPRECATED
You will need to create Oauth credentials

You need to use the Google Oauth2 Playground and supply the client ID and client Secret from the Google Cloud project 

You will need to supply a file of users to work on, although you can change this part of the flow pretty easily

You will also need to supply the Google Workspace user IDs of the admins which you want the matter to be shared with, use the Google Workspace Directory API for this

#  Download Vault Export then Upload it to Google Drive - DEPRECATED
You will need to create Oauth credentials

You need to use the Google Oauth2 Playground and supply the client ID and client Secret from the Google Cloud project

Your grant should include access to Google Drive, Google Vault and the Storage APIs. You can use read only for Storage API grants 

The script will then check the status of the export until it is completed

Then download the export, create a folder in drive & upload the export to that folder
