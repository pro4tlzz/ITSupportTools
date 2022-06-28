#vars
$datetime= Get-Date -Format  "dd-MM-yyyy-HH-mm"
$filename="delete-ad-user-$datetime.log"
$log_path="$PSScriptRoot\$filename"

#logging
Start-Transcript -Path $log_path

#unlock vault
$vaultpassword = (Import-CliXml /supersecretfolder/vaultpassword.xml).Password
Unlock-SecretStore -Password $vaultpassword

#vars
$admin=[System.Security.Principal.WindowsIdentity]::GetCurrent().Name
$admin_formatted= $admin -replace '.*\\'

#basic auth
$username=(Get-Secret -Name super_secret_api).GetNetworkCredential() | Select-Object -ExpandProperty UserName
$password=(Get-Secret -Name super_secret_password).GetNetworkCredential() | Select-Object -ExpandProperty Password

$auth = $username + ':' + $password
$Encoded = [System.Text.Encoding]::UTF8.GetBytes($auth)
$authorizationInfo = [System.Convert]::ToBase64String($Encoded)
$headers = @{"Authorization"="Basic $($authorizationInfo)"}

$Path="userstodelete.csv"

import-csv $path | foreach {

$aduser = Get-ADUser -Identity $_.SamAccountName -Properties Name, EmailAddress,DisplayName, samaccountname, ObjectGUID| select EmailAddress, DisplayName, samaccountname, ObjectGUID, Name

Write-Output "Proceeding with deleting user '$($aduser.Name)' '$($aduser.ObjectGUID)' '$($aduser.SamAccountName)'"
#tls 1.2
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12;
#var
$display_name=$aduser.DisplayName
#var
$atlassian_base_url="https://domain.atlassian.net"
#jql for api query
$jql="jql=project = $project AND issuetype = $issuetype AND `"Full Name[Short text]`" ~ `"$display_name`" AND status != DONE order by created DESC"

#formatted url
$uri="$atlassian_base_url/rest/api/2/search?$jql"

#get tickets and save session
$response = Invoke-RestMethod -Uri $uri  -Method Get -Headers $headers -SessionVariable "atlassian_session"

#assign key values to vars
$leaver_email = $response.issues[0].fields.customfield_10346.emailAddress
$ticket_key = $response.issues[0].key

#comment messages to use
$comment_data_message="Admin performing deletion is $admin_formatted. User who has been deleted is $($aduser.Name) , restore with command below"
$comment_data_command="Restore-ADObject -Identity $($aduser.ObjectGUID)"

#request body
$payload=@"
{"body":{"version":1,"type":"doc","content":[{"type":"paragraph","content":[{"type":"text","text":"$comment_data_message"}]},{"type":"codeBlock","attrs":{},"content":[{"type":"text","text":"$comment_data_command"}]}]},"properties":[{"key":"sd.public.comment","value":{"internal":true}}]}
"@
#new uri
$uri="$atlassian_base_url/rest/api/3/issue/$ticket_key/comment"
#Delete user
$deleted_user = Remove-ADUser -identity $aduser.samaccountname -Confirm:$False
#POST and use existing session
$response = Invoke-RestMethod -Uri $uri -Method POST -Body $payload -WebSession $atlassian_session -ContentType "application/json"

#Write Outputs
Write-Host "Deleted ADUser -Name $($aduser.Name), -SamAccountName $($aduser.samaccountname), -ObjectGUID $($aduser.ObjectGUID) on behalf of $admin_formatted"
Write-Host "$atlassian_base_url/browse/$ticket_key"
Write-Host "If you wish then restore user with: $comment_data_command"
}
Stop-Transcript