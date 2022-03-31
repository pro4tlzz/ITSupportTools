# App Group Report Workflow

## Okta Workflow Structure

Special thanks to [@gabrielsroka](https://github.com/gabrielsroka) for creating a flow which can be used to retrive the value of the links header when the Okta API is using pagination. [Click here](https://app.slack.com/client/T04QVKUQG/threads/thread/C011DBUDT28-1648568368.298839)

This Folder Flowpack performs the following for active Okta Applications:


- Performs a GET Call to list all active Applications & calls a flow to get the paginated links from the response headers
 - Clears all rows in a table
  - For each application:
    - Gets the groups assigned to a application
    - Performs a GET request to the groups endpoint for each group
      - Checks if the group is not an Okta group
       - Fills in a row in a table with the following information
        - objectClass.0 (type of group)
        - applicationId
        - applicationName
        - groupName
        - groupId 

## How to use

- Simply import applicationLifecycleManagement.folder into a folder within Okta Workflows
- Run the API endpoint call or change to a scheduled run

## Images

List Applications - Part 1 ![Screenshot 2022-03-31 at 15 18 40](https://user-images.githubusercontent.com/22709115/161077114-14b6250c-0a82-4aea-8776-2846484c9607.png)

List Applications - Part 2 ![image](https://user-images.githubusercontent.com/22709115/161077189-ab9e571c-3f67-4f52-918f-9c47e761a3f9.png)

[Okta] Get next Link header from headers Part 1 - Thanks ![Screenshot 2022-03-31 at 15 20 28](https://user-images.githubusercontent.com/22709115/161077535-eef645b0-6ee4-4ff0-9181-1792dc9891d2.png)

[Okta] Get next Link header from headers Part 2 ![Screenshot 2022-03-31 at 15 20 51](https://user-images.githubusercontent.com/22709115/161077624-94436182-fcbd-4538-a5ce-cb83eaf44f18.png)

Get Groups for App - Part 1 
![Screenshot 2022-03-31 at 15 21 50](https://user-images.githubusercontent.com/22709115/161077820-1b27cc98-d75b-4ed3-b47e-b94218dedcd2.png)

Get Groups for App - Part 2
![Screenshot 2022-03-31 at 15 22 03](https://user-images.githubusercontent.com/22709115/161077852-90ca25a0-dc68-4656-942f-b2533d0d6cbf.png)

Get Info for Group - Part 1
![Screenshot 2022-03-31 at 15 22 47](https://user-images.githubusercontent.com/22709115/161077982-fafe0d3d-e1d1-4e3a-a1c2-fd1147da6c8c.png)

Get Info for Group - Part 2

![Screenshot 2022-03-31 at 15 23 13](https://user-images.githubusercontent.com/22709115/161078081-44cf8c48-a0e2-43ec-a8ea-021b42287b12.png)

