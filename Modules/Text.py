import pygame
import os

class Text:
    @staticmethod
    def renderLabel(text, color, fontFamily, fontSize, x, y, align, display):
        font = pygame.font.Font('Resources/%s' % fontFamily, fontSize)
        label = font.render(text, True, pygame.Color(color))

        if align == 'topleft':
            labelRect = label.get_rect(topleft = (x, y))
        elif align == 'topright':
            labelRect = label.get_rect(topright = (x, y))
        else:
            labelRect = label.get_rect()
            labelRect.center = (x, y)

        display.blit(label, labelRect)