#!/bin/bash
# gets logged in user for looking at directory
loggedInUser=$( echo "show State:/Users/ConsoleUser" | scutil | awk '/Name :/ && ! /loginwindow/ { print $3 }' )
# checks Jamf Connect for current logged in Okta user
jamfConnectUser=$(defaults read /Users/$loggedInUser/Library/Preferences/com.jamf.connect.state.plist DisplayName)
curl=/usr/bin/curl
curl -s --location --request POST https://domain.workflows.okta.com/api/flo/$6/invoke > /dev/null \
--header x-api-client-token:$4 \
--header x-api-alias:$5 \
--header jamf-connect-username:$jamfConnectUser \
--header jamf-computer-name:$2