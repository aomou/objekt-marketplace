# NFT 電子卡展示平台

*本專案為 Django 架構學習用途，專注於 OOP 設計模式、資料庫關聯、分層架構等核心概念的實作練習。*

## 專案概述

**核心功能：**
1. NFT 卡片展示系統
2. 賣家管理販售清單（連動錢包檢查）
3. 買家查找與瀏覽功能

平台解決賣家需要手動管理販售清單的問題，透過錢包連動自動檢查卡片持有狀況。

### 問題描述

Modhaus 公司推出的 COSMO app 讓粉絲可以購買、收集、交換偶像的 NFT 電子卡。粉絲之間在進行買賣時會使用第三方網站如 objekt.top 或 apollo.cafe 整理要販售的小卡清單，但是這些平台的清單只儲存小卡編號（collection）無法連動到賣家的 NFT wallet，導致賣家若一次性賣出多張卡，需要自行手動從清單上移除小卡。

### 解決方案

建立一個可以連動 NFT wallet 的展示平台，讓賣家方便整理販售小卡的清單、快速標注價格、直接從區塊鏈取得圖片資訊，並提供聯絡資訊讓買家可以聯繫交易。

## NFT 卡片基本知識

Objekt 是由 MODHAUS 和區塊鏈公司 HASHED 合作開發的 NFT 項目，使用以太坊生態的 Layer 2 Abstract 鏈做為基礎進行 NFT 的發行和交易。和一般的 NFT 不同之處在於只能透過官方 COSMO app 進行傳送，無法在 OpenSea 等主流 NFT 平台交易或出價買賣。

Objekt NFT 電子小卡具有以下屬性：
- artist (藝人)
- member (成員) 
- collection (編號)
- season (發行季節)
- class (稀有等級)

## 核心功能

### 1. 卡片展示系統
- 卡片清單頁面（顯示圖片、價格、清單基本資訊、賣家聯絡方式）
- 卡片詳細頁面（完整屬性）
- 簡單搜尋功能（依藝人、成員、各項屬性）

### 2. 賣家管理系統
- 註冊/登入功能（用 cosmo id 當帳號名稱，簡單驗證是否和錢包地址符合）
- 錢包地址連結
- 上架/下架卡片、管理販售清單
- 價格設定
- 自動/手動同步錢包狀態

### 3. 買家查找系統
- 瀏覽所有上架卡片（以卡片為單位）
- 瀏覽所有販售清單（以清單為單位）
- 基本篩選（屬性、價格範圍）

## 技術架構設計

### 技術堆疊
- **後端：** Python + Django
- **資料庫：** SQLite 管理清單和使用者資訊
- **前端：** Django Templates + 基礎 CSS
- **外部整合：** Rarible API 獲取 NFT 資料和擁有者

### 分層架構練習
```
├── View Layer (Django Views + Templates)
│   ├── 卡片列表頁面
│   ├── 卡片詳細頁面  
│   ├── 販售清單列表頁面  
│   └── 賣家管理頁面
├── Service Layer (業務邏輯)
│   ├── 用戶服務
│   ├── 卡片管理服務
│   └── 錢包檢查服務
└── Model Layer (資料模型)
    └── Django ORM Models
```

## 資料庫設計

### 核心資料表
```python
# accounts / 用戶系統
User (Django 內建)
SellerProfile (user, wallet_address, contact_info)

# objekt / NFT 基礎資料表
Artist (artistId, name, tokenId, debutYear, sex) # tripleS, ARTMS 等
Member (name, artist:FK, number_int, number_str) # 成員資料
Season (name, artist, datetime)   # 把 Atom 01 分開存
Class (name, startwith, artist)   # 開始的數字
Collection (name, collectionNumber, physical) 
ObjektCard (collection, artist:FK, member:FK, season:FK, class:FK)

# marketplace / 販售清單
Listing (listId:PK, user:FK, objekt_card:FK, price, is_active, created_at)
```

## 專案檔案結構

