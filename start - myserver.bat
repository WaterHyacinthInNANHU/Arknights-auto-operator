@echo off
%1 start "" mshta vbscript:CreateObject("Shell.Application").ShellExecute("cmd.exe","/c ""%~s0"" ::","","runas",2)(window.close)&&exit
cd /d %~dp0
call ./src/userconfig/ActivateEnv.bat
cd  src
python myserverControl.py 
pause