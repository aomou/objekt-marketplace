from django.db import models

'''
定義 objekt 相關的資料表
- Artist 藝人團體
- Unit 小分隊 (待新增)
- Member 成員
- Season 季節
- Class 等級
- Collection 編號
- Objekt Type 卡面種類
- Objekt Card 卡片本體

'''

class Artist(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    tokenId = models.IntegerField()
    sex = models.CharField(max_length=5)

    def __str__(self):  # 預設顯示名字
        return self.name

    class Meta:
        ordering = ['tokenId']   # 預設 query 的排序

# class Unit(models.Model):     # OEC, AAA, KRE, UNM
#     artist = models.ForeignKey(Artist, on_delete=models.PROTECT) 
#     member = models.ForeignKey(Member, on_delete=models.PROTECT)
#     name = CharField(max_length=80)
#     debutDate = models.DateField(null=True)

class Member(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    artist = models.ForeignKey(Artist, on_delete=models.PROTECT, blank=True, null=True) 
    memberCode = models.CharField(max_length=50, blank=True, null=True)
    memberNum = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ['memberNum']   # 預設 query 的排序

    def __str__(self):
        return self.name

class Season(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    shortname = models.CharField(max_length=50, blank=True, null=True)
    artist = models.ForeignKey(Artist, on_delete=models.PROTECT, blank=True) 
    startDate = models.DateField(null=True, blank=True)
    endDate = models.DateField(null=True, blank=True)
    seasonPrefix = models.CharField(max_length=50)
    seasonNum = models.IntegerField()
    
    class Meta:
        unique_together = ("name", "artist")
        ordering = ['artist', 'startDate']

    def __str__(self):
        return self.name
    
class Class(models.Model):
    name = models.CharField(max_length=50)
    artist = models.ForeignKey(Artist, on_delete=models.PROTECT, null=True) # blank=True, 
    startNum = models.IntegerField(null=True) # blank=True, 

    class Meta:
        unique_together = ("name", "artist")
        ordering = ['artist', 'startNum']

    def __str__(self):
        return self.name

# TODO add artist to class mapping 

class Collection(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    collection_number = models.CharField(max_length=20, blank=True, null=True)
    collection_suffix = models.CharField(max_length=20, null=True)
    physical = models.BooleanField(default=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name



# 卡面
class ObjektType(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.PROTECT) 
    member = models.ForeignKey(Member, on_delete=models.PROTECT)
    season = models.ForeignKey(Season, on_delete=models.PROTECT)
    objekt_class = models.ForeignKey(Class, on_delete=models.PROTECT)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
    image_uri = models.CharField(max_length=300, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def shortname(self):
        shortname = self.season.shortname or self.season.name  # 避免為空值
        return f"{self.member.name} {shortname}{self.collection.name}"

    def __str__(self):
        return f"{self.season.name} {self.member.name} {self.collection.name}"    

    class Meta:
        ordering = ['artist', 'collection', 'member']

# 卡實體 with serial
class ObjektCard(models.Model):
    objekt_type = models.ForeignKey(ObjektType, on_delete=models.PROTECT)
    token_id = models.BigIntegerField(unique=True)
    # serial = models.IntegerField() 不會算
    owner_address = models.CharField(max_length=200)
    minted_at = models.DateTimeField(null=True, blank=True)
    last_seen_at = models.DateTimeField(null=True, blank=True)
    updated_at  = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.objekt_type} #{self.token_id} "
    
    def get_img(self):
        return self.objekt_type.image_uri