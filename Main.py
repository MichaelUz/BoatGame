import pygame
import random
import sys
import math
import time
import os

from pygame.locals import*
# Set frame rate  and delta time
frameRate = 30
deltaTime = 1/frameRate
# Set screen width and screen height
screenWidth = 960
screenHeight = 960
# Array of clans
clans = ["RED" , "GREEN" , "BLUE" , "YELLOW"]
#Keep track of whether or not one of the ships is circled
shipCircled = {"isCircled" : False , "currentCircled" : 0}
#Global boolean that is true when mouse button is clicked
clicked = False
menuClicked = False
#A random velocity
randomVelocity = [random.randint(-10,10)/10 , random.randint(-10,10)/10]
#Quadrants for spawning
quadrants = {
            1 : [random.randint(160 , 460) , random.randint(160 , 460)],
            2 : [random.randint(560 , 860) , random.randint(160 , 460)],
            3 : [random.randint(160 , 460) , random.randint(560 , 860)],
            4 : [random.randint(560 , 860) , random.randint(560 , 560)]
            }
#Some colors
colors = {"RED" : (255,0,0),
            "GREEN" : (0,255,0),
            "BLUE" : (0,0,255),
            "YELLOW" : (255,255,0)}
#Keeps track of time elapsed since start of game
timeElapsed =  0.0
#Keep track of time a which game started
timeStarted = 0.0
#Time of day
timeOfDay = "NONE"
#Initialize pygame and game data dictionary
def initialize():
    screen = initializePygame()
    return initializeData(screen)

def initializePygame():
    pygame.init()
    pygame.key.set_repeat(1,1)
    pygame.display.set_caption("Pirate Watch")
    return pygame.display.set_mode((960, 960))

def initializeData(screen, numShips = 30):

    # Array of clans to help initialize game
    global clans
    #Quadrants for spawning
    global quadrants

    gameData = {"screen" : screen,
                "background" : pygame.transform.scale(pygame.image.load("ressources/WaterBackground.png").convert_alpha(),(960,960)),
                "entities" : [],
                "isOpen" : True,
                "state" : "MENU",
                "gameDuration" : 60000,
                "shipsLeft" : numShips,
                 }

    # Initialize smaller Ships
    for i in range(numShips):
        gameData["entities"].append({"type" : "smallerShip",
                                    "velocity" : [random.randint(-10,10)/10 , random.randint(-10,10)/10],
                                    "clan" : "None",
                                    "hasEscaped" : False,
                                    "sprite" : pygame.transform.scale(pygame.image.load("ressources/ship (2).png").convert_alpha(),(33,56)),
                                    "id" : i + 101,
                                    "location" : [random.randint(160 , 860) , random.randint(160 , 860)],
                                    "size" : [33,56],
                                    "speed" : 2,
                                    "angle" : 0,
                                    "state" : "freeRoam",
                                    "captureDuration" : 10000,
                                    "captureTime" : 0,
                                    "hasAccelerated" : False})

    # Initialize Main Ships
    for i in range(4):
        gameData["entities"].append({"type" : "mainShip",
                                    "velocity" : [random.randint(-10,10)/10 , random.randint(-10,10)/10],
                                    "clan" : clans[i],
                                    "sprite" : pygame.transform.scale(pygame.image.load("ressources/ship (" + str(i+3) + ").png").convert_alpha(),(66,113)),
                                    "id" : i + 1,
                                    "location" : quadrants[i+1],
                                    "size" : [66,113],
                                    "speed" : 3,
                                    "angle" : 0,
                                    "drawCircle" : False,
                                    "state" : "freeRoam",
                                    "hasAccelerated" : False })

    for i in range(15):
        gameData["entities"].append({"type" : "clanInfluencer",
                                    "velocity" : [random.randint(-10,10)/10, random.randint(-10,10)/10],
                                    "id" : i + 201,
                                    "location" : [random.randint(160 , 860) , random.randint(160 , 860)],
                                    "clan" : clans[random.randint(0,3)],
                                    "size" : 20,
                                    "speed" : 1.2})

    return gameData


