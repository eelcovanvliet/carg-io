

REM inplace environment creation
call conda remove --prefix ./.venv --all -y
call conda create --prefix ./.venv -y
call activate ./.venv
call conda install pip -y
call pip install -r requirements.txt
cmd /k