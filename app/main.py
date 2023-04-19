from fastapi import FastAPI
from model import TestUserTable
from db import session

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

#　ユーザー情報一覧取得
@app.get("/test_users")
def get_user_list():
    users = session.query(TestUserTable).all()
    return users