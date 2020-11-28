cd /d %~dp0
cd ..
cd userconfig
call ActivateEnv.bat
cd /d %~dp0
for /L %%n in (1,0,10) do (
python getImg.py
)
pause