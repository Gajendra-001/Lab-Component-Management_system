@echo off
echo Starting reminder process at %date% %time% >> C:\Users\Gajendra\Desktop\iotlab\reminder_log.txt
cd /d C:\Users\Gajendra\Desktop\iotlab
call venv\Scripts\activate.bat
python manage.py send_return_reminders
deactivate
echo Completed reminder process at %date% %time% >> C:\Users\Gajendra\Desktop\iotlab\reminder_log.txt