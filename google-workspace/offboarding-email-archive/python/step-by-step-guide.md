## Step by Step Guide

1 - Create a Google Cloud Project 
  
  ![image](https://user-images.githubusercontent.com/22709115/161450264-2113335c-40db-4149-a6f9-3efa75940e88.png)

2 - Authorise APIs - Vault, Drive & Cloud Storage, & Admin SDK APIs 

  ![image](https://user-images.githubusercontent.com/22709115/161450295-6e58673d-64b6-4d26-95f6-03f5f4670fc9.png) ![image](https://user-images.githubusercontent.com/22709115/161450309-7351782b-c3f6-4a27-86a2-5f4dc7aba283.png) ![image](https://user-images.githubusercontent.com/22709115/161450334-079b5d92-42fe-4b65-84aa-9aca33e74087.png) ![image](https://user-images.githubusercontent.com/22709115/161451163-0155abb6-74f7-43f7-83d0-2f76e1f78610.png)


3 - Go to APIs & Services -> Credentials 

  ![image](https://user-images.githubusercontent.com/22709115/161450360-3c82ff85-a3ed-485b-9095-749d2139cfce.png)

4 - Click Create Credentials -> OAuth client ID 

  ![image](https://user-images.githubusercontent.com/22709115/161450374-ce68d9cf-47b4-49b6-bd8d-887c9a344fb4.png)

5 - Configure Consent Screen 

  ![image](https://user-images.githubusercontent.com/22709115/161450387-dcdb7ba5-fb39-4692-952b-398af4971e86.png)

6 - Select Internal

  ![image](https://user-images.githubusercontent.com/22709115/161450397-1e65ec30-48f7-4e97-95c2-ecf40da56dfa.png)

7 - Fill in required fields

  ![image](https://user-images.githubusercontent.com/22709115/161450469-5ea7a121-58cf-4a17-8f1d-421a8f273339.png)

8 - Skip the scopes section

  ![image](https://user-images.githubusercontent.com/22709115/161450548-30ec9301-80c4-4e52-b059-740365c8b693.png)

9 - Click Create Credentials -> OAuth client ID 

  ![image](https://user-images.githubusercontent.com/22709115/161450374-ce68d9cf-47b4-49b6-bd8d-887c9a344fb4.png)

10 - Choose Web Application as Application type and use https://developers.google.com/oauthplayground for the Authorized redirect URIs

  ![image](https://user-images.githubusercontent.com/22709115/161450610-46be2ea7-58f9-4e7c-87b4-84a047a03cb8.png)

11 - Save your Client ID & Secret somewhere safe

  ![image](https://user-images.githubusercontent.com/22709115/161450629-ddfc60f3-4464-47bc-87f1-7129285f13cc.png)

12 - Go to https://developers.google.com/oauthplayground/ Click the settings cog and enter your Client ID and Client Secret which you just took a note of 

 ![image](https://user-images.githubusercontent.com/22709115/161450682-b3de8fa1-9a30-433f-8f97-ccbe81fd3312.png)

13 - Select Cloud Storage API v1 Read Only 

  ![image](https://user-images.githubusercontent.com/22709115/161450718-f2b2828a-ee37-4e70-99c8-5ba59fdc51d3.png)

14 - Select Drive API v3 with full access 

  ![image](https://user-images.githubusercontent.com/22709115/161450736-50b511eb-60cb-427f-b83c-e7c241407054.png)

15 - Select Google Vault API v1 with full access 

  ![image](https://user-images.githubusercontent.com/22709115/161450754-a760836f-9edf-41d8-93d9-7f69a01322ca.png)

16 - Select Admin SDK API v1 with the user.readonly scope 

  ![image](https://user-images.githubusercontent.com/22709115/161451206-2ddb048b-cc33-4049-8d82-3fa5e901ca97.png)

17 - Click Authorise APIs and choose an account to continue with, this should be an account with access to Google Vault and Drive. Then allow the scopes

  ![image](https://user-images.githubusercontent.com/22709115/161450792-4740ee04-4027-4ecd-8ca8-e0b579c06e39.png)

18 - Click Exchange Authorization code for tokens and then save your refresh token in a safe place 

  ![image](https://user-images.githubusercontent.com/22709115/161450908-18470227-7deb-4137-9556-a2e5d5512ef8.png)

19 - Do a GET Request to https://admin.googleapis.com/admin/directory/v1/users/user for each administrator who the vault matter should be shared with. Note the value of the ID key

  ![image](https://user-images.githubusercontent.com/22709115/161451332-7cebb339-9bc0-49d3-84c4-486546359560.png)

20 - Open a code editor and open v2-google-vault.offboarding.py

21 - Change line 19 of the script to include a list of users you want to generate email archives for. E.g userList=["user1@domain.com,user2@domain.com"]

22 - Change line 20 of the script to include a list of Google Workspace User IDs for any accounts you want to share the Vault Matters with. Refer to Step 19.

23 - Change the rootFolderId="" variable to include the Google Drive folder ID where you want to upload the archives to

24 - From a IDE or Terminal of your choice invoke the script with python3 and substitue the variables with what you have saved

 ![image](https://user-images.githubusercontent.com/22709115/161451428-2abe3f5b-eb34-43fb-a241-d4826609aa7f.png)
 
25 - I haven't made the prettiest output yet so just wait for the export on the matter to be completed, if you wish you can modify the script with print messages

 ![image](https://user-images.githubusercontent.com/22709115/161451487-29e635a9-a4d4-42a2-a33c-1de964309fb2.png)

26 - You should see a matter created in Google Vault with an Export being procesed, once the export is complete the script will download it to a downloads folder in the same directory as the script. The script will check the export status every 30 seconds until it is complete.

 ![image](https://user-images.githubusercontent.com/22709115/161451512-1ad6d1a8-f3f7-458b-8f00-eb38b01b363f.png)

27 - Script will output the information related to the folder where the upload was completed 

 ![image](https://user-images.githubusercontent.com/22709115/161451762-34637012-d511-439f-bf7c-56f88bc0b94d.png)

28 - Success

 ![image](https://user-images.githubusercontent.com/22709115/161451805-997a0348-f113-4972-9696-9fcceaad2b8d.png)
