#  Google Matter, Search Query & Export Generator for leaver users
You will need to create Oauth credentials
You need to use the Google Oauth2 Playground and supply the client ID and client Secret from the Google Cloud project 
You will need to supply a file of users to work on, although you can change this part of the flow pretty easily
You will also need to supply the Google Workspace user IDs of the admins which you want the matter to be shared with, use the Google Workspace Directory API for this
#  Download Vault Export then Upload it to Google Drive
You will need to create Oauth credentials
You need to use the Google Oauth2 Playground and supply the client ID and client Secret from the Google Cloud project
Your grant should include access to Google Drive, Google Vault and the Storage APIs. You can use read only for Storage API grants 
The script will then check the status of the export until it is completed.
Then download the export, create a folder in drive & upload the export to that folder