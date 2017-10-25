import sys
import pygame
from Modules.Button import *
from Modules.Color import *
from Modules.Image import *
from Modules.Key import *
from Modules.Music import *
from Modules.Option import *
from Modules.Text import *
pygame.init()

class Menu:
    def __init__(self):
        # Default display settings
        self.defaultDisplayWidth = 1200
        self.defaultDisplayHeight = 700

        # Get monitor size info
        displayInfo = pygame.display.Info()
        self.monitorScreenWidth = displayInfo.current_w
        self.monitorScreenHeight = displayInfo.current_h

        # Set display starting configuration
        self.currentDisplayWidth = self.defaultDisplayWidth
        self.currentDisplayHeight = self.defaultDisplayHeight

        # Initialize display
        self.display = pygame.display.set_mode((self.currentDisplayWidth, self.currentDisplayHeight))
        pygame.display.set_caption('Cholo Fighter')
        
        # Initialize clock
        self.clock = pygame.time.Clock()

        # Play music
        Music.playSong('quiero_amanecer.mp3')
        Music.setVolume(Option.volume)

        # Current player being configured in the configure player menu
        self.configuredPlayer = 1

        # Current key being configured in the configure player menu
        self.configureKeyId = None

    def gameMenu(self):
        while True:
            # Analize events
            mousebuttonupTriggered = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    mousebuttonupTriggered = True
                    
            # Draw background
            self.display.fill(Color.white)
            pygame.draw.rect(self.display, Color.black, (20, 20, self.currentDisplayWidth - 40, self.currentDisplayHeight - 40))
            
            # Load the logo
            logo, logoRect = Image.loadImage('logo.png')
            logoRect.center = (self.currentDisplayWidth / 2, self.currentDisplayHeight * 0.65)
            self.display.blit(logo, logoRect)

            # Draw buttons
            buttonPlay = Button('Jugar', 'white', 'dolphins.ttf', 35, Color.black, Color.brightGreen, 150, 45, 250, 50, self.display)
            buttonMusic = Button('Musica', 'white', 'dolphins.ttf', 35, Color.black, Color.brightGreen, self.currentDisplayWidth - 400, 45, 250, 50, self.display)
            buttonQuit = Button('Salir', 'white', 'dolphins.ttf', 35, Color.black, Color.red, 150, 115, 250, 50, self.display)
            buttonOptions = Button('Opciones', 'white', 'dolphins.ttf', 35, Color.black, Color.brightGreen, self.currentDisplayWidth - 400, 115, 250, 50, self.display)

            # Listen for button clicked
            if mousebuttonupTriggered:
                if buttonPlay.mouseInBonudaries():
                    #self.gameSelection()
                    pass
                elif buttonMusic.mouseInBonudaries():
                    Music.toggleMusic()
                elif buttonQuit.mouseInBonudaries():
                    pygame.quit()
                    sys.exit()
                elif buttonOptions.mouseInBonudaries():
                    self.gameOptions()

            # Refresh
            pygame.display.update()
            self.clock.tick(20)

    def gameSelection(self):
        conn = create_connection()
        with conn:
            personajes = select_personajes(conn)

        juego = MainGame()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            pygame.draw.rect(self.display, black, (20, 20, 1160, 660))

            # for i in range(0, personajes.__len__()):
            #     xpos = (self.width / personajes.__len__()) / 2 + (self.width / personajes.__len__()) * i  # (x/n)(i+0.5)
            #     # nombre
            #     text_surf, text_rect = text_render(personajes[i].nombre, 'dolphins.ttf', 20)
            #     text_rect.center = (xpos, 300)
            #     self.display.blit(text_surf, text_rect)
            #     #vida
            #     text_surf, text_rect = text_render(str(personajes[i].vida), 'dolphins.ttf', 20)
            #     text_rect.center = (xpos, 350)
            #     self.display.blit(text_surf, text_rect)

            for i in range(0, personajes.__len__()):
                x_n = (self.width - 30 * 2) / personajes.__len__()
                xpos = 30 + i * x_n
                button = Button(personajes[i].nombre, xpos, 300, x_n, 50, black, bright_red, 27, None)
                button.draw_button(self.display)

            button = Button('Regresar', 30, 30, 150, 30, black, bright_orange, 20, self.game_menu)
            button.draw_button(self.display)
            button = Button('Jugar', (self.width-150) / 2, 500, 150, 50, black, bright_green, 35, juego.game)
            button.draw_button(self.display)

            text_surf, text_rect = text_render('Seleccion de Personajes', 'dolphins.ttf', 70)
            text_rect.center = (self.width / 2, 100)
            self.display.blit(text_surf, text_rect)

            pygame.display.update()
            self.clock.tick(20)

    def gameConfigurePlayer(self):
        while True:
             # Analize events
            mousebuttonupTriggered = False
            keydownTriggered = False
            keydownValue = None
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                else:
                    if event.type == pygame.MOUSEBUTTONUP:
                        mousebuttonupTriggered = True
                    if event.type == pygame.KEYDOWN:
                        keydownTriggered = True
                        keydownValue = event.key

            # Draw background
            self.display.fill(Color.white)
            pygame.draw.rect(self.display, Color.black, (20, 20, self.currentDisplayWidth - 40, self.currentDisplayHeight - 40))

            # Draw menu content
            buttonBack = Button('Regresar', 'white', 'dolphins.ttf', 20, Color.black, Color.brightOrange, 30, 30, 150, 30, self.display)

            buttonDefaults = Button('Reestablecer', 'white', 'dolphins.ttf', 20, Color.black, Color.brightOrange, self.currentDisplayWidth - 180, 30, 150, 30, self.display)

            Text.renderLabel('Configuración Jugador %s' % str(self.configuredPlayer), 'white', 'dolphins.ttf', 70, self.currentDisplayWidth / 2, 100, '', self.display)

            # First Column
            Text.renderLabel('Movimiento', 'white', 'dolphins.ttf', 32, 50, 200, 'topleft', self.display)

            Text.renderLabel('Arriba', 'white', 'dolphins.ttf', 24, 50, 250, 'topleft', self.display)
            if self.configuredPlayer == 1:
                buttonMoveUp = Button('...' if self.configureKeyId == 1 else Key.getKeyLabel(Option.controlPlayer1.moveUp), 'white', 'arial.ttf', 24, Color.black, Color.blue, (self.currentDisplayWidth / 2) - 200, 250, 150, 30, self.display)
            elif self.configuredPlayer == 2:
                buttonMoveUp = Button('...' if self.configureKeyId == 1 else Key.getKeyLabel(Option.controlPlayer2.moveUp), 'white', 'arial.ttf', 24, Color.black, Color.blue, (self.currentDisplayWidth / 2) - 200, 250, 150, 30, self.display)

            Text.renderLabel('Abajo', 'white', 'dolphins.ttf', 24, 50, 300, 'topleft', self.display)
            if self.configuredPlayer == 1:
                buttonMoveDown = Button('...' if self.configureKeyId == 2 else Key.getKeyLabel(Option.controlPlayer1.moveDown), 'white', 'arial.ttf', 24, Color.black, Color.blue, (self.currentDisplayWidth / 2) - 200, 300, 150, 30, self.display)
            elif self.configuredPlayer == 2:
                buttonMoveDown = Button('...' if self.configureKeyId == 2 else Key.getKeyLabel(Option.controlPlayer2.moveDown), 'white', 'arial.ttf', 24, Color.black, Color.blue, (self.currentDisplayWidth / 2) - 200, 300, 150, 30, self.display)
            
            Text.renderLabel('Izquierda', 'white', 'dolphins.ttf', 24, 50, 350, 'topleft', self.display)
            if self.configuredPlayer == 1:
                buttonMoveLeft = Button('...' if self.configureKeyId == 3 else Key.getKeyLabel(Option.controlPlayer1.moveLeft), 'white', 'arial.ttf', 24, Color.black, Color.blue, (self.currentDisplayWidth / 2) - 200, 350, 150, 30, self.display)
            elif self.configuredPlayer == 2:
                buttonMoveLeft = Button('...' if self.configureKeyId == 3 else Key.getKeyLabel(Option.controlPlayer2.moveLeft), 'white', 'arial.ttf', 24, Color.black, Color.blue, (self.currentDisplayWidth / 2) - 200, 350, 150, 30, self.display)
            
            Text.renderLabel('Derecha', 'white', 'dolphins.ttf', 24, 50, 400, 'topleft', self.display)
            if self.configuredPlayer == 1:
                buttonMoveRight = Button('...' if self.configureKeyId == 4 else Key.getKeyLabel(Option.controlPlayer1.moveRight), 'white', 'arial.ttf', 24, Color.black, Color.blue, (self.currentDisplayWidth / 2) - 200, 400, 150, 30, self.display)
            elif self.configuredPlayer == 2:
                buttonMoveRight = Button('...' if self.configureKeyId == 4 else Key.getKeyLabel(Option.controlPlayer2.moveRight), 'white', 'arial.ttf', 24, Color.black, Color.blue, (self.currentDisplayWidth / 2) - 200, 400, 150, 30, self.display)
            
            Text.renderLabel('Saltar', 'white', 'dolphins.ttf', 24, 50, 450, 'topleft', self.display)
            if self.configuredPlayer == 1:
                buttonJump = Button('...' if self.configureKeyId == 5 else Key.getKeyLabel(Option.controlPlayer1.jump), 'white', 'arial.ttf', 24, Color.black, Color.blue, (self.currentDisplayWidth / 2) - 200, 450, 150, 30, self.display)
            elif self.configuredPlayer == 2:
                buttonJump = Button('...' if self.configureKeyId == 5 else Key.getKeyLabel(Option.controlPlayer2.jump), 'white', 'arial.ttf', 24, Color.black, Color.blue, (self.currentDisplayWidth / 2) - 200, 450, 150, 30, self.display)
            
            # Second column
            Text.renderLabel('Ataque básico', 'white', 'dolphins.ttf', 32, (self.currentDisplayWidth / 2) + 50, 200, 'topleft', self.display)

            Text.renderLabel('Primario', 'white', 'dolphins.ttf', 24, (self.currentDisplayWidth / 2) + 50, 250, 'topleft', self.display)
            if self.configuredPlayer == 1:
                buttonPrimaryBasicAttack = Button('...' if self.configureKeyId == 6 else Key.getKeyLabel(Option.controlPlayer1.primaryBasicAttack), 'white', 'arial.ttf', 24, Color.black, Color.blue, self.currentDisplayWidth - 200, 250, 150, 30, self.display)
            elif self.configuredPlayer == 2:
                buttonPrimaryBasicAttack = Button('...' if self.configureKeyId == 6 else Key.getKeyLabel(Option.controlPlayer2.primaryBasicAttack), 'white', 'arial.ttf', 24, Color.black, Color.blue, self.currentDisplayWidth - 200, 250, 150, 30, self.display)
            
            Text.renderLabel('Secundario', 'white', 'dolphins.ttf', 24, (self.currentDisplayWidth / 2) + 50, 300, 'topleft', self.display)
            if self.configuredPlayer == 1:
                buttonSecondaryBasicAttack = Button('...' if self.configureKeyId == 7 else Key.getKeyLabel(Option.controlPlayer1.secondaryBasicAttack), 'white', 'arial.ttf', 24, Color.black, Color.blue, self.currentDisplayWidth - 200, 300, 150, 30, self.display)
            elif self.configuredPlayer == 2:
                buttonSecondaryBasicAttack = Button('...' if self.configureKeyId == 7 else Key.getKeyLabel(Option.controlPlayer2.secondaryBasicAttack), 'white', 'arial.ttf', 24, Color.black, Color.blue, self.currentDisplayWidth - 200, 300, 150, 30, self.display)
            
            Text.renderLabel('Poder', 'white', 'dolphins.ttf', 32, (self.currentDisplayWidth / 2) + 50, 350, 'topleft', self.display)

            Text.renderLabel('Básico', 'white', 'dolphins.ttf', 24, (self.currentDisplayWidth / 2) + 50, 400, 'topleft', self.display)
            keyCombination = ''
            started = False
            if self.configuredPlayer == 1:
                for key in Option.controlPlayer1.basicPower:
                    if started:
                        keyCombination += ' + ' + Key.getKeyLabel(key)
                    else:
                        keyCombination += Key.getKeyLabel(key)
                        started = True
            elif self.configuredPlayer == 2:
                for key in Option.controlPlayer2.basicPower:
                    if started:
                        keyCombination += ' + ' + Key.getKeyLabel(key)
                    else:
                        keyCombination += Key.getKeyLabel(key)
                        started = True
            Text.renderLabel(keyCombination, 'white', 'arial.ttf', 24, self.currentDisplayWidth - 55, 400, 'topright', self.display)

            Text.renderLabel('Especial', 'white', 'dolphins.ttf', 24, (self.currentDisplayWidth / 2) + 50, 450, 'topleft', self.display)
            keyCombination = ''
            started = False
            if self.configuredPlayer == 1:
                for key in Option.controlPlayer1.specialPower:
                    if started:
                        keyCombination += ' + ' + Key.getKeyLabel(key)
                    else:
                        keyCombination += Key.getKeyLabel(key)
                        started = True
            elif self.configuredPlayer == 2:
                for key in Option.controlPlayer2.specialPower:
                    if started:
                        keyCombination += ' + ' + Key.getKeyLabel(key)
                    else:
                        keyCombination += Key.getKeyLabel(key)
                        started = True
            Text.renderLabel(keyCombination, 'white', 'arial.ttf', 24, self.currentDisplayWidth - 55, 450, 'topright', self.display)

            # Listen for button clicked
            if mousebuttonupTriggered:
                if buttonBack.mouseInBonudaries():
                    self.configureKeyId = None
                    self.gameOptions()
                elif buttonDefaults.mouseInBonudaries():
                    # Player controls
                    if self.configuredPlayer == 1:
                        Option.controlPlayer1 = Option.Control(pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_l, pygame.K_i, pygame.K_o)
                    elif self.configuredPlayer == 2:
                        Option.controlPlayer2 = Option.Control(pygame.K_r, pygame.K_f, pygame.K_d, pygame.K_g, pygame.K_x, pygame.K_a, pygame.K_s)
                elif self.configureKeyId == None:
                    if buttonMoveUp.mouseInBonudaries():
                        self.configureKeyId = 1
                    if buttonMoveDown.mouseInBonudaries():
                        self.configureKeyId = 2
                    if buttonMoveLeft.mouseInBonudaries():
                        self.configureKeyId = 3
                    if buttonMoveRight.mouseInBonudaries():
                        self.configureKeyId = 4
                    if buttonJump.mouseInBonudaries():
                        self.configureKeyId = 5
                    if buttonPrimaryBasicAttack.mouseInBonudaries():
                        self.configureKeyId = 6
                    if buttonSecondaryBasicAttack.mouseInBonudaries():
                        self.configureKeyId = 7
            if keydownTriggered:
                if self.configureKeyId != None:
                    if self.configureKeyId == 1:
                        if self.configuredPlayer == 1:
                            if not Option.keyIsRepeated(keydownValue):
                                Option.controlPlayer1.moveUp = keydownValue
                                Option.controlPlayer1.updateBasicSpecialPower()
                            self.configureKeyId = None
                        elif self.configuredPlayer == 2:
                            if not Option.keyIsRepeated(keydownValue):
                                Option.controlPlayer2.moveUp = keydownValue
                                Option.controlPlayer2.updateBasicSpecialPower()
                            self.configureKeyId = None
                    if self.configureKeyId == 2:
                        if self.configuredPlayer == 1:
                            if not Option.keyIsRepeated(keydownValue):
                                Option.controlPlayer1.moveDown = keydownValue
                                Option.controlPlayer1.updateBasicSpecialPower()
                            self.configureKeyId = None
                        elif self.configuredPlayer == 2:
                            if not Option.keyIsRepeated(keydownValue):
                                Option.controlPlayer2.moveDown = keydownValue
                                Option.controlPlayer2.updateBasicSpecialPower()
                            self.configureKeyId = None
                    if self.configureKeyId == 3:
                        if self.configuredPlayer == 1:
                            if not Option.keyIsRepeated(keydownValue):
                                Option.controlPlayer1.moveLeft = keydownValue
                                Option.controlPlayer1.updateBasicSpecialPower()
                            self.configureKeyId = None
                        elif self.configuredPlayer == 2:
                            if not Option.keyIsRepeated(keydownValue):
                                Option.controlPlayer2.moveLeft = keydownValue
                                Option.controlPlayer2.updateBasicSpecialPower()
                            self.configureKeyId = None
                    if self.configureKeyId == 4:
                        if self.configuredPlayer == 1:
                            if not Option.keyIsRepeated(keydownValue):
                                Option.controlPlayer1.moveRight = keydownValue
                                Option.controlPlayer1.updateBasicSpecialPower()
                            self.configureKeyId = None
                        elif self.configuredPlayer == 2:
                            if not Option.keyIsRepeated(keydownValue):
                                Option.controlPlayer2.moveRight = keydownValue
                                Option.controlPlayer2.updateBasicSpecialPower()
                            self.configureKeyId = None
                    if self.configureKeyId == 5:
                        if self.configuredPlayer == 1:
                            if not Option.keyIsRepeated(keydownValue):
                                Option.controlPlayer1.jump = keydownValue
                                Option.controlPlayer1.updateBasicSpecialPower()
                            self.configureKeyId = None
                        elif self.configuredPlayer == 2:
                            if not Option.keyIsRepeated(keydownValue):
                                Option.controlPlayer2.jump = keydownValue
                                Option.controlPlayer2.updateBasicSpecialPower()
                            self.configureKeyId = None
                    if self.configureKeyId == 6:
                        if self.configuredPlayer == 1:
                            if not Option.keyIsRepeated(keydownValue):
                                Option.controlPlayer1.primaryBasicAttack = keydownValue
                                Option.controlPlayer1.updateBasicSpecialPower()
                            self.configureKeyId = None
                        elif self.configuredPlayer == 2:
                            if not Option.keyIsRepeated(keydownValue):
                                Option.controlPlayer2.primaryBasicAttack = keydownValue
                                Option.controlPlayer2.updateBasicSpecialPower()
                            self.configureKeyId = None
                    if self.configureKeyId == 7:
                        if self.configuredPlayer == 1:
                            if not Option.keyIsRepeated(keydownValue):
                                Option.controlPlayer1.secondaryBasicAttack = keydownValue
                                Option.controlPlayer1.updateBasicSpecialPower()
                            self.configureKeyId = None
                        elif self.configuredPlayer == 2:
                            if not Option.keyIsRepeated(keydownValue):
                                Option.controlPlayer2.secondaryBasicAttack = keydownValue
                                Option.controlPlayer2.updateBasicSpecialPower()
                            self.configureKeyId = None
                    
            # Refresh
            pygame.display.update()
            self.clock.tick(20)

    def gameOptions(self):
        while True:
            # Analize events
            mousebuttonupTriggered = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    mousebuttonupTriggered = True

            # Draw background
            self.display.fill(Color.white)
            pygame.draw.rect(self.display, Color.black, (20, 20, self.currentDisplayWidth - 40, self.currentDisplayHeight - 40))

            # Draw menu content
            buttonBack = Button('Regresar', 'white', 'dolphins.ttf', 20, Color.black, Color.brightOrange, 30, 30, 150, 30, self.display)

            buttonDefaults = Button('Reestablecer', 'white', 'dolphins.ttf', 20, Color.black, Color.brightOrange, self.currentDisplayWidth - 180, 30, 150, 30, self.display)

            Text.renderLabel('Opciones', 'white', 'dolphins.ttf', 70, self.currentDisplayWidth / 2, 100, '', self.display)

            Text.renderLabel('Pantalla completa', 'white', 'dolphins.ttf', 36, 50, 200, 'topleft', self.display)
            togglerFullscreen = Option.Toggler('Sí', 'No', 'white', 'dolphins.ttf', 36, Color.black, Color.brightOrange, self.currentDisplayWidth - 200, 200, 150, 30, Option.fullscreen, self.display)

            Text.renderLabel('Volumen', 'white', 'dolphins.ttf', 36, 50, 275, 'topleft', self.display)
            numericUpDownVolume = Option.NumericUpDown(str(int(Option.volume * 100)) + '%', 'white', 'dolphins.ttf', 36, Color.brightRed, Color.red, self.currentDisplayWidth - 205, 275, 30, self.display)

            Text.renderLabel('Tiempo límite', 'white', 'dolphins.ttf', 36, 50, 350, 'topleft', self.display)
            numericUpDownTimeLimit = Option.NumericUpDown(str(Option.timeLimit), 'white', 'dolphins.ttf', 36, Color.brightRed, Color.red, self.currentDisplayWidth - 205, 350, 30, self.display)

            Text.renderLabel('Número de rounds', 'white', 'dolphins.ttf', 36, 50, 425, 'topleft', self.display)
            numericUpDownRounds = Option.NumericUpDown(str(Option.rounds), 'white', 'dolphins.ttf', 36, Color.brightRed, Color.red, self.currentDisplayWidth - 205, 425, 30, self.display)

            Text.renderLabel('Controles Jugador 1', 'white', 'dolphins.ttf', 36, 50, 500, 'topleft', self.display)
            buttonConfigurePlayer1 = Button('Configurar', 'white', 'dolphins.ttf', 36, Color.black, Color.blue, self.currentDisplayWidth - 245, 500, 200, 50, self.display)

            Text.renderLabel('Controles Jugador 2', 'white', 'dolphins.ttf', 36, 50, 575, 'topleft', self.display)
            buttonConfigurePlayer2 = Button('Configurar', 'white', 'dolphins.ttf', 36, Color.black, Color.blue, self.currentDisplayWidth - 245, 575, 200, 50, self.display)

            # Listen for button clicked
            if mousebuttonupTriggered:
                if buttonBack.mouseInBonudaries():
                    self.gameMenu()
                elif buttonDefaults.mouseInBonudaries():
                    # Fullscreen
                    Option.fullscreen = False
                    self.currentDisplayWidth = self.defaultDisplayWidth
                    self.currentDisplayHeight = self.defaultDisplayHeight
                    pygame.display.set_mode((self.currentDisplayWidth, self.currentDisplayHeight))
                    # Volume
                    Option.volume = 0.50
                    Music.setVolume(Option.volume)
                    # Time limit                    
                    Option.timeLimit = 180
                    # Rounds
                    Option.rounds = 3
                elif togglerFullscreen.mouseInBonudaries():
                    Option.fullscreen = not Option.fullscreen
                    if Option.fullscreen:
                        self.currentDisplayWidth = self.monitorScreenWidth
                        self.currentDisplayHeight = self.monitorScreenHeight
                        pygame.display.set_mode((self.currentDisplayWidth, self.currentDisplayHeight), pygame.FULLSCREEN)
                    else:
                        self.currentDisplayWidth = self.defaultDisplayWidth
                        self.currentDisplayHeight = self.defaultDisplayHeight
                        pygame.display.set_mode((self.currentDisplayWidth, self.currentDisplayHeight))
                elif numericUpDownVolume.mouseAboveLeftArrow():
                    if round(Option.volume, 2) >= 0.05:
                        Option.volume -= 0.05
                        Music.setVolume(Option.volume)
                elif numericUpDownVolume.mouseAboveRightArrow():
                    if round(Option.volume, 2) <= 0.95:
                        Option.volume += 0.05
                        Music.setVolume(Option.volume)
                elif numericUpDownTimeLimit.mouseAboveLeftArrow():
                    if int(Option.timeLimit) >= 45:
                        Option.timeLimit = str(int(Option.timeLimit) - 15)
                elif numericUpDownTimeLimit.mouseAboveRightArrow():
                    if int(Option.timeLimit) <= 165:
                        Option.timeLimit = str(int(Option.timeLimit) + 15)
                elif numericUpDownRounds.mouseAboveLeftArrow():
                    if int(Option.rounds) >= 2:
                        Option.rounds = str(int(Option.rounds) - 1)
                elif numericUpDownRounds.mouseAboveRightArrow():
                    if int(Option.rounds) <= 4:
                        Option.rounds = str(int(Option.rounds) + 1)
                elif buttonConfigurePlayer1.mouseInBonudaries():
                    self.configuredPlayer = 1
                    self.gameConfigurePlayer()
                elif buttonConfigurePlayer2.mouseInBonudaries():
                    self.configuredPlayer = 2
                    self.gameConfigurePlayer()

            # Refresh
            pygame.display.update()
            self.clock.tick(20)