class Feld(object):
    def __init__(self,xWert,yWert):
        ''' 
        Eingabe: xWert: int, yWert: int
        Funktion: Initialisierungsmethode für das Feld
        Ausgabe: keine
        '''
        self.pos = (xWert,yWert)
        self.wert = 0
        
    def getPos(self):
        ''' 
        Eingabe: keine
        Funktion: Gibt Positions des Felds zurück
        Ausgabe: tuple
        '''
        return self.pos
    
    def getWert(self):
        ''' 
        Eingabe: keine
        Funktion: Gibt Wert des Feld-Objektes zurück.
        Ausgabe: int, Gegner-Objekt, Spieler-Objekt oder Kisten-Objekt
        '''
        return self.wert
    
    def setWert(self,pWert):
        ''' 
        Eingabe: int, Gegner-Objekt, Spieler-Objekt oder Kisten-Objekt
        Funktion: Ordnet self.wert einen angegebenen Wert zu
        Ausgabe: keine
        '''
        self.wert = pWert