# Handle input
def handleInput(gameData):
    global menuClicked
    global clicked
    global shipCircled
    events = pygame.event.get()
    for event in events:
        # Handle quitButton press
        if event.type == pygame.QUIT:
            gameData["isOpen"] = False
        if event.type == pygame.MOUSEBUTTONUP and shipCircled["isCircled"]:
            clicked = True
        elif event.type == pygame.MOUSEBUTTONUP:
            menuClicked = True

# Central render function
def render(gameData):
    global timeOfDay
    if timeOfDay == "DAY":
        gameData["screen"].blit(gameData["background"], (0,0))
    elif timeOfDay == "NIGHT":
        gameData["screen"].fill((0,0,130))
    for entity in gameData["entities"]:
        if entity["type"] == "smallerShip":
            renderShips(gameData, entity)
        elif entity["type"] == "mainShip":
            renderMainShips(gameData , entity)
        elif entity["type"] == "clanInfluencer":
            renderClanInfluencer(gameData,entity)

    renderScore(gameData, 910 , 920)
    pygame.display.flip()

# Render the smaller ships
def renderShips(gameData, entity):
    shipImages = ["ressources/ship (3).png", "ressources/ship (4).png" , "ressources/ship (5).png" , "ressources/ship (6).png"]
    if entity["clan"] != "None":
        entity["sprite"] = pygame.transform.scale(pygame.image.load(shipImages[clans.index(entity["clan"])]).convert_alpha(),(entity["size"][0],entity["size"][1]))
    if(entity["hasEscaped"] == False):
        newSprite = pygame.transform.rotate(entity["sprite"] , entity["angle"])
        newSpriteRect = newSprite.get_rect(center = (entity["location"][0] + entity["size"][0] / 2 , entity["location"][1] + entity["size"][1] / 2))
        gameData["screen"].blit(newSprite, (entity["location"][0] , entity["location"][1]))



# render the main ships
def renderMainShips(gameData, entity):
    if entity["drawCircle"]:
        pygame.draw.circle(gameData["screen"] , (0,0,0) , (int(entity["location"][0] + entity["size"][0]/2) , int(entity["location"][1] + entity["size"][1]/2)) , 150, 2 )

    newSprite = pygame.transform.rotate(entity["sprite"] , entity["angle"])
    newSpriteRect = newSprite.get_rect(center = (entity["location"][0] + entity["size"][0] / 2 , entity["location"][1] + entity["size"][1] / 2))
    gameData["screen"].blit(newSprite, (entity["location"][0] , entity["location"][1]))
# Render clanInfluencer
def renderClanInfluencer(gameData , entity):
    global colors
    pygame.draw.circle(gameData["screen"] , colors[entity["clan"]] , (int(entity["location"][0]) , int(entity["location"][1])), entity["size"])
#Render score
def renderScore(gameData , x , y):
    #Initialize text and image
    font = pygame.font.SysFont(None,48)
    color = (255,255,255)
    scoreSprite =  pygame.transform.scale(pygame.image.load("ressources/ship (1).png").convert_alpha(),(33,56))
    #Display Score and score
    scoreText = font.render(" X "+ str(gameData["shipsLeft"])  , True, color)
    scoreRect = scoreText.get_rect()
    scoreRect.centerx = x
    scoreRect.centery = y
    gameData["screen"].blit(scoreText,scoreRect)
    gameData["screen"].blit(scoreSprite , (x-70 , y-30) )

