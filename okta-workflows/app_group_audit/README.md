# App Group Report Workflow

## OKTA Workflow Structure

This Folder Flowpack performs the following for active OKTA Applications:


- Performs a GET Call to list all active Applications & calls a flow to get the paginated links from the response headers
 - Clears all rows in a table
  - For each application:
    - Gets the groups assigned to a application
    - Performs a GET request to the groups endpoint for each group
      - Checks if the group is not an OKTA group
       - Fills in a row in a table with the following information
        - objectClass.0 (type of group)
        - applicationId
        - applicationName
        - groupName
        - groupId 

## How to use

- Simply import applicationLifecycleManagement.folder into a folder within OKTA Workflows
- Run the API endpoint call or change to a scheduled run

## Images

![Flow 1 -]()
![Flow 2 -]()
![Flow 3 -]()