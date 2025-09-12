'''
清理 objekt traits json 資料

1. 從本地端讀取檔案 / cosmo api 取得 json 
2. 清理資料
3. 透過 Django ORM 匯入 Model / DB

'''


import os, json
from pathlib import Path
import django

# 啟動 Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import transaction
from apps.objekt.models import Collection, Class # 之後加入其他表

# 讀取檔案
# 1) request from cosmo api
# todo

# 2) read from local file
base = Path(__file__).resolve().parent
with open(base / 'data/objekttraits.json', encoding="utf8") as file:
    data = json.load(file)

traits = dict()

for trait in data:
    trait_name = trait['key']['value']
    trait_raw_list = trait['values']
    traits[trait_name] = [option['value'] for option in trait_raw_list]

collections = traits.get('Collection', [])
classes = traits.get('Class', [])

created = {'collection': 0, 'class': 0}  # 記錄新加入的數量

# 如果要重寫可先刪掉
# Collection.objects.all().delete()
# Class.objects.all().delete()


# 寫入資料
# 把資料庫操作 包成一組 有錯會全部 rollback 只有全部成功才會寫入
with transaction.atomic():

    # collection
    for name in collections:
        # 判斷 physical, 擷取 collection_number 數字部分
        is_physical = str(name).strip().endswith('A')
        digits = ''.join(ch for ch in str(name) if ch.isdigit())
        suffix = str(name)[-1]
        collection_number = digits or None

        # 先查詢有沒有此 name，有查到就回傳 is_new = False，沒有就新增 is_new=T
        obj, is_new = Collection.objects.update_or_create( 
            name = name,
            defaults = {
                'collection_number': collection_number,
                'collection_suffix': suffix,
                'physical': is_physical,
            },
        )
        if is_new: 
            created['collection'] += 1

    # class
    for cname in classes:
        obj, is_new = Class.objects.update_or_create(
            name = cname,
        )
        if is_new: created['class'] += 1

    # artist

    # member

    # season

    

print('Done.', created)



