import pygame
from Code.klasse_feld import Feld
from Code.klasse_spieler import Spieler
from Code.klasse_gegner import Gegner
from Code.klasse_kiste import Kiste
from Code.klasse_menue import Menu
from random import randint, choice, seed
from pygamepopup.menu_manager import MenuManager
seed()

class Raster(object):
    def __init__(self,pBreite,pHoehe,pFenster,pMain):
        ''' 
        Eingabe: pBreite: int, poehe: int, pFenster: pygame.Surface, pMain: Main
        Funktion: Initialisierungsmethode für das Raster
        Ausgabe: keine
        '''
        self.runde = 1
        self.__kisteBild = pygame.image.load("Bilder/kiste.png")
        self.__spielerBild = pygame.image.load("Bilder/character.png")
        pygame.transform.scale(self.__spielerBild,(100,100))
        self.__gegnerBild = pygame.image.load("Bilder/gegner.png")
        self.__hintergrundBild = pygame.image.load("Bilder/Background.png")
        
        self.spielefenster = pFenster
        self.main = pMain
        self.menuManager = MenuManager(pFenster)
        self.menu = Menu(self.menuManager)
        self.spieler = Spieler(self,(0,0))
        self.gegner = [Gegner(self),Gegner(self)]
        self.kiste = [Kiste(self),Kiste(self),Kiste(self)]
        # Maße
        self.__breite = pBreite
        self.__hoehe = pHoehe
        # RasterListe erstellen
        self.__rasterListe = []
        self.__schonBenutzt = [(0,0)]
        #hoehe listen mit jeweils breite felder
        for y in range(self.__hoehe):
            self.__rasterListe.append([])
            for x in range(self.__breite):
                self.__rasterListe[y].append(Feld(x,y)) 
        self.__rasterListe[0][0].setWert(self.spieler)
        for gegner in self.gegner:
            self.__objPlazieren(gegner)
        for kiste in self.kiste:
            self.__objPlazieren(kiste)
        self.getoeteteGegner = 0
        self.insgTote = 0

    def setTasteneingabenAttribute(self,pAttr,pWert):
        ''' 
        Eingabe: pAttr: str, pWert: int
        Funktion: Führt Spieler-Methode aus, diese setzt ein durch pAttr ausgewähltes Attribute auf pWert. Benutzt um eingelesene Tasteneingaben zwischenzuspeichern
        Ausgabe: keine
        '''
        self.spieler.setTasteneingabenAttributeSpieler(pAttr,pWert)
                
    def __objPlazieren(self,pObj):
        ''' 
        Eingabe: pObj: Spieler-,Kisten- oder Gegner-Objekt
        Funktion: Ordnet einem zufällig bestimmten Feld das Objekt zu. Abhängig von schon vorhandenen Objekten und Rasterdimension.
        Ausgabe: keine
        '''
        breite = self.__breite-1
        hoehe = self.__hoehe-1
        for gegner in self.gegner:
            if not gegner.getPos() in self.__schonBenutzt:
                self.__schonBenutzt.append(gegner.getPos())
        for kiste in self.kiste:
            if not kiste.getPos() in self.__schonBenutzt:
                self.__schonBenutzt.append(kiste.getPos())
        for element in [(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]:
            pos = (self.spieler.getPos()[0]+element[0],self.spieler.getPos()[1]+element[1])
            if not pos in self.__schonBenutzt and not (pos[0]<0 or pos[1]<0):
                self.__schonBenutzt.append(pos)
        randKoord = (randint(0,breite),randint(0,hoehe))
        if not randKoord in self.__schonBenutzt:
            self.feldAendern(randKoord[0],randKoord[1],pObj)
            pObj.setPos((randKoord[0],randKoord[1]))
            self.__schonBenutzt.append(randKoord) 
        else:
            self.__objPlazieren(pObj)    
        
    def rasterMalen(self):
        ''' 
        Eingabe: keine
        Funktion: Durchläuft self.rasterListe und zeichnet in Abhängigkeit von den Werten der Felder-Objekte ein Bild auf das spielefenster
        Ausgabe: keine
        '''
        for y in range(self.__hoehe):
            for x in range(self.__breite):
                if self.__rasterListe[y][x].getWert() == self.spieler:
                    spielerBild = self.__spielerBild.get_rect(topleft=(20*x+100*x,20*y+100*y),size=(100, 100))
                    self.spielefenster.blit(self.__spielerBild,spielerBild)
                if self.__rasterListe[y][x].getWert() in self.gegner:
                    gegnerBild = self.__gegnerBild.get_rect(topleft=(20*x+100*x,20*y+100*y),size=(100, 100))
                    self.spielefenster.blit(self.__gegnerBild,gegnerBild)
                if self.__rasterListe[y][x].getWert() in self.kiste:
                    kistenBild = self.__kisteBild.get_rect(topleft=(20*x+100*x,20*y+100*y),size=(100, 100))
                    self.spielefenster.blit(self.__kisteBild,kistenBild)
                if self.__rasterListe[y][x].getWert() == 0:
                    hintergrundBild = self.__hintergrundBild.get_rect(topleft=(20*x+100*x,20*y+100*y),size=(100, 100))
                    self.spielefenster.blit(self.__hintergrundBild,hintergrundBild)      
             
                
    def rasterAusgeben(self):
        ''' 
        Eingabe: keine
        Funktion: Printed die Werte der Felder-Objekte in self.rasterListe
        Ausgabe: keine
        '''
        for spalten in range(self.__hoehe):
            print("Spalte:",spalten)
            for zeilen in range(self.__breite):
                print(self.__rasterListe[spalten][zeilen].getWert())
                
    def feldWertAusgeben(self,pX,pY):
        ''' 
        Eingabe: pX: int, pY: int
        Funktion: Stellt ein Tutorial-Popup-Fenster auf dem Bildschirm da
        Ausgabe: int, Kiste-Objekt, Spieler-Objekt oder Gegner-Objekt
        '''
        return self.__rasterListe[pY][pX].getWert()
                        
    def feldAendern(self,x,y,wert):
        ''' 
        Eingabe: x: int, y: int, wert: 0, Spieler-,Kisten- oder Gegner-Objekt
        Funktion: Methode die direkte Änderung an self.rasterListe ersetzt. Ändert den Wert eines durch Koordinaten angegeben Feld-Objektes.
        Ausgabe: tuple
        '''
        if x > self.__breite:
            x = x-self.__breite
        if y > self.__hoehe:
            y = y-self.__hoehe
        self.__rasterListe[y][x].setWert(wert)
        
    def findSpieler(self):
        ''' 
        Eingabe: keine
        Funktion: Gibt Position des Spielers zurück
        Ausgabe: tuple
        '''
        # xy koord des spieler ausgeben in rasterListe aus feldenr
        for y in range(self.__hoehe):
            for x in range(self.__breite):
                if self.__rasterListe[y][x].getWert() == self.spieler:
                    return (x,y)
                
    def getKampfAktiv(self):
        ''' 
        Eingabe: keine
        Funktion: Gibt das kampf_aktiv Attribut des Spielers zurück. Wird benutzt um zu prüfen ob ein neuer Kampf schon möglich ist oder ob der Spieler sich bewegen darf
        Ausgabe: boolean
        '''
        return self.spieler.getKampfAktiv()
    
    def setKampfAktiv(self,pWert):
        ''' 
        Eingabe: pWert: boolean
        Funktion: Ordnet dem kampf_aktiv Attribut des Spielers eienn Wert zu
        Ausgabe: keine
        '''
        self.spieler.kampf_aktiv = pWert
        
    def getMenuOffen(self):
        ''' 
        Eingabe: keine
        Funktion: Gibt das menuOffen Attribut des Menus zurück. Benutzt um zu prüfen, ob ein weiteres Menü geöffnet werden kann
        Ausgabe: keine
        '''
        return self.menu.menuOffen
            
    def __neueRunde(self):
        ''' 
        Eingabe: keine
        Funktion: Stellt runde*2 neue Gegner und 1 Kiste auf dem Raster auf. Wird ausgerufen wenn alle Gegner einer Runde besiegt wurden.
        Ausgabe: keine
        '''
        self.__schonBenutzt = []
        self.__schonBenutzt.append(self.findSpieler())
        for x in range(self.runde*2):
            gegner = Gegner(self)
            self.__objPlazieren(gegner)
            self.gegner.append(gegner)
        kiste = Kiste(self)
        self.__objPlazieren(kiste)
        self.kiste.append(kiste)


    def pruefen(self):
        ''' 
        Eingabe: keine
        Funktion: Prüft ob alle Gegner eine Runde getötet werden und keine Menüs offen sind. Löst dann eine neue Runde aus
        Ausgabe: keine
        '''
        if self.getoeteteGegner == self.runde*2 and not self.menu.menuOffen:
            if (len(self.kiste)+1 + (self.runde+1)*2 + 9) < (self.__breite * self.__hoehe):
                self.getoeteteGegner = 0
                self.runde += 1
                self.menu.neueRunde()
                self.__neueRunde()
            else:
                #print("spielfeld zu voll")
                self.menu.zuViel(self.spieler)
                
    def getHoehe(self):
        ''' 
        Eingabe: keine
        Funktion: Gibt die Hoehe des Raster zurück
        Ausgabe: int
        '''
        return self.__hoehe
    
    def getBreite(self):
        ''' 
        Eingabe: keine
        Funktion: Gibt die Breite des Raster zurück
        Ausgabe: int
        '''
        return self.__breite
    
    def gegnerInDerNaehe(self):
        ''' 
        Eingabe: keine
        Funktion: Prüft ob sich der spieler in der Nähe also 0 Felder entfernt von einem Gegner befindet
        Ausgabe: boolean
        '''
        for feld in self.spieler.nachbarFelder():
            if feld in self.gegner:
                return feld