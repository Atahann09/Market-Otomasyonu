from tkinter import *
import sqlite3
import tkinter.messagebox
from datetime import datetime
import tkinter as tk
import os
from tkinter import messagebox
from pyzbar.pyzbar import decode
from PIL import Image
import pyqrcode

suan = datetime.now()
conn = sqlite3.connect("veriler.db")
c = conn.cursor()

class Urun():
    def __init__(self, uAdi, marka, fiyat, skt, uCesidi, stok):
        self.uAdi = uAdi
        self.marka = marka
        self.fiyat = fiyat
        self.skt = skt
        self.uCesidi = uCesidi
        self.stok = stok

    def __str__(self):
        return self.stok

class SuperMarket:

    def __init__(self, pencere):

        self.ilkGiris = True
        self.gunlukToplamMusteri = 0
        self.toplamfiyat = 0
        self.toplamCiro = 0
        self.gunlukToplamIade = 0
        self.paraustu = 0
        self.pencere = pencere
        self.baslik = Label(self.pencere, text="Yazılım Market", font=('calibri 55 bold'), fg='black', bg='white')
        self.baslik.place(x=440, y=25)

        self.urunadi = Label(self.pencere, text="Ürün Adı Gir", width=20, borderwidth=2, relief="groove", font=(' bold', 10), bg = "white")
        self.urunadi.place(x=5, y=480)
        self.urunadi_gir = Entry(self.pencere, width=30)
        self.urunadi_gir.place(x=185, y=480)

        self.marka = Label(self.pencere, text="Ürün Markası Gir", width=20, borderwidth=2, relief="groove", font=(' bold', 10), bg = "white")
        self.marka.place(x=5, y=520)
        self.marka_gir = Entry(self.pencere, width=30)
        self.marka_gir.place(x=185, y=520)

        self.fiyat = Label(self.pencere, text="Ürün Fiyatı Gir", width=20, borderwidth=2, relief="groove", font=(' bold', 10), bg = "white")
        self.fiyat.place(x=5, y=560)
        self.fiyat_gir = Entry(self.pencere, width=30)
        self.fiyat_gir.place(x=185, y=560)

        self.skt = Label(self.pencere, text="Ürünün Son Kullanma Tarihi", width=20, borderwidth=2, relief="groove",font=(' bold', 10), bg = "white")
        self.skt.place(x=405, y=480)
        self.skt_gir = Entry(self.pencere, width=30)
        self.skt_gir.place(x=585, y=480)

        self.cesidi = Label(self.pencere, text="Ürünün Çeşidini Gir", width=20, borderwidth=2, relief="groove",font=(' bold', 10), bg = "white")
        self.cesidi.place(x=405, y=520)
        self.urunCesidi_gir = Entry(self.pencere, width=30)
        self.urunCesidi_gir.place(x=585, y=520)

        self.stok = Label(self.pencere, text="Ürünün Stok Sayısı", width=20, borderwidth=2, relief="groove",font=(' bold', 10), bg = "white")
        self.stok.place(x=405, y=560)
        self.stok_gir = Entry(self.pencere, width=30)
        self.stok_gir.place(x=585, y=560)

        self.butonekle = tk.Button(self.pencere, text="Ürünü Ekle",relief="raised", borderwidth=3,  width=30, height=2, bg='#FF8800', fg='white',font =('calibri 12 bold'),
                             command=self.ekle)
        self.butonekle.place(x=240, y=600)

        #Sil
        self.etiket2 = tk.Label(self.pencere, text="Ürün Sil",font =('calibri 12 bold'))
        self.etiket2.place(x=750, y=282, anchor='center')
        self.silinecekurunadi = tk.Entry(self.pencere, width=20)
        self.silinecekurunadi.place(x=700, y=300)
        self.butonsil = tk.Button(self.pencere, text="Sil", bg = "red", command=self.sil, font =('calibri 12 bold'), fg = "white")
        self.butonsil.place(x=740, y=320)

        #UrunStokSorgula
        self.etiket3 = tk.Label(self.pencere, text = "Ürün Stok sorgula",font =('calibri 12 bold'))
        self.etiket3.place(x=750, y=180, anchor='center')
        self.stogusorulanurunadi = tk.Entry(self.pencere, width=20)
        self.stogusorulanurunadi.place(x=700, y=200)
        self.butonsor = tk.Button(self.pencere, text="Stok Sor", command=self.stoksor, font =('calibri 12 bold'), bg = "white")
        self.butonsor.place(x=715, y=220)

        #SonKullanmaTarihigecenleriSil
        self.etiket4 = tk.Label(self.pencere, text="Silinmesi istenilen tarih (Örn: 01.01.2019)", font =('calibri 12 bold'))
        self.etiket4.place(x=750, y=380, anchor='center')
        self.silinecektarih = tk.Entry(self.pencere, width=20)
        self.silinecektarih.place(x=700, y=390)
        self.butonsonkullanma = tk.Button(self.pencere, text="SKT", command=self.tarihsil, font =('calibri 12 bold'), bg = "white")
        self.butonsonkullanma.place(x=740, y=420)

        #SatisYap
        self.etiket13 = tk.Label(self.pencere, text="Satışı Yapılacak Ürünü Adedi =", font=('calibri 12 bold'))
        self.etiket13.place(x=1000, y=185, anchor='center')
        self.satisyapilacakurunadedi = tk.Entry(self.pencere, width=20)
        self.satisyapilacakurunadedi.place(x=1110, y=174)

        self.etiket7 = tk.Label(self.pencere, text="Satışı Yapılacak Ürünü Girin =", font=('calibri 12 bold'))
        self.etiket7.place(x=1000, y=210, anchor='center')
        self.satisyapilacakurun = tk.Entry(self.pencere, width=20)
        self.satisyapilacakurun.place(x=1110, y=202)
        self.butonsatis = tk.Button(self.pencere, text="Satış Yap",relief="raised", borderwidth=2, width=20, height=1,
                                   bg='#FF8800', fg='white', font=('calibri 12 bold'), command=self.satisyap)
        self.butonsatis.place(x=1100, y=230)

        #Fiskes
        self.butonfiskes = tk.Button(self.pencere, text = "Fiş Kes",command =self.FisKes, relief="raised", borderwidth=2,  width=20, height=1, bg='lightblue',
                                     fg='black', font =('calibri 12 bold'),)
        self.butonfiskes.place(x=1100, y=400)
        #listele
        self.butonliste = tk.Button(self.pencere, text="Ürünleri Listele", command=self.listele, relief="raised", borderwidth=3,  width=30, height=2, bg='lightblue',
                                    fg='black',font =('calibri 12 bold'))
        self.butonliste.place(x=80, y=70)

        #iadeal
        self.etiket17 = tk.Label(self.pencere, text="İade Edilecek Ürünü Girin", font=('calibri 12 bold'))
        self.etiket17.place(x=1090, y=460, anchor='center')
        self.etiket18 = tk.Label(self.pencere, text="İade Ürün Sayısı", font=('calibri 12 bold'))
        self.etiket18.place(x=1260, y=460, anchor='center')

        self.iadealma = tk.Entry(self.pencere, width=20)
        self.iadealma.place(x=1030, y=480)

        self.iadealmasayi = tk.Entry(self.pencere, width=20)
        self.iadealmasayi.place(x=1190, y=480)

        self.butoniade = tk.Button(self.pencere, text="İade Al", command=self.iade, relief="raised", borderwidth=2,
                                     width=20, height=1, bg='white',
                                     fg='black', font=('calibri 12 bold'), )
        self.butoniade.place(x=1100, y=515)
        #gunlukmusterisayisi
        self.butonmusteri = tk.Button(self.pencere, text="Günlük Toplam Müşteri", command=self.gunlukmusteri, relief="raised", borderwidth=2,
                                   width=20, height=1, bg='white',
                                   fg='black', font=('calibri 12 bold'), )
        self.butonmusteri.place(x=1100, y=565)
        #gunlukCiroHesapla
        self.butongunlukar = tk.Button(self.pencere, text="Günlük Toplam Ciro", command=self.gunlukciro,relief="raised", borderwidth=2,
                                       width=20, height=1, bg='white',
                                       fg='black', font=('calibri 12 bold'), )
        self.butongunlukar.place(x=1100, y=630)
        #nakital
        self.etiket14 = tk.Label(self.pencere, text="Nakit Ödenecek Tutar = ", font=('calibri 12 bold'))
        self.etiket14.place(x=1000, y=330, anchor='center')
        self.odenennakit = tk.Entry(self.pencere, width=20)
        self.odenennakit.place(x=1100, y=320)

        #qrcode
        self.qrolusturen = tk.Entry(self.pencere, width=20)
        self.qrolusturen.place(x=950, y=54)
        self.butonqrolus = tk.Button(self.pencere,text="Qr kod Oluştur", font=('calibri 12 bold'), command=self.qrolustur, bg='black', fg='white')
        self.butonqrolus.place(x=1010, y=100, anchor='center')

        self.qrokuen = tk.Entry(self.pencere, width=20)
        self.qrokuen.place(x=1100, y=54)
        self.butonqroku = tk.Button(self.pencere, text="Qr kod Oku", font=('calibri 12 bold'),
                                     command=self.qroku, bg='black', fg='white')
        self.butonqroku.place(x=1154, y=100, anchor='center')

    def qrolustur(self):
        qr = pyqrcode.create(self.qrolusturen.get())
        qr.png(self.qrolusturen.get()+'.png', scale=8)



    def gunlukciro(self):
        self.etiket12 = tk.Label(self.pencere,
                                 text="Bugün toplam Ciro {} TL".format(self.toplamCiro),
                                 font=('calibri 12 bold'))
        self.etiket12.place(x=1190, y=680, anchor='center')

    def gunlukmusteri(self):
        self.etiket11 = tk.Label(self.pencere, text="Bugün toplam {} müşteri gelmiştir".format(self.gunlukToplamMusteri), font=('calibri 12 bold'))
        self.etiket11.place(x=1200, y=615, anchor='center')

    def iade(self):
        self.val15 = self.iadealmasayi.get()
        self.val12 = self.iadealma.get()
        sorgu = "SELECT * FROM veriler WHERE UrunAdi = ?"
        c.execute(sorgu, (self.val12,))
        urunler = c.fetchall()
        sayi = int(self.val15)

        stok = urunler[0][5]
        stok += sayi
        self.toplamCiro -= urunler[0][2] * sayi
        sorgu2 = "UPDATE veriler SET Stok = ? WHERE UrunAdi = ?"
        c.execute(sorgu2, (stok, self.val12))
        conn.commit()
        tkinter.messagebox.showinfo("Bilgi", "İade alındı.")
        self.gunlukToplamIade += 1

    def listele(self):
        self.butonliste.configure(bg = "white",text ="Tüm Ürünler Listelendi", fg="black")
        self.urunadlari = Text(self.pencere, width=12, bg = "lightblue", height=15, font=('calibri 11 bold'))
        self.urunadlari.place(x=80, y=135)
        self.UrunCesitleri = Text(self.pencere, width=12, bg = "lightblue", height=15, font=('calibri 11 bold'))
        self.UrunCesitleri.place(x=160, y=135)
        self.markalar = Text(self.pencere, width=12, bg = "lightblue", height=15, font=('calibri 11 bold'))
        self.markalar.place(x=240, y=135)
        self.fiyatlar = Text(self.pencere, width=12, bg = "lightblue", height=15, font=('calibri 11 bold'))
        self.fiyatlar.place(x=320, y=135)
        self.sonkullanma = Text(self.pencere, width=18, bg = "lightblue", height=15, font=('calibri 11 bold'))
        self.sonkullanma.place(x=400, y=135)
        self.stok = Text(self.pencere, width=12, bg = "lightblue", height=15, font=('calibri 11 bold'))
        self.stok.place(x=520, y=135)

        c.execute("SELECT Stok FROM veriler")
        column = c.fetchall()
        self.stok.insert(END, "Stok Sayısı" + "\n")
        for column in column:
            self.stok.insert(END, column)
            self.stok.insert(END, "\n")

        c.execute("SELECT SKT FROM veriler")
        column = c.fetchall()
        self.sonkullanma.insert(END, "Son kullanma tarihi" + "\n")
        for column in column:
            self.sonkullanma.insert(END, column)
            self.sonkullanma.insert(END, "\n")

        c.execute("SELECT UrunAdi FROM veriler")
        column = c.fetchall()
        self.urunadlari.insert(END, "Ürün Adı"+"\n")
        for column in column:
            self.urunadlari.insert(END, column)
            self.urunadlari.insert(END, "\n")

        c.execute("SELECT Marka FROM veriler")
        column = c.fetchall()
        self.markalar.insert(END, "Ürün Markası" + "\n")
        for column in column:
            self.markalar.insert(END, column)
            self.markalar.insert(END, "\n")

        c.execute("SELECT Fiyat FROM veriler")
        column = c.fetchall()
        self.fiyatlar.insert(END, "Ürün Fiyat" + "\n")
        for column in column:
            self.fiyatlar.insert(END, column)
            self.fiyatlar.insert(END, "\n")

        c.execute("SELECT UrunCesidi FROM veriler")
        column = c.fetchall()
        self.UrunCesitleri.insert(END, "Ürün Cesidi" + "\n")
        for column in column:
            self.UrunCesitleri.insert(END, column)
            self.UrunCesitleri.insert(END, "\n")

    def satisyap(self):
        self.val13 = self.satisyapilacakurunadedi.get()
        self.val10 = self.satisyapilacakurun.get()
        self.satisyapveri()

    def qroku(self):
        d = decode(Image.open(self.qrokuen.get() + '.png'))
        okunan = d[0].data.decode('ascii')
        sorgu = "SELECT * FROM veriler WHERE UrunAdi = ?"
        c.execute(sorgu, (okunan,))
        urun = c.fetchall()
        self.urunstok = urun[0][5]
        self.urunstok -= 1
        self.toplamfiyat += urun[0][2]
        sorgu2 = "UPDATE veriler SET Stok = ? WHERE UrunAdi = ?"
        c.execute(sorgu2, (self.urunstok, okunan))
        conn.commit()

    def satisyapveri(self):
        sorgu = "SELECT * FROM veriler WHERE UrunAdi = ?"
        c.execute(sorgu, (self.val10,))
        urun = c.fetchall()
        q = int(self.val13)
        if (len(urun) == 0):
            self.etiket8 = tk.Label(self.pencere, text="Bu ürün bulunmuyor.",font=('calibri 12 bold'))
            self.etiket8.place(x=1000, y=260, anchor='center')
        self.urunstok = urun[0][5]
        self.urunstok -= q
        self.toplamfiyat += urun[0][2] * q
        self.ilkGiris = False
        self.etiket8 = tk.Label(self.pencere, text="Ürün Sepete Eklendi.", font=('calibri 12 bold'))
        self.etiket8.place(x=1320, y=210, anchor='center')
        sorgu2 = "UPDATE veriler SET Stok = ? WHERE UrunAdi = ?"
        c.execute(sorgu2, (self.urunstok, self.val10))
        conn.commit()

    def FisKes(self):
        self.val14 = self.odenennakit.get()
        self.etiket10 = tk.Label(self.pencere, text="Sepetin toplam Fiyatı =", font =('calibri 12 bold'))
        self.etiket10.place(x=1000, y=360, anchor='center')
        self.etiket9 = tk.Label(self.pencere, text=self.toplamfiyat, font =('calibri 12 bold'))
        self.etiket9.place(x=1120, y=360, anchor='center')
        self.gunlukToplamMusteri += 1
        self.toplamCiro += self.toplamfiyat
        self.paraustu += int(self.val14)
        self.paraustu -= int(self.toplamfiyat)
        self.etiket16 = tk.Label(self.pencere, text="Ödenecek Para üstü =", font=('calibri 12 bold'))
        self.etiket16.place(x=1000, y=390, anchor='center')
        self.etiket15 = tk.Label(self.pencere, text=self.paraustu, font=('calibri 12 bold'))
        self.etiket15.place(x=1120, y=390, anchor='center')

        self.ilkGiris = True
        self.toplamfiyat = 0

    def stoksor(self):
        self.val8 = self.stogusorulanurunadi.get()
        self.stoksorveri()
    def stoksorveri(self):
        sorgu = "SELECT * FROM veriler WHERE UrunAdi = ?"
        c.execute(sorgu, (self.val8,))
        urunler = c.fetchall()
        toplamurun = 0
        for i in urunler:
            toplamurun += i[5]
        self.etiket5 = tk.Label(self.pencere, text= toplamurun, font =('calibri 12 bold'))
        self.etiket5.place(x=800, y=210, anchor='center')

    def ekle(self):
        self.val1 = self.urunadi_gir.get()
        self.val2 = self.marka_gir.get()
        self.val3 = self.fiyat_gir.get()
        self.val4 = self.skt_gir.get()
        self.val5 = self.urunCesidi_gir.get()
        self.val6 = self.stok_gir.get()
        self.ekleveri()
    def ekleveri(self):
        c.execute(
            'CREATE TABLE IF NOT EXISTS veriler(UrunAdi TEXT,Marka TEXT,Fiyat INT,SKT TEXT,UrunCesidi TEXT,Stok INT)')
        c.execute('INSERT INTO veriler(UrunAdi ,Marka ,Fiyat ,SKT ,UrunCesidi ,Stok) VALUES(?,?,?,?,?,?)',
                  (self.val1, self.val2, self.val3, self.val4, self.val5, self.val6))
        conn.commit()
        tkinter.messagebox.showinfo("Bilgi", "Eklendi.")

    def sil(self):
        self.val7 = self.silinecekurunadi.get()
        self.Urunsilveri()
    def Urunsilveri(self):
        sorgu2 = "SELECT * FROM veriler WHERE UrunAdi = ?"
        c.execute(sorgu2, (self.val7,))
        silinecekUrunler = c.fetchall()
        sorgu = "DELETE FROM veriler WHERE UrunAdi = ?"
        c.execute(sorgu, (self.val7,))
        conn.commit()
        tkinter.messagebox.showinfo("Bilgi", "Silindi.")

    def tarihsil(self):
        self.val9 = self.silinecektarih.get()
        self.tarihsilveri()

    def tarihsilveri(self):
        sorgu = "SELECT * FROM veriler"
        sorgu2 = "DELETE FROM veriler WHERE UrunAdi = ?"
        c.execute(sorgu)
        butunurunler = c.fetchall()
        if (len(butunurunler) == 0):
            self.etiket6 = tk.Label(self.pencere, text="Hic Urun Bulunamadı")
            self.etiket6.place(x=700, y=440, anchor='center')
        else:
            for i in butunurunler:
                sktlistesi = i[3].split(".")
                tarihlistesi = self.val9.split(".")
                if (tarihlistesi[2] >= sktlistesi[2]):
                    c.execute(sorgu2, (i[0], ))
                    conn.commit()
                elif (tarihlistesi[2] == sktlistesi[2] and tarihlistesi[1] > sktlistesi[1]):
                    c.execute(sorgu2, (i[0], ))
                    conn.commit()
                elif (tarihlistesi[2] == sktlistesi[2] and tarihlistesi[1] == sktlistesi[1] and tarihlistesi[0] >
                      sktlistesi[0]):
                    c.execute(sorgu2, (i[0], ))
                    conn.commit()

    def VeritabaniBaglantisiniKes(self):
        conn.close()
