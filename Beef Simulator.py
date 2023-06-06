""" Beef Simulator

        please read this from top to bottom, skipping around may prove confusing


    * play as ufo, move around above planet surface
    * Use tractor beam to abduct cows for points
    * tractor beam pulls up cows gradually, using momentum
    * army tanks shoot at you, you lose health if hit
    * use secondary button to fire back at them for (less) points
    * if you accidentally hit a cow, you lose health
    * if you accidentally abduct an army tank, you lose health
    * abducting cows also heals you a small amount
    * health counts down instead of subtracting all at once, so you always have a chance to abduct a cow before it hits 0
    

    
"""

# imprts all systems to be used in the game engine and otherwise
import pygame, sceneEngine, spriteEngine, uiEngine, random, math, sys

#initiates the game
pygame.init()

# this is a list of global variables that get shared from all game object classes, I will list out their functions:
# status - the message at the top of the screen
# score - points accumulated by player, displayed in top left
# fuel - health in the top left, counts down to master health 1 by 1, game ends if it reaches 0. Doesn't count 1 by 1 if fuel is increased
# level - used for managing what spawns. Level 1: just cow Level 2: just enemy Level 3: cow and enemy Level: 4 two cows and two enemies
# masterFuel - tracks damage taken. If masterFuel is 1000 and player takes 250 damage, masterFuel is now 750, and fuel will count down from 1000 until it reaches 750
# reset - bool that resets the cows and enemies
# beam - bool that tells classes if space is being pressed without having to apply key input to every class
# speed - controls how fast cows and enemies move left and right, increases after score is 2000 and increases more every 1000 points infinitely
d = {'status' : "Press space to abduct cows", 'score' : 0, 'fuel' : 1000, 'level' : 1, 'masterFuel' : 1000, 'reset' : False, 'beam' : False, 'speed' : 5}

# colours for future reference
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)



# everything from this 5 layer '#' wall is directly related to scene engine
# for a general break down, it defines two custom sprite classes with physics that all classes/objects in the game will use
# a scene engine controlling the screen and refreshing the sprites every frame
# some various ui functions such as a label, button, multilabel, and slider, which put text on screen
# skip to next '#' wall please
##########################################################################
##########################################################################
##########################################################################
##########################################################################
##########################################################################
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
        #right here
        
        self.mainSprites = pygame.sprite.OrderedUpdates(self.sprites)
        self.groups.append(self.mainSprites)
        
        self.screen.blit(self.background, (0, 0))
        text = font.render(d['status'], True, WHITE, BLACK)
        display_surface.blit(text, textRect)
        #text2 = font.render("dx: %.2f, dy: %.2f" % (self.ufo.dx, self.ufo.dy), True, WHITE, BLACK)
        #display_surface.blit(text2, text2Rect)
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

class BasicSprite(pygame.sprite.Sprite):
    """ use this sprite when you want to 
        directly control the sprite with dx and dy
        or want to extend in another direction than DirSprite
    """
    def __init__(self, scene):
        pygame.sprite.Sprite.__init__(self)
        self.screen = scene.screen
        self.image = pygame.Surface((25, 25))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.x = 100
        self.y = 100
        self.dx = 0
        self.dy = 0

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.checkBounds()
        self.rect.center = (self.x, self.y)
        
    def checkBounds(self):
        scrWidth = self.screen.get_width()
        scrHeight = self.screen.get_height()
        
        if self.x > scrWidth:
            self.x = 0
        if self.x < 0:
            self.x = scrWidth
        if self.y > scrHeight:
            self.y = 0
        if self.y < 0:
            self.y = scrHeight

