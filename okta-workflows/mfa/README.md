# MFA Report Workflow - Audit user MFA in OKTA

## OKTA Workflow Structure


This Flopack performs the following for a given OKTA group:


- Uses an API endpoint action to list the group members and passes the response to the 'Get Factor for user' flow using Streaming
  - Checks if the member of the group is active and then performs the following
    - Performs a GET request to the /api/v1/users/$USER/factors endpoint
      - Calls a Helper Flow 'Get type of factor' passing the response body as an item and an object containing username, Id & Status
      - Fills in a row in a table with the following information
        - id (factor)
        - factorType
        - CredentialId
        - provider
        - authenticatorName (FIDO)
- On a schedule checks the table where factorType is equal to sms
- Sends an email to the user notifying them that sms as a factor will be disabled

## How to use

- Simply import MFA.folder into a folder within OKTA Workflows
- Change the group ID in the flow 'Group Members - streamed Helper Flow'

## Images
Step 1 - Group Members - streamed Helper Flow

   ![Step 1 - Group Members - streamed Helper Flow](https://user-images.githubusercontent.com/22709115/161848999-e972bb17-da59-40a1-82d7-0b5ebb462b05.png)

Step 2 - Get Factor for use

   ![Step 2 - Get Factor for user](https://user-images.githubusercontent.com/22709115/161849026-db993c49-b3db-48eb-a797-adc0b1c162f5.png)
  
Step 3 - Get type of factor

   ![Step 3 - Get type of factor](https://user-images.githubusercontent.com/22709115/161849064-c1a80e8f-0e4e-469d-a2a7-f9293713fc26.png)

Step 4 - On a schedule list all users with sms enrolled as a factor

Step 5 - Send an email to each user who has sms enrolled as a factor