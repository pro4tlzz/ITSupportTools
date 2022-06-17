Start-Transcript -path "transcript-restore-user.log"
$Path="loopthrougme.csv"
$users=import-csv $path 
ForEach ($user in $users) 
{
    $tempName = [string]$user.SamAccountName
    Get-ADObject -Filter {samaccountname -eq $tempName} -IncludeDeletedObjects | Select-Object -ExpandProperty ObjectGUID -outvariable user_guid
    $first_guid=$user_guid[0]
    Restore-ADObject -Identity $first_guid
    Write-Host "Restored Deleted user $tempName with ObjectGUID $first_guid" 
}
Stop-Transcript
