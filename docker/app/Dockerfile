FROM python:3.10-bullseye

ENV PATH /workspace/vendor/bin:$PATH
ENV PYTHONPATH /workspace/vendor/bin
ENV PYTHONUSERBASE /workspace/vendor

RUN pip install black

WORKDIR /workspace

COPY requirements.txt .

RUN pip install -r requirements.txt