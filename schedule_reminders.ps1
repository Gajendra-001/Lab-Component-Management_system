$action = New-ScheduledTaskAction -Execute "C:\Users\Gajendra\Desktop\iotlab\send_reminders.bat" -WorkingDirectory "C:\Users\Gajendra\Desktop\iotlab"
$trigger = New-ScheduledTaskTrigger -Daily -At 11:30AM
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -DontStopOnIdleEnd -AllowStartIfOnBatteries -MultipleInstances IgnoreNew
$principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest
$task = New-ScheduledTask -Action $action -Trigger $trigger -Settings $settings -Principal $principal -Description "Sends email reminders for component returns"
Register-ScheduledTask -TaskName "IoT Lab Reminders" -InputObject $task -Force 