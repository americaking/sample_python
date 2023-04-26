from fastapi import FastAPI
from typing import List  # ネストされたBodyを定義するために必要
from starlette.middleware.cors import CORSMiddleware  # CORSを回避するために必要
from model import UserTable
from db2 import session
import datetime
import pytz

app = FastAPI()

# CORSを回避するために設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/users")
def read_users():
    users = session.query(UserTable).all()
    return users

@app.get("/time/{timezone}")
def get_local_time(timezone: int):
        # タイムゾーンを指定して現在の時間を取得
        local_time = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=timezone)))
        # 時間をフォーマットしてレスポンスを作成
        response = {
            "timezone": timezone,
            "time": local_time.strftime("%Y-%m-%d %H:%M:%S")
        }
        return response

def get_country_from_timezone(timezone_offset):
    """
    TODO:タイムゾーンの数値から国判定できないか。
    タイムゾーンの数値から国を判定する関数
    :param timezone_offset: タイムゾーンの数値 (例: -9, 3, 8)
    :return: 国名 (例: "アメリカ", "日本", "中国")
    """
    # タイムゾーンオフセットを時間差に変換する
    hours_offset = timezone_offset / 3600

    # タイムゾーンオフセットに対応するタイムゾーン名を取得する
    timezone_name = pytz.country_timezones.get(hours_offset)

    if timezone_name:
        # タイムゾーン名から国名を取得する
        country_name = pytz.country_names.get(timezone_name[0])
        return country_name
    else:
        return None