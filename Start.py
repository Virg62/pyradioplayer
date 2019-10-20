#! /usr/bin/python3
# -*- coding: utf-8 -*-
#
try:
    import vlc
except:
    print("Le module VLC requis n'est pas présent sur le système! Veuillez l'installer")
    print("Avec la commande suivante: pip install python-vlc")
    exit(0)


import sys, urllib, urllib.request, json, io
from PIL import Image
from PIL.ImageQt import ImageQt
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Application(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.initUI()

    def initUI(self):
        self.setStyle(QStyleFactory.create('fusion'))
        p = self.palette()
        p.setColor(QPalette.Window, QColor(53,53,53))
        p.setColor(QPalette.Button, QColor(53,53,53))
        p.setColor(QPalette.Highlight, QColor(142,45,197))
        p.setColor(QPalette.ButtonText, QColor(255,255,255))
        p.setColor(QPalette.WindowText, QColor(255,255,255))
        self.setPalette(p)

class Window(QMainWindow):
    def __init__(self):
        self.yourapilink = "390-server/radio/" # Ici votre lien d'API
        super().__init__()
        self.initUI()
        self.ajoutListe()
    

    def getRadios(self):
        rep = urllib.request.urlopen("http://"+self.yourapilink+"searchST.php?nom=*").read()
        reponse = json.loads(rep)
        return reponse

    def ajoutListe(self):
        self.listwidget = QListWidget(self)

        """


        self.listwidget.insertItem(0,"Grand Lille Info")
        self.listwidget.insertItem(1,"Nostalgie")
        self.listwidget.insertItem(2,"lorem")
        self.listwidget.insertItem(3,"ipsum")

        """
        self.radioList=self.getRadios()
        for x, i in enumerate(self.radioList):
            #print(print(x, i)
            if i != "neant":
                self.listwidget.insertItem(x,i)

        self.listwidget.clicked.connect(self.clicked)
        self.listwidget.setFixedHeight(self.height())
        self.listwidget.setFixedWidth(200)
        tailleutile=self.width()-self.listwidget.width()
        self.radiotitlelabel.move(tailleutile/2-self.radiotitlelabel.width()/2+self.listwidget.width(),0)
        #self.radiotitlelabel.setFixedWidth(tailleutile)
        self.listwidget.show()
        self.replaceitems()
    

    def placeimptelemts(self):
        # 18 % en hauteur pour le logo de la station
        
        pass

    def clicked(self,qmodelindex):
        item = self.listwidget.currentItem()
        
        # if self.currentlyPlaying != "non":
        #     self.player.stop()
            

        if self.currentlyPlaying != item.text():
            self.player.stop()
            self.checkThreadTimer.stop()
            self.checkThreadTimer.start()
            self.currentlyPlaying=item.text()
            self.replaceText("radio",item.text())
            self.replaceText("logo",self.radioList[item.text()][2])
            self.player=vlc.MediaPlayer(self.radioList[item.text()][0])
            self.player.play()
            self.identplay=self.radioList[item.text()][4]
            self.updateTit()
            #print(item.text(), self.radioList[item.text()][2])


    def initUI(self):
        self.setGeometry(10, 10, 1024, 576)
        self.setFixedSize(1280,720)
        self.htmlh={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}
        #self.taille = int(0.41666667*self.height())
        self.setWindowTitle('PyQT-RadioPlayer')
        self.logo=Image.open("logo-header.png")
        
        self.imgpoc=urllib.request.urlopen("http://cdn.absoluteradio.co.uk/artists/1-1/320x320/0.jpg").read()
        #self.statusBar().showMessage("Aucun événement")
        self.setMenuBar()
        self.currentlyPlaying="non"
        self.identplay="non"
        self.actualtitle="something"
        self.player=vlc.MediaPlayer()
        self.setCenter()

        self.infolabel=QLabel("PAS DE TEXTE",self)
        self.infolabel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        # Récupération font ...
        font1 = QFont(self.infolabel.font())
        font1.setPointSize(20)
        font2=QFont(font1)
        font2.setBold(True)
        self.infolabel.setFont(font1)
        self.infolabel.setText("[PAS DE TEXTE]")
        self.infolabel.adjustSize()


        self.radiotitlelabel=QLabel("PyQT-RadioPlayer",self)
        self.radiotitlelabel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        self.radiotitlelabel.setText("PyQT-RadioPlayer")
        self.radiotitlelabel.adjustSize()

        self.radiologolabel=QLabel(self)
        self.radiologolabel.setPixmap(QPixmap("logo-header.png"))
        self.radiologolabel.setScaledContents(True)
        self.radiologolabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)


        self.musicpoc = QLabel(self)
        self.musicpoc.setFixedSize(QSize(300,300))
        self.musicpoc.setPixmap(QPixmap("essai.jpg"))
        self.musicpoc.setScaledContents(True)
        self.musicpoc.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

        self.musictitle=QLabel("[PAS DE TITRE]",self)
        self.musictitle.setFont(font2)
        self.musictitle.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        self.musictitle.setText("[PAS DE TITRE]")
        self.musictitle.adjustSize()

        self.musicartist=QLabel("[PAS D'ARTISTE]",self)
        self.musicartist.setFont(font1)
        self.musicartist.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        self.musicartist.setText("[PAS D'ARTISTE]")
        self.musicartist.adjustSize()


        self.musicartist.hide()
        self.musictitle.hide()
        self.musicpoc.hide()
        
        
        self.checkThreadTimer =QTimer(self)
        self.checkThreadTimer.setInterval(7000) #.5 seconds
        self.checkThreadTimer.timeout.connect(self.updateTit)

        


        self.addBTN()
        self.show()

    def addBTN(self):
        self.nFS=QPushButton("&FullScreen",self)
        self.nFS.clicked.connect(self.togglefullscreen)
        self.nFS.move(self.width()-self.nFS.width(),self.height()-self.nFS.height())

    def setMenuBar(self):
        # Remplir le code ici
        pass


    def replaceText(self, elemt, value):
        if elemt == "radio":
            self.radiotitlelabel.setText(value)
            self.radiotitlelabel.adjustSize()
        elif elemt == "logo":
            if "http" not in value:
                value="http://"+self.yourapilink+value
            elif "https" in value:
                value=value.replace("https","http")
            try:
                req = urllib.request.Request(value,data=None,headers=self.htmlh)
                dllogo=urllib.request.urlopen(req).read()
                monimage=io.BytesIO(dllogo)
                self.logo=Image.open(monimage)
            except:
                self.logo=Image.open("logo-header.png")
        elif elemt == "titre":
            self.musictitle.show()
            self.musictitle.setText(value)
            self.musictitle.adjustSize()
        elif elemt == "artist":
            self.musicartist.show()
            self.musicartist.setText(value)
            self.musicartist.adjustSize()
        elif elemt == "poc":
            
            self.taille = int(0.41666667*self.height())
            
            #self.imgpoc=value
            self.musicpoc.show()
        elif elemt == "info":
            self.infolabel.show()
            self.infolabel.setText(value)
            self.infolabel.adjustSize()
        self.replaceitems()

    def setCenter(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    def togglefullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()
        self.replaceitems()

    def topoc(self, url):
        if "http" not in url:
            url="http://"+self.yourapilink+url
        elif "https" in url:
            url=url.replace("https","http")

        try:
            dt=urllib.request.Request(url,data=None,headers=self.htmlh)
            self.imgpoc=urllib.request.urlopen(dt).read()
            
        except:
            self.imgpoc=urllib.request.urlopen("https://cdn.absoluteradio.co.uk/artists/1-1/320x320/0.jpg").read()
    def replaceitems(self):
        self.taille=int(0.4166667*self.height())
        self.musicpoc.setFixedSize(QSize(self.taille, self.taille))
        #print(self.taille)
        self.listwidget.setFixedHeight(self.height())
        tailleutile=self.width()-self.listwidget.width()
        self.radiotitlelabel.move(tailleutile/2-self.radiotitlelabel.width()/2+self.listwidget.width(),0)
        tailleyLogo=0.18*self.height()
        taillexLogo=tailleutile
        self.radiologolabel.setFixedHeight(tailleyLogo)
        self.radiologolabel.setFixedWidth(taillexLogo)
        self.radiologolabel.setPixmap(self.resizeImage(taillexLogo,tailleyLogo, self.logo))
        self.radiologolabel.move(tailleutile/2-self.radiologolabel.width()/2+self.listwidget.width(),self.radiotitlelabel.height())
        #print(tailleutile, tailleutile/2-self.radiotitlelabel.width()/2+self.listwidget.width())
        #self.radiotitlelabel.setFixedWidth(tailleutile/2)
        self.nFS.move(self.width()-self.nFS.width(),self.height()-self.nFS.height())
        
        hauteurinterressante = self.radiotitlelabel.height()+self.radiologolabel.height()
        hauteurutile = self.height()-(self.radiotitlelabel.height()+self.radiologolabel.height())
        #print(hauteurinterressante, hauteurutile)
        self.infolabel.move(tailleutile/2-self.infolabel.width()/2+self.listwidget.width(),hauteurutile/2-self.infolabel.height()/2+hauteurinterressante)
        self.musicpoc.move(self.listwidget.width()+100,hauteurutile/2-self.musicpoc.height()/2+hauteurinterressante)
        #print(hauteurutile/2-self.musicpoc.height()/2+hauteurinterressante, self.musicpoc.height(), hauteurutile, hauteurinterressante)
        
        y1 = int(((hauteurutile/2-self.musicpoc.height()/2+hauteurinterressante) + (hauteurutile/2-self.infolabel.height()/2+hauteurinterressante))/2)
        y2 = int(((hauteurutile/2-self.musicpoc.height()/2+hauteurinterressante+int(0.4166667*self.height())) + (hauteurutile/2-self.infolabel.height()/2+hauteurinterressante))/2)
        
        
        xif=self.listwidget.width()+100+self.taille+50
        self.musictitle.move(xif, y1 - self.musictitle.height()/2 )
        self.musicartist.move(xif, y2 - self.musicartist.height()/4)
        
        
        try:
            monimage=io.BytesIO(self.imgpoc)
            img=Image.open(monimage)
        except:
            img=Image.open("logo-header.png")
        self.musicpoc.setPixmap(self.resizeImage(self.taille,self.taille,img))
        
            


    def updateTit(self):
        
        
        try:
            rep = urllib.request.urlopen("http://"+self.yourapilink+"req.php?rad="+self.identplay+"&r=21").read().decode("utf8")
            reponse = json.loads(rep)
            print(reponse)
            if reponse['tit'] != self.actualtitle:
                if reponse["titAvail"] == "True":
                    self.infolabel.hide()

                    self.actualtitle=reponse['tit']
                    self.replaceText("titre",reponse['titre'])
                    self.replaceText("artist",reponse['artist'])




                    self.topoc(reponse["pochetteURL"])
                    
                    self.wintitle=self.currentlyPlaying+ " - "+reponse['artist']+" - "+reponse['titre']
                    self.musicpoc.show()
                    
                    

                else:
                    self.musicartist.hide()
                    self.musicpoc.hide()
                    self.musictitle.hide()
                    if reponse['tit'] != "":
                        self.replaceText("info", reponse['tit'])
                        self.wintitle=self.currentlyPlaying+" - " + reponse['tit']
                    else:
                        self.replaceText("info", self.radioList[self.currentlyPlaying][1])

            self.replaceitems()
        
        
        
        
        except:
            self.replaceText("info",self.radioList[self.currentlyPlaying][1])
            self.wintitle = self.currentlyPlaying + " - " + self.radioList[self.currentlyPlaying][1]
            self.musicartist.hide()
            self.musictitle.hide()
            self.musicpoc.hide()
        
        self.setWindowTitle('PyQT-RadioPlayer - ' + self.wintitle )




    def resizeImage(self,finalx, finaly, img):
        finalx=int(finalx)
        finaly=int(finaly)
        mni = Image.new("RGBA",(finalx,finaly))
        
        ximg=img.size[0]
        yimg=img.size[1]

        nheight = finaly
        nwidth  = int(nheight * ximg / yimg)
        img = img.resize((nwidth, nheight), Image.ANTIALIAS)
        #print(nheight, nwidth)
        mni.paste(img,(int(finalx/2-nwidth/2),0))

        res=ImageQt(mni)
        return QPixmap.fromImage(res)

    # def about(self):
    #     # Remplir le code ici
    #     pass

    # def quit(self):
    #     # Remplir le code ici
    #     pass

app = Application([])
win = Window()
app.exec_()
