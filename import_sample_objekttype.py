'''
1. 從 cosmo api 取得 objekt type 測試資料
2. 透過 Django ORM 匯入 Model / DB

'''

# ---- 取得資料 ----
import requests, json, time
import pandas as pd 

baseurl = 'https://api.cosmo.fans/bff/v3/objekts/nft-metadata/'
# 改用 token api 可以獲得背面圖
# https://api.cosmo.fans/objekt/v1/token/9416482
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

target_tokenId_list = [
    160207, 160097, 160187, 160101, 160060, 781026, 781047, 2619899, 1480866, 10808020, 1081378, 14648866, 931878, # FCO
    248336, 2619910, 2324261, 4678651, 14762743, 14676141, 4474069, 4477659,   # SCO
    696109, 696521, 4047647, 4256836, 12820781, 13691784, 13699221, 836425, 3128144, # DCO
    1040471, 6877276, 14617765, 14763904,   # WCO PCO
]

target_tokenId_list = [
    15664269, 15664201, 15634320, 15516611, 14954163, 14761377, 13713631, 14675699, 12795605, 
    14131346, 14072344, 14069489, 14070045, 13832921, 13832937, 13737391, 13733620, 13735541,
    13460870, 12834026, 11865153, 3446274, 608728, 613832, 672189, 671894, 572453, 572654, 
    7314117, 7139780, 7139793
]

target_tokenId_list = [
    10778096, 6877338, 6877191, 6877357, 6877273, 429276, 8110359, 433026, 1422139, 1018620, 
    1018764, 9932466, 924159, 4446352, 2285931, 14129569, 2898946, 9546265
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
        try:
            # 不能直接傳 str 要改成從 model get instance
            name = otype['name']
            img = otype['image']
            tokenId = otype['tokenId']
            artist = Artist.objects.get(name=otype['attributes']['Artist'])
            objekt_class = Class.objects.get(name=otype['attributes']['Class'], artist=artist)
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
        except Exception as e:
            print(f'Failed to import {name}')
            print(e)
            continue

print('Imported objekt type:', imported)