```
py_project/
├── manage.py              # Django 管理指令入口
├── config/                # 專案設定檔
│   ├── settings.py           # 資料庫、應用程式設定
│   ├── urls.py               # 主要 URL 路由設定
│   └── wsgi.py               # Web 伺服器介面設定
├── apps/                 
│   ├── accounts/          # 用戶系統模組
│   │   ├── models.py         # 用戶相關資料模型 (SellerProfile)
│   │   ├── views.py          # 登入、註冊、個人資料頁面
│   │   ├── urls.py           # 用戶功能相關路由
│   │   └── services.py       # 用戶業務邏輯 (註冊驗證、資料處理)
│   ├── objekt/            # NFT卡片核心模組  
│   │   ├── models.py         # 卡片資料模型 (Artist, Member, ObjektCard)
│   │   ├── views.py          # 卡片展示頁面 (清單、詳細頁)
│   │   ├── urls.py           # 卡片瀏覽相關路由
│   │   └── services.py       # 卡片業務邏輯 (搜尋、篩選)
│   └── marketplace/       # 交易市場模組
│       ├── models.py         # 交易資料模型 (Listing)
│       ├── views.py          # 賣家管理、買家瀏覽頁面
│       ├── urls.py           # 市場功能路由
│       └── services.py       # 交易業務邏輯 (上架、價格管理、錢包檢查)
├── static/             # 靜態檔案 (CSS、圖片等)
│   ├── css/                  # 樣式檔案
│   │   └── style.css         # 基礎樣式 (簡單佈局、按鈕樣式)
│   └── images/               # 圖片資源
├── templates/          # HTML 模板檔案
│   ├── base.html          # 基礎頁面模板 (導覽列、頁腳)
│   ├── objekt/            # 卡片相關頁面模板
│   │   ├── list.html        # 卡片清單頁面
│   │   └── detail.html      # 卡片詳細頁面
│   ├── marketplace/       # 市場相關頁面模板
│   │   ├── seller_dashboard.html  # 賣家管理後台
│   │   └── browse.html      # 買家瀏覽頁面
│   └── accounts/          # 用戶相關頁面模板
│       ├── register.html    # 註冊頁面
│       ├── login.html       # 登入頁面
│       └── accountinfo.html # 會員資訊頁面
├── requirements.txt    # Python 套件依賴清單
├── objekttraits.json   # NFT 屬性資料檔案 (用於初始化資料)
└── db.sqlite3          # SQLite 資料庫檔案 (執行後產生)
```

### 檔案功能說明

**models.py**: 定義資料庫資料表結構，ORM 關聯設計
**views.py**: 處理 HTTP 請求，串接 Service 和 Template
**services.py**: 商業邏輯層，OOP 設計模式
**urls.py**: URL 路由設定，決定網址對應哪個 View
**templates/**: HTML 頁面模板，基礎 CSS 樣式

## 前端方案

### 頁面設計重點
- 卡片展示（圖片 + 基本資訊）
- 基礎表單樣式（登入、註冊、上架）
- 簡單的導覽列和篩選選單

## 開發時程規劃（3 週）

### 第 1 週：Django 基礎
**目標：** 建立專案結構

- **Day 1-2：** Django 專案初始化
  - 專案建立、settings 設定
  - 建立 apps 資料夾結構
- **Day 3-4：** 資料模型設計
  - 設計 Model 類別、資料表
  - 整理 fixture 或寫 seed_objekt management command 一次性匯入 traits 基本屬性
  - 寫基本查詢 filter by traits
- **Day 5-7：** Service 層設計
  - 建立業務邏輯類別
  - 練習封裝、抽象化概念
  - 簡單的錢包檢查邏輯

### 第 2 週：Django Views + Templates
**目標：** 實現基本頁面功能

- **Day 8-10：** 用戶系統
  - 註冊、登入功能
  - 基礎 HTML 模板
- **Day 11-14：** 卡片展示系統
  - 卡片列表頁面
  - 卡片詳細頁面
  - 簡單搜尋功能

### 第 3 週：市場功能 + 整合測試
**目標：** 完成 MVP 核心功能

- **Day 15-17：** 賣家管理功能
  - 上架/下架介面
  - 價格設定功能
- **Day 18-21：** 整合測試與優化
  - 功能測試
  - 基礎樣式調整
  - 部署準備
