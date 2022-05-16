#!/bin/zsh
if [ -f /Library/ManagedFrameworks/Python/Python3.framework/Versions/Current/Resources/Info.plist ]
then
pyv=$(/usr/libexec/PlistBuddy -c "print CFBundleVersion" /Library/ManagedFrameworks/Python/Python3.framework/Versions/Current/Resources/Info.plist)
echo "<result>"$pyv"</result>"
else
echo "<result>"Info.plist not present, ManagedPython may not be installed"</result>"
fi