# Orchestra Backend API

## Instalation

1. Install all the dependencies running `sudo apt install python3.8 python3.8-dev virtualenv build-essential mysql-server mysql-client libmysqlclient-dev libsqlclient-dev libssl-dev -y`
2. Run `docker-compose up -d` to launch the DB container. If it fails, check that mysql.service isn't already running (in Linux, run `systemctl stop mysql.service` to stop it).
3. Create a Python 3.8 virtual environment (`virtualenv -p python3.8 .venv`). This step is only needed the first time you run the project.
4. Activate the python env running `source .venv/bin/activate`.
5. Inside the python environment, run `pyhton3 init_dbs.py` to create all the DB tables and `pipenv install` to install all the project dependencies inside the virtualenv.
6. Reboot the virtual environment, run `deactivate` and then `source .venv/bin/activate` again.

## Usage

Once the project is installed, make sure to have up and running the DB container and active the virtualenv. Then, run `flask run` inside de virtualenv.

## Test

Note: Docker DB container must be up.
Note 2: It's necessary to have executed `pyhton3 init_dbs.py` inside the pipenv shell.

1. In the .env file, change the DB_ENGINE env variable to match the DB_ENGINE_TEST env variable.
2. To execute the test run `pipenv run test` inside the orchestra-backend root folder.
3. To use the production database, change back the DB_ENGINE value.
