import pygamepopup
from pygamepopup.menu_manager import MenuManager
from pygamepopup.components import Button, InfoBox, TextElement
import pygame

class Menu(object):
    def __init__(self,pManager):
        ''' 
        Eingabe: pManager: MenuManager
        Funktion: Initialisierungsmethode für das Menu
        Ausgabe: keine
        '''
        pygame.font.init()
        self.__pixelfont = pygame.font.Font("pixelfont.ttf",18)
        self.__pixelfontHeader = pygame.font.Font("pixelfont.ttf",24)
        self.__menuManager = pManager
        self.__exitRequest = False
        self.menuOffen = False
        self.__hintergrund = "Bilder/BG_Menue.png"
        self.__hintergrundRot = "Bilder/BG_Menue_Rot.png"
        pygamepopup.configuration.set_info_box_title_font(self.__pixelfontHeader)
        pygamepopup.configuration.set_button_title_font(self.__pixelfont)
        pygamepopup.configuration.set_text_element_font(self.__pixelfont)
        pygamepopup.configuration.set_info_box_background(self.__hintergrund)
        
    def tutorialPopup(self):
        ''' 
        Eingabe: keine
        Funktion: Stellt ein Tutorial-Popup-Fenster auf dem Bildschirm da
        Ausgabe: keine
        '''
        self.menuOffen = True
        self.__tutorial = InfoBox(
            title="Grundlegende Tasteneingaben",
            element_grid=
            [
            [TextElement(text="Bewegung",text_color="red")],
            [TextElement(text="WASD oder Pfeiltasten")],
            [TextElement(text="Kisten oeffnen",text_color="red")],
            [TextElement(text="O")],
            [TextElement(text="Inventar oeffnen",text_color="red")],
            [TextElement(text="I")],
            [TextElement(text="Tutorial wieder aufrufen",text_color="red")],
            [TextElement(text="H")],
            [Button(title="OK", callback=lambda: self.tutorialPopup2())],
            ],
            width=500,
            has_close_button=False,
            identifier="tutorial1")
        self.__menuManager.open_menu(self.__tutorial)  
        
    def tutorialPopup2(self):
        ''' 
        Eingabe: keine
        Funktion: Stellt ein Tutorial-Popup-Fenster zum Kampf auf dem Bildschirm da
        Ausgabe: keine
        '''
        self.__menuManager.close_given_menu("tutorial1")
        self.menuOffen = True
        self.__tutorial2 = InfoBox(
            title="Kampf",
            element_grid=
            [
            [TextElement(text="Kaempfe werden automatisch gestartet!",text_color="red")],
            [TextElement(text="Abkuerzungen",text_color="red")],
            [TextElement(text="AT: Bonus auf Angriff, PA: Bonus auf Ruestung, HE: Punkt die Leben wieder erhoehen")],
            [TextElement(text="Angreifen",text_color="red")],
            [TextElement(text="direkter Angriff auf den Gegner, zieht LP des Gegners")],
            [TextElement(text="Warten",text_color="red")],
            [TextElement(text="Greift nicht an, bekommt aber in der naechsten Runde +2 Schaden")],
            [Button(title="Fertig", callback=lambda: self.menuSchliessen())],
            ],
            width=500,
            has_close_button=False)
        self.__menuManager.open_menu(self.__tutorial2)  

    def kistenPopup(self,pWerte):
        ''' 
        Eingabe: pWerte: list
        Funktion: Stellt ein Kisten-Popup-Fenster auf dem Bildschirm da
        Ausgabe: keine
        '''
        self.menuOffen = True
        self.__kistenMenu = InfoBox(
            title="Kiste wurde geoeffnet!",
            element_grid=
            [
            [TextElement(text="Du findest:",text_color="red")],
            [TextElement(text=pWerte[-1],text_color=pWerte[-2][1])],
            [TextElement(text="AT"+str(pWerte[0]))],
            [TextElement(text="PA"+str(pWerte[1]))],
            [TextElement(text="HE"+str(pWerte[2]))],
            [Button(title="Mitnehmen", callback=lambda: self.menuSchliessen())],
            ],
            has_close_button=False,
            )
        self.__menuManager.open_menu(self.__kistenMenu)
        
    def kistenNichtPopup(self):
        '''
        Eingabe: keine
        Funktion: Stellt ein Popup-Fenster auf dem Bildschirm da, das benutzt wird wenn Kiste geöffnet werden soll aber Inventar voll ist
        Ausgabe: keine
        '''
        self.menuOffen = True
        self.__kistenNichtMenu = InfoBox(
            title="Kiste kann nicht geoeffnet werden",
            title_color="red",
            element_grid=
            [
            [TextElement(text="Inventar voll!",text_color="red")],
            [TextElement(text="Oeffne mit I das Inventar und entferne Gegenstände!")],
            [Button(title="OK", callback=lambda: self.menuSchliessen())],
            ],
            has_close_button=False)
        self.__menuManager.open_menu(self.__kistenNichtMenu)

    def inventarPopup(self,pWerte,pInventar):
        ''' 
        Eingabe: pWert: list, pInventar: Inventar object
        Funktion: Stellt ein Inventar-Popup-Fenster auf dem Bildschirm da
        Ausgabe: keine
        '''
        self.menuOffen = True
        self.__inventarMenu = InfoBox(
            title="Inventar",
            element_grid=
            [
            [TextElement(text="Dein Inventar enthaelt:")],
            [TextElement(text=pWerte[0][0],text_color=pWerte[0][1])],
            [Button(title=pWerte[0][2], callback=lambda:pInventar.gegenstandBenutzen(9),size=(80,20),no_background=True)],
            [TextElement(text=pWerte[1][0],text_color=pWerte[1][1])],
            [Button(title=pWerte[1][2], callback=lambda:pInventar.gegenstandBenutzen(8),size=(80,20),no_background=True)],
            [TextElement(text=pWerte[2][0],text_color=pWerte[2][1])],
            [Button(title=pWerte[2][2], callback=lambda:pInventar.gegenstandBenutzen(7),size=(80,20),no_background=True)],
            [TextElement(text=pWerte[3][0],text_color=pWerte[3][1])],
            [Button(title=pWerte[3][2], callback=lambda:pInventar.gegenstandBenutzen(6),size=(80,20),no_background=True)],
            [TextElement(text=pWerte[4][0],text_color=pWerte[4][1])],
            [Button(title=pWerte[4][2], callback=lambda:pInventar.gegenstandBenutzen(5),size=(80,20),no_background=True)],
            [TextElement(text=pWerte[5][0],text_color=pWerte[5][1])],
            [Button(title=pWerte[5][2], callback=lambda:pInventar.gegenstandBenutzen(4),size=(80,20),no_background=True)],
            [TextElement(text=pWerte[6][0],text_color=pWerte[6][1])],
            [Button(title=pWerte[6][2], callback=lambda:pInventar.gegenstandBenutzen(3),size=(80,20),no_background=True)],
            [TextElement(text=pWerte[7][0],text_color=pWerte[7][1])],
            [Button(title=pWerte[7][2], callback=lambda:pInventar.gegenstandBenutzen(2),size=(80,20),no_background=True)],
            [TextElement(text=pWerte[8][0],text_color=pWerte[8][1])],
            [Button(title=pWerte[8][2], callback=lambda:pInventar.gegenstandBenutzen(1),size=(80,20),no_background=True)],
            [TextElement(text=pWerte[9][0],text_color=pWerte[9][1])],
            [Button(title=pWerte[9][2], callback=lambda:pInventar.gegenstandBenutzen(0),size=(80,20),no_background=True)],
            [Button(title="Inventar schliessen", callback=lambda: self.menuSchliessen())]
            ],
            has_close_button=False)
        self.__menuManager.open_menu(self.__inventarMenu)
        
    def kampfPopup(self,pKampfmanager):
        ''' 
        Eingabe: pKampfmanager: Kampfmanager object
        Funktion: Stellt ein Kampf-Popup-Fenster auf dem Bildschirm da
        Ausgabe: keine
        '''
        self.menuOffen = True
        self.__kampfMenu = InfoBox(
            title="Kampf findet statt, waehle Aktion aus",
            element_grid=[
            [TextElement(text="o==[]::::::::::::::::>",text_color="grey")],
            [TextElement(text=pKampfmanager.menuAusgabe()[-1])],
            [TextElement(text=pKampfmanager.menuAusgabe()[-3],text_color="green")],
            [TextElement(text=pKampfmanager.menuAusgabe()[-2],text_color="red")],
            [TextElement(text=pKampfmanager.menuAusgabe()[0]+"["+str(pKampfmanager.menuAusgabe()[3])+"/"+str(pKampfmanager.menuAusgabe()[4])+"]")],
            [TextElement(text=">Deine Aktuellen Werte:")],
            [TextElement(text=">>Angriff: "+str(pKampfmanager.menuAusgabe()[1]))],   
            [TextElement(text=">>Ruestung: "+str(pKampfmanager.menuAusgabe()[2]))],
            [TextElement(text=pKampfmanager.menuAusgabe()[5]+"(Gegner) "+"["+str(pKampfmanager.menuAusgabe()[6])+"/"+str(pKampfmanager.menuAusgabe()[7])+"]")],           
            [Button(title="Angriff", callback=lambda: pKampfmanager.spielerAngriff())],
            [Button(title="Warten",callback=lambda: pKampfmanager.warten())],
            [TextElement(text="o==[]::::::::::::::::>",text_color="grey")],],
            has_close_button=False,
            identifier="kampf")
        self.__menuManager.open_menu(self.__kampfMenu)
    
    def kampfFertigPopup(self,pWerte):
        ''' 
        Eingabe: keine
        Funktion: Stellt ein Popup-Fenster auf dem Bildschirm da wenn der Kampf abgeschlossen ist
        Ausgabe: keine
        '''
        self.menuOffen = True
        self.__kampfFertigMenu=InfoBox(
            title="Kampf beendet!",
            title_color="red",
            element_grid=[
            [TextElement(text="Gegner wurde besiegt")],
            [TextElement(text=pWerte[0])],
            [TextElement(text=pWerte[1])],
            [Button(title="OK", callback=lambda: self.menuSchliessen())]
            ],
            has_close_button=False)
        self.__menuManager.open_menu(self.__kampfFertigMenu)
        
    def gameover(self,pSpieler):
        ''' 
        Eingabe: keine
        Funktion: Stellt ein GameOver-Popup-Fenster auf dem Bildschirm da wenn die leben des Spielers auf <= 0 gesunken sind
        Ausgabe: keine
        '''
        self.menuOffen = True
        self.__gameOverMenu = InfoBox(
            title="Game Over!",
            element_grid=
            [
            [Button(title="Schliessen", callback=lambda: pSpieler.gameover())]
            ],
            background_path=self.__hintergrundRot,
            has_close_button=False)
        self.__menuManager.open_menu(self.__gameOverMenu)
        
    def zuViel(self,pSpieler):
        ''' 
        Eingabe: keine
        Funktion: Stellt ein Popup-Fenster auf dem Bildschirm da wenn zuviele Gegner erzeugt werden soll als Platz uf dem Raster ist
        Ausgabe: keine
        '''
        self.menuOffen = True
        self.__zuvielmenu = InfoBox(
            title="Zu kleines Spielfeld!",
            element_grid=
            [
            [Button(title="OK", callback=lambda: pSpieler.gameover())]
            ],
            background_path=self.__hintergrundRot,
            has_close_button=False)
        self.__menuManager.open_menu(self.__zuvielmenu)
        
    def neueRunde(self):
        ''' 
        Eingabe: keine
        Funktion: Stellt ein Popup-Fenster auf dem Bildschirm da wenn alle Gegner für eine Runde besiegt wurden. Kündigt eine neue Runde an.
        Ausgabe: keine
        '''
        self.menuOffen = True
        self.__neueRundeMenu = InfoBox(
            title="Neue Runde beginnt",
            element_grid=
            [
            [Button(title="OK", callback=lambda: self.menuSchliessen())]
            ],
            has_close_button=False)
        self.__menuManager.open_menu(self.__neueRundeMenu)
        
    def menuSchliessen(self):
        ''' 
        Eingabe: keine
        Funktion: Schließt das aktuelle Menü. TutorialFertig wird benötigt wenn das erste Menü also das Tutorial Popup geschlossen wurde
        Ausgabe: keine
        '''
        self.__menuManager.close_active_menu()
        self.menuOffen = False
    '''
    Methoden ab hier übernommen von https://pygame-popup-manager.readthedocs.io/en/latest/examples.html siehe Literaturverzeichnis 5.
    '''
    def click(self, pButton, pPosition):
        ''' 
        Eingabe: button: int, position: pygame.Vector2
        Funktion: Gibt die Position eines Linksklicks der Maus weiter an das aktive Menu
        Ausgabe: boolean
        '''
        self.__menuManager.click(pButton, pPosition)
        return self.__exitRequest
    
    def exit(self):
        ''' 
        Eingabe: keine
        Funktion: Setzt das exit_request Attribut auf True. Wird in der Hauptschleife wieder nach events geprüft wird bei click True zurückgegben und self.run dadurch auf False gesetzt. Dann schließt sich das Programm
        Ausgabe: keine
        '''
        self.__exitRequest = True
        
    def motion(self, pPosition):
        ''' 
        Eingabe: position: pygame.Vector2
        Funktion: Gibt ein Bewegungsevent als eine Verschiebung des Mauszeigers an das aktive Menu weiter
        Ausgabe: keine
        '''
        self.__menuManager.motion(pPosition)