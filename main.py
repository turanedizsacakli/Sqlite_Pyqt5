from PyQt5.QtWidgets import *
from addProduct import *
import sys
from PyQt5 import QtWidgets
import sqlite3


class myApp(QtWidgets.QMainWindow,QDialog):
    def __init__(self):
        super(myApp, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.window=QMainWindow()
        # butonlar
        self.ui.btnEkle.clicked.connect(self.addProduct)
        self.ui.btnListele.clicked.connect(self.listOfRecords)
        self.ui.btnKategoriyeGoreListele.clicked.connect(self.callWithCategory)
        self.ui.btnSil.clicked.connect(self.deleteRecords)
        self.ui.btnGuncelle.clicked.connect(self.updateRecords)
        # Veritabanı işlemleri
        self.connecting = sqlite3.connect("urunler.db")
        self.process = self.connecting.cursor()
        self.connecting.commit()
        table = self.process.execute("create table if not exists urun (urunKodu int, urunAdi text, birimFiyat int, stokMiktari int, urunAciklaması text, marka text, kategori text)")
        self.connecting.commit()


    def addProduct(self):
        UrunKodu = int(self.ui.lneurunKodu.text())
        UrunAdi = self.ui.lneurunAdi.text()
        BirimFiyat = int(self.ui.lnebirimFiyat.text())
        StokMiktari = int(self.ui.lnestokMiktari.text())
        UrunAciklama = self.ui.lneurunAciklama.text()
        Marka = self.ui.cmbMarka.currentText()
        Kategori = self.ui.cmbKategori.currentText()

        try:
            ekle = "insert into urun (urunKodu,urunAdi,birimFiyat,stokMiktari,urunAciklaması,marka,kategori) values (?,?,?,?,?,?,?)"
            self.process.execute(ekle,(UrunKodu,UrunAdi,BirimFiyat,StokMiktari,UrunAciklama,Marka,Kategori))
            self.connecting.commit()
            self.listOfRecords()
            self.ui.statusbar.showMessage("Kayıt Ekleme İşlemi Başarılı",10000)
        except Exception as error:
            self.ui.statusbar.showMessage("Kayıt Eklenemedi Hata Çıktı === "+str(error))


    def listOfRecords(self):
        self.ui.tblListele.clear()
        self.ui.tblListele.setHorizontalHeaderLabels(("Ürün Kodu","Ürün Adi","Birim Fiyatı","Stok Miktarı","Ürün Açıklama","Markası","Kategori"))
        self.ui.tblListele.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        queryOfMe = "select * from urun"
        self.process.execute(queryOfMe)

        for indexSatir, kayitNumarasi in enumerate(self.process):
            for indexSutun, kayitSutun in enumerate(kayitNumarasi):
                self.ui.tblListele.setItem(indexSatir,indexSutun,QTableWidgetItem(str(kayitSutun)))
        #self.listOfRecords() 
         
    def callWithCategory(self):
        listOfCategory = self.ui.cmbKategorListele.currentText()

        queryOfMe = "select * from urun where kategori = ?"
        self.process.execute(queryOfMe,(listOfCategory,))
        self.ui.tblListele.clear()
        for indexSatir, kayitNumarasi in enumerate(self.process):
            for indexSutun, kayitSutun in enumerate(kayitNumarasi):
                self.ui.tblListele.setItem(indexSatir,indexSutun,QTableWidgetItem(str(kayitSutun)))


    def deleteRecords(self):
        beDeletedMessage = QMessageBox.question(self.window,"Silme Onayı","Silmek İstediğinizden Emin Misiniz ?",QMessageBox.Yes | QMessageBox.No)

        if beDeletedMessage == QMessageBox.Yes:
            recordChoosen = self.ui.tblListele.selectedItems()
            recordWillBeDeleted = recordChoosen[0].text()

            queryOfMe = "delete from urun where urunKodu = ?"
            try:
                self.process.execute(queryOfMe,(recordWillBeDeleted,))
                self.connecting.commit()
                self.ui.statusbar.showMessage("Kayıt Başarıyla Silindi")
                self.listOfRecords()
            except Exception as error:
                self.ui.statusbar.showMessage("Kayıt Silinirken Hata Çıktı === "+str(error))
        
        else:
            self.ui.statusbar.showMessage("Silme İşlemi İptal Edildi...")
        
#kayıtları güncellemede sorunlar var...seçili alanı okuyup yazması lazım direkt...

    def updateRecords(self):
        
        updatedMessage = QMessageBox.question(self.window,"Güncelleme Onayı","Bu kaydı Güncellemek istediğinizden Emin Misiniz ?",QMessageBox.Yes | QMessageBox.No)

        if updatedMessage == QMessageBox.Yes:
            try:
                UrunKodu = self.ui.lneurunKodu.text()
                UrunAdi = self.ui.lneurunAdi.text()
                BirimFiyati = self.ui.lnebirimFiyat.text()
                StokMiktari = self.ui.lnestokMiktari.text()
                UrunAciklama = self.ui.lneurunAciklama.text()
                Marka = self.ui.cmbMarka.currentText()
                Kategori = self.ui.cmbKategori.currentText()

                if UrunAdi == "" and BirimFiyati == "" and StokMiktari == "" and UrunAciklama == "" and Marka == "":
                    self.process.execute("update urun set kategori = ? where urunKodu = ?",(Kategori,UrunKodu))
                elif UrunAdi == "" and BirimFiyati == "" and StokMiktari == "" and UrunAciklama == "" and Kategori == "":
                    self.process.execute("update urun set marka = ? where urunKodu = ?",(Marka,UrunKodu)) 
                elif UrunAdi == "" and BirimFiyati == "" and StokMiktari == "" and Marka == "" and Kategori == "":
                    self.process.execute("update urun set urunAciklaması = ? where urunKodu = ?",(UrunAciklama,UrunKodu))
                elif UrunAdi == "" and BirimFiyati == "" and UrunAciklama == "" and Marka == "" and Kategori == "":
                    self.process.execute("update urun set stokMiktari = ? where urunKodu = ?",(StokMiktari,UrunKodu))
                elif UrunAdi == "" and StokMiktari == "" and UrunAciklama == "" and Marka == "" and Kategori == "":
                    self.process.execute("update urun set birimFiyat = ? where urunKodu = ?",(BirimFiyati,UrunKodu))
                elif BirimFiyati == "" and StokMiktari == "" and UrunAciklama == "" and Marka == "" and Kategori == "":
                    self.process.execute("update urun set urunAdi = ? where urunKodu = ?",(UrunAdi,UrunKodu))
                else:
                    self.process.execute("update urun set urunAdi = ?, birimFiyat = ? , stokMiktari = ?, urunAciklaması = ?, marka = ?, kategori = ? where urunKodu = ?",(UrunAdi,BirimFiyati,StokMiktari,UrunAciklama,Marka, Kategori,UrunKodu))
                self.connecting.commit()
                listOfRecords()
                self.ui.statusbar.showMessage("Kayıt Başarıyla Güncellendi")
            except Exception as error:
                self.ui.statusbar.showMessage("Kayıt Güncellemede Hata Çıktı === "+str(error))
        else:
            self.ui.statusbar.showMessage("Güncelleme İptal Edildi")




def app():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet("QPushButton {border-radius:10px; background-color: black; color:white; border:10px;}")
    widget=QtWidgets.QStackedWidget()
    widget.addWidget(myApp())
    win = myApp()
    win.show()
    sys.exit(app.exec_())
    
app()


