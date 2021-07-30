# Orchestra Backend API

## Usage

1. Install all the dependencies running `sudo apt install python3.8 python3.8-dev virtualenv build-essential mysql-server mysql-client libmysqlclient-dev libsqlclient-dev libssl-dev -y`
2. Run `docker-compose up -d`. If it fails, check that mysql.service isn't already running (in linux, run `systemctl stop mysql.service` to stop it).
3. Create a Python 3.8 virtual environment (virtualenv -p python3.8 venv). This step is only needed the first time you run the project.
4. Activate the python env running `source venv/bin/activate`.
5. Inside the python environment, run `pipenv install`.
6. Inside the python environment, run `flask run`.

## Test

Note: It's necessary to have executed `pyhton3 init_dbs.py inside the pipenv shell`

1. In the .env file, change the DB_ENGINE env variable to match the DB_ENGINE_TEST env variable.
1. To execute the test run `pipenv run test` inside the orchestra-backend root folder.
1. To use the production database, change back the DB_ENGINE value.
