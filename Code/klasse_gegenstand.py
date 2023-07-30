from random import choice, seed, randint, choices
seed()

class Gegenstand(object):
    def __init__(self,pTyp,pRaster):
        ''' 
        Eingabe: pRaster: Raster, pTyp: str
        Funktion: Initialisierungsmethode für den Gegenstand
        Ausgabe: keine
        '''
        self.__raster = pRaster
        self.__typ = pTyp
        self.__seltenheiten = [("Gewöhnlich","White"),("Ungewöhnlich","Green"),("Selten","Blue"),("Episch","Purple"),("Legendär","Orange")]
        self.__seltenheit = choices(self.__seltenheiten, weights=[10,5,3,2,1],k=1)[0]
        materialien = ["Holz","Stein","Eisen","Gold","Emerald","Papier","Glas","Silber"]
        traenke = ["Heil","Lebens","Energie"]
        angriffEndungen = ["schwert","dolch","stab","speer","kugel"]
        verteidigungEndungen = ["schild","blech","wand","aura"]
        trankEndungen = ["trank","trunk","flaeschchen","flasche"]
        self.__parade = 0
        self.__attacke = 0
        self.__heilen = 0
        self.__name = ""
        if self.__typ == "Heilen":
            self.__heilen = randint(0,5)+self.__raster.runde*2
            self.__name = str(choice(traenke)+choice(trankEndungen)) + " "
            self.__seltenheit = ("H","White")
        elif self.__typ == "PermaHeilen":
            self.__heilen = randint(1,3)
            self.__name = "Permanenter " + str(choice(traenke)+choice(trankEndungen)) + " "
            self.__seltenheit = ("P","White")
        elif self.__typ == "Angriff":
            self.__attacke = self.__seltenheiten.index(self.__seltenheit)+self.__raster.runde
            self.__name = "[" + self.__seltenheit[0][0] + "] " + str(choice(materialien)+choice(angriffEndungen)) + " "
        elif self.__typ == "Verteidigung":
            self.__parade = self.__seltenheiten.index(self.__seltenheit)+round(self.__raster.runde*0.5)
            self.__name = "[" + self.__seltenheit[0][0] + "] " + str(choice(materialien)+choice(verteidigungEndungen)) + " "
        self.__verrechnet = False
        
    def getTyp(self):
        ''' 
        Eingabe: 
        Funktion: Gibt self.__typ Attribut aus
        Ausgabe: string
        '''
        return self.__typ
        
    def setVerrechnet(self,pEingabe):
        ''' 
        Eingabe: pEingabe: boolean
        Funktion: Setzt self.__verrechnet auf pEingabe. Wird nachdem verrechnen der Wert im Inventar aufgerufen.
        Ausgabe: keine
        '''
        self.__verrechnet = pEingabe
    
    def werteAusgeben(self):
        ''' 
        Eingabe: keine
        Funktion: Gibt die 6 Werte des Gegenstand-Objekts zurück
        Ausgabe: list
        '''
        return [self.__attacke,self.__parade,self.__heilen,self.__verrechnet,self.__seltenheit,self.__name]