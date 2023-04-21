Get-ChildItem -Path F:\Others -Recurse -File | 
    Select-Object FullName, Name, @{n='SizeGB';e={$_.Length / 1GB}}, LastWriteTime, @{n='Owner';e={(Get-Acl $_.FullName).Owner}} |
    ForEach-Object {
        $_.SizeGB = $_.SizeGB.ToString("N2")
        $_.LastWriteTime = $_.LastWriteTime.ToString("dd.MM.yyyy")
        $_
    } |
    Sort-Object SizeGB -Descending |
    Select-Object -First 1000 |
    Export-Csv -Path F:\Others\output.csv -NoTypeInformation -Delimiter "`t"
