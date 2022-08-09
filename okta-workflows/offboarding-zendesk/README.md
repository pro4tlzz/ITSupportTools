# Offboarding - Zendesk - Save $$$

## OKTA Workflow Structure

The OIN app for Zendesk has SCIM, however it only suspends users on deactivation. It doesn't change their role, as a result you end up paying $$$ in licensing cost.


This Flopack performs the following:
- When a user is unassigned from Zendesk a helper flow is triggered, the Okta User ID is sent to the helper flow
 - The helper flow does a lookup for the Okta user to fetch the Okta username
  - The helper flow searches all Zendesk users using the query of the Okta username
   - The helper flow uses the first object in the search result, it updates the user to the 'end-user' role

- 

## How to use

- Simply import offboardingZendes.folder into a folder within OKTA Workflows
- Configure the 'User Unassigned from Application' card in the flow 'User Unassigned from Zendesk', enter the appID of your Zendesk app instance

## Images
Step 1 - User Unassigned from Zendesk

![image](https://user-images.githubusercontent.com/22709115/183752802-f416554b-165e-4da9-a8ca-abecb8c58faa.png)

Step 2 - Zendesk Offboarding

![image](https://user-images.githubusercontent.com/22709115/183752838-00a589fc-e213-41de-a72b-8db7de9a671e.png)
