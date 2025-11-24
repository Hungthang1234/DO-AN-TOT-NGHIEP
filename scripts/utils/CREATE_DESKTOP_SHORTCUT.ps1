$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("$env:USERPROFILE\Desktop\Dự Đoán Giá Nhà.lnk")
$Shortcut.TargetPath = "$PSScriptRoot\MENU.bat"
$Shortcut.WorkingDirectory = "$PSScriptRoot"
$Shortcut.Description = "Dự đoán giá bất động sản - Machine Learning"
$Shortcut.Save()

Write-Host ""
Write-Host "✓ Đã tạo shortcut trên Desktop!" -ForegroundColor Green
Write-Host ""
Write-Host "Bạn có thể double-click icon 'Dự Đoán Giá Nhà' trên Desktop để chạy!" -ForegroundColor Cyan
Write-Host ""
pause