# Central update function
def update(gameData):
    global timeElapsed
    #Cases where we should exit the game
    if timeElapsed > gameData["gameDuration"] and gameData["state"] == "GAME" and gameData["shipsLeft"] >0:
        gameData["state"] = "WON"
    if gameData["shipsLeft"] <=0 and gameData["state"] == "GAME":
        gameData["state"] = "LOST"
    #Update entities in the game
    for entity in gameData["entities"]:
        if entity["type"] == "smallerShip" and entity["hasEscaped"] == False:
            updateShip(gameData, entity , False)
        elif entity["type"] == "mainShip":
            updateMainShip(gameData, entity, True)
        elif entity["type"] == "clanInfluencer":
            updateClanInfluencer(gameData, entity)


# openWinScreen
def openWinScreen(gameData):
    gameData["screen"].fill((0,180,0))
    #Intialize font
    font = pygame.font.SysFont(None,96)
    #Display screen
    winText = font.render("YOU WIN !!!", True, (255,255,255))
    winRect = winText.get_rect()
    winRect.centerx = 480
    winRect.centery = 150
    gameData["screen"].blit(winText , winRect)
    renderScore(gameData, 480,480)
    pygame.display.update()
#open lose screen
def openLoseScreen(gameData):
    gameData["screen"].fill((180,0,0))
    #Intialize font
    font = pygame.font.SysFont(None,96)
    #Display screen
    loseText = font.render("YOU LOSE :<", True, (255,255,255))
    loseRect = loseText.get_rect()
    loseRect.centerx = 480
    loseRect.centery = 150
    gameData["screen"].blit(loseText , loseRect)
    renderScore(gameData, 480,480)
    pygame.display.update()

# Update the smaller ships
def updateShip(gameData, entity, mainShipBool):
    global randomVelocity
    global screenWidth
    global screenHeight
    #Move the smaller ship when it is part of a clan and when it isn't
    if mainShipBool == True or entity["clan"] == "None" or entity["state"] == "freeRoam":
        entity["location"][0] += entity["velocity"][0] * entity["speed"]
        entity["location"][1] += entity["velocity"][1] * entity["speed"]
    elif entity["clan"] != "None" and entity["state"] == "captured" and not mainShipBool:
        for mainShip in gameData["entities"]:
            if mainShip["type"] == "mainShip":
                if mainShip["clan"] == entity["clan"]:
                    entity["location"][0] += mainShip["velocity"][0] * mainShip["speed"]
                    entity["location"][1] += mainShip["velocity"][1] * mainShip["speed"]


    # Rotate ships
    deltaX = (entity["location"][0]+entity["size"][0]/2 + entity["velocity"][0]*120) - (entity["location"][0]+entity["size"][0]/2)
    deltaY = (entity["location"][1]+entity["size"][1]/2 + entity["velocity"][1]*120) - (entity["location"][1]+entity["size"][1]/2)
    entity["angle"] = math.atan2(deltaY , deltaX) * -1 * (180 / math.pi) + 90

    #make smaller ship join clan of mainShip and control different states of ship based on situation
    for mainShip in gameData["entities"]:
        if mainShip["type"] == "mainShip":
            distance = ((entity["location"][0] - mainShip["location"][0])**2+
                        (entity["location"][1] - mainShip["location"][1])**2)**0.5
            if entity["clan"] == "None" and distance < 130 and entity["state"] != "captured":
                entity["state"] = "captured"
                entity["clan"] = mainShip["clan"]
                entity["velocity"] = mainShip["velocity"]
                entity["captureTime"] = timeElapsed
            elif entity["clan"] == mainShip["clan"] and distance < 130 and entity["state"] != "captured":
                entity["state"] = "captured"
                entity["clan"] = mainShip["clan"]
                entity["velocity"] = mainShip["velocity"]
                entity["captureTime"] = timeElapsed
            elif entity["clan"] == mainShip["clan"] and distance > 130 and entity["state"] != "freeRoam":
                entity["state"] = "freeRoam"
                entity["velocity"] = [random.randint(-10,10)/10, random.randint(-10,10)/10]
    # Don't let ship go out the play area
    if mainShipBool == True:
        if entity["location"][0 ] + entity["size"][0] >= screenWidth or entity["location"][0] < 0:
            entity["velocity"][0] *= -1
        if entity["location"][1] + entity["size"][1] >= screenHeight or entity["location"][1] < 0:
            entity["velocity"][1] *= -1

    #change smaller ship clan if they come in contact with clanInfluencer
    if mainShipBool == False:
        for clanInfluencer in gameData["entities"]:
            if clanInfluencer["type"] == "clanInfluencer":
                distance = ((entity["location"][0] + entity["size"][0]/2 - clanInfluencer["location"][0])**2
                            +(entity["location"][1] + entity["size"][1]/2 - clanInfluencer["location"][1])**2)**0.5
                if distance < clanInfluencer["size"]:
                    entity["clan"] = clanInfluencer["clan"]

    #Make ship return to freeRoam after certain amount of time and randomly change clan
    if mainShipBool == False and entity["captureTime"] + entity["captureDuration"] < timeElapsed and entity["state"] == "captured" :
        entity["state"] = "freeRoam"
        entity["clan"] = clans[random.randint(0,3)]
        entity["velocity"] = [random.randint(-10,10)/10, random.randint(-10,10)/10]
    #This will increane the speed of smaller ships as time goes by
    if timeElapsed > 30000 and entity["hasAccelerated"] == False:
        entity["hasAccelerated"] = True
        entity["speed"] *=2
    #Ship will have escaped if it exists play area
    if mainShipBool == False and entity["state"] == "freeRoam":
        if (entity["location"][0]+entity["size"][0] < 0 or
            entity["location"][0]-entity["size"][0] > 960 or
            entity["location"][1]+entity["size"][1] < 0 or
            entity["location"][1]-entity["size"][1] > 960):
            '''-----'''
            entity["hasEscaped"] = True
            gameData["shipsLeft"] -= 1
