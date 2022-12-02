#################################################
# term project fall '22: skincare simulator
#
# Your name: Linnea
# Your andrew id: lleaver
#################################################

import random

from cmu_112_graphics import *
#from PIL import Image, ImageTk

#classes

class Issue:
    def __init__(self, name):
        self.name = name
        self.status = "active"
        self.reactions = loadTripleColList('reactSkin.csv')
        print (self.reactions)
        self.productsUsed = []
    
    def __repr__(self):
        return self.name
    
    def getName(self):
        return self.name
    
    def getStatus(self):
        return self.status
    
    def changeStatus(self, newStatus):
        self.status = newStatus

    def useNewProduct(self, product):
        #dictionary?
        if product in self.reactions:
            return 1
        else:
            return 0
        
    def drawSelf(self,canvas,app):
        #edit to create images
        canvas.create_text(app.width/2, (app.height)/3 + 5,
                        text=f'insert image here',
                        font='Arial 10 bold',
                        fill='blue')
    
    
class Product:
    def __init__(self, name, x, y):
        self.interactions = {}
        self.name = name
        self.x = x
        self.y = y
        self.isClicked = False
    
    def getName(self):
        return self.name
    
    def getLoc(self):
        return (self.x, self.y)
    
    def getIsClicked(self):
        return self.isClicked

    def getClickableArea(self):
        #top left
        x0= self.x - (50)
        y0= self.y - (70)
        #bottom right
        x1= self.x + 50
        y1 = self.y + 70
        return x0,y0,x1,y1
    
    def changeLoc(self, x, y):
        self.x = x
        self.y = y
    
    def drawProduct(self, canvas, app):
        canvas.create_text(self.x, self.y,
                        text=f'{self.name}',
                        font='Arial 10 bold',
                        fill='blue')
        png = PhotoImage(file = 'bottle.png')
        png = png.subsample(5, 5)
        canvas.create_image(self.x, self.y, image = png)
    
    def selectSelf(self, canvas):
        canvas.create_rectangle(self.getClickableArea())
    
    def checkClick(self, mousex, mousey):
        rect = self.getClickableArea()
        if (rect[0] < mousex) and (rect[2] > mousex) and \
            (rect[1] < mousey) and (rect[3] > mousey):
                print(f"clicked {self.name} in area {rect}")
                self.isClicked = True
        else:
            self.isClicked = False
        return self.isClicked

#functions
#read data from the files
def loadSingleColList(filename):
    with open(filename, "r", encoding="utf-8") as f:
        fileString = f.read()
    list = []
    for line in fileString.splitlines():
        list.append(line)
    return list

def loadTripleColList(filename):
    with open(filename, "r", encoding="utf-8") as f:
        fileString = f.read()
    list = []
    for line in fileString.splitlines():
        items = line.split(",")
        list.append([items[0],items[1],items[2]])
    return list

#pick a new random skin condition
def generateNewIssue():
    #fill out further- probably want to read from file
    #and then add link to image like for little alchemy
    options = loadSingleColList('issues.csv')
    name = random.choice(options)
    issue = Issue(name)
    return issue

def startNewGame():
    productReactions = loadTripleColList("reactProduct.csv")
    skinReactions = loadTripleColList("reactSkin.csv")
    condition = generateNewIssue()
    points = 0
    screen = "start"
    return condition, points, productReactions, skinReactions, screen

def startNewTry(app):
    if app.points > app.highScore:
        app.highScore = app.points
    app.points = 0
    app.condition = generateNewIssue()
    app.screen = "start"

def calculatePoints(app):
    return app.points

#graphics
def appStarted(app):
    startingInfo = startNewGame()
    app.condition = startingInfo[0]
    app.points = startingInfo[1]
    app.productReactions = startingInfo[2]
    app.skinReactions = startingInfo[3]
    app.screen = startingInfo[4]
    app.productsList = loadSingleColList("products.csv")
    app.products = []
    app.highScore = 0

    #create list of product instances equally spaced
    slicex = (app.width/(len(app.productsList)))-10
    i = 0.5
    for item in app.productsList:
        width = max(10,len(item)/2)
        app.products.append(Product(item,(slicex+width) * i, 100))
        i += 1

def keyPressed(app, event):
    if app.screen == "start":
        if event.key == "Return":
            app.screen = "play"
    elif app.screen == "play":
        if event.key == "d":
            app.screen = "finish"
    elif app.screen == "finish":
        if event.key == "Return":
            startNewTry(app)

def mousePressed(app, event):
    if app.screen == "play":
        for item in app.products:
            if item.checkClick(event.x, event.y):
                app.points += app.condition.useNewProduct(item.getName())

def redrawAll(app, canvas):
    #screen the user starts on
    if app.screen == "start":
        canvas.create_text(app.width/2, app.height*(2/3),
                        text=f'Press Enter to start new game!',
                        font='Arial 20 bold',
                        fill='blue')
        canvas.create_text(app.width/2, app.height/2,
                        text=f'Your High Score: {app.highScore}',
                        font='Arial 20 bold',
                        fill='green')
    
    #screen for playing the game
    elif app.screen == "play":
        canvas.create_text(app.width/2, app.height*(5/6),
                        text=f'current points = {app.points}, \
                        \nPress D to end game',
                        font='Arial 10 bold',
                        fill='blue')
        canvas.create_text(app.width/2, app.height*(2/3),
                        text=f'condition = {app.condition}',
                        font='Arial 20 bold',
                        fill='blue')
        drawAllProducts(canvas,app)
        drawSkinRepresentation(canvas,app)
        drawIssue(canvas, app)

        #test
        for item in app.products:
            if item.getIsClicked() == True:
                item.selectSelf(canvas)
    
    #end screen
    elif app.screen == "finish":
        canvas.create_text(app.width/2, app.height*(2/3),
                        text=f'Game Over! You have {app.points} points.',
                        font='Arial 20 bold',
                        fill='blue')
        canvas.create_text(app.width/2, app.height*(1/3),
                        text=f'Press Enter to try again!',
                        font='Arial 20 bold',
                        fill='blue')

#graphics helper functions
def drawAllProducts(canvas, app):
        for item in app.products:
            item.drawProduct(canvas, app)

def drawSkinRepresentation(canvas, app):
    num = 200
    for i in range(3):
        canvas.create_line(app.width*1/4, num + (i*50),
                            app.width*3/4, num + (i*50),
                            width = 2,
                            activewidth = 6) 

def drawIssue(canvas,app):
    app.condition.drawSelf(canvas,app)  

#Start graphics loop
runApp(width=600, height=600)
