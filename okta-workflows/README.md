# MFA Report Workflow

## OKTA Workflow

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