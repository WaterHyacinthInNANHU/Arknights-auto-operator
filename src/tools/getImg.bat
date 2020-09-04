cd /d %~dp0
cd ..
cd ..
call ActivateEnv.bat
cd /d %~dp0
python getImg.py 
pause