class SuperSprite(pygame.sprite.Sprite):
    """ An enhanced Sprite class
        expects a gameEngine.Scene class as its one parameter
        Use methods to change image, direction, speed
        Will automatically travel in direction and speed indicated
        Automatically rotates to point in indicated direction
        Five kinds of boundary collision
    """

    def __init__(self, scene):
        pygame.sprite.Sprite.__init__(self)
        self.scene = scene
        self.screen = scene.screen
        
        #create constants
        self.WRAP = 0
        self.BOUNCE = 1
        self.STOP = 2
        self.HIDE = 3
        self.CONTINUE = 4
        
        #create a default text image as a placeholder
        #This will usually be changed by a setImage call
        self.font = pygame.font.Font("freesansbold.ttf", 30)
        self.imageMaster = self.font.render(">sprite>", True, (0, 0,0), (0xFF, 0xFF, 0xFF))
        self.image = self.imageMaster
        self.rect = self.image.get_rect()
        
        #create properties
        #most will be changed through method calls
        self.x = 200
        self.y = 200
        self.dx = 0
        self.dy = 0
        self.dir = 0
        self.rotation = 0
        self.speed = 0
        self.maxSpeed = 10
        self.minSpeed = -3
        self.boundAction = self.WRAP
        self.pressed = False
        self.oldCenter = (100, 100)
    
    def update(self):
        self.oldCenter = self.rect.center
        self.checkEvents()
        self.__rotate()
        self.__calcVector()
        self.__calcPosition()
        self.checkBounds()
        self.rect.center = (self.x, self.y)
    
    def checkEvents(self):
        """ overwrite this method to add your own event code """
        pass

    def __rotate(self):
        """ PRIVATE METHOD
            change visual orientation based on 
            rotation property.
            automatically called in update.
            change rotation property directly or with 
            rotateBy(), setAngle() methods
        """
        oldCenter = self.rect.center
        self.oldCenter = oldCenter
        self.image = pygame.transform.rotate(self.imageMaster, self.rotation)
        self.rect = self.image.get_rect()
        self.rect.center = oldCenter
    
    def __calcVector(self):
        """ calculates dx and dy based on speed, dir
            automatically called in update() 
        """
        theta = self.dir / 180.0 * math.pi
        self.dx = math.cos(theta) * self.speed
        self.dy = math.sin(theta) * self.speed
        self.dy *= -1
    
    def __calcPosition(self):
        """ calculates the sprites position adding
            dx and dy to x and y.
            automatically called in update()
        """
        self.x += self.dx
        self.y += self.dy

    def checkBounds(self):
        """ checks boundary and acts based on 
            self.BoundAction.
            WRAP: wrap around screen (default)
            BOUNCE: bounce off screen
            STOP: stop at edge of screen
            HIDE: move off stage and wait
            CONTINUE: keep going at present course and speed
            
            automatically called by update()
        """
        
        scrWidth = self.screen.get_width()
        scrHeight = self.screen.get_height()
        
        #create variables to simplify checking
        offRight = offLeft = offTop = offBottom = offScreen = False
        
        if self.x > scrWidth:
            offRight = True
        if self.x < 0:
            offLeft = True
        if self.y > scrHeight:
            offBottom = True
        if self.y < 0:
            offTop = True
            
        if offRight or offLeft or offTop or offBottom:
            offScreen = True
        
        if self.boundAction == self.WRAP:
            if offRight:
                self.x = 0
            if offLeft:
                self.x = scrWidth
            if offBottom:
                self.y = 0
            if offTop:
                self.y = scrHeight
        
        elif self.boundAction == self.BOUNCE:
            if offLeft or offRight:
                self.dx *= -1
            if offTop or offBottom:
                self.dy *= -1
                
            self.updateVector()
            self.rotation = self.dir
        
        elif self.boundAction == self.STOP:
            if offScreen:
                self.speed = 0
        
        elif self.boundAction == self.HIDE:
            if offScreen:
                self.speed = 0
                self.setPosition((-1000, -1000))
        
        elif self.boundAction == self.CONTINUE:
            pass
            
        else:
            # assume it's CONTINUE - keep going forever
            pass    
    
    def setSpeed(self, speed):
        """ immediately sets the objects speed to the 
            given value.
        """
        self.speed = speed

    def speedUp(self, amount):
        """ changes speed by the given amount
            Use a negative value to slow down
        """
        self.speed += amount
        if self.speed < self.minSpeed:
            self.speed = self.minSpeed
        if self.speed > self.maxSpeed:
            self.speed = self.maxSpeed
    
    def setAngle(self, dir):
        """ sets both the direction of motion 
            and visual rotation to the given angle
            If you want to set one or the other, 
            set them directly. Angle measured in degrees
        """            
        self.dir = dir
        self.rotation = dir
    
    def turnBy (self, amt):
        """ turn by given number of degrees. Changes
            both motion and visual rotation. Positive is
            counter-clockwise, negative is clockwise 
        """
        self.dir += amt
        if self.dir > 360:
            self.dir = amt
        if self.dir < 0:
            self.dir = 360 - amt
        self.rotation = self.dir
    
    def rotateBy(self, amt):
        """ change visual orientation by given
            number of degrees. Does not change direction
            of travel. 
        """
        self.rotation += amt
        if self.rotation > 360:
            self.rotation = amt
        if self.rotation < 0:
            self.rotation = 360 - amt
    
    def setImage (self, image):
        """ loads the given file name as the master image
            default setting should be facing east.  Image
            will be rotated automatically """
        self.imageMaster = pygame.image.load(image)
        self.imageMaster = self.imageMaster.convert()
    
    def setDX(self, dx):
        """ changes dx value and updates vector """
        self.dx = dx
        self.updateVector()
    
    def addDX(self, amt):
        """ adds amt to dx, updates vector """
        self.dx += amt
        self.updateVector()
        
    def setDY(self, dy):
        """ changes dy value and updates vector """
        self.dy = dy
        self.updateVector()

    def addDY(self, amt):
        """ adds amt to dy and updates vector """
        self.dy += amt
        self.updateVector()
    
    def setComponents(self, components):
        """ expects (dx, dy) for components
            change speed and angle according to dx, dy values """
            
        (self.dx, self.dy) = components
        self.updateVector()
        
    def setBoundAction (self, action):
        """ sets action for boundary.  Values are
            self.WRAP (wrap around edge - default)
            self.BOUNCE (bounce off screen changing direction)
            self.STOP (stop at edge of screen)
            self.HIDE (move off-stage and stop)
            self.CONTINUE (move on forever)
            Any other value allows the sprite to move on forever
        """
        self.boundAction = action

    def setPosition (self, position):
        """ place the sprite directly at the given position
            expects an (x, y) tuple
        """
        (self.x, self.y) = position
        
    def moveBy (self, vector):
        """ move the sprite by the (dx, dy) values in vector
            automatically calls checkBounds. Doesn't change 
            speed or angle settings.
        """
        (dx, dy) = vector
        self.x += dx
        self.y += dy
        self.__checkBounds()

    def forward(self, amt):
        """ move amt pixels in the current direction
            of travel
        """
        
        #calculate dx dy based on current direction
        radians = self.dir * math.pi / 180
        dx = amt * math.cos(radians)
        dy = amt * math.sin(radians) * -1
        
        self.x += dx
        self.y += dy
        
    def addForce(self, amt, angle):
        """ apply amt of thrust in angle.
            change speed and dir accordingly
            add a force straight down to simulate gravity
            in rotation direction to simulate spacecraft thrust
            in dir direction to accelerate forward
            at an angle for retro-rockets, etc.
        """

        #calculate dx dy based on angle
        radians = angle * math.pi / 180
        dx = amt * math.cos(radians)
        dy = amt * math.sin(radians) * -1
        
        self.dx += dx
        self.dy += dy
        self.updateVector()
        
    def updateVector(self):
        #calculate new speed and angle based on dx, dy
        #call this any time you change dx or dy
        
        self.speed = math.sqrt((self.dx * self.dx) + (self.dy * self.dy))
        
        dy = self.dy * -1
        dx = self.dx
        
        radians = math.atan2(dy, dx)
        self.dir = radians / math.pi * 180

    def setSpeedLimits(self, max, min):
        """ determines maximum and minimum
            speeds you will allow through
            speedUp() method.  You can still
            directly set any speed you want
            with setSpeed() Default values:
                max: 10
                min: -3
        """
        self.maxSpeed = max
        self.minSpeed = min

    def dataTrace(self):
        """ utility method for debugging
            print major properties
            extend to add your own properties
        """
        
            
    def mouseDown(self):
        """ boolean function. Returns True if the mouse is 
            clicked over the sprite, False otherwise
        """
        self.pressed = False
        if pygame.mouse.get_pressed() == (1, 0, 0):
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.pressed = True
        return self.pressed
    
    def clicked(self):
        """ Boolean function. Returns True only if mouse
            is pressed and released over sprite
            
        """
        released = False
        if self.pressed:
            if pygame.mouse.get_pressed() == (0, 0, 0):
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    released = True
            return released
        
    def collidesWith(self, target):
        """ boolean function. Returns True if the sprite
            is currently colliding with the target sprite,
            False otherwise
        """
        collision = False
        if self.rect.colliderect(target.rect):
            collision = True
        return collision
    
    def collidesGroup(self, target):
        """ wrapper for pygame.sprite.spritecollideany() function
            simplifies checking sprite - group collisions
            returns result of collision check (sprite from group 
            that was hit or None)
        """
        collision = pygame.sprite.spritecollideany(self, target)
        return collision
        
    def distanceTo(self, point):
        """ returns distance to any point in pixels
            can be used in circular collision detection
        """
        (pointx, pointy) = point
        dx = self.x - pointx
        dy = self.y - pointy
        
        dist = math.sqrt((dx * dx) + (dy * dy))
        return dist
    
    def dirTo(self, point):
        """ returns direction (in degrees) to 
            a point """
        
        (pointx, pointy) = point
        dx = self.x - pointx
        dy = self.y - pointy
        dy *= -1
        
        radians = math.atan2(dy, dx)
        dir = radians * 180 / math.pi
        dir += 180
        return dir
    
    def drawTrace(self, color=(0x00, 0x00, 0x00)):
        """ traces a line between previous position
            and current position of object 
        """
        pygame.draw.line(self.scene.background, color, self.oldCenter,
                         self.rect.center, 3)
        self.screen.blit(self.scene.background, (0, 0))
    


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

