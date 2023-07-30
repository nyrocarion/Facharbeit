from Code.klasse_gegenstand import Gegenstand
from random import choices, seed
seed()

class Kiste(object):
    def __init__(self,pRaster):
        ''' 
        Eingabe: pRaster: Raster
        Funktion: Initialisierungsmethode für die Kiste
        Ausgabe: keine
        '''
        seltenheit = choices(["Angriff","Verteidigung","Heilen","PermaHeilen"],weights=[6,4,3,2],k=1)
        self.__gegenstand = Gegenstand(seltenheit[0],pRaster)
        self.__raster = pRaster
        self.__pos = None
        self.__geoeffnet = False
        
    def setPos(self,pPos):
        ''' 
        Eingabe: pPos: tuple
        Funktion: Setzt self.pos auf den angegeben Wert. Wird im Raster-Objekt benutzt nachdem die Position zufällig ausgewählt wurde.
        Ausgabe: keine
        '''
        self.__pos = pPos
        
    def getPos(self):        
        ''' 
        Eingabe: keine
        Funktion: Gibt positions Attribut der Kiste zurück
        Ausgabe: tuple of int
        '''
        return self.__pos
        
    def kisteWirdGeoeffnet(self):
        ''' 
        Eingabe: keine
        Funktion: Lässt die Kiste verschwinden indem der Wert des Feldes auf dem die Kiste steht auf 0 gesetzt wird. Gibt Gegenstand-Objekt der Kiste zurück
        Ausgabe: Gegenstand-Objekt
        '''
        self.__raster.feldAendern(self.getPos()[0],self.getPos()[1],0)
        self.__raster.kiste.remove(self)
        self.__geoeffnet = True
        return self.__gegenstand