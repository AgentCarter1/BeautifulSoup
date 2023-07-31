import requests
from bs4 import BeautifulSoup as bts
import pymongo

# MongoDB bağlantı bilgileri
mongo_url = "mongodb://localhost:27017/"  # Varsayılan bağlantı URL'si (yerel sunucu)

# MongoDB istemcisini oluştur
client = pymongo.MongoClient(mongo_url)

# "smartmaple" adında bir veritabanı oluştur
db = client["smartmaple"]

# "kitapyurdu" ve "kitapsepeti" adında iki koleksiyon oluştur
kitapyurdu_collection = db["kitapyurdu"]
kitapsepeti_collection = db["kitapsepeti"]

def parseKitapsepetiURL(url):
    result = requests.get(url,headers={"User-Agent":"Mozilla/5.0"})
    soup = bts(result.text, 'html.parser')
    return soup

TotalLinkKitapSepeti = []

for totalLink in range(1,3):#linkler arasında dolaşıp bütün linkleri toplama !!! Kaç sayfadan veri almak istediğimiz aralığı belirtiyoruz  !!!
    
    TotalLinkKitapSepeti.append("https://www.kitapsepeti.com/roman?stock=1&pg="+str(totalLink))

ALL_KitapSepeti_URL = []

for products in TotalLinkKitapSepeti[::]:#bütün kitapların tek tek url bilgileri toplanıyor
    html = parseKitapsepetiURL(products)

    for link in html.find_all("div",{"class":"productItem"}):
        ALL_KitapSepeti_URL.append("https://www.kitapsepeti.com"+link.a["href"])


resultKitapSepeti = []
for details in ALL_KitapSepeti_URL[::]:#kitapların bilgilerini alıyoruz
    html = parseKitapsepetiURL(details)
    Book_name = html.find("h1",{"id":"productName"}).text.strip()
    Writer = html.find("a",{"id":"productModelText"}).text.strip()
    Publisher = html.find("a",{"class":"product-brand"}).text.strip()
    price = html.find("span",{"class":"product-price"}).text.strip()
    resultKitapSepeti.append([Book_name,Writer,Publisher,price])

for data in resultKitapSepeti:#kitap bilgilerini veritabanına kaydediyoruz
    kitapyurdu_data = [
        {
            "kullanilanSite": "Kitapyurdu",
            "kitapAdi": data[0],
            "kitapYazari": data[1],
            "KitapYayinevi": data[2],
            "KitapFiyati": data[3],
        },
    ]
    kitapsepeti_collection.insert_many(kitapyurdu_data)


def parseURL(url):
    result = requests.get(url,headers={"User-Agent":"Mozilla/5.0"})
    soup = bts(result.text, 'html.parser')
    return soup

Total_Link = []

for totalLink in range(1,3):
    Total_Link.append("https://www.kitapyurdu.com/index.php?route=product/category&page="+str(totalLink)+"&filter_category_all=true&path=1_1033&filter_in_stock=1&filter_in_shelf=1&sort=purchased_365&order=DESC")

ALL_PRODUCT_URL = []

for products in Total_Link[::]:
    html = parseURL(products)

    for link in html.find_all("div",{"class":"product-cr"}):
        ALL_PRODUCT_URL.append(link.a["href"])

result = []
for details in ALL_PRODUCT_URL[::]:
    html = parseURL(details)
    Book_name = html.find("h1",{"class":"pr_header__heading"}).text.strip()
    Writer = html.find("a",{"class":"pr_producers__link"}).text.strip()
    Publisher = html.find("div",{"class":"pr_producers__publisher"}).text.strip()
    price = html.find("div",{"class":"price__item"}).text.strip()
    result.append([Book_name,Writer,Publisher,price])

for data in result:
    kitapyurdu_data = [
        {
            "kullanilanSite": "Kitapyurdu",
            "kitapAdi": data[0],
            "kitapYazari": data[1],
            "KitapYayinevi": data[2],
            "KitapFiyati": data[3],
        },
    ]
    kitapyurdu_collection.insert_many(kitapyurdu_data)

client.close()