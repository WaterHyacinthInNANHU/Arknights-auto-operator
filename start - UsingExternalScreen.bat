@echo off
%1 start "" mshta vbscript:CreateObject("Shell.Application").ShellExecute("cmd.exe","/c ""%~s0"" ::","","runas",2)(window.close)&&exit
DisplaySwitch /internal
rem delay 10 sec
ping -n 10 127.0.0.1>nul
cd  %~dp0
call ActivateEnv.bat
cd src
python test.py 
DisplaySwitch /external
pause