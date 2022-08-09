# Google Calendar - Share a users' free busy status with another domain
## OKTA Workflow Structure


This Flopack performs the following:
- When a user is assigned to Google Workspace a helper flow is triggered, the application username is sent to the helper flow
 - The helper flow does a POST to the /v3/calendars/$usercalendar/acl endpoint, it sends a body with a domain specified. This domain will be able to see free / busy on the users' calendar
- An optional 3rd flow can be used to paginate through all Google Workspace users and share their calendar exactly the same way using the same helper flow

- 

## How to use

- Simply import shareGoogleCalendarExternalDomain.folder into a folder within OKTA Workflows
- Configure the 'User Assigned from Application' card in the flow 'User Unassigned to Google Workspace', enter the appID of your Zendesk app instance

## Images
Step 1 - User assigned to Google Workspace


Step 2 - Cal share domain A with domain B 


Paginate all the users and share their calendars!