############################################################################
############################################################################
############################################################################
############################################################################
############################################################################
# everything from this point forward has to do with the game logic
        

# this appears briefly to refresh the black behind the text since I couldn't figure out the ui system above in time to complete this
class BlackBox(spriteEngine.SuperSprite):
    def __init__(self, scene):
        spriteEngine.SuperSprite.__init__(self,scene)
        self.setImage("BlackBox.gif")
        self.x = 0
        self.y = -300

    prevStatus = "null"
    # checks for a multitude of situations when the text might leave artifacts, and quickly moves the black box on top of it for a frame to clean it up
    def checkEvents(self):
        if self.prevStatus == d['status'] and d['fuel'] != 999 and d['fuel'] != 998 and d['fuel'] != 997 and d['fuel'] != 99  and d['fuel'] != 98  and d['fuel'] != 97 and d['fuel'] != 9:
            self.y = -900
            self.x -900
        else:
            self.y = 0
            self.x = 0
            self.prevStatus = d['status']


# the white dot shot by both armedship1 and armedship2
class Bullet(spriteEngine.SuperSprite):
    def __init__(self, scene):
        spriteEngine.SuperSprite.__init__(self,scene)
        self.setImage("bullet.gif")
        self.x = 300
        self.y = 300
        # bool for if bullet is active
        self.shooting = False
        self.xStart = 0
        self.yStart = 0

    def checkEvents(self):
        #resets
        if d['reset']:
            self.shooting = False
        
        if self.shooting :

            self.y -= 10
            
        else:

            self.x = -900
            self.y = -900

        if self.y < 0:

            self.shooting = 0
    # gets x and y positions from game class to start from respective shooter
    # activates bullet as hitbox
    def shoot(self):
        self.x = self.xStart
        self.y = self.yStart
        self.shooting = True


