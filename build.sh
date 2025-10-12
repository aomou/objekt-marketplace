#!/usr/bin/env bash
# exit on error
set -o errexit

# 安裝 pack
pip install -r requirements.txt

# 收集靜態檔案
python manage.py collectstatic --no-input

# 資料庫 migrate
python manage.py migrate

# 首次部署時要用
# 建立 admin / superuser 
# python manage.py createsuperuser --noinput || true   

# 匯入 fixture（放在各 app 的 fixtures 資料夾）
python manage.py loaddata apps/objekt/fixtures/objekt_fixtures.json || true
# python manage.py loaddata apps/accounts/fixtures/accounts_fixtures.json || true
# python manage.py loaddata apps/marketplace/fixtures/marketplace_fixtures.json || true

