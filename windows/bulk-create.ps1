#Bulk create AD users and file shares for them
Import-Csv "C:\adusers.csv" | ForEach-Object {
$upn = $_.SamAccountName + "yourdomain"
New-ADUser -Name $_.Name `
-GivenName $_."GivenName" `
-Surname $_."Surname" `
-DisplayName $_."Name" `
-SamAccountName  $_."samAccountName" `
-UserPrincipalName  $upn `
-Path $_."Path" `
-EmailAddress $_."EmailAddress" `
-ChangePasswordAtLogon:$True `
-AccountPassword (ConvertTo-SecureString "insert_Password" -AsPlainText -force) -Enabled $true
Add-ADPrincipalGroupMembership -Identity $_."samAccountName" -MemberOf ($_."Groups" -split',')
New-ADOrganizationalUnit -Name $_."samAccountName" -Path "OU=yourOu,DC=your,DC=domain,DC=com"
New-ADGroup -Name "Write_share_$($_."samAccountName")" -GroupCategory Security -GroupScope Domain -DisplayName "Write_Share_$($_."samAccountName")" -Path "OU=$($_."samAccountName"),OU=user,DC=your,DC=domain,DC=com"
New-ADGroup -Name "Read_share_$($_."samAccountName")" -GroupCategory Security -GroupScope Domain -DisplayName "Read_Share_$($_."samAccountName")" -Path "OU=$($_."samAccountName"),OU=user,DC=your,DC=domain,DC=com"
New-Item -Path "D:\Sharse\$($_."samAccountName")\MyDocuments" -ItemType "directory" -Force
$securitygroupwrite = "Write_share_$($_."samAccountName")"
$securitygroupread = "Read_share_$($_."samAccountName")"
New-SMBShare -Name $_."samAccountName" -Path "D:\Shares\$($_."samAccountName")\MyDocuments" -FullAccess "Administrators" -ChangeAccess $securitygroupwrite -ReadAccess $securitygroupread
Add-ADPrincipalGroupMembership -Identity $_."samAccountName" -MemberOf "Write_share_$($_."samAccountName")"
Add-ADPrincipalGroupMembership -Identity $_."samAccountName" -MemberOf "Read_share_$($_."samAccountName")"
$acl = Get-Acl "D:\Shares\$($_."samAccountName")\MyDocuments"
$AccessRuleWrite = New-Object System.Security.AccessControl.FileSystemAccessRule("Domain\Write_share_$($_."samAccountName")","FullControl","ContainerInherit, ObjectInherit", "None","Allow")
$AccessRuleExecute = New-Object System.Security.AccessControl.FileSystemAccessRule("Domain\Read_share_$($_."samAccountName")","ReadAndExecute","ContainerInherit, ObjectInherit", "None","Allow")
$AccessRuleRead = New-Object System.Security.AccessControl.FileSystemAccessRule("Domain\Read_share_$($_."samAccountName")","Read","ContainerInherit, ObjectInherit", "None","Allow")
$acl.SetAccessRule($AccessRuleWrite)
$acl.SetAccessRule($AccessRuleRead)
$acl.SetAccessRule($AccessRuleExecute)
$acl | Set-Acl 
$acl = Get-Acl "D:\Shares\$($_."samAccountName")\MyDocuments"
}