# the player, this is the script that moves it around
class UFO(spriteEngine.SuperSprite):
    def __init__(self, scene):
        spriteEngine.SuperSprite.__init__(self, scene)
        # sets physics limits
        self.thrust = .5
        self.maxThrust = 6
        self.setImage("ufoship2.gif")
        self.setAngle(0)
        # bool for when space is pressed
        self.beam = False
        self.x = self.screen.get_width() / 2
        self.y = self.screen.get_height() /2
        

    def checkEvents(self):

        # sets boundaries on top and bottom of playable area, bounces player back
        if self.y < 80:
            self.dy = -self.dy
            self.y = 81

        if self.y > 320:
            self.dy = -self.dy
            self.y = 319
        
        self.checkKeys()

    # checks for input
    def checkKeys(self):
        keys = pygame.key.get_pressed()

        # tells all classes when tractor beam is in use
        if keys[pygame.K_SPACE]:
            
            self.beam = True
            d['beam'] = True
        
        else:

            self.beam = False

        # moves player around using dx and dy momentum variables from the supersprite class
        # added a clause that slows the ship to an eventual hault when no keys are pressed
        if keys[pygame.K_UP] and self.dy > -self.maxThrust and self.beam == False:
            self.dy -= self.thrust

        elif keys[pygame.K_DOWN] and self.dy < self.maxThrust and self.beam == False:
            self.dy += self.thrust
        else:
            if self.dy > 1:
                self.dy -= 0.2
            elif self.dy < -1:
                self.dy += 0.2
            else:
                self.dy = 0
            
            
        # same as above
        if keys[pygame.K_RIGHT] and self.dx < self.maxThrust and self.beam == False:
            self.dx += self.thrust
            
            
        elif keys[pygame.K_LEFT] and self.dx > -self.maxThrust and self.beam == False:
            self.dx -= self.thrust

        else:
            if self.dx > 1:
                self.dx -= 0.2
            elif self.dx < -1:
                self.dx += 0.2
            else:
                self.dx = 0
            
        # updates movement
        self.updateVector()

# the image for the planet at the bottom of the screen
class Planet(spriteEngine.SuperSprite):

    def __init__(self, scene):
        spriteEngine.SuperSprite.__init__(self, scene)
        self.setImage("planet.gif")
        self.x = 300
        self.y = (self.screen.get_height() / 1.1)



