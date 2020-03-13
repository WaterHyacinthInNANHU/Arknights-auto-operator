DisplaySwitch /clone
rem delay 10 sec
ping -n 10 127.0.0.1>nul
cd  %~dp0
call ActivateEnv.bat
python test.py 
DisplaySwitch /external
pause