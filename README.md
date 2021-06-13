# Orchestra Backend API

## Usage

1. Install all the dependencies running `sudo apt install python3.8 python3.8-dev virtualenv build-essential mysql-server mysql-client libmysqlclient-dev libsqlclient-dev libssl-dev -y`
1. Create a Python 3.8 virtual environment (virtualenv -p python3.8 venv)
1. Activate it running `source venv/bin/activate`
1. Inside the environment run `pip install -r requirements`
1. Run `docker-compose up -d`

## Test

1. To execute the test run `pipenv run test` inside the orchestra-backend root folder.
