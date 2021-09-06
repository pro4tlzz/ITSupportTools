#!/bin/bash
# EA based off https://community.jamf.com/t5/jamf-pro/uptime-7-days-smart-group-need-help-with-extension-attribute/m-p/129348/highlight/true#M118461 by @alexjdale
uptimeRes=$(uptime)
if [ "$(echo $uptimeRes | grep day)" ]; then
    uptimeDays=$(echo $uptimeRes | awk '{print $3}')
else
    uptimeDays=1
fi
echo "<result>$uptimeDays</result>"
daysToForce="$((14-$uptimeDays))"
if [ $uptimeDays -ge 7 ]
then 
/Library/Application\ Support/JAMF/bin/jamfHelper.app/Contents/MacOS/jamfHelper -windowType hud  -title "IT" -heading "Restart Warning" -description "Your Mac has not been restarted for over $uptimeDays days, please restart your Mac. In $daysToForce days you will have to restart your Mac" -icon /usr/local/Branding/.jpeg
elif [ $uptimeDays -ge 14 ]
then
/Library/Application\ Support/JAMF/bin/jamfHelper.app/Contents/MacOS/jamfHelper -windowType Utility  -title "IT" -heading "Restart Notice" -description "Your Mac has not been restarted for over $uptimeDays days, please restart your Mac" -icon /usr/local/Branding/.jpg
fi%       