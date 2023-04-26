FROM python:3.9-buster

WORKDIR /usr/src/server
ADD requirements.txt .
# requirements.txtにリストされたパッケージをインストールする
RUN pip install --trusted-host pypi.python.org -r requirements.txt

RUN pip install --no-cache-dir datetime
RUN pip install --no-cache-dir fastapi

CMD ["uvicorn", "main:api", "--reload"]