# Insight API Request to create objects and link attributes from the JIRA Directory API
For a given user a query is performed in the Atlassian Insight API, if the user does not have a matching object then an object is created for them in the schema.
You will need to provide the schema.
The script will query the JIRA API to get the accountID of the user so this can be linked to an attribute in the object