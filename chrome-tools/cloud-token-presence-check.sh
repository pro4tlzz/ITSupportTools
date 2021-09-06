#!/bin/bash
loggedInUser=$( scutil <<< "show State:/Users/ConsoleUser" | awk '/Name :/ && ! /loginwindow/ { print $3 }' )
if [[ "$loggedInUser" == "root" ]]; then
echo "No user logged in"
exit
else
echo "$loggedInUser is logged in, proceeding"
fi
if [ -d /Users/$loggedInUser/Library/Application\ Support/Google/Chrome\ Cloud\ Enrollment ] 
then
    echo "<result>"Directory Cloud Enrollment exists"</result>"
else
    echo "<result>"Directory Cloud Enrollment does not exist, exiting"</result>"
    exit
fi