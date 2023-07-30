class Charakter(object):
    def __init__(self,pRaster,pPos,pLeben,pAngriff,pRuestung,pName,pBewegt):
        ''' 
        Eingabe: pRaster: Raster, pPos: tuple, pLeben: int, pAngriff: int, pRuestung: int,pName: str, pBewegt: bool
        Funktion: Initialisierungsmethode für den Charakter
        Ausgabe: keine
        '''
        self.__pos = pPos
        self.__raster = pRaster
        self.__bewegt = pBewegt
        self.__name = pName
        self.__leben = pLeben
        self.__maxLeben = self.__leben
        self.__angriff = pAngriff
        self.__ruestung = pRuestung
        
    def menuAusgabe(self):
        ''' 
        Eingabe: keine
        Funktion: Gibt Werte von 5 Attributen des Charakters aus: self.__name,self.__angriff,self.__ruestung,self.__leben und self.__maxLeben
        Ausgabe: list
        '''
        return [self.__name,self.__angriff,self.__ruestung,self.__leben,self.__maxLeben]
        
    def getBewegt(self):
        ''' 
        Eingabe: keine
        Funktion: Gibt Wert von self.__bewegt Attribut zurück. Wir vom Gegner genutzt, um zu prüfen, ob der Spieler sich bewegt hat.
        Ausgabe: boolean
        '''
        return self.__bewegt
    
    def setBewegt(self,pWert):
        ''' 
        Eingabe: pWert: boolean
        Funktion: Ordnet self.__bewegt pWert zu
        Ausgabe: keine
        '''
        self.__bewegt = pWert
        
    def wertAnpassen(self,pWahl,pWert):
        ''' 
        Eingabe: pWahl: int, pWert: int
        Funktion: Ändert einen durch pWahl angegebenes Attribut um pWert
        Ausgabe: keine
        '''
        # Angriff Ruestung Leben
        if pWahl == 0:
            self.__angriff+=pWert
        elif pWahl == 1:
            self.__ruestung+=pWert
        elif pWahl == 2:
            self.__leben+=pWert
        elif pWahl == 3:
            self.__maxLeben+=pWert
        
    def lebenBar(self):
        ''' 
        Eingabe: keine
        Funktion: Erzeugt eine Anzahl von | zwischen 2 eckigen Klammern. Wird zur Visualisierung der Leben im Kampf verwendet
        Ausgabe: string
        '''
        schonGemacht =False
        counter = self.__maxLeben//3
        ausgabe = "["
        if self.__leben == self.__maxLeben:
            for x in range(1,counter+1,1):
                ausgabe+="|"
        else:
            for x in range(1,counter+1,1):
                if 3*x < self.__leben:
                    ausgabe+="|"
                else:
                    if self.__leben <= 3 and not schonGemacht:
                        ausgabe += "|"
                        schonGemacht = True
                    else:
                        ausgabe+=" "
        ausgabe += "]"
        return ausgabe
    
    def umgebungPruefen(self,pTest):
        ''' 
        Eingabe: pTest: tuple
        Funktion: Prüft ob in einer bestimmten Richtung angegeben durch Koordinatenmodifikationen in pTest ein Feld mit einem Wert = 0 vorhanden ist.
        Ausgabe: boolean
        '''
        x = self.__pos[0]+pTest[0]
        y = self.__pos[1]+pTest[1]
        if self.__raster.feldWertAusgeben(x,y)==0:
            return True
        else:
            return False
        
    def setPos(self,pPos):
        ''' 
        Eingabe: pPos: tuple
        Funktion: Setzt self.pos auf durch Parameter angegeben Position
        Ausgabe: keine
        '''
        self.__pos = pPos
        
    def getPos(self):
        ''' 
        Eingabe: keine
        Funktion: Gibt aktuelle gespeicherte Position in self.pos aus
        Ausgabe: tuple
        '''
        return self.__pos
    
    def richtungPruefen(self,pRichtung):
        ''' 
        Eingabe: pRichtung: tuple
        Funktion: prüft ob das feld nebendran auf das man gehen will überhaupte existiert
        Ausgabe: boolean
        '''
        x = self.getPos()[0]
        y = self.getPos()[1]
        if (x+pRichtung[0] < self.__raster.getBreite() and x+pRichtung[0] >= 0) and (y+pRichtung[1] < self.__raster.getHoehe() and y+pRichtung[1] >= 0):
            return True
             
    def nachbarFelder(self):
        ''' 
        Eingabe: keine
        Funktion: Gibt eine Liste mit den Werten der 4 Felder-Objekte um den Spieler herum aus. Reihenfolge: rechts, unten, links, oben
        Ausgabe: list 
        '''
        felder = []
        x = self.getPos()[0]
        y = self.getPos()[1]
        koord = [(1,0),(0,1),(-1,0),(0,-1)]
        for koordinatenAenderung in koord:
            if self.richtungPruefen(koordinatenAenderung):
                #felder.append(self.raster.rasterListe[y+koordinatenAenderung[1]][x+koordinatenAenderung[0]].getWert())
                felder.append(self.__raster.feldWertAusgeben(x+koordinatenAenderung[0],y+koordinatenAenderung[1]))
            else:
                felder.append("Außerhalb")
        return felder
        
    def rechts(self):
        ''' 
        Eingabe: keine
        Funktion: Verschiebt den Charakter nach rechts auf dem Raster und setzt altes Feld zum Normalzustand zurück
        Ausgabe: keine
        '''
        self.__raster.feldAendern(self.__pos[0]+1,self.__pos[1],self)
        self.__raster.feldAendern(self.__pos[0],self.__pos[1],0)
        self.setPos((self.__pos[0]+1,self.__pos[1],self))
        self.__bewegt = True
        
    def links(self):
        ''' 
        Eingabe: keine
        Funktion: Verschiebt den Charakter nach links auf dem Raster und setzt altes Feld zum Normalzustand zurück
        Ausgabe: keine
        '''
        self.__raster.feldAendern(self.__pos[0]-1,self.__pos[1],self)
        self.__raster.feldAendern(self.__pos[0],self.__pos[1],0)
        self.setPos((self.__pos[0]-1,self.__pos[1],self))
        self.__bewegt = True
        
    def hoch(self):
        ''' 
        Eingabe: keine
        Funktion: Verschiebt den Charakter nach oben auf dem Raster und setzt altes Feld zum Normalzustand zurück
        Ausgabe: keine
        '''
        self.__raster.feldAendern(self.__pos[0],self.__pos[1]-1,self)
        self.__raster.feldAendern(self.__pos[0],self.__pos[1],0)
        self.setPos((self.__pos[0],self.__pos[1]-1))
        self.__bewegt = True
        
    def runter(self):
        ''' 
        Eingabe: keine
        Funktion: Verschiebt den Charakter nach unten auf dem Raster und setzt altes Feld zum Normalzustand zurück
        Ausgabe: keine
        '''
        self.__raster.feldAendern(self.__pos[0],self.__pos[1]+1,self)
        self.__raster.feldAendern(self.__pos[0],self.__pos[1],0)
        self.setPos((self.__pos[0],self.__pos[1]+1))
        self.__bewegt = True