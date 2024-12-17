#! /usr/bin/env bash
# DB 준비 대기
# until alembic upgrade head
# do
#   echo "DB not ready"
#   sleep 1
# done
python migration/init_db.py
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload