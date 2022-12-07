#################################################
# term project fall '22: skincare simulator
#
# Your name: Linnea
# Your andrew id: lleaver
#################################################

###
# citations
# https://tkdocs.com/pyref/photoimage.html
# https://tkdocs.com/shipman/create_image.html
###

import random

from cmu_112_graphics import *

#classes
class Issue:
    def __init__(self, name):
        self.name = name
        self.status = "active"
        self.productsUsed = []
        
        self.useResults = self.loadReactions()
        self.productReactions = self.loadProductReactions()
    
    def loadReactions(self):
        with open('csv/reactSkin.csv', "r", encoding="utf-8") as f:
            fileString = f.read()
        list = {}
        for line in fileString.splitlines():
            items = line.split(",")
            if items[0] == self.name:
                list[items[1].strip()] =items[2].strip()
        return list
    
    def loadProductReactions(self):
        with open('csv/reactProduct.csv', "r", encoding="utf-8") as f:
            fileString = f.read()
        list = []
        for line in fileString.splitlines():
            items = line.split(",")
            if items[0] == self.name:
                list.append(items[1].strip(), items[2].strip())
        return list
    
    def __repr__(self):
        return self.name
    
    def getName(self):
        return self.name.strip()
    
    def getStatus(self):
        return self.status
    
    def changeStatus(self, newStatus):
        self.status = newStatus
    
    def getProductsUsed(self):
        return self.productsUsed

    def useNewProduct(self, productname):
        if productname == None:
            return 0
        if productname in self.productsUsed:
            return -2
        for item in self.productReactions:
            if productname in item:
                return -3
        else:
            self.productsUsed.append(productname)
            if productname in self.useResults:
                return self.useResults[productname]
            else:
                return 0
            
    def drawSelf(self,canvas,app):
        canvas.create_text(app.width/2, (app.height)/3 + 5,
                        text=f'insert {self.name} here',
                        font='Times 15 bold',
                        fill='red')
    
    def getClickableArea(self, app):
        #top left
        x0= app.width/4
        y0= app.height/4
        #bottom right
        x1= app.width*(3/4)
        y1 = app.height*(3/4)
        return x0,y0,x1,y1
    
    def isInClickableArea(self, mousex, mousey, app):
        rect = self.getClickableArea(app)
        if (rect[0] < mousex) and (rect[2] > mousex) and \
            (rect[1] < mousey) and (rect[3] > mousey):
                return True
        else:
            return False
    
class Product:
    def __init__(self, name, x, y, img):
        self.interactions = {}
        self.name = name
        self.image = img
        self.smallerimage = img.subsample(2,2)

        self.x = x
        self.y = y
    
    def getName(self):
        return self.name
    
    def getLoc(self):
        return (self.x, self.y)
    
    def getImg(self):
        return self.image

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
        canvas.create_image(self.x, self.y, image = self.image, 
                        activeimage = self.smallerimage)
    
    def checkClick(self, mousex, mousey):
        rect = self.getClickableArea()
        if (rect[0] < mousex) and (rect[2] > mousex) and \
            (rect[1] < mousey) and (rect[3] > mousey):
                return True
        else:
            return False

#functions
#read data from the files
def loadSingleColList(filename):
    with open(filename, "r", encoding="utf-8") as f:
        fileString = f.read()
    list = []
    for line in fileString.splitlines():
        items = line.split(",")
        list.append(items[0])
    return list

def loadDoubleColList(filename):
    with open(filename, "r", encoding="utf-8") as f:
        fileString = f.read()
    list = []
    for line in fileString.splitlines():
        items = line.split(",")
        list.append((items[0],items[1].strip()))
    return list

#pick a new random skin condition
def generateNewIssue():
    options = loadSingleColList('csv/issues.csv')
    print(options)
    name = random.choice(options)
    issue = Issue(name)
    return issue

def startNewGame():
    condition = generateNewIssue()
    points = 0
    screen = "start"
    return condition, points, screen

def startNewTry(app):
    if app.points > app.highScore:
        app.highScore = app.points
    app.points = 0
    app.condition = generateNewIssue()
    app.screen = "start"
    app.currentlySelecting = None
    app.drawDialogue = False
    app.textToDisplay = "Error"
    app.secondText = "Error"

def calculatePoints(app):
    numProducts = len(app.condition.getProductsUsed())
    if (app.points > 0) and (numProducts == 1):
        return "A"
    elif (app.points > 0) and (numProducts <= 2):
        return "B"
    elif (app.points == 0) or (numProducts > 2):
        return "C"
    else:
        return "F"

def loadProductImage(app, filename):
    png = PhotoImage(file = filename)
    png = png.subsample(4, 4)
    return png

#graphics
def appStarted(app):
    startingInfo = startNewGame()
    app.condition = startingInfo[0]
    app.points = startingInfo[1]
    app.screen = startingInfo[2]
    app.productsList = loadDoubleColList("csv/products.csv")
    app.products = []
    app.highScore = 0
    app.currentlySelecting = None
    app.drawDialogue = False
    app.textToDisplay = "Error"
    app.secondText = "Error"
    app.skinLink = "images/"+app.condition.getName()+"skin.png"
    app.skinImg = PhotoImage(file = f"images/{app.condition.getName()}skin.png").subsample(2, 2)
    app.titleImg = PhotoImage(file= "images/gametitle.png").subsample(3, 3)

    #create list of product instances equally spaced
    slicex = (app.width/(len(app.productsList)))-10
    i = 0.5
    for item in app.productsList:
        width = max(10,len(item[0])/2)
        image = loadProductImage(app, item[1])
        app.products.append(Product(item[0],(slicex+width) * i, 100, image))
        i += 1