# cow1 that you abduct
class Cow(spriteEngine.SuperSprite):

    def __init__(self, scene):
        spriteEngine.SuperSprite.__init__(self, scene)
        self.setImage("cow2.gif")
        self.x = 300
        self.y = (self.screen.get_height() / 1.2)
        # used for determining if on ground
        self.grounded = True
        # which direction the cow is  mooving
        self.direction = "right"
        # used to track if in the tractor beam
        self.beaming = False
        # used for randomizing which direction the cow moves upon reset
        self.rand = 0

    def checkEvents(self):
        # doesn't spawn in level 2 for tutorial purposes
        if d['level'] == 2:
            self.x = -300
            self.y = -300
            self.dx = 0
            self.dy = 0
        else:
            # if cow on ground, move left and right and bounce on screen
            if self.grounded:
                if self.direction == "right":
                    self.x += d['speed']
                else:
                    self.x -= d['speed']

                if self.x > self.screen.get_width():
                    self.x = self.screen.get_width() - 1
                    self.direction = "left"

                if self.x < 0:
                    self.x = 1
                    self.direction = "right"

            # if not on ground, determine if being beamed up, falling to the ground, or already below the ground, and move accordingly
            else:

                if self.beaming and d['beam'] == True:
                    
                    self.dy -= 1
                    if self.y > 401:
                        self.dy = 0
                        self.y = 400
                else:
                    if self.y < 390:
                        self.dy += 2
                    else:
                        self.y = (self.screen.get_height() / 1.2)
                        self.dy = 0
                        self.grounded = True
                        self.beaming = False
        # update movement
        self.updateVector()

    # sets cow to a random x position on the ground moving a random direction
    # also resets its variables
    def reset(self):

        self.rand = random.randint(0, 1)
        if self.rand == 0:
            self.direction = "left"
        else:
            self.direction = "right"

        self.x = random.randint(0, self.screen.get_width())

        self.y = (self.screen.get_height() / 1.2)
        self.dy = 0
        self.grounded = True
        self.beaming = False

# same thing as cow1 but doesn't spawn till level 4
class Cow2(spriteEngine.SuperSprite):

    def __init__(self, scene):
        spriteEngine.SuperSprite.__init__(self, scene)
        self.setImage("cow2.gif")
        self.x = 300
        self.y = (self.screen.get_height() / 1.2)
        self.grounded = True
        self.direction = "right"
        self.beaming = False
        self.rand = 0

    def checkEvents(self):

        # doesn't spawn until level 4
        if d['level'] < 4:
            self.x = -300
            self.y = -300
            self.dx = 0
            self.dy = 0
        else:

            if self.grounded:
                if self.direction == "right":
                    self.x += d['speed']
                else:
                    self.x -= d['speed']

                if self.x > self.screen.get_width():
                    self.x = self.screen.get_width() - 1
                    self.direction = "left"

                if self.x < 0:
                    self.x = 1
                    self.direction = "right"

            else:

                if self.beaming and d['beam'] == True:
                    #self.y -= 5
                    self.dy -= 1
                    if self.y > 401:
                        self.dy = 0
                        self.y = 400
                    
                else:
                   
                    if self.y < 390:
                        #self.y += 10
                        self.dy += 2
                    else:
                        self.y = (self.screen.get_height() / 1.2)
                        self.dy = 0
                        self.grounded = True
                        self.beaming = False

        self.updateVector()

    def reset(self):

        self.rand = random.randint(0, 1)
        if self.rand == 0:
            self.direction = "left"
        else:
            self.direction = "right"

        self.x = random.randint(0, self.screen.get_width())

        self.y = (self.screen.get_height() / 1.2)
        self.dy = 0
        self.grounded = True
        self.beaming = False

# the tracor beam
class Beam(spriteEngine.SuperSprite):

    def __init__(self, scene):
        spriteEngine.SuperSprite.__init__(self, scene)
        self.setImage("whitewall.gif")
        self.x = 300
        self.y = (self.screen.get_height() / 2)
        # used for tracking ufo position
        self.xNeo = 0
        self.yNeo = 0
        # used for shaking effect
        self.shake = 0
        self.speed = 2
        
            
    def checkEvents(self):
        self.checkKeys()

    def checkKeys(self):
        keys = pygame.key.get_pressed()

        # makes beam disapear, cause I couldn't figure out how to append sprites to the sprites list in time
        if keys[pygame.K_SPACE]:
            self.setImage("whitewall.gif")
        else:
            self.setImage("BlackBox.gif")
            self.x = -300
            self.y = -300

    def setPos(self):

        # randomly selects a number to determine if it's above the position, above and to the left, above and to the right, below and to the right, etc.
        # when rapidly randomizing position around the position it's supposed to be gives the beam an energy-like effect
        shake = random.randint(0, 8)
        if shake == 0:
            self.x = self.xNeo
            self.y = self.yNeo
        elif shake == 1:
            self.x = self.xNeo + self.speed
            self.y = self.yNeo + self.speed
        elif shake == 2:
            self.x = self.xNeo
            self.y = self.yNeo + self.speed
        elif shake == 3:
            self.x = self.xNeo - self.speed
            self.y = self.yNeo + self.speed
        elif shake == 4:
            self.x = self.xNeo + self.speed
            self.y = self.yNeo
        elif shake == 5:
            self.x = self.xNeo - self.speed
            self.y = self.yNeo
        elif shake == 6:
            self.x = self.xNeo + self.speed
            self.y = self.yNeo - self.speed
        elif shake == 7:
            self.x = self.xNeo
            self.y = self.yNeo - self.speed
        elif shake == 8:
            self.x = self.xNeo - self.speed
            self.y = self.yNeo - self.speed

