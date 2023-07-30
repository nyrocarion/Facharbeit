from random import randint,seed
seed()

class Kampfmanager(object):
    def __init__(self,pSpieler,pGegner,pRaster):
        ''' 
        Eingabe: pRaster: Raster, pSpieler: Spieler, pGegner: Gegner
        Funktion: Initialisierungsmethode für den Kampfmanager
        Ausgabe: keine
        '''
        self.__raster = pRaster
        self.__spieler = pSpieler
        self.__gegner = pGegner
        self.__spielerbonus = 0
        self.__gegnerbonus = 0
        self.__gewartet = 0
        
    def menuAusgabe(self):
        ''' 
        Eingabe: keine
        Funktion: Gibt aktuelle Werte des Spielers und Gegners zurück. Benutzt für Visualisierung im Popup-Fenster
        Ausgabe: list
        '''
        output = [self.__spieler.menuAusgabe()[0],self.__spieler.menuAusgabe()[1],self.__spieler.menuAusgabe()[2],self.__spieler.menuAusgabe()[3],self.__spieler.menuAusgabe()[4],self.__gegner.menuAusgabe()[0],self.__gegner.menuAusgabe()[3],self.__gegner.menuAusgabe()[4]]
        output.append(self.__spieler.lebenBar())
        output.append(self.__gegner.lebenBar())
        if self.__gewartet > 0:
            output.append("Du hast "+str(self.__gewartet)+" Runden auf deinen Angriff gewartet! Beim naechsten Angriff erhaelst du einen Bonus von +"+str(self.__gewartet*2)+" auf deinen Angriffswert.")
        else:
            output.append(" ")
        return output
        
    def __bonusGenerieren(self,pMax,gMax):
        ''' 
        Eingabe: pMax: int, gMax: int
        Funktion: Generiert einen zufälligen Bonus für Spieler und Gegner zwischen 1 und dem jeweiligen Maximalwert
        Ausgabe: keine
        '''
        self.__spielerbonus = randint(1,pMax)
        self.__gegnerbonus = randint(1,gMax)
        
    def warten(self):
        ''' 
        Eingabe: keine
        Funktion: Alternative zu self.spielerAngriff. Kein Angriff wird ausgeführt dafür wird der Schadensbonus um 2 pro Warte Aktion wiederholt
        Ausgabe: keine
        '''
        if self.__spieler.kampf_aktiv:
            self.__gewartet +=1
            self.__gegnerAngriff()
            #self.aktuelleSituationAusgeben()
            self.__lebenAufNull()
        
    def __lebenAufNull(self):
        ''' 
        Eingabe: keine
        Funktion: Prüft ob der Leben-Wert vom Spieler- oder Gegner-Objekt <= 0 ist. Abbruchskriterium für die Kampfsimulation.
        Ausgabe: keine
        '''
        if self.__spieler.menuAusgabe()[3] <= 0:
            #print("spieler tod")
            self.__raster.setKampfAktiv(False)
            self.__raster.menuManager.close_active_menu()
            self.__raster.menu.menuOffen = False
            self.__spieler.besiegt()
        elif self.__gegner.menuAusgabe()[3] <= 0:
            #print("gegner besiegt")
            self.__raster.setKampfAktiv(False)
            self.__raster.menuManager.close_active_menu()
            self.__raster.menu.menuOffen = False
            self.__raster.getoeteteGegner += 1
            self.__raster.insgTote += 1
            self.__raster.menu.kampfFertigPopup(self.__kampfFertigMenuAusgabe())
            self.__gegner.besiegt()
            self.__raster.gegner.remove(self.__gegner)
        
    def spielerAngriff(self):
        ''' 
        Eingabe: keine
        Funktion: Zieht vom Leben-Wert des Gegner-Objekt Punkte ab in Abhängigkeit von Spieler-Werten, Boni und gegnerischen Werten. Danach folgt der gegnerische Angriff
        Ausgabe: keine
        '''
        if self.__spieler.kampf_aktiv:
            self.__bonusGenerieren(6,3)
            angriffSpieler = self.__spieler.menuAusgabe()[1]+self.__spielerbonus+self.__gewartet*2
            self.__gewartet = 0
            abwehrGegner = self.__gegner.menuAusgabe()[2]+self.__gegnerbonus
            self.__abziehen(angriffSpieler-abwehrGegner,self.__gegner,"Leben")
            self.__gegnerAngriff()
            #self.aktuelleSituationAusgeben()
            self.__lebenAufNull()
        
    def __gegnerAngriff(self):
        ''' 
        Eingabe: keine
        Funktion: Zieht vom Leben-Wert des Spieler-Objekts Punkte ab in Abhängigkeit von Gegner-Werten, Boni und Spieler-Werten.
        Ausgabe: boolean
        '''
        self.__bonusGenerieren(3,6)
        abwehrSpieler = self.__spieler.menuAusgabe()[2]+self.__spielerbonus
        angriffGegner = self.__gegner.menuAusgabe()[1]+self.__gegnerbonus
        self.__abziehen(angriffGegner-abwehrSpieler,self.__spieler,"Leben")
        self.__raster.menuManager.close_active_menu()
        self.__raster.menu.kampfPopup(self)

    def __abziehen(self,pAbzug,pCharakter,pWert):
        ''' 
        Eingabe: pAbzug: int, pWert: tuple
        Funktion: Zieht von einem Wert des Spielers/Gegners Punkte ab.
        Ausgabe: keine
        '''
        if not pAbzug <= 0:
            if pWert=="Angriff":
                pCharakter.wertAnpassen(0,-pAbzug)
            elif pWert=="Ruestung":
                pCharakter.wertAnpassen(1,-pAbzug)           
            elif pWert=="Leben":
                pCharakter.wertAnpassen(2,-pAbzug)           
    
    def __kampfFertigMenuAusgabe(self):
        ''' 
        Eingabe: keine
        Funktion: Erstellt strings die im Menü nach einem erfolgreich abgeschlossenem Kampf angezeigt werden.
        Ausgabe: list of string
        '''
        output = []
        output.append("Du hast noch "+str(self.__spieler.menuAusgabe()[3])+" von " +str(self.__spieler.menuAusgabe()[4]) +" Leben." )
        output.append("Seit Spielbeginn hast du "+str(self.__raster.insgTote)+" Gegner besiegt!")
        return output