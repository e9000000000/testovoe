# test
near finish


# how to run
## env variables
`POSTGRES_PASSWORD` - very strong password from database
`POSTGRES_DB` - very strong password from database
`TGBOT_TOKEN` - set bot [token](https://core.telegram.org/bots/api)
`PGDATA_PATH` - path to postgres database files

## google api
create project [here](https://console.cloud.google.com/apis/dashboard) or use existing  
enable `Google Drive API` and `Google Sheets API`  
create `Service Account` and add new key in json format  
provide path to downloaded .json file in `config.py:GOOGLE_CREDITS_PATH`

## frontend
build
```bash
docker-compose --profile prepare up --build --no-start
docker-compose --profile run build-webui
```

## database
if posetgres data is already initialized docker will not create database, so you have to do it manualy
```bash
docker-compose up --build --no-start
docker-compose run -d --name postgres postgres
docker exec -it postgres /bin/bash
psql --user=postgres  # use any user which have rights to create database and another user
```
```sql
CREATE DATABASE yourDatabaseName;
CREATE USER sameUsernameAsDatabase;
GRANT ALL PRIVILEGES ON DATABASE yourDatabaseName TO sameUsernameAsDatabase;
```

## run
```bash
docker-compose up
```

# how to use
## telegram notification
bot commands:
- `/start` - enable notifications
- `/stop` - disable notifications
