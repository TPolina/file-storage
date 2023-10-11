# File Storage

Simple FastAPI-based application.

## Features

- Upload file to the database;
- Download file from the database;
- Get info about file without downloading;
- Get top 10 largest files;
- No ORM, simple DB connection.

## Installation

Python must be already installed

```shell
git git@github.com:TPolina/file-storage.git
cd file-storage
python3 -m venv venv
source venv/bin/activate
pip install -r requirments.txt
python3 db/prepare_db.py
python3 -m uvicorn main:app --reload 
```
