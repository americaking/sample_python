FROM python:3.7

WORKDIR /usr/src/server
ADD requirements.txt .
# requirements.txtにリストされたパッケージをインストールする
RUN pip install --trusted-host pypi.python.org -r requirements.txt