#Update the maine ship
def updateMainShip(gameData, entity, mainShip):
    global shipCircled
    global clicked
    updateShip(gameData , entity , mainShip)
    mousePos = pygame.mouse.get_pos()
    distanceToCursor = ((mousePos[0] - entity["location"][0])**2 + (mousePos[1] - entity["location"][1]) **2)**0.5


    #Draw the ship's influence circle when it is being hovered by the mouse and
    #Make sure only one ship can be circled at a time
    if distanceToCursor < 150 and not shipCircled["isCircled"] :
        entity["drawCircle"] = True
        shipCircled["isCircled"] = True
        shipCircled["currentCircled"] = entity["id"]
    elif distanceToCursor > 150 and shipCircled["currentCircled"] == entity["id"] :
        entity["drawCircle"] = False
        shipCircled["isCircled"] = False

    shipImages = ["ressources/ship (3).png", "ressources/ship (4).png" , "ressources/ship (5).png" , "ressources/ship (6).png"]
    if clicked and entity["drawCircle"]:
            entity["sprite"] = pygame.transform.scale(pygame.image.load(shipImages[changeClan(gameData, entity)]).convert_alpha(),(66,113))
            clicked = False
#Update clanInfluencer
def updateClanInfluencer(gameData,entity):
    # Move clanInfluencer
    entity["location"][0] += entity["velocity"][0]
    entity["location"][1] += entity["velocity"][1]

    #Make sure clanInfluencer stays on screen
    if entity["location"][0 ] + entity["size"] >= screenWidth or entity["location"][0] - entity["size"] < 0:
        entity["velocity"][0] *= -1
    if entity["location"][1] + entity["size"] >= screenHeight or entity["location"][1] - entity["size"] < 0:
        entity["velocity"][1] *= -1
