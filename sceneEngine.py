""" sceneEngine.py 
    modified from the gameEngine.py
    from Andy Harris, 2006
"""

import pygame, math, sys, spriteEngine
pygame.init()


    
class Scene(object):
    """ encapsulates the IDEA / ALTER framework
        properties:
        sprites - a list of sprite objects
            that forms the primary sprite group
        background - the background surface
        screen - the display screen
        
        it's generally best to add all sprites 
        as attributes, so they can have access
        to each other if needed    
    """
    
    def __init__(self):
        """ initialize the game engine
            set up a sample sprite for testing
        """
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480))
        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill((0, 0, 0))
        
        self.sampleSprite = spriteEngine.SuperSprite(self)
        self.sampleSprite.setSpeed(3)
        self.sampleSprite.setAngle(0)
        self.sampleSprite.boundAction = self.sampleSprite.WRAP
        self.sprites = [self.sampleSprite]
        self.groups = []
    
    def start(self):
        """ sets up the sprite groups
            begins the main loop
        """
        self.mainSprites = pygame.sprite.OrderedUpdates(self.sprites)
        self.groups.append(self.mainSprites)
        
        self.screen.blit(self.background, (0, 0))
        self.clock = pygame.time.Clock()
        self.keepGoing = True
        while self.keepGoing:
            self.__mainLoop()

    def stop(self):
        """stops the loop"""
        self.keepGoing = False
    
    def __mainLoop(self):
        """ manage all the main events 
            automatically called by start
        """
        self.clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keepGoing = False
                pygame.display.quit()
                pygame.quit()
                sys.exit()
            self.doEvents(event)
        
        self.update()
        for group in self.groups:
            group.clear(self.screen, self.background)
            group.update()
            group.draw(self.screen)
        
        pygame.display.flip()

    def makeSpriteGroup(self, sprites):
        """ create a group called groupName
            containing all the sprites in the sprites 
            list.  This group will be added after the 
            sprites group, and will automatically
            clear, update, and draw
        """
        tempGroup = pygame.sprite.OrderedUpdates(sprites)
        return tempGroup
    
    def addGroup(self, group):
        """ adds a sprite group to the groups list for
            automatic processing 
        """
        self.groups.append(group)

    def doEvents(self, event):
        """ overwrite this method to add your own events.
            Works like normal event handling, passes event
            object
        """
        pass
        
    def update(self):
        """ happens once per frame, after event parsing.
            Overwrite to add your own code, esp event handling
            that doesn't require event obj. (pygame.key.get_pressed, 
            pygame.mouse.get_pos, etc)
            Also a great place for collision detection
        """
        pass
    
    def setCaption(self, title):
        """ set's the scene's title text """
        pygame.display.set_caption(title)


if __name__ == "__main__":
    # change this code to test various features of the engine
    # This code will not run when gameEngine is run as a module
    # (as it usually will be
        
    game = Scene()
##    thing = SuperSprite(game)
##    thing.setSpeed(5)
##    thing.setBoundAction(thing.BOUNCE)
##    thing.setAngle(230)
##    game.sprites = [thing]
    
    game.start()
