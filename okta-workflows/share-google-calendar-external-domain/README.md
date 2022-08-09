# Google Calendar - Share a users' free busy status with another domain
## OKTA Workflow Structure


This Flopack performs the following:
- When a user is assigned to Google Workspace a helper flow is triggered, the application username is sent to the helper flow
 - The helper flow does a POST to the /v3/calendars/$usercalendar/acl endpoint, it sends a body with a domain specified. This domain will be able to see free / busy on the users' calendar
- An optional 3rd flow can be used to paginate through all Google Workspace users and share their calendar exactly the same way using the same helper flow

## How to use

- Simply import shareGoogleCalendarExternalDomain.folder into a folder within OKTA Workflows
- Configure the 'User Assigned from Application' card in the flow 'User Unassigned to Google Workspace', enter the appID of your Zendesk app instance

## Images
Step 1 - User assigned to Google Workspace

![image](https://user-images.githubusercontent.com/22709115/183755278-784bb549-210d-433a-86d6-536fb8efba16.png)

Step 2 - Cal share domain A with domain B 

![image](https://user-images.githubusercontent.com/22709115/183755339-8374db8d-08a1-4277-b60e-7a3904dad0fa.png)


Paginate all the users and share their calendars! [Uses same pagination from here](https://github.com/pro4tlzz/ITSupportTools/tree/main/okta-workflows/inactive-google-workspace-users)

Use a url like ```https://admin.googleapis.com/admin/directory/v1/users?domain=domainA.com```

Part 1 
![image](https://user-images.githubusercontent.com/22709115/183755590-e12870df-d282-49d2-bda4-41fc07702044.png)

Part 2
![image](https://user-images.githubusercontent.com/22709115/183755643-e56daf7e-dbf2-487d-af6d-eccf5647cd74.png)
