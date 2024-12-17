FROM python:3.12.1-slim

# 시스템 업데이트 및 필수 패키지 설치
RUN apt-get update && apt-get install -y \
    build-essential \
    && apt-get clean

WORKDIR /tmp

COPY pyproject.toml .
COPY poetry.lock .

RUN pip install "poetry==1.8.3" poetry-plugin-export
RUN poetry export -f requirements.txt --output /tmp/requirements.txt --without-hashes --with dev --with migration

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

WORKDIR /app
COPY . /app

ENV PYTHONPATH=/app

RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]