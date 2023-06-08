""" uiEngine.py 
    modified from the gameEngine.py
    from Andy Harris, 2006
"""

import pygame, math, sys
pygame.init()


class Label(pygame.sprite.Sprite):
    """ a basic label 
        properties: 
            font: font to use
            text: text to display
            fgColor: foreground color
            bgColor: background color
            center: position of label's center
            size: (width, height) of label
    """
    
    def __init__(self, fontName = "freesansbold.ttf"):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(fontName, 20)
        self.text = ""
        self.fgColor = ((0x00, 0x00, 0x00))
        self.bgColor = ((0xFF, 0xFF, 0xFF))
        self.center = (100, 100)
        self.size = (150, 30)

    def update(self):
        self.image = pygame.Surface(self.size)
        self.image.fill(self.bgColor)
        fontSurface = self.font.render(self.text, True, self.fgColor, self.bgColor)
        #center the text
        xPos = (self.image.get_width() - fontSurface.get_width())/2
        
        self.image.blit(fontSurface, (xPos, 0))
        self.rect = self.image.get_rect()
        self.rect.center = self.center

class Button(Label):
    """ a button based on the label 
        same properties as label +
        active: True if user is clicking on sprite
                False if user is not currently clicking
        clicked: True when user releases mouse over a 
                 currently active button
    """

    def __init__(self):
        Label.__init__(self)
        self.active = False
        self.clicked = False
        self.bgColor = (0xCC, 0xCC, 0xCC)
    
    def update(self):
        Label.update(self)
        
        self.clicked = False

        #check for mouse input
        if pygame.mouse.get_pressed() == (1, 0, 0):
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.active = True

        #check for mouse release
        if self.active == True:
            if pygame.mouse.get_pressed() == (0, 0, 0):
                self.active = False
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    self.clicked = True

class Scroller(Button):
    """ like a button, but has a numeric value that 
        can be decremented by clicking on left half
        and incremented by clicking on right half.
        new atributes:
            value: the scroller's numeric value
            minValue: minimum value
            maxValue: maximum value
            increment: How much is added or subtracted
            format: format of string interpolation
    """
    
    def __init__(self):
        Button.__init__(self)
        self.minValue = 0
        self.maxValue = 10
        self.increment = 1
        self.value = 5
        self.format = "<<  %.2f  >>"
        
    def update(self):
        Button.update(self)
        if self.active:
            (mousex, mousey) = pygame.mouse.get_pos()
            if mousex < self.rect.centerx:
                self.value -= self.increment
                if self.value < self.minValue:
                    self.value = self.minValue
            else:
                self.value += self.increment
                if self.value > self.maxValue:
                    self.value = self.maxValue

        self.text = self.format % self.value

class MultiLabel(pygame.sprite.Sprite):
    """ accepts a list of strings, creates a multi-line
        label to display text 
        same properties as label except textLines
        is a list of strings. There is no text
        property.
        Set the size manually. Vertical size should be at 
        least 30 pixels per line (with the default font)
    """
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.textLines = ["This", "is", "sample", "text"]
        self.font = pygame.font.Font("freesansbold.ttf", 20)
        self.fgColor = ((0x00, 0x00, 0x00))
        self.bgColor = ((0xFF, 0xFF, 0xFF))
        self.center = (100, 100)
        self.size = (150, 100)
        
    def update(self):
        self.image = pygame.Surface(self.size)
        self.image.fill(self.bgColor)
        numLines = len(self.textLines)
        vSize = self.image.get_height() / numLines
        
        for lineNum in range(numLines):
            currentLine = self.textLines[lineNum]
            fontSurface = self.font.render(currentLine, True, self.fgColor, self.bgColor)
            #center the text
            xPos = (self.image.get_width() - fontSurface.get_width())/2
            yPos = lineNum * vSize
            self.image.blit(fontSurface, (xPos, yPos))
        
        self.rect = self.image.get_rect()
        self.rect.center = self.center

if __name__ == "__main__":
    # change this code to test various features of the engine
    # This code will not run when gameEngine is run as a module
    # (as it usually will be
        
    game = Scene()
    thing = SuperSprite(game)
    thing.setSpeed(5)
    thing.setBoundAction(thing.BOUNCE)
    thing.setAngle(230)
    game.sprites = [thing]
    
    game.start()
