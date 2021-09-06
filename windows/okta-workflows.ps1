#Similar Functionality to the JAMF script which utiiises Jamf Connect
$email=([adsi]"LDAP://$(whoami /fqdn)").mail
echo $email
$pcname=hostname
$headers = New-Object "System.Collections.Generic.Dictionary[[String],[String]]"
$headers.Add("x-api-client-token", "$1")
$headers.Add("x-api-alias", "$2")
$headers.Add("jamf-connect-username", $email)
$headers.Add("jamf-computer-name", $pcname)
$response = Invoke-RestMethod 'https://domain.workflows.okta.com/api/flo/$3/invoke' -Method 'POST' -Headers $headers
$response | ConvertTo-Json  