# enemy ship, is the same script as cows because they function the same way
# they don't appear on level 1, that's the only reason this is a separate script
# all other differences handled in the game class
class ArmedShip(spriteEngine.SuperSprite):

    def __init__(self, scene):
        spriteEngine.SuperSprite.__init__(self, scene)
        self.setImage("armedship.gif")
        self.grounded = True
        self.direction = "right"
        self.beaming = False
        self.rand = 0
        self.reset()

    def checkEvents(self):
        # doesn't spawn on level 1
        if d['level'] == 1:
            self.x = -300
            self.y = -300
            self.dx = 0
            self.dy = 0

        else:

            if self.grounded:
                if self.direction == "right":
                    self.x += d['speed']
                else:
                    self.x -= d['speed']

                if self.x > self.screen.get_width():
                    self.x = self.screen.get_width() - 1
                    self.direction = "left"

                if self.x < 0:
                    self.x = 1
                    self.direction = "right"

            else:

                if self.beaming and d['beam'] == True:
                    #self.y -= 5
                    self.dy -= 1
                    if self.y > 401:
                        self.dy = 0
                        self.y = 400
                    
                else:
                   
                    if self.y < 390:
                        #self.y += 10
                        self.dy += 2
                    else:
                        self.y = (self.screen.get_height() / 1.2)
                        self.dy = 0
                        self.grounded = True
                        self.beaming = False

        self.updateVector()

    def reset(self):
        self.rand = random.randint(0, 1)
        if self.rand == 0:
            self.x =  self.x = self.screen.get_width() - 1
            self.direction = "left"
        else:
            self.x = 1
            self.direction = "right"

        self.y = (self.screen.get_height() / 1.2)
        self.dy = 0
        self.grounded = True
        self.beaming = False

# see the first armed ship
class ArmedShip2(spriteEngine.SuperSprite):

    def __init__(self, scene):
        spriteEngine.SuperSprite.__init__(self, scene)
        self.setImage("armedship.gif")
        self.grounded = True
        self.direction = "right"
        self.beaming = False
        self.rand = 0
        self.reset()

    def checkEvents(self):
        # doesn't spawn till level 4
        if d['level'] < 4:
            self.x = -300
            self.y = -300
            self.dx = 0
            self.dy = 0

        else:

            if self.grounded:
                if self.direction == "right":
                    self.x += d['speed']
                else:
                    self.x -= d['speed']

                if self.x > self.screen.get_width():
                    self.x = self.screen.get_width() - 1
                    self.direction = "left"

                if self.x < 0:
                    self.x = 1
                    self.direction = "right"

            else:

                if self.beaming and d['beam'] == True:
                    #self.y -= 5
                    self.dy -= 1
                    if self.y > 401:
                        self.dy = 0
                        self.y = 400
                    
                else:
                   
                    if self.y < 390:
                        #self.y += 10
                        self.dy += 2
                    else:
                        self.y = (self.screen.get_height() / 1.2)
                        self.dy = 0
                        self.grounded = True
                        self.beaming = False

        self.updateVector()

    def reset(self):
        self.rand = random.randint(0, 1)
        if self.rand == 0:
            self.x =  self.x = self.screen.get_width() - 1
            self.direction = "left"
        else:
            self.x = 1
            self.direction = "right"

        self.y = (self.screen.get_height() / 1.2)
        self.dy = 0
        self.grounded = True
        self.beaming = False

# the bullet fired by the player
# is the same as the bullet class, but shoots down instead
class Bomb(spriteEngine.SuperSprite):
    
    def __init__(self, scene):
        spriteEngine.SuperSprite.__init__(self, scene)
        self.setImage("ufoshot.gif")
        self.x = self.screen.get_width() / 2
        self.y = self.screen.get_height() / 2
        self.shooting = False
        self.startpos = False
        self.xStart = 0
        self.yStart = 0
        
    def checkEvents(self):
    
        if self.y > 400:
            self.shooting = False
            self.startpos = False

        if self.shooting:
            self.y += 10
            self.setImage("ufoshot.gif")
        else:
            
            self.x = -300
            self.y =900
            
                
            
        self.checkKeys()
            
    def checkKeys(self):
        keys = pygame.key.get_pressed()


        if keys[pygame.K_c]:
            
            if self.shooting == False:
                self.startpos = True

    def shootMe(self):
        self.x = self.xStart
        self.y = self.yStart
        self.shooting = True
        self.startpos = False

        
    
