# Hain.co API

Hain.co is an Android based Canteen Ordering Application designed for school canteens aiming for a
better, contactless dining experience. 

This repository contains the backend of our application

## Developing the project

For the Python server, first you should create a Python virtual environment and activate it in your terminal

```bash
# create a venv
python -m venv venv

# activate the venv
venv\Scripts\activate

# install dependencies
pip install -r requirements.txt
```

To start the python server, you can 

```bash
# for the Python server (separate terminal)
uvicorn backend.server:app --reload --port 8080
```