$path = "FOLDER"
Get-WinEvent -FilterHashtable @{
    'LogName' = 'Microsoft-Windows-TaskScheduler/Operational'
    'ID'      = 200, 201
} | Where-Object {
    $_.Properties[0].Value -like "*\$path\*"
}| Group-Object ActivityID | ForEach-Object {
    $start = $_.Group |
             Where-Object { $_.Id -eq 200 -and $_.Properties[0].Value -like "*\$path\*" } |
             Select-Object -Expand TimeCreated -First 1
    $end   = $_.Group |
             Where-Object { $_.Id -eq 201 -and $_.Properties[0].Value -like "*\$path\*" } |
             Select-Object -Expand TimeCreated -First 1

    New-Object -Type PSObject -Property @{
        'TaskName'  = $_.Group[0].Properties[0].Value
        'StartTime' = $start
        'EndTime' = $end
        'Duration'  = ($end - $start).TotalSeconds
        }
    }