#control the menu screen
def controlMenu(gameData):
    global menuClicked
    global timeOfDay
    #Menu initialization
    font = pygame.font.SysFont(None,48)
    idleColor = (255,255,255)
    highlightedColor = (150,150,150)
    gameData["screen"].fill((0,100,155))
    #Display Start Game Button
    startGameText = font.render("START GAME(DAY)" , True, idleColor)
    startGameRect = startGameText.get_rect()
    startGameRect.centerx = 480
    startGameRect.centery = 300
    #Check if mouse is over text
    mousePos = pygame.mouse.get_pos()
    if (mousePos[0] > startGameRect.x and mousePos[0] < startGameRect.x + startGameRect.width
        and mousePos[1] > startGameRect.y and mousePos[1] < startGameRect.y + startGameRect.height):
        startGameText = font.render("START GAME(DAY)", True , highlightedColor)
        if menuClicked:
            menuClicked = False
            timeOfDay =  "DAY"
            openRules(gameData)
    gameData["screen"].blit(startGameText,startGameRect)
    #Display Start Game(Night) Button
    startGameNightText = font.render("START GAME(NIGHT)" , True, idleColor)
    startGameNightRect = startGameNightText.get_rect()
    startGameNightRect.centerx = 480
    startGameNightRect.centery = 480
    #Check if mouse is over text
    mousePos = pygame.mouse.get_pos()
    if (mousePos[0] > startGameNightRect.x and mousePos[0] < startGameNightRect.x + startGameNightRect.width
        and mousePos[1] > startGameNightRect.y and mousePos[1] < startGameNightRect.y + startGameNightRect.height):
        startGameNightText = font.render("START GAME(NIGHT)", True , highlightedColor)
        if menuClicked:
            menuClicked = False
            timeOfDay = "NIGHT"
            openRules(gameData)
    gameData["screen"].blit(startGameNightText,startGameNightRect)

    #Display Rules Game Button
    rulesText = font.render("WELCOME TO PIRATE WATCH !" , True, idleColor)
    rulesRect = rulesText.get_rect()
    rulesRect.centerx = 480
    rulesRect.centery = 660
    gameData["screen"].blit(rulesText,rulesRect)

    pygame.display.update()
# Helper method that handles changing the main ship's clan
def changeClan(gameData, entity):
    shipImages = ["ressources/ship (3).png", "ressources/ship (4).png" , "ressources/ship (5).png" , "ressources/ship (6).png"]
    #Cycles main ship through clans
    #Also makes sure that there remains only one ship per clan
    if clans.index(entity["clan"]) < 3:
        index = clans.index(entity["clan"]) + 1
        for otherMainShip in gameData["entities"]:
            if otherMainShip["type"] == "mainShip" and otherMainShip["clan"] == clans[index]:
                otherMainShip["clan"] = clans[index-1]
                otherMainShip["sprite"] = pygame.transform.scale(pygame.image.load(shipImages[index-1]).convert_alpha(), (otherMainShip["size"][0], otherMainShip["size"][1]))
        entity["clan"] = clans[index]
    else:
        index = 0
        for otherMainShip in gameData["entities"]:
            if otherMainShip["type"] == "mainShip" and otherMainShip["clan"] == clans[index]:
                otherMainShip["clan"] = clans[index +3]
                otherMainShip["sprite"] = pygame.transform.scale(pygame.image.load(shipImages[index+3]).convert_alpha(), (otherMainShip["size"][0], otherMainShip["size"][1]))
        entity["clan"] = clans[index]
    return index
#Helper method that loads menu
def openMenu(gameData):
    gameData["state"] = "MENU"
#Helper method that starts the gameData
def startGame(gameData):
    gameData["state"] = "GAME"
