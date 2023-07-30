from Code.klasse_charakter import Charakter
from random import randint, choice
from Code.klasse_kampfmanager import Kampfmanager

class Gegner(Charakter):
    def __init__(self,pRaster):
        ''' 
        Eingabe: pRaster: Raster
        Funktion: Initialisierungsmethode für den Gegner
        Ausgabe: keine
        '''
        self.__pos = (1,1)
        self.__raster = pRaster
        self.__name = "Schnork"
        self.__leben = 20+self.__raster.runde*4
        self.__ruestung = 5+round(self.__raster.runde*0.1)
        self.__angriff = 5+round(self.__raster.runde*0.2)
        self.__vorherGegangenListe = [True,False,False,False]
        super().__init__(pRaster=self.__raster,pLeben=self.__leben,pRuestung=self.__ruestung,pAngriff=self.__angriff,pBewegt=False,pName=self.__name,pPos=self.__pos)
       
    def __alternativeBewegungFinden(self):
        ''' 
        Eingabe: pStart: int
        Funktion: Sucht nach eine alternativen Bewegungsrichtung in Abhängigkeit von der aktuell gewollten Richtung in pStart. Richtungen sind ab 0 mit rechts im Uhrzeigersinn durchnummeriert.
        Ausgabe: string
        '''
        #print("alternative suchen")
        pxpos = self.__raster.findSpieler()[0]
        pypos = self.__raster.findSpieler()[1]
        xpos = self.getPos()[0]
        ypos = self.getPos()[1]
        start=0
        # An Hinternis vorbei laufen
        
        if self.__vorherGegangenListe[3]:
            if self.nachbarFelder()[3]!=0:
                if pxpos < xpos:
                    start = 2
                else: 
                    start = 0
            else:
                start = 3
        elif self.__vorherGegangenListe[0]:
            if self.nachbarFelder()[0]!=0:
                if pypos < ypos:
                    start = 3
                else: 
                    start =1
            else:
                start = 0
        elif self.__vorherGegangenListe[1]:
            if self.nachbarFelder()[1]!=0:
                if pxpos < xpos:
                    start = 2
                else: 
                    start = 0
            else:
                start = 1
        elif self.__vorherGegangenListe[2]:
            if self.nachbarFelder()[2]!=0:
                if pypos < ypos:
                    start = 3   
                else: 
                    start =1
            else:
                start = 2
        # Möglichkeit suchen
        gehtNicht = 0
        for counter in range(4):
            stelle = (counter+start)%4
            if self.nachbarFelder()[stelle] == 0:
                #print("0 gefunden! bei:", stelle)
                break
            else:
                gehtNicht += 1
        if gehtNicht <4:
            #print("Gewählte Richtung: ",stelle)
            if stelle == 0:
                return "rechts"
            elif stelle == 1:
                return "runter"
            elif stelle == 2:
                return "links"
            elif stelle == 3:
                return "hoch"    
        else:
            #print("Bewegung momentan nicht möglich!")
            pass

            
    def resetVorherGegangen(self):
        ''' 
        Eingabe: keine
        Funktion: Setzt die liste die angibt in welche Richtung sich der Gegner vorher bewegt wird zurück.
        Ausgabe: keine
        '''
        for x in range(4):
            self.__vorherGegangenListe[x]=False
    
    def bewegung(self):
        ''' 
        Eingabe: keine
        Funktion: Zuständig für die Koordinierung der Bewegung des Gegners
        Ausgabe: keine
        '''
        if self.__raster.spieler.getBewegt() and self.__leben > 0:
            pxpos = self.__raster.findSpieler()[0]
            pypos = self.__raster.findSpieler()[1]
            xpos = self.getPos()[0]
            ypos = self.getPos()[1]
            gewaehlteRichtung=""
            #Welche Richtung wird zuerst überprüft? 
            if not self.__raster.spieler in self.nachbarFelder():
                # wenn Differenz zw X-Koords größer ist als zw Y-Koords oder vorher Vertikal gelaufen wurde
                if abs(pxpos-xpos) > abs(pypos-ypos): 
                    gewaehlteRichtung=self.__xbewegung(pypos,ypos,pxpos,xpos)
                # wenn Differenz zw X-Koords kleiner ist als zw Y-Koords oder vorher Horizontal gelaufen wurde
                elif abs(pxpos-xpos) < abs(pypos-ypos): 
                    gewaehlteRichtung=self.__ybewegung(pypos,ypos,pxpos,xpos)
                # wenn Differenz zw x und y Koords gleich ist dann random eine zuerst zu prüfenden Richtung raussuchen
                else:
                    gewaehlteRichtung=choice([self.__xbewegung(pypos,ypos,pxpos,xpos),self.__ybewegung(pypos,ypos,pxpos,xpos)])
                self.resetVorherGegangen()
                if gewaehlteRichtung != "":
                    if gewaehlteRichtung =="rechts":
                        self.rechts()
                        self.__vorherGegangenListe[0] = True
                    elif gewaehlteRichtung == "links":
                        self.links()
                        self.__vorherGegangenListe[2] = True
                    elif gewaehlteRichtung == "hoch":
                        self.hoch()
                        self.__vorherGegangenListe[3] = True
                    elif gewaehlteRichtung == "runter":
                        self.runter()
                        self.__vorherGegangenListe[1] = True
        if not self.__raster.getKampfAktiv() and self.__raster.spieler in self.nachbarFelder() and not self.__raster.getMenuOffen():
            self.__raster.setKampfAktiv(True)
            self.kampfmanager = Kampfmanager(self.__raster.spieler,self,self.__raster)
            self.__raster.menu.kampfPopup(self.kampfmanager) 
                
        
                                 
    def __ybewegung(self,pypos,ypos,pxpos,xpos):
        ''' 
        Eingabe: pypos: int, ypos: int, pxpos: int, xpos: int
        Funktion: Bestimmt eine Richtung anhand der Y-Koordinaten von Spieler und Gegner. Löst alternativeBewegungFinden-Methode aus, wenn Richtung blockiert ist
        Ausgabe: string
        '''
        # hoch gehen
        if pypos < ypos:
            if self.nachbarFelder()[3]==0: #or self.vorherHochGegangen:
                return "hoch"
            else:
                return self.__alternativeBewegungFinden()
        # nach unten gehen
        elif pypos > ypos:
            if self.nachbarFelder()[1]==0: #or self.vorherRunterGegangen:
                return "runter"
            else:
                return self.__alternativeBewegungFinden()
        # y-Koord gleich
        elif pypos == ypos:
            return self.__xbewegung(pypos,ypos,pxpos,xpos)
            
    def __xbewegung(self,pypos,ypos,pxpos,xpos):
        ''' 
        Eingabe: pypos: int, ypos: int, pxpos: int, xpos: int
        Funktion: Bestimmt eine Richtung anhand der X-Koordinaten von Spieler und Gegner. Löst alternativeBewegungFinden-Methode aus, wenn Richtung blockiert ist
        Ausgabe: string
        '''
        if pxpos < xpos:
            if self.nachbarFelder()[2]==0: #or self.vorherLinksGegangen:
                return "links"
            else:
                return self.__alternativeBewegungFinden()
        elif pxpos > xpos:
            if self.nachbarFelder()[0]==0: #or self.vorherRechtsGegangen:
                return "rechts"
            else:
                return self.__alternativeBewegungFinden()
        elif pxpos == xpos:
            return self.__ybewegung(pypos,ypos,pxpos,xpos)
                                
    def besiegt(self):
        ''' 
        Eingabe: keine
        Funktion: Setzt in der rasterListe das Feld auf dem der Gegner aktuell steht auf den Wert Null
        Ausgabe: keine
        '''
        self.__raster.feldAendern(self.getPos()[0],self.getPos()[1],0)