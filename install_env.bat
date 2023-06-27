

REM create requirements.txt 
REM NOTE: on windows % is escaped using %%
REM =======================================
echo # requirements > requirements.txt
echo numpy==1.24.3 >> requirements.txt
echo pandas==2.0.0 >> requirements.txt
echo Pint==0.20.1 >> requirements.txt
echo pytest==7.3.1 >> requirements.txt
echo pytest-cov==4.0.0 >> requirements.txt
echo -e . >> requirements.txt

REM inplace environment creation
REM =======================================
call conda remove --prefix ./.venv --all -y
call conda create --prefix ./.venv -y
call activate ./.venv
call conda install pip -y
call pip install -r requirements.txt