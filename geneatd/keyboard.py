# -*- coding: utf-8 -*-

#geneaTD - A multi-touch tower defense game.
#Copyright (C) 2010-2011 Frederic Kerber, Pascal Lessel, Michael Mauderer 
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#For more information contact the geneaTD team: info@geneatd.de
#

from libavg import *
import math
from mainMenu import MainMenu
import util
import os
from libavg.AVGAppUtil import getMediaDir

g_player = avg.Player.get()

keySpacing = 6


keys_left = []
keys_right = []
shifted=(False, False)
first_left = True
first_right = True


class Keyboard(object): 
    """
    This class represents a virtual keyboard.
    """  

    def __init__(self, parentNode, showPlayer1, showPlayer2, highscore, points, main):
        """
        The constructor for the virtual keyboard class. 
        parentNode - the parent node where the keyboard should appear on.
        """
        self.highscoreComingUp=False
        self.highscoreComingUp2=False
        self.fading1Out = False
        self.fading2Out = False
        self.initSides(parentNode)
        self.highscore = highscore
        self.points = points
        self.main = main
        self.showKeyBoard(parentNode, showPlayer1, showPlayer2)
        self.parentNode = parentNode
        
        
    def initSides(self, parentNode):
        """
        Init the two sides of the field.
        """
        self.left = avg.ImageNode(id="KBLeftPart", opacity=1, href=os.path.join(getMediaDir(__file__, "resources"), "splashL.jpg"), pos=(0,0), size=(util.width/2, util.height), parent=parentNode)
        self.right = avg.ImageNode(id="KBRightPart", opacity=1, href=os.path.join(getMediaDir(__file__, "resources"), "splashR.jpg"), pos=(util.halfwidth,0), size=(util.halfwidth, util.height), parent=parentNode)



    def showKeyBoard(self, parentNode, showPlayer1, showPlayer2):
        
        global shifted
        shifted=(False, False)
        global first_left
        first_left = True
        global first_right
        first_right = True
        
        self.divLeftAppended = False
        self.divRightAppended = False
        
        
        def backClick(event):
            """
            Method is called if one clicks on the back button in highscore menu.
            """
            self.back.unlink(True)
            self.back = None
            self.highscore.hide()
            self.left.unlink(True)
            self.left = None
            self.right.unlink(True)
            self.right = None
            MainMenu(parentNode, g_player, self.main)

        
        self.up1= not showPlayer1
        self.up2= not showPlayer2
        
        if (self.up1 and self.up2):
            
            highscoreDiv = avg.DivNode(pos=(0,0),opacity = 0, size=(util.width, util.height), parent=parentNode)
            
            
            self.highscore.show(highscoreDiv)
            
            
            self.back = avg.ImageNode(id="ButtonBack", opacity=1, href = os.path.join(getMediaDir(__file__, "resources"), "labels/arrow.png"), pos = (-400, util.buttonMarginBottom), size = util.helpAndCloseButtonSize, parent=highscoreDiv)
            self.back.swapHref = os.path.join(getMediaDir(__file__, "resources"), "labels/arrowGlow.png")
            self.back.setEventHandler(avg.CURSORDOWN, avg.TOUCH | avg.MOUSE, backClick);
            self.back.setEventHandler(avg.CURSOROVER, avg.TOUCH | avg.MOUSE, lambda event : glow(event, self.back));
            self.back.setEventHandler(avg.CURSOROUT, avg.TOUCH | avg.MOUSE, lambda event : glow(event, self.back));
           
            avg.LinearAnim(self.back, "pos", 1000, self.back.pos, (util.width // 600 , self.back.pos.y)).start()
            avg.fadeIn(highscoreDiv, 3000)

        self.main.victoryLeft.unlink(True)
        self.main.victoryRight.unlink(True)
        self.main.victoryLeft = None
        self.main.victoryRight = None
        
        def keyUp(char, id):
            node = g_player.getElementByID(str(id))
            
            if char == 'BACK':
                node.text=node.text[0:-1]
                return
            
            if len(node.text)<12:
                node.text = node.text+char
            global first_left
            if id==1 and first_left:
                first_left = False
                shift(1)
            global first_right
            if id==2 and first_right:
                first_right = False
                shift(2)
                
                
        def glow(event, node):
            """
            Method for glow effect on cursor over - switches images.
            """
            node.href , node.swapHref = node.swapHref, node.href

        def changeColor(what, value):
            what.color = value  
      
      
        def closeLeftKeyboard():
            self.keyBoardDivLeft.unlink(True)
            closeKeyboardPre()


        def closeRightKeyboard():
            self.keyBoardDivRight.unlink(True)
            closeKeyboardPre()

      
        def closeKeyboardPre():
            if (self.up1 and self.up2 and not self.highscoreComingUp):

                self.highscoreComingUp=True
                if self.divLeftAppended:
                    avg.fadeOut(self.divLeft, 800, closeKeyboard)    
                if self.divRightAppended:
                    avg.fadeOut(self.divRight, 800, closeKeyboard)    



        def closeKeyboard():
            
            if (self.up1 and self.up2 and not self.highscoreComingUp2):

                self.highscoreComingUp2=True
                  
                 
                if self.divLeftAppended:
                    self.divLeft.unlink(True)
                    self.divLeft = None
                    self.keyBoardDivLeft = None
                    self.player1TextDiv = None
                    self.player1Box = None
                    self.player1Text = None
                    global shiftNode_left
                    shiftNode_left = None
                if self.divRightAppended:
                    self.divRight.unlink(True)
                    self.divRight = None
                    self.keyBoardDivRight = None
                    self.player2TextDiv = None
                    self.player2Box = None
                    self.player2Text = None
                    global shiftNode_right
                    shiftNode_right = None
                                     
                global keys_left
                global keys_right
                keys_left = []
                keys_right = []
                highscoreDiv = avg.DivNode(pos=(0,0), opacity=0, size=(util.width, util.height))
                  
                self.highscore.show(highscoreDiv)
                
                
                self.back = avg.ImageNode(id="ButtonBack", opacity=1, href = os.path.join(getMediaDir(__file__, "resources"), "labels/arrow.png"), pos = (-400, util.buttonMarginBottom), size = util.helpAndCloseButtonSize, parent=highscoreDiv)
                self.back.swapHref = os.path.join(getMediaDir(__file__, "resources"), "labels/arrowGlow.png")
                self.back.setEventHandler(avg.CURSORDOWN, avg.TOUCH | avg.MOUSE, backClick);
                self.back.setEventHandler(avg.CURSOROVER, avg.TOUCH | avg.MOUSE, lambda event : glow(event, self.back));
                self.back.setEventHandler(avg.CURSOROUT, avg.TOUCH | avg.MOUSE, lambda event : glow(event, self.back));
                
                avg.LinearAnim(self.back, "pos", 1000, self.back.pos, (util.width // 600 , self.back.pos.y), False, None, lambda : self.parentNode.appendChild(highscoreDiv)).start()
                avg.fadeIn(highscoreDiv, 3000)

                
        def enterUp(id):
            node = g_player.getElementByID(str(id))
               
               
            if id==1:
                if not self.fading1Out:
                    self.fading1Out = True
                    
                    if len(node.text)!=0:
                        self.highscore.addEntry(node.text, self.points[id-1])
                        changeColor(self.player1Box,"000000")             
                        avg.LinearAnim(self.player1TextDiv, "pos", 1250, (self.player1TextDiv.pos.x,self.player1TextDiv.pos.y), (self.player1TextDiv.pos.x//2,self.player1TextDiv.y)).start()
                    else:
                        avg.fadeOut(self.player1TextDiv, 1250)
                    avg.fadeOut(self.keyBoardDivLeft,800, closeLeftKeyboard)
                    self.up1=True  
                    
            else:
                if not self.fading2Out:
                    self.fading2Out = True
                    
                    if len(node.text)!=0:
                        self.highscore.addEntry(node.text, self.points[id-1])
                        changeColor(self.player2Box,"000000")             
                        avg.LinearAnim(self.player2TextDiv, "pos", 1250, (self.player2TextDiv.pos.x,self.player2TextDiv.pos.y), (self.player2TextDiv.pos.x*2,self.player2TextDiv.y)).start()
                    else:
                        avg.fadeOut(self.player2TextDiv, 1250)
                    avg.fadeOut(self.keyBoardDivRight,800, closeRightKeyboard)
                    self.up2=True


 
        def shift(side):
            global shifted
            if side==1:
                keys = keys_left
                shifted = (not shifted[0], shifted[1])
                global shiftNode_left
                if shifted[0]:
                    shiftNode_left.fillopacity=0.6
                else:
                    shiftNode_left.fillopacity=0.0
            else:
                keys = keys_right
                shifted = (shifted[0], not shifted[1])
                global shiftNode_right
                if shifted[1]:
                    shiftNode_right.fillopacity=0.6
                else:
                    shiftNode_right.fillopacity=0.0

            if shifted[side-1]:
                    for (x,y) in keys:
                        if 97<= ord(x.char) <= 122:
                            x.char = chr(ord(x.char)-32)   
                            y.text = x.char
                        
            else:
                    for (x,y) in keys:
                        if 65<= ord(x.char) <= 90:
                            x.char = chr(ord(x.char)+32)   
                            y.text = x.char
                        

                        
        def placeKeyNode(parentNode, x, y, angle, char, id):
            
            keyNodeDiv = avg.DivNode(pos=(x,y), parent=parentNode)
            keyNodeDiv.char = char
            keyNodeDiv.side = id
            keyNodeDiv.setEventHandler(avg.CURSORUP,avg.TOUCH | avg.MOUSE, lambda event : keyUp(keyNodeDiv.char, keyNodeDiv.side))
            
            avg.RectNode(size=(util.keyHeight, util.keyHeight), pos=(0,0), parent=keyNodeDiv)
            
            keyWordNode = avg.WordsNode(fontsize=util.convertFontSize(40), variant="Bold", text=char, angle=angle, pivot=(0,0), parent=keyNodeDiv)
            if id==1: 
                keyWordNode.pos=(util.width//21,util.height//65)
            else:
                keyWordNode.pos=(-util.width//200,util.height//16)
            keyWordNode.font = "DejaVu Sans Mono"
            if id==1:
                keys_left.append((keyNodeDiv, keyWordNode))
            else:
                keys_right.append((keyNodeDiv, keyWordNode))
                

        def placeBackNode(parentNode, x, y, angle, id):
            keyNodeDiv = avg.DivNode(pos=(x,y), parent=parentNode)
            keyNodeDiv.side=id
            keyNodeDiv.setEventHandler(avg.CURSORUP,avg.TOUCH | avg.MOUSE, lambda event : keyUp("BACK", keyNodeDiv.side))
            
            avg.RectNode(size=(util.keyHeight, util.keyHeight), pos=(1,0), parent=keyNodeDiv)
            keyWordNode = avg.ImageNode(href=os.path.join(getMediaDir(__file__, "resources"), "keyArrow.png"), angle=angle, pivot=(0,0), parent=keyNodeDiv)
            keyWordNode.size=(util.height//20,util.height//20)
            
            if id==1: 
                keyWordNode.pos=(util.width//25,util.height//50)
            else:
                keyWordNode.pos=(util.width//100,util.height//16)
        

        def placeUpNode(parentNode, x, y, angle, id):
            keyNodeDiv = avg.DivNode(pos=(x,y), parent=parentNode)
            keyNodeDiv.side = id
            keyNodeDiv.setEventHandler(avg.CURSORUP,avg.TOUCH | avg.MOUSE, lambda event : shift(keyNodeDiv.side))
            
            keyNode = avg.RectNode(fillcolor="FFFFFF", fillopacity=0.6, size=(util.keyHeight, util.keyHeight), pos=(1,0), parent=keyNodeDiv)
            
            keyWordNode = avg.ImageNode(href=os.path.join(getMediaDir(__file__, "resources"), "keyArrow.png"), angle=angle, size=(util.height//20,util.height//20), pivot=(0,0), parent=keyNodeDiv)

            if id==1: 
                keyWordNode.pos=(util.width//25,util.height//16)
                global shiftNode_left
                shiftNode_left = keyNode
            else:
                keyWordNode.pos=(util.width//80,util.height//65)
                global shiftNode_right
                shiftNode_right = keyNode


        def placeenterNode(parentNode, x, y, angle, id):
            keyNodeDiv = avg.DivNode(pos=(x,y), parent=parentNode)
            keyNodeDiv.side = id
            keyNodeDiv.setEventHandler(avg.CURSORUP,avg.TOUCH | avg.MOUSE, lambda event : enterUp(keyNodeDiv.side))
            
            avg.RectNode(size=(util.keyHeight, 2*util.keyHeight+6), pos=(1,0), parent=keyNodeDiv)

            keyWordNode = avg.WordsNode(font="DejaVu Sans Mono", fontsize=util.convertFontSize(40), variant="Bold", text="OK", angle=angle, pivot=(0,0), parent=keyNodeDiv)
            
            if id==1: 
                keyWordNode.pos=(util.width//21,util.height//35)
            else:
                keyWordNode.pos=(0,util.height//8)
        

        if showPlayer1:
            self.divLeftAppended = True
            self.divLeft = avg.DivNode(pos=(0,0), opacity=0, size=(util.halfwidth, util.height), parent=parentNode)
            self.keyBoardDivLeft = avg.DivNode(pos=(0,0), size=(util.halfwidth // 3*2, util.height), parent=self.divLeft)
            i=0
            for char in unicode("qwertyuiop"):
                placeKeyNode(self.keyBoardDivLeft, util.width//40*9, (util.height//50 + i * (util.keyHeight+keySpacing)), math.pi/2, char, 1)
                i=i+1;
                
            placeBackNode(self.keyBoardDivLeft, util.width//40*9, (util.height//50+i*(util.keyHeight+keySpacing)), math.pi/2, 1)
                
            i=0
            for char in unicode("asdfghjkl"):
                placeKeyNode(self.keyBoardDivLeft, util.width//40*6, (util.height//20 + i * (util.keyHeight+keySpacing)), math.pi/2, char, 1)
                i=i+1;
            
            placeenterNode(self.keyBoardDivLeft, util.width//40*6, (util.height//20+i * (util.keyHeight+keySpacing)),  math.pi/2, 1)
    
    
            placeUpNode(self.keyBoardDivLeft, util.width//40*3, util.height//12, math.pi, 1)
            i=1
            for char in unicode("zxcvbnm,."):
                placeKeyNode(self.keyBoardDivLeft, util.width//40*3, (util.height//12 + i * (util.keyHeight+keySpacing)), math.pi/2, char, 1)
                i=i+1;
                
            self.player1TextDiv = avg.DivNode(size=(util.width //15, util.height), pos=(util.width //3, 0), parent=self.divLeft)    
            self.player1Box=avg.RectNode(fillopacity=0.8, fillcolor="000000", size=(util.width // 20, util.height//4*3), pos=(0, util.height//10), parent=self.player1TextDiv)
                        
            self.player1Text=avg.WordsNode(font="DejaVu Sans Mono", fontsize=util.convertFontSize(40), variant="Bold", angle=math.pi/2, pivot=(0,0), parent=self.player1TextDiv, pos=(self.player1Box.size.x//10*11, util.height//8), id=str(1))
            shift(1)
            avg.fadeIn(self.divLeft, 3000)


        if showPlayer2:
            
            self.divRightAppended = True
            self.divRight = avg.DivNode(pos=(util.halfwidth,0), opacity = 0, size=(util.halfwidth, util.height), parent=parentNode)
            self.keyBoardDivRight = avg.DivNode(pos=(0,0), size=(util.halfwidth, util.height), parent=self.divRight)

            placeBackNode(self.keyBoardDivRight, util.width//40*9, util.height//24, math.pi/2*3, 2)


            i=1
            for char in unicode("poiuytrewq"):
                placeKeyNode(self.keyBoardDivRight, util.width//40*9, (util.height//24 + i * (util.keyHeight+keySpacing)), math.pi/2*3, char, 2)
                i=i+1;
     
     
            placeenterNode(self.keyBoardDivRight, util.width//40*12, 12,  math.pi/2*3, 2)
    
                
            i=0
            for char in unicode("lkjhgfdsa"):
                placeKeyNode(self.keyBoardDivRight, util.width//40*12, (util.height//10+util.keyHeight + i * (util.keyHeight+keySpacing)), math.pi/2*3, char, 2)
                i=i+1;
    
            i=0
            for char in unicode(".,mnbvcxz"):
                placeKeyNode(self.keyBoardDivRight, util.width//40*15, (util.height//12 + i * (util.keyHeight+keySpacing)), math.pi/2*3, char, 2)
                i=i+1;
                    
            placeUpNode(self.keyBoardDivRight, util.width//40*15, (util.height//12 + i * (util.keyHeight+keySpacing)), 0, 2)

            self.player2TextDiv = avg.DivNode(size=(util.width //15, util.height), pos=(util.width //8, 0), parent=self.divRight)    
            self.player2Box = avg.RectNode(fillopacity=0.8, fillcolor="000000", size=(util.width // 20, util.height//4*3), pos=(0, util.height//9), parent=self.player2TextDiv)
            
            self.player2Text = avg.WordsNode(font="DejaVu Sans Mono", fontsize=util.convertFontSize(40), variant="Bold", id=str(2), angle=math.pi / 2*3, pivot=(0,0), pos=(0, util.height//32*27), parent=self.player2TextDiv)
            
            
            shift(2)
            
            avg.fadeIn(self.divRight, 3000)
            
