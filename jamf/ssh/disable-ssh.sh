#!/bin/zsh
remotelogin=$(systemsetup -getremotelogin)
actualStatus=$(cut -d ":" -f2 <<< $remotelogin)
echo $actualStatus
if [[ $actualStatus == " On" ]]; then
systemsetup -f -setremotelogin off
remotelogin=$(systemsetup -getremotelogin)
echo $remotelogin
else
echo "Exiting because SSH status is not enabled"
fi
