Start-Transcript -Path $PSScriptRoot\transcript.log
$scriptToInvoke=$PSScriptRoot+"\install.bat"
 
$Content = Get-Content -Path $PSScriptRoot\install.bat

$var1="HOSTNAME="+$env:COMPUTERNAME+"^"
$Content.replace("HOSTNAME=^",$var1) | Set-Content $PSScriptRoot\install.bat

$Content = Get-Content -Path $PSScriptRoot\install.bat

$FQDN=[System.Net.Dns]::GetHostByName($env:computerName).HostName
$var2="HOSTINTERFACE="+$FQDN+"^"
$Content.replace("HOSTINTERFACE=^",$var2) | Set-Content $PSScriptRoot\install.bat

$Content = Get-Content -Path $PSScriptRoot\install.bat

$var3="HOSTMETADATA=^"
$Content.replace("HOSTMETADATA=^",$var3) | Set-Content $PSScriptRoot\install.bat

$Content = Get-Content -Path $PSScriptRoot\install.bat

$var4="HOSTMETADATAITEM=system.uname"+"^"
$Content.replace("HOSTMETADATAITEM=^",$var4) | Set-Content $PSScriptRoot\install.bat

$Content = Get-Content -Path $PSScriptRoot\install.bat

Start-Process powershell $scriptToInvoke -Verb "runas" 