class anasayfa:

    def __init__(self, giris):
        self.giris = giris
        self.sol = Frame(giris, width=1100, height=600, bg='#73CFF8')
        self.bgImage = PhotoImage(file = r'supermarket.png')
        self.bg = Label(self.sol,image = self.bgImage)
        self.bg.place(relwidth =1,relheight = 1)
        self.sol.pack(side=LEFT)
        self.baslik = Label(self.sol, text="Yazılım Market", font=('calibri 55 bold'), fg='white', bg='#FF8800')
        self.baslik.place(x=325, y=25)
        self.baslik = Label(self.sol, text="HOŞGELDİNİZ", font=('calibri 43 bold'), fg='white', bg='#FF8800')
        self.baslik.place(x=400, y=130)

        def butontikla2():
            but2 = Tk()
            alisveris = SuperMarket(but2)
            but2.geometry("1450x750")
            but2.resizable(False, False)
            but2.mainloop()

        self.butim = PhotoImage(file = r'button.png')
        self.c = Button(giris, text="Alışveriş Yap", command=butontikla2, image = self.butim, width=470, height=117, fg="white",
                        font="calibri 13 bold")

        self.c.place(relx=0.5, rely=0.7, anchor=CENTER)


mw = Tk()
m = anasayfa(mw)
mw.geometry("1100x600")
mw.configure(background="#73CFF8")
mw.resizable(0, 0)
mw.mainloop()
