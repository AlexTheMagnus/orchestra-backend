![image](https://user-images.githubusercontent.com/37160608/151696467-8359a550-8f7b-47b5-a0d3-e6dfb0fffc68.png)
# 🎶📖🎶 Orchestra Backend API 🎶📖🎶

## Table of contents

- [Pre-installation requirements](#pre-installation-requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Test](#test)
- [Uninstall](#uninstall)



## Pre-installation requirements
- python3.8
- python3.8-dev
- virtualenv
- build-essential
- mysql-server
- mysql-client
- libmysqlclient-dev
- libsqlclient-dev
- libssl-dev

The all can be easily installed running `sudo apt install python3.8 python3.8-dev virtualenv build-essential mysql-server mysql-client libmysqlclient-dev libsqlclient-dev libssl-dev -y`.

> ⚠️ These requirements will allow Orchestra to work on Ubuntu 20.04. For other operative systems they might change.



## Installation

1. Run `docker-compose up -d` to launch the DB container. If it fails, check that mysql.service isn't already running (in Linux, run `systemctl stop mysql.service` to stop it).
2. Create a Python 3.8 virtual environment (`virtualenv -p python3.8 .venv`). This step is only needed the first time you run the project.
3. Activate the python env running `source .venv/bin/activate`.
4. Inside the python environment, run `pyhton3 init_dbs.py` to create all the DB tables and `pipenv install` to install all the project dependencies inside the virtualenv.
5. Reboot the virtual environment, run `deactivate` and then `source .venv/bin/activate` again.



## Configuration

Clone the `.env.example` file and rename it as `.env`. Then set up the following parameters:

- **DB_ENGINE**: DB container location.
- **CLIENT_ID**: Spotify app client ID (Can be obtained from [Spotify for Developers](https://developer.spotify.com/dashboard/applications))
- **CLIENT_SECRET**: Spotify app client secret (Can be obtained from [Spotify for Developers](https://developer.spotify.com/dashboard/applications))
- **SPOTIPY_REDIRECT_URI**: Orchestra frontend location.



## Usage

Once the project is installed and configured, make sure to have up and running the DB container and active the virtualenv. Then, run `flask run` inside the virtualenv.



## Test

> ⚠️ Docker DB container must be up.  
> ⚠️ Instalation and configuration steps are needed to run the tests. 

1. In the `.env` file, change the `DB_ENGINE` env variable to match the testing DB.
2. To execute the tests run `pipenv run test` from the orchestra-backend root folder.
3. To use the production database, change back the DB_ENGINE value.



## Uninstall

The whole project is installed inside a virtual env. So, it's just needed to remove the project folder and the virtual env folder to uninstalled it completely. If you have followed the [Installation](#installation) section, your virtual environment will be inside the project folder in a folder named `.venv`.