# controls the game 
class Game(sceneEngine.Scene):
    def __init__(self):
        sceneEngine.Scene.__init__(self)
        self.setCaption("Lunar Lander - arrow key to begin")
        
        
       
        # all game objects: the backdrop, two cows, two armedships and their bullets, the ufo, its beam, and its bullet
        # also the black box for the ui
        self.blackbox = BlackBox(self)
        self.ufo = UFO(self)
        

        self.bullet = Bullet(self)
        self.bullet2 = Bullet(self)

        self.planet = Planet(self)
        
        self.cow = Cow(self)
        self.cow2 = Cow2(self)
        
        self.beam = Beam(self)
        
        self.armedship = ArmedShip(self)
        self.armedship2 = ArmedShip2(self)
        
        self.bomb = Bomb(self)

        self.sprites = [self.blackbox, self.planet, self.beam, self.ufo, self.cow, self.cow2, self.bomb, self.bullet, self.armedship, self.armedship2, self.bullet2]
        
        self.timer = 60

        self.speedTimer = 2000
    
    def update(self):

        # ups the speed every 1000 points after 2000
        if d['score'] > self.speedTimer:
            self.speedTimer += 1000
            d['speed'] += 1

        # resets everything after player takes damage
        # extra rules written for different levels
        if d['reset']:
            d['reset'] = False

            self.armedship.reset()
            self.armedship2.reset()
            self.cow.reset()
            if d['level'] == 4:
                self.cow2.reset()

        # moves things around for level change
        if d['score'] > 1000 and d['level'] == 3:
            d['level'] = 4
            self.cow2.reset()
            self.armedship2.reset()
        

        # makes bullet fire at player when armed ship within x range
        if self.bullet.shooting == False:
            if self.armedship.grounded and self.armedship.x > (self.ufo.x - 20) and self.armedship.x < (self.ufo.x + 20):
                self.bullet.xStart = self.armedship.x
                self.bullet.yStart = self.armedship.y
                self.bullet.shoot()

        # makes bullet2 fire at player when armed ship2 within x range
        if self.bullet2.shooting == False:
            if self.armedship2.grounded and self.armedship2.x > (self.ufo.x - 20) and self.armedship2.x < (self.ufo.x + 20):
                self.bullet2.xStart = self.armedship2.x
                self.bullet2.yStart = self.armedship2.y
                self.bullet2.shoot()
       
        # shoots the player bullet when space is pressed
        if self.bomb.startpos:
            self.bomb.xStart = self.ufo.x
            self.bomb.yStart = self.ufo.y
            self.bomb.shootMe()

        # fuel counts down 1 by 1 if masterFuel is less than it, game ends when it reaches 0
        # counting up doesn't count 1 by 1
        if d['fuel'] != d['masterFuel']:
            if d['fuel'] < d['masterFuel']:
                d['fuel'] = d['masterFuel']
            else:
                d['fuel'] -= 1

        if d['masterFuel'] < 1:
            d['masterFuel'] = 0

        if d['fuel'] < 1:
            d['reset'] = True
        

        if d['fuel'] < 1:
            print("Your score was " + str(d['score']))
            pygame.quit()

        # gives the beam coordinates for the ufo so it can move there
        # spawns beam
        if d['beam']:
            self.beam.xNeo = self.ufo.x
            self.beam.yNeo = self.ufo.y + 150
            self.beam.setPos()

        
        
    
        # checks when objects hit each other
        self.checkCollisions()
    

        # refreshes all ui text
        text = font.render(d['status'], True, WHITE, BLACK)
        display_surface.blit(text, textRect)
        
        text2 = font.render("Beef Sim by Jaime 'fox'", True, WHITE, BLACK)
        display_surface.blit(text2, text2Rect)
        text3 = font.render(("Health: " + str(d['fuel'])), True, WHITE, BLACK)
        display_surface.blit(text3, text3Rect)
        text4 = font.render(("Score: " + str(d['score'])), True, WHITE, BLACK)
        display_surface.blit(text4, text4Rect)
        
    def checkCollisions(self):
        #check possible collisions of every different object: (armedship & ufo) * 2, (ufoshot & armedship) * 2, (ufo & cow) * 2, and lastly (ufo & enemyshot) * 2
        if self.timer > 0:

            self.timer -= 1

        else:

            # when ufo hit by enemy bullet1, take damage and despawn {reset} all objects
            if self.ufo.collidesWith(self.bullet) and self.bullet.shooting == True:
                d['masterFuel'] -= 250
                d['reset'] = True
                self.bullet.shooting = False
                d['status'] = "You were shot"

            # when ufo hit by bullet2, same basic function as bullet1
            if self.ufo.collidesWith(self.bullet2) and self.bullet2.shooting == True:
                d['masterFuel'] -= 250
                d['reset'] = True
                self.bullet2.shooting = False
                d['status'] = "You were shot"

            # when cow collides with beam, cow is not grounded and in the beam
            if self.cow.collidesWith(self.beam) and self.ufo.beam == True:
                self.cow.grounded = False
                self.cow.beaming = True
            else:
                self.cow.beaming = False

            # when cow2 collides with tractor beam, do same as cow1
            if self.cow2.collidesWith(self.beam) and self.ufo.beam == True:
                self.cow2.grounded = False
                self.cow2.beaming = True
            else:
                self.cow2.beaming = False

            # when ufo collects cow, add health (fuel/ masterFuel) and point to score, resets the cow
            if self.ufo.collidesWith(self.cow):
                
                self.cow.reset()
                d['score'] += 100
                if d['masterFuel'] < 950:
                    d['masterFuel'] += 50
                else:
                    d['masterFuel'] = 1000

                if d['level'] == 1:
                    d['status'] = "Press C to shoot at military"
                    d['level'] = 2
                    self.armedship.reset()
                   
                else:
                    d['status'] = "Picked up a cow!"

            # when ufo collects cow2, do same as cow1
            if self.ufo.collidesWith(self.cow2):
                
                self.cow2.reset()
                d['score'] += 100
                if d['masterFuel'] < 950:
                    d['masterFuel'] += 50
                else:
                    d['masterFuel'] = 1000
    
                d['status'] = "Picked up a cow!"

            # when bomb hits cow, ufo takes damage and resets all objects
            if self.bomb.collidesWith(self.cow) and self.bomb.shooting:

                d['reset'] = True
                self.bomb.shooting = False
                d['masterFuel'] -= 250
                d['status'] = "Don't shoot cows!"

            # when bomb hits cow2, do same as when it hits cow1
            if self.bomb.collidesWith(self.cow2) and self.bomb.shooting:

                d['reset'] = True
                self.bomb.shooting = False
                d['masterFuel'] -= 250
                d['status'] = "Don't shoot cows!"
                
            # when enemyship hits tractor beam, enemyship is no longer grounded and beam bool is true
            if self.armedship.collidesWith(self.beam) and self.ufo.beam == True:
                self.armedship.grounded = False
                self.armedship.beaming = True
            else:
                self.armedship.beaming = False

            # when enemy2ship hits beam, do same as enemy1
            if self.armedship2.collidesWith(self.beam) and self.ufo.beam == True:
                self.armedship2.grounded = False
                self.armedship2.beaming = True
            else:
                self.armedship2.beaming = False

            # when ufo abducts enemy, hurt player
            if self.ufo.collidesWith(self.armedship):
                
                d['reset'] = True
                d['masterFuel'] -= 250
                d['status'] = "Don't pick up military vehicles!"


            # when ufo hits enemy2, hurt player
            if self.ufo.collidesWith(self.armedship2):
                
                d['reset'] = True
                d['masterFuel'] -= 250
                d['status'] = "Don't pick up military vehicles!"

            # when enemy hit by player's bullet, add to score and reset that enemy
            if self.bomb.collidesWith(self.armedship) and self.bomb.shooting:
                
                self.armedship.reset()
                self.bomb.shooting = False
                d['score'] += 50
                if d['level'] == 2:
                    d['level'] = 3
                    self.cow.reset()
                d['status'] = "Scratch one bogey!"

            # when enemy hit by player's bullet, add to score and reset that enemy
            if self.bomb.collidesWith(self.armedship2) and self.bomb.shooting:
                
                self.armedship2.reset()
                self.bomb.shooting = False
                d['score'] += 50
                d['status'] = "Scratch one bogey!"

            

        

                

    
# defines all ui text, width and height for reference, and all texts' rectangles
width = 600
height = 600

display_surface = pygame.display.set_mode((width, height ))

font = pygame.font.Font('freesansbold.ttf', 24)

# displays message text
text = font.render(d['status'], True, WHITE, BLACK)
textRect = text.get_rect()
textRect.center = (width // 1.7, height // 12)
# my title
text2 = font.render('Beef Sim by Jaime', True, WHITE, BLACK)
text2Rect = text2.get_rect()
text2Rect.center = (width // 1.8, height // 24)
# displays health
text3 = font.render('Health: ', True, WHITE, BLACK)
text3Rect = text3.get_rect()
text3Rect.center = (width // 15, height // 24)
# displays score
text4 = font.render('Score: ', True, WHITE, BLACK)
text4Rect = text4.get_rect()
text4Rect.center = (width // 15, height // 12)

# starts the game
def main():
    game = Game()
    game.start()
    
if __name__ == "__main__":
    main()
