@echo off
%1 start "" mshta vbscript:CreateObject("Shell.Application").ShellExecute("cmd.exe","/c ""%~s0"" ::","","runas",2)(window.close)&&exit
cd  %~dp0
call ActivateEnv.bat
cd  src
python wechatControl.py 
pause