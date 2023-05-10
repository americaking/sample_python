from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.responses import FileResponse
from typing import List  # ネストされたBodyを定義するために必要
from starlette.middleware.cors import CORSMiddleware  # CORSを回避するために必要
from model import UserTable
from db2 import session
import datetime
import pytz
import chardet
import os
import requests
import bs4
from bs4 import BeautifulSoup
from urllib.error import HTTPError
from urllib.request import urlopen

app = FastAPI()

# CORSを回避するために設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

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
    
def getTitle(url):
    # URLからHTMLを取得
    response = requests.get(url)

    # レスポンスのステータスコードを確認
    if response.status_code == 200:
        html = response.text

        # BeautifulSoupを使ってHTMLを解析
        soup = BeautifulSoup(html, "html.parser")

        # データを抽出する処理（ここでは例としてタイトルを取得）
        title_element = soup.title

        # タイトル要素が存在するかチェック
        if title_element:
            title = title_element.string

            # テキストファイルに書き出す
            with open("./usr/src/server/scraped_data.txt", "w", encoding="utf-8") as file:
                file.write(title)
        else:
            print("タイトル要素が見つかりませんでした。")
    else:
        print("URLへのアクセスが失敗しました。ステータスコード:", response.status_code)

def scrape_data(url: str):
    # テキストファイルに書き出す
    # with open("scraped_data.txt", "w", encoding="utf-8") as file:
    #     file.write(getTitle(url))
    # return 
    return getTitle(url)

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    # ファイルのエンコーディングを推測する
    encoding = chardet.detect(contents)["encoding"]
    # 推測されたエンコーディングでファイルを読み込む
    contents = contents.decode(encoding)
    # ファイルの内容を処理する
    return {"filename": file.filename, "contents": contents}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.post("/uploadfiles/")
async def create_upload_files(files: List[UploadFile] = File(...)):
    results = []
    for file in files:
        filename = file.filename
        if not allowed_file(filename):
            results.append({"filename": filename, "status": "error", "message": "invalid file format"})
        else:
            contents = await file.read()
            # ファイルの内容を処理する
            results.append({"filename": filename, "status": "success"})
    return results

@app.post("/writefile/")
async def write_file(file: UploadFile = File(...), text: str = Form(...)):
    try:
        with open(file.filename, "w", encoding="utf-8") as f:
            f.write(text)
    except Exception as e:
        return {"filename": file.filename, "text": text, "status": "error", "message": str(e)}
    else:
        return {"filename": file.filename, "text": text, "status": "success"}
    
@app.get("/download/")
async def download_file():
    filename = "example.txt"
    return FileResponse(filename)

@app.get("/file_exists/")
async def file_exists(filename: str):
    if not os.path.exists(filename):
        raise HTTPException(status_code=404, detail="File not found")
    else:
        return {"message": "File exists"}
    
@app.get("/scrape2")
async def scrape():
    url = "https://example.com"
    response = requests.get(url)
    html = response.text

    # BeautifulSoupを使ってHTMLを解析
    soup = BeautifulSoup(html, "html.parser")
    # スクレイピングしたい処理を実装する
    title = soup.find("title").text
    return {"title": title}

@app.get("/scrape_output1")
async def scrape_output():
    # スクレイピング対象のURL
    url = "https://example.com"

    # URLからHTMLを取得
    response = requests.get(url)

    # レスポンスのステータスコードを確認
    if response.status_code == 200:
        html = response.text

        # BeautifulSoupを使ってHTMLを解析
        soup = BeautifulSoup(html, "html.parser")

        # データを抽出する処理（ここでは例としてタイトルを取得）
        title_element = soup.title

        # タイトル要素が存在するかチェック
        if title_element:
            title = title_element.string

            # テキストファイルに書き出す
            with open("scraped_data.txt", "w", encoding="utf-8") as file:
                file.write(title)

            return {"message": "スクレイピングが成功し、データをファイルに保存しました。"}
        else:
            return {"message": "タイトル要素が見つかりませんでした。"}
    else:
        return {"message": f"URLへのアクセスが失敗しました。ステータスコード: {response.status_code}"}