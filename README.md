# Orchestra Backend API

## Usage

1. Install all the dependencies running `sudo apt install python3.8 python3.8-dev virtualenv build-essential mysql-server mysql-client libmysqlclient-dev libsqlclient-dev libssl-dev -y`
1. Create a Python 3.8 virtual environment (virtualenv -p python3.8 venv)
1. Activate it running `source venv/bin/activate`
1. Inside the environment run `pip install -r requirements`
1. Run `docker-compose up -d`

## Test

Note: It's necessary to have executed `pyhton3 init_dbs.py inside the pipenv shell`

1. In the .env file, change the DB_ENGINE env variable to match the DB_ENGINE_TEST env variable.
1. To execute the test run `pipenv run test` inside the orchestra-backend root folder.
1. To use the production database, change back the DB_ENGINE value.
