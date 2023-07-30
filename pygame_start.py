import pygame
import pygamepopup
import time
from Code.klasse_raster import Raster
import sys

class Main(object):
    def __init__(self):
        pygame.init()
        pygamepopup.init()
        self.__spielefenster = pygame.display.set_mode(size=(1000,1000))
        self.__clock = pygame.time.Clock()        
        self.__raster = Raster(5,5,self.__spielefenster,self)
        self.__raster.rasterMalen()
        self.__raster.menu.tutorialPopup()   
               
    def hauptschleife(self):
        self.run = True
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    # Bewegung
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.__raster.setTasteneingabenAttribute("links",True)
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.__raster.setTasteneingabenAttribute("rechts",True)
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.__raster.setTasteneingabenAttribute("hoch",True)
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.__raster.setTasteneingabenAttribute("runter",True)
                    # Spieleraktionen
                    if event.key == pygame.K_o:
                        self.__raster.setTasteneingabenAttribute("kiste",True)
                    if event.key == pygame.K_k:
                        self.__raster.setTasteneingabenAttribute("angreifen",True)
                    if event.key == pygame.K_i:
                        self.__raster.setTasteneingabenAttribute("inventar",True)
                    if event.key == pygame.K_h:
                        self.__raster.menu.tutorialPopup() 
                    # Debugging
                    if event.key == pygame.K_t:
                        self.__raster.rasterAusgeben()
                    if event.key == pygame.K_p:
                        print(self.__raster.spieler.nachbarFelder())
                    if event.key == pygame.K_ESCAPE:
                        if not self.__raster.spieler.kampf_aktiv:
                            self.__raster.menu.menuSchliessen()
                    if event.key == pygame.K_1:
                        self.__raster.spieler.wertAnpassen(2,-10)
                # sagt dem aktiven Menu wo die Maus gerade ist
                elif event.type == pygame.MOUSEMOTION:
                    self.__raster.menuManager.motion(event.pos)
                # prüft welcher knopf gedrückt wurde
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1 or event.button == 3:  
                        self.run = not self.__raster.menuManager.click(event.button, event.pos)   
            self.__raster.pruefen()
            if not self.__raster.menu.menuOffen:
                self.__raster.spieler.bewegung()
            self.__raster.spieler.update()
            for gegner in self.__raster.gegner:
                gegner.bewegung()
            self.__raster.spieler.setBewegt(False)
            self.__spielefenster.fill((55, 51,51))
            self.__raster.rasterMalen()
            self.__raster.menuManager.display()
            pygame.display.flip()
            self.__clock.tick(10)
            time.sleep(0.1)
        pygame.quit()
        sys.exit()   
          
main = Main()
main.hauptschleife()