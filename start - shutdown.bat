cd  %~dp0
call ActivateEnv.bat
python test.py 
shutdown -s -t 10
pause