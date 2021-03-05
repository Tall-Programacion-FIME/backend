#!/usr/bin/env bash
python /app/app/backend_pre_start.py
alembic upgrade head