def mousePressed(app, event):
    if app.screen == "play":
        for item in app.products:
            if(item.checkClick(event.x, event.y)):
                newSelection = Product(item.getName(), event.x, event.y, item.getImg())
                app.currentlySelecting = newSelection
        app.drawDialogue = False
        if app.secondText == 'Round complete! Click to end game':
            app.screen = "finish"

def mouseDragged(app, event): 
    if (app.currentlySelecting) and (app.screen == "play"):
        app.currentlySelecting.changeLoc(event.x, event.y)

def mouseReleased(app, event):
    if (app.currentlySelecting) and (app.screen == "play"):
        if app.condition.isInClickableArea(event.x, event.y, app):
            result = int(app.condition.useNewProduct(app.currentlySelecting.getName()))
            app.drawDialogue = True
            if result > 0:
                app.textToDisplay = f'Successfully addressed {app.condition.getName()} using item {app.currentlySelecting.getName()}'
                app.secondText = 'Round complete! Click to end game'
            elif result == -2: 
                app.textToDisplay = f'You have already used {app.currentlySelecting.getName()}, try again!' 
                app.secondText = 'Click to exit'
            elif result == -1:
                app.textToDisplay = f'Uh Oh, {app.currentlySelecting.getName()} has worsened the {app.condition.getName()}'
                app.secondText = 'Click to exit'
            elif result == -3:
                app.textToDisplay = f'Uh Oh, {app.currentlySelecting.getName()} has reacted witfh another product, causing irritation!'
                app.secondText = 'Round complete! Click to end game'
            else:
                app.textToDisplay = f'No change!'
                app.secondText = 'Click to exit'
            app.points += result
            if app.points < -1:
                app.textToDisplay = f'Oh No! Your skin has become too damaged. You lose this round!'
                app.secondText = 'Round complete! Click to end game'
            return result
        app.currentlySelecting = None

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

def redrawAll(app, canvas):
    #screen the user starts on
    if app.screen == "start":
        drawStart(canvas, app)
    
    #screen for playing the game
    elif app.screen == "play":
        drawAllProducts(canvas,app)
        drawSkinRepresentation(canvas,app)

        canvas.create_text(app.width/2, app.height*(5/6),
                        text=f'Skin Concern: {app.condition.getName()}',
                        font='Times 15 bold',
                        fill='black')
        canvas.create_text(app.width * (1/6), app.height*(8/9),
                        text=f'Back to Home',
                        font='Arial 15 bold',
                        fill='light blue',
                        activefill = 'blue')
        canvas.create_text(app.width * (5/6), app.height*(8/9),
                        text=f'End Game',
                        font='Arial 15 bold',
                        fill='light blue',
                        activefill = 'blue')
        if app.drawDialogue:
            canvas.create_rectangle(app.width-200, app.height-200,
                                    200, 200, fill="light blue")
            canvas.create_text(app.width/2, app.height*(1/2),
                        text=app.textToDisplay,
                        font='Arial 30 bold',
                        fill='black',
                        justify = 'center',
                        width = 400)
            canvas.create_text(app.width/2, app.height*(1/2) +70,
                        text=app.secondText,
                        font='Arial 10 bold',
                        fill='grey',)
        elif app.currentlySelecting:
            app.currentlySelecting.drawProduct(canvas,app)
    
    #end screen
    elif app.screen == "finish":
        temptext = f'Game Over! \nYour final point score was {app.points} points.'
        temptext += f' Your final grade, based on products used, was {calculatePoints(app)}.'
        canvas.create_text(app.width/2, app.height*(1/3),
                        text=temptext,
                        font='Arial 30 bold',
                        fill='grey',
                        width = 500,
                        justify = 'center')
        canvas.create_text(app.width/2, app.height*(2/3),
                        text= "Press Enter to try again!",
                        font='Arial 20 bold',
                        fill='light blue')

#graphics helper functions
def drawAllProducts(canvas, app):
    for item in app.products:
        item.drawProduct(canvas, app)

def drawSkinRepresentation(canvas, app):
    canvas.create_image(app.width/2, app.height/2,
                        image = app.skinImg)

def drawIssue(canvas,app):
    app.condition.drawSelf(canvas,app)  

def drawStart(canvas, app):
    canvas.create_text(app.width/2, app.height*(2/3),
                        text=f'Press Enter to start new game!',
                        font='Arial 20 bold',
                        fill='blue')
    canvas.create_text(app.width/2, app.height/2,
                        text=f'Your High Score: {app.highScore}',
                        font='Arial 20 bold',
                        fill='green')
    canvas.create_image(app.width/2, app.height/3-15,
                        image = app.titleImg)

#Start graphics loop
runApp(width=900, height=600)
