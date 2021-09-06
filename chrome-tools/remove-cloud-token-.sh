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
    echo "Directory Cloud Enrollment exists" 
    rm -drv /Users/$loggedInUser/Library/Application\ Support/Google/Chrome\ Cloud\ Enrollment
else
    echo "Directory Cloud Enrollment does not exist, exiting"
    exit
fi
[ -d /Users/$loggedInUser/Library/Application\ Support/Google/Chrome\ Cloud\ Enrollment ] && echo "Directory Cloud Enrollment still exists." || echo "Directory Cloud Enrollment does not exist and was removed."