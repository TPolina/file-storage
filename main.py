import os

import psycopg2
from fastapi import FastAPI, UploadFile, HTTPException, Response
from db.prepare_db import DB_CREDENTIALS

app = FastAPI()

db_connection = psycopg2.connect(**DB_CREDENTIALS)


def save_file_to_db(file_name, file_content, file_size):
    cursor = db_connection.cursor()
    cursor.execute(
        "INSERT INTO files (name, content, size) VALUES (%s, %s, %s) RETURNING id",
        (file_name, file_content, file_size),
    )
    result = cursor.fetchone()
    db_connection.commit()
    cursor.close()

    return result[0] if result else None


def get_file_from_db(file_id):
    cursor = db_connection.cursor()
    cursor.execute("SELECT name, content FROM files WHERE id = %s", (file_id,))
    result = cursor.fetchone()
    cursor.close()

    return result


def get_file_info_from_db(file_id):
    cursor = db_connection.cursor()
    cursor.execute("SELECT name, size FROM files WHERE id = %s", (file_id,))
    result = cursor.fetchone()
    cursor.close()

    return result


def get_top_files():
    cursor = db_connection.cursor()
    cursor.execute("SELECT id, name, size FROM files ORDER BY size DESC LIMIT 10")
    result = cursor.fetchall()
    cursor.close()

    return result


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/files")
async def upload_file(file: UploadFile):
    file_name = os.path.basename(file.filename)
    file_content = await file.read()
    file_size = len(file_content)

    file_id = save_file_to_db(file_name, file_content, file_size)

    if file_id:
        return {"file_id": file_id}

    raise HTTPException(status_code=400, detail="Bad Request")


@app.get("/files/{file_id}")
async def download_file(file_id: str):
    if not file_id.isdigit():
        raise HTTPException(status_code=400, detail="Bad request")

    file = get_file_from_db(int(file_id))

    if file:
        file_name, file_content = file
        file_name = os.path.basename(file_name)

        headers = {"Content-Disposition": f"attachment; filename='{file_name}'"}

        return Response(content=file_content.tobytes(), headers=headers)

    raise HTTPException(status_code=404, detail="File not found")


@app.head("/files/{file_id}")
async def get_file_info(file_id: str):
    file_info = get_file_info_from_db(int(file_id))

    if file_info:
        file_name, file_size = file_info

        headers = {
            "file_id": file_id,
            "file_name": file_name,
            "file_size": str(file_size),
        }

        return Response(headers=headers)

    raise HTTPException(status_code=404, detail="File not found")


@app.get("/top")
async def get_top_size_files():
    files = get_top_files()

    if files:
        top_files = [
            {"file_id": file_id, "file_name": file_name, "file_size": file_size}
            for (file_id, file_name, file_size) in files
        ]

        return top_files

    raise HTTPException(status_code=400, detail="Bad Request")
