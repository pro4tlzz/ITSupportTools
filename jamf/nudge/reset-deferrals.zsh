#!/bin/zsh
​
#based off Nudge LA Post Install logic https://github.com/macadmins/nudge/blob/main/build_assets/postinstall-launchagent#L35 All Credtis to Erik Gomez
​
# Current console user information
console_user=$(/usr/bin/stat -f "%Su" /dev/console)
console_user_uid=$(/usr/bin/id -u "$console_user")
userHomeDir=$(dscacheutil -q user | grep $console_user | awk 'NR==2 {print $2}')
deferralFile="$userHomeDir/Library/Preferences/com.github.macadmins.Nudge.plist"
​
  # Only rm the preferences file if a user is logged in, otherwise fail
  if [[ -z "$console_user" ]]; then
    echo "Did not detect user"
    exit 1
  elif [[ "$console_user" == "loginwindow" ]]; then
    echo "Detected Loginwindow Environment"
    exit 1
  elif [[ "$console_user" == "_mbsetupuser" ]]; then
    echo "Detect SetupAssistant Environment"
    exit 1
  elif [[ "$console_user" == "root" ]]; then
    echo "Detect root as currently logged-in user"
    exit 1
  else
   sudo -u $console_user /usr/bin/defaults delete $deferralFile
    echo "Removed $deferralFile file"
  fi
