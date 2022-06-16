# test
just started


# how to run
## google api
create project [here](https://console.cloud.google.com/apis/dashboard) or use existing  
enable `Google Drive API` and `Google Sheets API`  
create `Service Account` and add new key in json format  
provide path to downloaded .json file in `config.py:GOOGLE_CREDITS_PATH`

## run
install [python3.10](https://www.python.org/)
```bash
python -m pip install poetry
poetry install
poetry run python main.py
```
