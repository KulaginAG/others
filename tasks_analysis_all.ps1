$path = "TasksFolder"
$today = Get-Date -Format 'yyyy-MM-dd'
$outputFilePath = 'C:\PATH\TO\FILE.csv'

Get-WinEvent -FilterHashtable @{
    'LogName' = 'Microsoft-Windows-TaskScheduler/Operational'
    'ID'      = 200, 201
} | Where-Object {
    $_.Properties[0].Value -like "*\$path\*" -and
    $_.TimeCreated.Date -eq $today
} | Group-Object ActivityID | ForEach-Object {
    $start = $_.Group |
             Where-Object { $_.Id -eq 200 -and $_.Properties[0].Value -like "*\$path\*" } |
             Select-Object -ExpandProperty TimeCreated -First 1
    $end   = $_.Group |
             Where-Object { $_.Id -eq 201 -and $_.Properties[0].Value -like "*\$path\*" } |
             Select-Object -ExpandProperty TimeCreated -First 1

    $taskData = [PSCustomObject]@{
        'TaskName'  = $_.Group[0].Properties[0].Value
        'StartTime' = $start
        'EndTime'   = $end
        'Duration'  = ($end - $start).TotalSeconds
    }

    $taskData | Export-Csv -Path $outputFilePath -Append -NoTypeInformation
}
