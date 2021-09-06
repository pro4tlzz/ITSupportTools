Import the .flow into and then add the script into JAMF.

Use the generated client token and alias in OKTA as variables.


This script reads the logged in user and then checks their email address from Jamf Connect, the script then sends off the information in a web request to OKTA Workflows which in turns updates the user profile
