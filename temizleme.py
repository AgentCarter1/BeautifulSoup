import pymongo

# MongoDB bağlantı bilgileri
mongo_url = "mongodb://localhost:27017/"  # Varsayılan bağlantı URL'si (yerel sunucu)

# MongoDB istemcisini oluştur
client = pymongo.MongoClient(mongo_url)

# "smartmaple" veritabanına eriş
db = client["smartmaple"]

# "kitapyurdu" koleksiyonuna eriş
kitapyurdu_collection = db["kitapyurdu"]
kitapsepeti_collection = db["kitapsepeti"]
# Tüm verileri sil 
result = kitapyurdu_collection.delete_many({})
result2 = kitapsepeti_collection.delete_many({})
# Silme işleminden etkilenen belge sayısını yazdır
print(f"{result.deleted_count} belge silindi.")
print(f"{result2.deleted_count} belge silindi.")
# Bağlantıyı kapat
client.close()
