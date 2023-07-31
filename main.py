from PyQt5 import QtWidgets
import sys
from PyQt5.QtWidgets import *
from panel import *
import pymongo
import re
import os
from PyQt5.QtGui import QFont
import re
import schedule

os.system("python temizleme.py")
os.system("python takeData.py")

def run_tasks():
    os.system("python temizleme.py")
    os.system("python takeData.py")

# schedule kütüphanesi ile işlemi planlayalım
schedule.every(2).days.at("12:00").do(run_tasks)

#Arayüz ekranını açalım
uygulama = QApplication(sys.argv)
pencere = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(pencere)
pencere.show()

#Veritabanına bağlanalım
mongo_url = "mongodb://localhost:27017/"
client = pymongo.MongoClient(mongo_url)
db = client["smartmaple"]
kitapyurdu_collection = db["kitapyurdu"]
kitapsepeti_collection = db["kitapsepeti"]
# Tabloyu sıfırlayarak varolan içeriği temizle
ui.tableWidget.setRowCount(0)
ui.tableWidget_2.setRowCount(0)
ui.tableWidget.setColumnCount(4)  # 4 sütun
ui.tableWidget_2.setColumnCount(4)  # 4 sütun
ui.tableWidget.setHorizontalHeaderLabels(["Kitap Adı", "Kitap Yazarı", "Kitap Yayınevi", "Kitap Fiyati"])  # Sütun başlıkları
ui.tableWidget_2.setHorizontalHeaderLabels(["Kitap Adı", "Kitap Yazarı", "Kitap Yayınevi", "Kitap Fiyati"])  # Sütun başlıkları
font = QFont()
font.setPointSize(14)  # 14 punto büyüklüğünde fon
# Sütun başlığı fontunu ayarlayalım
ui.tableWidget.horizontalHeader().setFont(font)
ui.tableWidget_2.horizontalHeader().setFont(font)
# Veriri MongoDB veritabanından çek
kitapyurdu_data = kitapyurdu_collection.find()
kitapsepeti_data = kitapsepeti_collection.find()
# Tabloya verileri ekleyerek doldur
for row_idx, (data_kitapYurdu,data_kitapSepeti) in enumerate(zip(kitapyurdu_data,kitapsepeti_data)):
    ui.tableWidget.insertRow(row_idx)
    ui.tableWidget.setItem(row_idx, 0, QtWidgets.QTableWidgetItem(data_kitapYurdu["kitapAdi"]))
    ui.tableWidget.setItem(row_idx, 1, QtWidgets.QTableWidgetItem(data_kitapYurdu["kitapYazari"]))
    ui.tableWidget.setItem(row_idx, 2, QtWidgets.QTableWidgetItem(data_kitapYurdu["KitapYayinevi"]))
    ui.tableWidget.setItem(row_idx, 3, QtWidgets.QTableWidgetItem(str(data_kitapYurdu["KitapFiyati"])))
    #---------------------------------------------------------------------------------------------------
    ui.tableWidget_2.insertRow(row_idx)
    ui.tableWidget_2.setItem(row_idx, 0, QtWidgets.QTableWidgetItem(data_kitapSepeti["kitapAdi"]))
    ui.tableWidget_2.setItem(row_idx, 1, QtWidgets.QTableWidgetItem(data_kitapSepeti["kitapYazari"]))
    ui.tableWidget_2.setItem(row_idx, 2, QtWidgets.QTableWidgetItem(data_kitapSepeti["KitapYayinevi"]))
    ui.tableWidget_2.setItem(row_idx, 3, QtWidgets.QTableWidgetItem(str(data_kitapSepeti["KitapFiyati"])))

#Seçilen aralıktaki ürünleri listeleyelim
def item_clicked():
    item =  ui.listWidget.currentItem()
    pattern = r"\d+"  
    matches = re.findall(pattern, item.text())
    ui.tableWidget.setRowCount(0)   
    start = int(matches[0])-1
    end = int(matches[1])-1
  
    kitapyurdu_data = kitapyurdu_collection.find()[start:end]
    for row_idx, data_kitapYurdu in enumerate(kitapyurdu_data):
        ui.tableWidget.insertRow(row_idx)
        ui.tableWidget.setItem(row_idx, 0, QtWidgets.QTableWidgetItem(data_kitapYurdu["kitapAdi"]))
        ui.tableWidget.setItem(row_idx, 1, QtWidgets.QTableWidgetItem(data_kitapYurdu["kitapYazari"]))
        ui.tableWidget.setItem(row_idx, 2, QtWidgets.QTableWidgetItem(data_kitapYurdu["KitapYayinevi"]))
        ui.tableWidget.setItem(row_idx, 3, QtWidgets.QTableWidgetItem(str(data_kitapYurdu["KitapFiyati"])))
    

for i in range(0,53):
    if i == 0:
        ui.listWidget.insertItem(i,(str(i+1)+" - "+str(20*(i+1))))
    ui.listWidget.insertItem(i+1,(str(((i+1)*20)+1)+" - "+str(20*(i+2))))

ui.listWidget.clicked.connect(item_clicked)

def item_clicked2():
    item =  ui.listWidget_2.currentItem()
    pattern = r"\d+"  
    matches = re.findall(pattern, item.text())
    ui.tableWidget_2.setRowCount(0)   
    start = int(matches[0])-1
    end = int(matches[1])-1
  
    kitapsepeti_data = kitapsepeti_collection.find()[start:end]
    for row_idx, data_kitapSepeti in enumerate(kitapsepeti_data):
        ui.tableWidget_2.insertRow(row_idx)
        ui.tableWidget_2.setItem(row_idx, 0, QtWidgets.QTableWidgetItem(data_kitapSepeti["kitapAdi"]))
        ui.tableWidget_2.setItem(row_idx, 1, QtWidgets.QTableWidgetItem(data_kitapSepeti["kitapYazari"]))
        ui.tableWidget_2.setItem(row_idx, 2, QtWidgets.QTableWidgetItem(data_kitapSepeti["KitapYayinevi"]))
        ui.tableWidget_2.setItem(row_idx, 3, QtWidgets.QTableWidgetItem(str(data_kitapSepeti["KitapFiyati"])))

for i in range(0,524):
    if i == 0:
        ui.listWidget_2.insertItem(i,(str(i+1)+" - "+str(20*(i+1))))
    ui.listWidget_2.insertItem(i+1,(str(((i+1)*20)+1)+" - "+str(20*(i+2))))

ui.listWidget_2.clicked.connect(item_clicked2)

sys.exit(uygulama.exec_())