Start-Transcript -path "transcript-remove-user.log"
$Path="loopthrougme.csv"
import-csv $path | foreach {
 Remove-ADUser -Identity $_.SamAccountName -Confirm:$false
 echo "Deleted user $_.SamAccountName"
} 
Stop-Transcript