#Helper method that opens up rules page
def openRules(gameData):
    global menuClicked
    gameData["state"] = "RULES"
    #Page initialization
    font = pygame.font.SysFont(None,30)
    idleColor = (255,255,255)
    highlightedColor = (150,150,150)
    gameData["screen"].fill((0,100,155))
    #Display rules
        #Story
    story1= font.render("The police have purposely  leaked fake news of a very large treasure in the Indian Ocean", True , idleColor)
    story2= font.render("near the East coast of Africa in  order lure pirates into a trap. However, once in the area", True , idleColor)
    story3= font.render("the pirates start to suspect that something is up, you have to try and keep the pirates", True, idleColor)
    story4= font.render("within the area until the police arrives which is in one minute. Don’t let them get away!", True, idleColor)

        #Rules
    text1 = font.render("- Your goal is to keep the smaller pirate ships inside the play area", True, idleColor)
    text1s= font.render("until the police arrive to arrest them.", True , idleColor)
    text2 = font.render("- Smaller ships will follow the larger ship if they're of the same color and are close enough.", True , idleColor)
    text2s= font.render(" They're four clans each represented by one color : RED, GREEN , BLUE and YELLOW", True , idleColor)
    text3 = font.render("- You can change the color of the larger ships by clicking on them.", True , idleColor)
    text3s= font.render("However, every color will be represented at all times.", True , idleColor)
    text4 = font.render("- Watch out for clan influencers (colored circles)!", True , idleColor)
    text4s= font.render("They will change the clan of a ship they collide with to their own color.",True, idleColor)
    text5 = font.render("- All ships will get quicker over time. Smaller ships will stop following a larger ship", True , idleColor)
    text5s= font.render("and randomly change to another clan if they have been following that ship for 10 seconds.", True, idleColor)

    #Arrays representing story and rules
    story = [story1, story2, story3, story4]
    text = [text1, text1s, text2, text2s, text3, text3s, text4, text4s, text5, text5s]

    #Display story
    for i in range(len(story)):
        storyRect = story[i].get_rect()
        storyRect.centerx = 480
        storyRect.centery = (i+1)*50
        gameData["screen"].blit(story[i], storyRect)


    #Display Rules
    mainLineIndex = 1
    for i in range(len(text)):
        textRect = text[i].get_rect()
        textRect.centerx = 480
        if (i+1) % 2 != 0:
            textRect.centery = mainLineIndex * 100 + 200
            mainLineIndex +=1
        else:
            textRect.centery = (mainLineIndex-1)*100 + 240
        gameData["screen"].blit(text[i], textRect)


    #Start Game
    startButtonText = font.render("I'M READY!" , True, idleColor)
    startButtonRect = startButtonText.get_rect()
    startButtonRect.centerx = 880
    startButtonRect.centery = 900
    #Check if mouse is over text
    mousePos = pygame.mouse.get_pos()
    if (mousePos[0] > startButtonRect.x and mousePos[0] < startButtonRect.x + startButtonRect.width
        and mousePos[1] > startButtonRect.y and mousePos[1] < startButtonRect.y + startButtonRect.height):
        startButtonText = font.render("LET'S GO!", True , highlightedColor)
        if menuClicked:
            menuClicked = False
            startGame(gameData)
    gameData["screen"].blit(startButtonText,startButtonRect)

    pygame.display.update()


#Helper method that handles getting distance between two objects
def getDistance(pos1 , pos2):
    distance = ((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)**0.5
    return distance

def main() :
    global timeElapsed
    #Initialize Data and pygame
    gameData = initialize()
    #Central Menu Loop
    while gameData["state"] == "MENU" and gameData["isOpen"] == True:
        handleInput(gameData)
        controlMenu(gameData)
    #Control rules screen loop
    while gameData["state"] == "RULES" and gameData["isOpen"] == True:
        handleInput(gameData)
        openRules(gameData)
    #Central gameLoop
        #Initialize clock object
    Clock = pygame.time.Clock()
    while gameData["isOpen"] and gameData["state"] == "GAME":
        timeElapsed += Clock.tick()
        handleInput(gameData)
        update(gameData)
        render(gameData)
        time.sleep(0.01)
    #Win Screen Loop
    while gameData["state"] == "WON" and gameData["isOpen"] == True:
        handleInput(gameData)
        openWinScreen(gameData)
    #Lose screen Loop
    while gameData["state"] == "LOST" and gameData["isOpen"] == True:
        handleInput(gameData)
        openLoseScreen(gameData)

    # Exit pygame and python
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
