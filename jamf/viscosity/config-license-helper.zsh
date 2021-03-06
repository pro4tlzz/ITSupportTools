#!/bin/zsh

loggedInUser=$( scutil <<< "show State:/Users/ConsoleUser" | awk '/Name :/ && ! /loginwindow/ { print $3 }' )
userHomeDir=$(dscacheutil -q user | grep $loggedInUser | awk 'NR==2 {print $2}')
viscosityVPNConnectionPath="/Library/Application Support/Viscosity/OpenVPN/1"
viscosityPrefrencesPath="${userHomeDir}/Library/Preferences"
pathToConnectionFolder="${userHomeDir}/${viscosityVPNConnectionPath}"

configFilePath="${pathToConnectionFolder}/config.conf"
caFilePath="${pathToConnectionFolder}/ca.crt"
takeyFilePath="${pathToConnectionFolder}/ta.key"
preferenceFilePath="${viscosityPrefrencesPath}/com.viscosityvpn.Viscosity.plist"

mkdir -p $pathToConnectionFolder

cat << EOF > $configFilePath
#-- Configuration Generated By Viscosity --#

Your config file

EOF

cat << EOF > $caFilePath

Your cert

EOF

cat << EOF > $takeyFilePath

Your OVPN Key

EOF

cat << EOF > $preferenceFilePath

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>License</key>
	<string> your license key /string>
</dict>
</plist>

EOF

chown $loggedInUser:"staff" $configFilePath
chown $loggedInUser:"staff" $caFilePath
chown $loggedInUser:"staff" $takeyFilePath
chown $loggedInUser:"staff" $preferenceFilePath

chmod 600 $preferenceFilePath
chmod 755 $configFilePath $caFilePath $takeyFilePath
xattr -rc $configFilePath $caFilePath $takeyFilePath $preferenceFilePath 

#Credits to Jesse for this https://github.com/autopkg/jessepeterson-recipes/blob/master/SparkLabs/Viscosity.munki.recipe#L43
if [ -f "/Applications/Viscosity.app/Contents/MacOS/Viscosity" ]
then
    echo "Found Viscosity.app, installing helper tools..."
    /Applications/Viscosity.app/Contents/MacOS/Viscosity -installHelperTool YES 2>&1
fi
