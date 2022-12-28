## Create environment
```
py -3.9 -m venv venv
.\venv\Scripts\activate
or
source ./venv/bin/activate
```

if ubuntu 
### Deactivate environment
```
deactivate
```

## Install library
```
pip install --upgrade pip
pip install -r requirements.txt 
```

## Run

```
uvicorn main:app --host 0.0.0.0 --reload

INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [26968] using WatchFiles
INFO:     Started server process [24208]
INFO:     Waiting for application startup.
INFO: 
```
