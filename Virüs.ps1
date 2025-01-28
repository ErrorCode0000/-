while ($true) {
    Start-Job -ScriptBlock { Write-Error " " }
}