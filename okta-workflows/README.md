# MFA Report Workflow

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

## How to use

- Simply import MFA.folder into a folder within OKTA Workflows
- Change the group ID in the flow 'Group Members - streamed Helper Flow'

## Images

![Step 1 - Group Members - streamed Helper Flow](https://github.com/pro4tlzz/ITSupportTools/blob/main/okta-workflows/Group%20Members%20-%20streamed%20Helper%20Flow.png)
![Step 2 - Get Factor for user](https://github.com/pro4tlzz/ITSupportTools/blob/main/okta-workflows/Get%20Factor%20for%20user.png)
![Step 3 - Get type of factor](https://github.com/pro4tlzz/ITSupportTools/blob/main/okta-workflows/Get%20type%20of%20factor.png)