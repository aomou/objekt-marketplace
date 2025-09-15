'''
1. 從 cosmo api 取得 objekt type 測試資料
2. 透過 Django ORM 匯入 Model / DB

'''

# ---- 取得資料 ----
import requests, json, time
import pandas as pd 

baseurl = 'https://api.cosmo.fans/bff/v3/objekts/nft-metadata/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Accept': 'application/json',
}

def get_nft_metadata(url=baseurl, tokenId=1):
    url = str(url) + str(tokenId)
    try:
        response = requests.get(url, headers=headers, timeout=3)  # 可加上 timeout 保險
        response.raise_for_status()  # 若回傳 4xx/5xx 也會跳 Exception
    except requests.exceptions.RequestException as e:
        print(f"Failed request for token {tokenId} — {e}")
        return None

    response_json = json.loads(response.text)

    name = response_json['name']
    img = response_json['image']
    attr = response_json['attributes']
    artist = objekt_class = member = season = collection = None
    for trait in attr:
        if trait['trait_type'] == 'Artist':
            artist = trait['value']
        elif trait['trait_type'] == 'Class':
            objekt_class = trait['value']
        elif trait['trait_type'] == 'Member':
            member = trait['value']
        elif trait['trait_type'] == 'Season':
            season = trait['value']
        elif trait['trait_type'] == 'Collection':
            collection = trait['value']
    
    metadata = {
        'name': name,
        'image': img,
        'tokenId': tokenId,
        'attributes': {
            'Artist': artist,
            'Class': objekt_class,
            'Member': member,
            'Season': season,
            'Collection': collection,
        }
    }

    return metadata

def get_list_nft_metadata(tk_list=[1, 145000]):
    results = list()
    for tk_id in tk_list:
        mtdata = get_nft_metadata(baseurl, tk_id)
        time.sleep(0.1)
        if mtdata:
            results.append(mtdata)
        else:
            print(f'Token id: {tk_id} not found')
            continue
    return results

target_tokenId_list = [
    1, 10000, 100000, 1001000, 1501000, 2001000, 2501000, 5001000, 6501000, 8001000, 
    10001000, 11001000, 12001000, 13001000, 13689200
    ]

data = get_list_nft_metadata(target_tokenId_list)

for i in data:
    print(i['name'])


# ---- 匯入資料 ----

import django, os

# 啟動 Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import transaction
from apps.objekt.models import Collection, Class, Artist, Member, Season, ObjektType

imported = 0

# 寫入資料庫
with transaction.atomic():
    for otype in data:
        # 不能直接傳 str 要改成從 model get instance
        name = otype['name']
        img = otype['image']
        tokenId = otype['tokenId']
        artist = Artist.objects.get(name=otype['attributes']['Artist'])
        objekt_class = Class.objects.get(name=otype['attributes']['Class'])
        member = Member.objects.get(name=otype['attributes']['Member'])
        season = Season.objects.get(name=otype['attributes']['Season'])
        collection = Collection.objects.get(name=otype['attributes']['Collection'])
        
        # 先查詢有沒有此 name，有查到就回傳 is_new = False，沒有就新增 is_new=T
        obj, is_new = ObjektType.objects.update_or_create( 
            artist = artist,
            member = member,
            season = season,
            objekt_class = objekt_class,
            collection = collection,
            image_uri = img,
        )
        if is_new: 
            imported += 1

print('Imported objekt type:', imported)
