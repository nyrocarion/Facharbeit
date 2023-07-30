from Code.klasse_inventar import Inventar
from Code.klasse_kampfmanager import Kampfmanager
from Code.klasse_charakter import Charakter
import pygame, sys

class Spieler(Charakter):
    def __init__(self,pRaster,pPos):
        ''' 
        Eingabe: pRaster: Raster, pPos: tuple of int
        Funktion: Initialisierungsmethode für den Spieler
        Ausgabe: keine
        '''
        self.__raster = pRaster
        #bewegung
        self.__linksGedrueckt = False
        self.__rechtsGedrueckt = False
        self.__hochGedrueckt = False
        self.__runterGedrueckt = False
        self.__kisteOeffnen = False
        self.__inventarOeffnen = False
        self.__angreifen = False
        self.__kampfAktiv = False
        self.__bewegt = False
        #werte + items
        self.__pos = pPos
        self.__name = "David"
        self.__inventar = Inventar(self,self.__raster)   
        self.__leben = 50
        self.__angriff = 5
        self.__ruestung = 5
        super().__init__(pRaster=self.__raster,pLeben=self.__leben,pRuestung=self.__ruestung,pAngriff=self.__angriff,pBewegt=False,pName=self.__name,pPos=self.__pos)
        
    def __aufheben(self,pGegenstand):
        ''' 
        Eingabe: pGegenstand: Gegenstand-Objekt
        Funktion: Fügt der inventarListe der self.inventar-Objekt einen angegebenen Gegenstand hinzu
        Ausgabe: keine
        '''
        self.__inventar.__hinzufuegen__(pGegenstand)
                           
    def bewegung(self):
        ''' 
        Eingabe: keine
        Funktion: Bewegt das Spieler-Objekt indem es die Werte der Felder-Objekte in der Rasterliste ändert. 
        Die mögliche Richtung der Bewegung ist abhängig von der Spielerposition, den Rastermaßen und anderen Objekten die im Weg stehen können.
        Prüfen ob die Bedingungen für Kiste öffnen / Kampf beginnen erfüllt sind wenn die zugehörige Taste gedrückt wird.
        Ausgabe: keine
        '''
        test = [self.__rechtsGedrueckt,self.__linksGedrueckt,self.__hochGedrueckt,self.__runterGedrueckt]
        if sum(bool(x) for x in test) == 1 and not self.__kampfAktiv:
            #rechts
            if self.__rechtsGedrueckt and self.nachbarFelder()[0] == 0:
                    self.rechts()
            #links
            if self.__linksGedrueckt and self.nachbarFelder()[2] == 0:
                    self.links()
            #hoch
            if self.__hochGedrueckt and self.nachbarFelder()[3] == 0:
                    self.hoch()
            #runter
            if self.__runterGedrueckt and self.nachbarFelder()[1] == 0:
                    self.runter()
        # Kiste
        if self.__kisteOeffnen:
            for feld in self.nachbarFelder():
                if feld in self.__raster.kiste:
                    if not self.__inventar.inventarVoll():
                        self.__inventar.hinzufuegen(feld.kisteWirdGeoeffnet())
                        self.__raster.menu.kistenPopup(self.__inventar.neustenGegenstandAusgeben().werteAusgeben())
                        break
                    else:
                        self.__raster.menu.kistenNichtPopup()
                        if not self.__raster.menu.menuOffen:
                            self.__raster.menu.inventarPopup()
        # Kampf
        gegnerobj = self.__raster.gegnerInDerNaehe()
        if self.__angreifen and gegnerobj in self.__raster.gegner and not self.__kampfAktiv:
            self.__kampfAktiv = True
            self.kampfmanager = Kampfmanager(self,gegnerobj,self.__raster)
            self.__raster.menu.kampfPopup(self.kampfmanager) 
        # Inventar
        if self.__inventarOeffnen:
            self.__raster.menu.inventarPopup(self.__inventar.menuAusgabe(),self.__inventar)
            
    def update(self):
        ''' 
        Eingabe: keine
        Funktion: Setzt sämtliche Spieler-Objekt-Variablen die durch Tasteneingaben gesteuert werden auf False, wird genutzt um nach der Verarbeitung der Eingaben wieder auf den Ursprungszustsand zurückzukommen.
        Ausgabe: tuple
        '''
        self.__linksGedrueckt = False
        self.__rechtsGedrueckt = False
        self.__hochGedrueckt = False
        self.__runterGedrueckt = False
        self.__kisteOeffnen = False
        self.__angreifen = False
        self.__inventarOeffnen = False  
        self.__inventar.updateSpielerwerte()
                
    def setTasteneingabenAttributeSpieler(self,pAttr,pWert):
        ''' 
        Eingabe: pAttr: str, pWert: int
        Funktion: Setzt ein durch pAttr ausgewähltes Attribute auf pWert. Benutzt um eingelesene Tasteneingaben zwischenzuspeichern
        Ausgabe: keine
        '''
        if pAttr == "hoch":
            self.__hochGedrueckt = pWert
        elif pAttr == "runter":
            self.__runterGedrueckt = pWert
        elif pAttr == "rechts":
            self.__rechtsGedrueckt = pWert
        elif pAttr == "links":
            self.__linksGedrueckt = pWert
        elif pAttr == "kiste":
            self.__kisteOeffnen = pWert
        elif pAttr == "inventar":
            self.__inventarOeffnen = pWert
        elif pAttr == "angreifen":
            self.__angreifen = pWert
        elif pAttr == "kampf":
            self.__kampfAktiv = pWert
        elif pAttr == "bewegt":
            self.__bewegt = pWert

    def besiegt(self):
        ''' 
        Eingabe: keine
        Funktion: Setzt in der rasterListe das Feld auf dem der Gegner aktuell steht auf den Wert Null und löscht sich selbst.
        Ausgabe: keine
        '''
        self.__raster.feldAendern(self.getPos()[0],self.getPos()[1],0)
        self.__raster.menu.gameover(self)
        
    def gameover(self):
        ''' 
        Eingabe: keine
        Funktion: Beendet die Hauptschleife und schließt das pygameFenster
        Ausgabe: keine
        '''
        self.__raster.main.run = False
        pygame.quit()
        sys.exit()
        
    def getKampfAktiv(self):
        ''' 
        Eingabe: keine
        Funktion: Gibt das kampfAktiv Attribut des Spielers zurück. Wird benutzt um zu prüfen ob ein neuer Kampf schon möglich ist oder ob der Spieler sich bewegen darf
        Ausgabe: boolean
        '''
        return self.__kampfAktiv
    
            

            