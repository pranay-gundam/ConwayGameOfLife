from tkinter import *
from cmu_112_graphics import *
from LifeGame import *
import time


#from https://www.cs.cmu.edu/~112/notes/notes-graphics.html#customColors
def rgbString(red, green, blue):
    return "#%02x%02x%02x" % (red, green, blue)




class StartMode(Mode):
    def redrawAll(mode, canvas):
        font2 = 'ComicSansMS 60 bold'
        font3 = 'ComicSansMS 30 bold'
        canvas.create_rectangle(0, 0, mode.width, mode.height, 
                                fill= 'black')
        canvas.create_text(mode.width//2,  mode.height/5, text = "Conway Game of Life", fill = 'white', font = font2)
        
        if int(time.time()) % 2 == 0:
            canvas.create_text(mode.width//2,  3*mode.height/5, text = "Press Enter to Start", fill = 'white', font = font3)

    def keyPressed(mode, event):
        nums = ["0","1","2","3","4","5","6","7","8","9"]
        curnum = ""
        # If we click enter
        if event.key == "Enter":
            mode.app.setActiveMode(mode.app.gameMode)


class GameMode(Mode):
    def appStarted(mode):
        mode.hasRows = False
        mode.hasCols = False
        mode.choose = False
        mode.start = False
        mode.curnum = ""
        mode.rows = 0
        mode.cols = 0
        mode.board = []
        mode.isPaused = False
        mode.game = None
        mode.gen = 0
        mode.timer = 0
    
    def mousePressed(mode, event):
        x = event.x
        y = event.y

        if not mode.start and mode.choose:
            cell_row = int(y // (mode.height / mode.rows))
            cell_col = int(x // (mode.width / mode.cols))
            mode.board[cell_row][cell_col] = 1 - mode.board[cell_row][cell_col]

    def keyPressed(mode, event):
        
        nums = ["0","1","2","3","4","5","6","7","8","9"]
        
        # If we click enter
        if event.key == "Enter":
            if not mode.choose and not mode.start and not mode.hasRows and not mode.hasCols:
                mode.hasRows = True
                mode.rows = int(mode.curnum)
                
                mode.curnum = ""
            elif not mode.choose and not mode.start and mode.hasRows and not mode.hasCols:
                mode.hasCols = True
                mode.cols = int(mode.curnum)
                
                mode.curnum = ""
                mode.board = [[0 for i in range(mode.cols)] for j in range(mode.rows)]
                mode.choose = True
            elif mode.choose and not mode.start:
                mode.start = True
                mode.game = playGame(mode.board)
                
        if event.key == "Space":
            if mode.start:
                mode.isPaused = not mode.isPaused


        if event.key == "Backspace":
            mode.app.setActiveMode(mode.app.startMode)

        if event.key in nums:
            if not mode.start:
                mode.curnum += event.key

    def timerFired(mode):
        if mode.start:
            mode.timer += 1
            if mode.timer % 5 == 0 and not mode.isPaused and mode.start:
                mode.gen += 1
                mode.board = mode.game.next_gen()
                
    def redrawAll(mode, canvas):
        font2 = 'ComicSansMS 60 bold'
        font3 = 'ComicSansMS 30 bold'
        font4 = 'ComicSansMS 10 bold'
        canvas.create_rectangle(0, 0, mode.width, mode.height, 
                                fill= 'black')
    
        if not mode.start and not mode.hasRows and not mode.hasCols:
            canvas.create_text(mode.width//2,  mode.height/5, text = "How many rows?", fill = 'white', font = font2)
            canvas.create_text(mode.width//2,  3*mode.height/5, text = mode.curnum, fill = 'white', font = font3)
        elif not mode.start and mode.hasRows and not mode.hasCols:
            canvas.create_text(mode.width//2,  mode.height/5, text = "How many columns?", fill = 'white', font = font2)
            canvas.create_text(mode.width//2,  3*mode.height/5, text = mode.curnum, fill = 'white', font = font3)
        elif not mode.start and mode.choose:
            for irow in range(mode.rows):
                canvas.create_line(0, mode.height/mode.rows*irow, mode.width, mode.height/mode.rows*irow, fill = 'white')
            for icol in range(mode.cols):
                canvas.create_line(mode.width/mode.cols*icol, 0, mode.width/mode.cols*icol, mode.height, fill = 'white')
                
            
            for irow in range(mode.rows):
                for icol in range(mode.cols):
                    if mode.board[irow][icol] == 1:
                        canvas.create_rectangle(icol * mode.width / mode.cols, 
                                                irow * mode.height / mode.rows, 
                                                (icol+1) * mode.width / mode.cols, 
                                                (irow+1) * mode.height / mode.rows,
                                                fill = "yellow")
        elif mode.start:

            for irow in range(mode.rows):
                canvas.create_line(0, mode.height/mode.rows*irow, mode.width, mode.height/mode.rows*irow, fill = 'white')
            for icol in range(mode.cols):
                canvas.create_line(mode.width/mode.cols*icol, 0, mode.width/mode.cols*icol, mode.height, fill = 'white')
                
            
            for irow in range(mode.rows):
                for icol in range(mode.cols):
                    if mode.board[irow][icol] == 1:
                        canvas.create_rectangle(icol * mode.width / mode.cols, 
                                                irow * mode.height / mode.rows, 
                                                (icol+1) * mode.width / mode.cols, 
                                                (irow+1) * mode.height / mode.rows,
                                                fill = "yellow")
            canvas.create_text(mode.width / 2, 20, text = str(mode.gen) + "-th Gen", fill = 'red', font = font4)
            
class Game(ModalApp):
    def appStarted(app):
        app.startMode = StartMode()
        app.gameMode = GameMode()
        
        app.setActiveMode(app.startMode)


app = Game(width=1200, height=610)
