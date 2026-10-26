#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
if [ ! -f .env ]; then cp .env.example .env; fi
uv sync --locked
uv run python manage.py migrate --noinput
uv run python manage.py seed_portfolio
uv run python manage.py import_design
exec uv run python manage.py runserver 127.0.0.1:8000

