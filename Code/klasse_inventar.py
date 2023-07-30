class Inventar(object):
    def __init__(self,pSpieler,pRaster):
        ''' 
        Eingabe: pSpieler: Spieler, pRaster: Raster
        Funktion: Initialisierungsmethode für das Inventar
        Ausgabe: keine
        '''
        self.__inventarListe = [False,False,False,False,False,False,False,False,False,False]
        self.__gegenstaendeAnzahl = 0
        self.__spieler = pSpieler
        self.__raster = pRaster
        
    def hinzufuegen(self,pGegenstand):
        ''' 
        Eingabe: pGegenstand: Gegenstand-Objekt
        Funktion: Fügt self.inventarListe ein Gegenstand-Objekt hinzu wenn noch Platz im Inventar vorhanden ist also noch ein Listenelement False ist.
        Ausgabe: keine
        '''
        for x in range(9,-1,-1):
            if not self.__gegenstaendeAnzahl == 10 and self.__inventarListe[x] == False:
                self.__inventarListe[x] = pGegenstand
                self.__gegenstaendeAnzahl +=1
                break
            
    def __loeschen(self,pIndex):
        ''' 
        Eingabe: pIndex: int
        Funktion: Löscht einen Gegenstand aus dem Inventar und passt die Spielerwerte an.
        Ausgabe: keine
        '''
        if self.__inventarListe[pIndex].getTyp()!="Heilen":
            self.__spieler.wertAnpassen(0,-abs(self.__inventarListe[pIndex].werteAusgeben()[0]))
            self.__spieler.wertAnpassen(1,-abs(self.__inventarListe[pIndex].werteAusgeben()[1]))
        self.__inventarListe.remove(self.__inventarListe[pIndex])
        self.__inventarListe.insert(0,False)
        self.__gegenstaendeAnzahl -= 1
        
    def gegenstandBenutzen(self,pIndex):
        ''' 
        Eingabe: pIndex: int
        Funktion: 
        Ausgabe: Methode wird durch Knopfdruck im Inventarmenü ausgelöst. Dient zum Heilen von leben durch einen Heiltrank oder nur zum Entfernen eines Gegenstandes
        '''
        if not self.__inventarListe[pIndex] == False:
            heilendePunkte = self.__inventarListe[pIndex].werteAusgeben()[2]
            if heilendePunkte > 0:
                '''Alternative: heilen nur möglich, wenn genug Schaden genommen wurde damit der Heiltrank die Leben bis maximal maxLeben heilt
                if not self.__spieler.menuAusgabe()[3]+heilendePunkte > self.__spieler.menuAusgabe()[4]:
                    self.__spieler.wertAnpassen(2,heilendePunkte)
                    self.__loeschen(self.__inventarListe.index(self.__inventarListe[pIndex]))
                else:
                    #print("Nicht genug Schaden um mit diesem Trank zu heilen")
                '''
                if self.__spieler.menuAusgabe()[3]+heilendePunkte >= self.__spieler.menuAusgabe()[4]:
                    heilendePunkte = self.__spieler.menuAusgabe()[5] - self.__spieler.menuAusgabe()[4]
                self.__spieler.wertAnpassen(2,heilendePunkte)
                self.__loeschen(self.__inventarListe.index(self.__inventarListe[pIndex]))
            else:
                self.__loeschen(self.__inventarListe.index(self.__inventarListe[pIndex]))
            self.__raster.menu.menuSchliessen()
            self.__raster.menu.inventarPopup(self.menuAusgabe(),self)
        else:
            #print("kein Gegenstand")
            pass
              
    def updateSpielerwerte(self):
        ''' 
        Eingabe: keine
        Funktion: Wenn Gegenstand noch nicht verrechnet wurde werden seine Werte auf die Werte des Spielers addiert.
        Ausgabe: keine
        '''
        for gegenstand in self.__inventarListe:
            if gegenstand !=False and not gegenstand.werteAusgeben()[3]:
                if gegenstand.getTyp() == "PermaHeilen":
                    self.__spieler.wertAnpassen(2,gegenstand.werteAusgeben()[2])
                    self.__spieler.wertAnpassen(3,gegenstand.werteAusgeben()[2])
                    self.__loeschen(self.__inventarListe.index(gegenstand))
                else:
                    self.__spieler.wertAnpassen(0,gegenstand.werteAusgeben()[0])
                    self.__spieler.wertAnpassen(1,gegenstand.werteAusgeben()[1])
                    gegenstand.setVerrechnet(True)
                
        
    def inventarAusgeben(self):
        ''' 
        Eingabe: keine
        Funktion: Gibt die Liste der Gegenstandsobjekte aus die momentan im Inventar vorhanden sind.
        Ausgabe: self.inventarListe: list
        '''
        return self.__inventarListe
    
    def inventarVoll(self):
        ''' 
        Eingabe: keine
        Funktion: Gibt True zurück wenn das Attribut gegenstaendeAnzahl gleich 10 ist
        Ausgabe: bool
        '''
        if self.__gegenstaendeAnzahl == 10:
            return True 
        else: 
            return False
    
    def gegenstandAusgeben(self,pStelle):
        ''' 
        Eingabe: pStelle: int
        Funktion: Gibt ein Gegenstand-Objekt an einer übergebenen Stelle der self.inventarListe aus
        Ausgabe: Gegenstand-Objekt
        '''
        return self.__inventarListe[pStelle]
    
    def neustenGegenstandAusgeben(self):
        ''' 
        Eingabe: keine
        Funktion: Gibt das zuletzt aufgehobene Gegenstand-Objekt us
        Ausgabe: Gegenstand-Objekt
        '''
        #if self.gegenstaendeAnzahl <= 10:
        for x in range(len(self.__inventarListe)):
            if self.__inventarListe[x]!=False:
                return self.__inventarListe[x]

    def menuAusgabe(self):
        ''' 
        Eingabe: keine
        Funktion: Erstelle eine Liste mit den Werten der Gegenstands-Objekten in self.inventarListe. Benutzt zur Visualisierung im Popup-Fenster.
        Ausgabe: output: list
        '''
        output = []
        for gegenstand in self.__inventarListe:
            if not gegenstand == False:
                if not gegenstand.getTyp()=="Heilen":
                    output.append((gegenstand.werteAusgeben()[-1]+"AT: "+str(gegenstand.werteAusgeben()[0])+" PA: "+str(gegenstand.werteAusgeben()[1]),gegenstand.werteAusgeben()[-2][1],"Entfernen"))
                else:
                    output.append((gegenstand.werteAusgeben()[-1]+"HE: "+str(gegenstand.werteAusgeben()[2]),"White","Benutzen"))
            else:
                output.append(("","white",""))
        output.reverse()
        return output