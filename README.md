# test
near finish


# how to run
## env variables
`POSTGRES_PASSWORD` - very strong password from database
`TGBOT_TOKEN` - set bot [token](https://core.telegram.org/bots/api)

## google api
create project [here](https://console.cloud.google.com/apis/dashboard) or use existing  
enable `Google Drive API` and `Google Sheets API`  
create `Service Account` and add new key in json format  
provide path to downloaded .json file in `config.py:GOOGLE_CREDITS_PATH`

## database
install [docker](https://www.docker.com/)
```bash
# TODO: put it in docker-compose
docker run -e POSTGRES_PASSWORD --net=host postgres
```

## run
install [python3.10](https://www.python.org/)
```bash
python -m pip install poetry
poetry install
poetry run python main.py
```

# how to use
## telegram notification
write to bot:
- `/start` - enable notifications
- `/stop` - disable notifications
