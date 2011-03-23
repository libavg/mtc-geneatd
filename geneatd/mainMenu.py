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
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#For more information contact the geneaTD team: info@geneatd.de
#

from libavg import *
import math
import os
from libavg.AVGAppUtil import getMediaDir
from highscore import Highscore
import util
import time




maxHelpCounter = 18

buttonSound = "soundfiles/sound_button.mp3"

class MainMenu(object):
    
    def __init__(self, parentNode, g_player, main):
        """
        The constructor for the main menu class. 
        parentNode - the parent node where the menu should be set.
        """
        self.main = main
        self.player = g_player
        self.initSides(parentNode)
        self.initMainButtonsAndHeader(parentNode)
        self.parentNode = parentNode
       
        
        self.highscore = Highscore(os.path.expanduser('~'), self.player)
      
        self.musicPlayer = main.musicPlayer
        self.musicPlayer.playTune("soundfiles/music_menu.mp3", True)
        
      
        self.soundPlayer = main.soundPlayer
        
        if (self.musicPlayer.volume == 0 or self.soundPlayer.volume == 0):
            self.muteWithoutChange()
        
        self.timeChosen = False
        self.pointsChosen = False
        main._mm = self
   
    def glow(self, event, node):
        """
        Method for glow effect on cursor over - switches images.
        """
        node.href , node.swapHref = node.swapHref, node.href
   

    def initSides(self, parentNode):
        """
        Init the two sides of the field.
        """
        self.left = avg.ImageNode(id="LeftPart", opacity=1, href=os.path.join(getMediaDir(__file__, "resources"), "splashL.jpg"), pos=(0,0), size= (util.width // 2, util.height), parent=parentNode)
        self.right = avg.ImageNode(id="RightPart", opacity=1, href=os.path.join(getMediaDir(__file__, "resources"), "splashR.jpg"), pos=(util.width // 2, 0), size= (util.width // 2, util.height), parent=parentNode)
        

      
    def initOneButton(self, node, size, pos, href, swapHref, clickMethod, angle=0):
        """
        Initialize one button.
        """
        node.size = size
        node.pos = pos
        node.href = os.path.join(getMediaDir(__file__, "resources"), href)
        node.swapHref = os.path.join(getMediaDir(__file__, "resources"), swapHref)
        node.pivot=(0,0)
        node.angle=angle
        node.setEventHandler(avg.CURSORDOWN, avg.TOUCH | avg.MOUSE, clickMethod)
        node.setEventHandler(avg.CURSOROVER, avg.TOUCH | avg.MOUSE, lambda event : self.glow(event, node));
        node.setEventHandler(avg.CURSOROUT, avg.TOUCH | avg.MOUSE, lambda event : self.glow(event, node));

    
    def initMainButtonsAndHeader(self, parentNode):
        """
        Initialize the buttons.
        """
        
        self.qs1Clicked = False
        self.qs2Clicked = False
        
        self.qs1 = avg.ImageNode(id="ButtonQS1", opacity=1, parent=parentNode)
        self.qs2 = avg.ImageNode(id="ButtonQS2", opacity=1, parent=parentNode)
        self.start = avg.ImageNode(id="ButtonStart", opacity=1, parent=parentNode)
        self.score = avg.ImageNode(id="ButtonHighscore", opacity=1, parent=parentNode)
        self.end = avg.ImageNode(id="ButtonEnd", opacity=1, parent=parentNode) 
        self.help = avg.ImageNode(id="ButtonHelp", opacity=1, parent=parentNode)
        self.back = avg.ImageNode(id="ButtonBack", opacity=1, parent=parentNode)
        self.mute = avg.ImageNode(id="ButtonMute", opacity=1)
        self.end2 = avg.ImageNode(id="ButtonEnd2", opacity=1, parent=parentNode)
        self.help2 = avg.ImageNode(id="ButtonHelp2", opacity=1, parent=parentNode)
     
        #node, size, pos, href, swapHref, clickMethod, [angle]
        self.initOneButton(self.qs1, (util.width//6, util.height//16) ,(util.width//24,util.height//2-util.width//12),"labels/Quickstart.png","labels/Quickstart.png",self.qs1Click, math.pi/2)
        self.initOneButton(self.qs2, (util.width//6, util.height //16),(util.width-util.width//24,util.height//2+util.width//12),"labels/Quickstart.png","labels/Quickstart.png",self.qs2Click, math.pi/2*3)
        self.initOneButton(self.start, util.buttonSize,((util.width - util.buttonSize[0]) / 2, util.buttonMarginTop),"labels/start.png","labels/startGlow.png",self.startClick)      
        self.initOneButton(self.score, util.buttonSize,((util.width - util.buttonSize[0]) / 2, util.buttonMarginTop + util.buttonSize[1] + util.buttonSpace),"labels/highscore.png","labels/highscoreGlow.png",self.scoreClick)      
        self.initOneButton(self.end, util.helpAndCloseButtonSize,((util.width - util.helpAndCloseButtonSize[0]), 0),"labels/x.png","labels/xGlow.png",self.endClick)      
        self.initOneButton(self.help, util.helpAndCloseButtonSize,((util.width - 2 * util.helpAndCloseButtonSize[0]), 0),"labels/qmark.png","labels/qmarkGlow.png",self.helpClick)      
        self.initOneButton(self.back, util.helpAndCloseButtonSize,(-2*util.helpAndCloseButtonSize[0], util.buttonMarginBottom),"labels/arrow.png","labels/arrowGlow.png",self.fromScoreMenu)      
        self.initOneButton(self.mute, (util.height//20,util.height//20),(util.width//2-util.width//60, util.height-util.height//13),"labels/mute.png","labels/mute.png",self.muteClick)      
        self.initOneButton(self.end2, util.helpAndCloseButtonSize,(0, 0),"labels/x.png","labels/xGlow.png",self.endClick)      
        self.initOneButton(self.help2, util.helpAndCloseButtonSize,(util.helpAndCloseButtonSize[0], 0),"labels/qmark.png","labels/qmarkGlow.png",self.helpClick)      
        

        if self.main.musicEnabled:
            parentNode.appendChild(self.mute)

       
        self.header = avg.ImageNode(id="Header", opacity=1, href=os.path.join(getMediaDir(__file__, "resources"), "labels/GeneaTD2.png"), size=(util.width // 3,util.height //8), pos= (util.width//2 - util.width //6, util.height//20), parent=parentNode)


    def createPointMenuButtons(self, parentNode):
        """
        Initialize the buttons and the label of the points menu.
        """
        self.back.setEventHandler(avg.CURSORDOWN, avg.TOUCH | avg.MOUSE, lambda event: self.fromPointMenu(event, parentNode))
        self.back.href = os.path.join(getMediaDir(__file__, "resources"), "labels/arrow.png")
        self.back.swapHref = os.path.join(getMediaDir(__file__, "resources"), "labels/arrowGlow.png")
              
        yPos = util.height//2
        xPosSpace = util.width//6
        firstXPos = xPosSpace//5*4
       
        
        self.points100 = avg.ImageNode(id="points100", opacity=1, parent=parentNode)
        self.points200 = avg.ImageNode(id="points200", opacity=1, parent=parentNode)
        self.points300 = avg.ImageNode(id="points300", opacity=1, parent=parentNode)
        self.points400 = avg.ImageNode(id="points400", opacity=1, parent=parentNode)
        self.pointsInf = avg.ImageNode(id="pointInf", opacity=1, parent=parentNode)
       
        #node, size, pos, href, swapHref, clickMethod
        self.initOneButton(self.points100, util.helpAndCloseButtonSize, (0, 0), "labels/100.png", "labels/100Glow.png", lambda x: self.pointClick(x, 100))
        self.initOneButton(self.points200, util.helpAndCloseButtonSize, (0, 0), "labels/200.png", "labels/200Glow.png", lambda x: self.pointClick(x, 200))
        self.initOneButton(self.points300, util.helpAndCloseButtonSize, (0, 0), "labels/300.png", "labels/300Glow.png", lambda x: self.pointClick(x, 300))
        self.initOneButton(self.points400, util.helpAndCloseButtonSize, (0, 0), "labels/400.png", "labels/400Glow.png", lambda x: self.pointClick(x, 400))
        self.initOneButton(self.pointsInf, (util.width//30, util.height//10), (0, 0), "labels/8.png", "labels/8Glow.png", lambda x: self.pointClick(x, -1))      
             
        self.pointsInf.pivot = (0, 0);
        self.pointsInf.angle = math.pi / 2
        
        self.points100.pos = (firstXPos, yPos)
        self.points200.pos = (self.points100.pos.x + xPosSpace, yPos)
        self.points300.pos = (self.points200.pos.x + xPosSpace, yPos)
        self.points400.pos = (self.points300.pos.x + xPosSpace, yPos)
        self.pointsInf.pos = (self.points400.pos.x + xPosSpace + util.height//10, yPos+util.height//200*3)
  
       
    def letBackButtonAppear(self):
        """
        Helper method for letting the back button come in.
        """
        self.back.sensitive = True
        self.back.href = os.path.join(getMediaDir(__file__, "resources"), "labels/arrow.png")
        self.back.swapHref = os.path.join(getMediaDir(__file__, "resources"), "labels/arrowGlow.png")
        avg.LinearAnim(self.back, "pos", 300, self.back.pos, (util.width//60 , self.back.pos.y)).start()
        

    def createTimeMenuButtons(self, parentNode):
        """
        Initialize the buttons and the label of the time menu.
        """
        self.back.setEventHandler(avg.CURSORDOWN, avg.TOUCH | avg.MOUSE, lambda event: self.fromTimeMenu(event,parentNode))
        self.letBackButtonAppear()
        
        yPos = util.height//2
        xPosSpace = util.width//6
        firstXPos = xPosSpace//5*4
        
        self.time5 = avg.ImageNode(id="time5", opacity=1, parent=parentNode)
        self.time10 = avg.ImageNode(id="time10", opacity=1, parent=parentNode)
        self.time15 = avg.ImageNode(id="time15", opacity=1, parent=parentNode)
        self.time30 = avg.ImageNode(id="time30", opacity=1, parent=parentNode)
        self.timeInf = avg.ImageNode(id="timeInf", opacity=1, parent=parentNode)
       
        #node, size, pos, href, swapHref, clickMethod
        self.initOneButton(self.time5, util.helpAndCloseButtonSize, (0,0), "labels/5.png", "labels/5Glow.png", lambda x: self.timeClick(x,5))
        self.initOneButton(self.time10, util.helpAndCloseButtonSize, (0,0), "labels/10.png", "labels/10Glow.png", lambda x: self.timeClick(x,10))
        self.initOneButton(self.time15, util.helpAndCloseButtonSize, (0,0), "labels/15.png", "labels/15Glow.png", lambda x: self.timeClick(x,15))
        self.initOneButton(self.time30, util.helpAndCloseButtonSize, (0,0), "labels/30.png", "labels/30Glow.png", lambda x: self.timeClick(x,30))
        self.initOneButton(self.timeInf, (util.width//30,util.height//10), (0,0), "labels/8.png", "labels/8Glow.png", lambda x: self.timeClick(x,-1))
                          
        self.timeInf.pivot = (0,0);
        self.timeInf.angle = math.pi / 2
        
        self.time5.pos = (firstXPos,yPos)
        self.time10.pos = (self.time5.pos.x+xPosSpace,yPos)
        self.time15.pos = (self.time10.pos.x+xPosSpace,yPos)
        self.time30.pos = (self.time15.pos.x+xPosSpace,yPos)
        self.timeInf.pos = (self.time30.pos.x+xPosSpace+util.height//10,yPos+util.height//200*3)
  

    def createHelpMenuButtons(self, helpDiv):
        """
        Initialize the buttons for the help menu.
        """
        self.back.setEventHandler(avg.CURSORDOWN, avg.TOUCH | avg.MOUSE, lambda event: self.fromHelpMenu(event))
        self.letBackButtonAppear()
 
        self.hback = avg.ImageNode(id="ButtonHelpBack", opacity=1, parent=helpDiv)
        self.hforward = avg.ImageNode(id="ButtonHelpForward", opacity=1, parent=helpDiv)
        
 
        self.initOneButton(self.hback, util.helpAndCloseButtonSize, (util.width//24,util.height//32), "labels/lq.png", "labels/lqGlow.png", self.hbackClickWrapper)
        self.initOneButton(self.hforward, util.helpAndCloseButtonSize, (util.width//7*6,util.height//32), "labels/gq.png", "labels/gqGlow.png", self.hforwardClickWrapper)      
        
        
 
    def moveMiddleMenuOut(self, x=None):
        """
        Method moves the buttons in the middle out. The second parameter is the function that should be called afterwards.
        """           
        self.start.sensitive = False
        self.score.sensitive = False
        self.qs1.sensitive =False
        self.qs2.sensitive =False

        if (x == None):
            avg.LinearAnim(self.start, "pos", 400, self.start.pos, (self.start.pos.x, -util.buttonSize[1])).start()
            avg.LinearAnim(self.qs1, "pos", 400, self.qs1.pos, (self.qs1.pos.x, -util.height//2)).start()
            avg.LinearAnim(self.qs2, "pos", 400, self.qs2.pos, (self.qs2.pos.x, -util.height//2)).start()
            avg.LinearAnim(self.score, "pos", 570, self.score.pos, (self.score.pos.x, -util.buttonSize[1])).start()
        else:
            avg.LinearAnim(self.start, "pos", 400, self.start.pos, (self.start.pos.x, -util.buttonSize[1])).start()
            avg.LinearAnim(self.qs1, "pos", 400, self.qs1.pos, (self.qs1.pos.x, -util.height//2)).start()
            avg.LinearAnim(self.qs2, "pos", 400, self.qs2.pos, (self.qs2.pos.x, -util.height//2)).start()
            avg.LinearAnim(self.score, "pos", 570, self.score.pos, (self.score.pos.x, -util.buttonSize[1]), False, None, x).start()
        
        avg.LinearAnim(self.header, "opacity", 300, self.header.opacity, 0.0).start()
    
    
    def moveMenuIn(self):
        """
        Method that moves the buttons from of screen into the scene.
        """       
        self.start.href = os.path.join(getMediaDir(__file__, "resources"), "labels/start.png")
        self.start.swapHref = os.path.join(getMediaDir(__file__, "resources"), "labels/startGlow.png")
        self.score.href = os.path.join(getMediaDir(__file__, "resources"), "labels/highscore.png")
        self.score.swapHref = os.path.join(getMediaDir(__file__, "resources"), "labels/highscoreGlow.png")
        self.qs1.href = os.path.join(getMediaDir(__file__, "resources"), "labels/Quickstart.png")
        self.qs1.swapHref = os.path.join(getMediaDir(__file__, "resources"), "labels/Quickstart.png")
        self.qs2.href = os.path.join(getMediaDir(__file__, "resources"), "labels/Quickstart.png")
        self.qs2.swapHref = os.path.join(getMediaDir(__file__, "resources"), "labels/Quickstart.png")

        self.start.sensitive = True
        self.score.sensitive = True
        self.qs1.sensitive =True
        self.qs2.sensitive =True
         
      
        avg.LinearAnim(self.qs1, "pos", 400, self.qs1.pos, (util.width//24,util.height//2-util.width//12)).start()
        avg.LinearAnim(self.qs2, "pos", 400, self.qs2.pos, (util.width-util.width//24,util.height//2+util.width//12)).start()
        avg.LinearAnim(self.start, "pos", 750, self.start.pos, ((util.width - util.buttonSize[0]) / 2, util.buttonMarginTop)).start()
        avg.LinearAnim(self.score, "pos", 570, self.score.pos, ((util.width - util.buttonSize[0]) / 2, util.buttonMarginTop + util.buttonSize[1] + util.buttonSpace)).start()
        avg.LinearAnim(self.header, "opacity", 1200, self.header.opacity, 1.0).start()
      
    
    def introGame(self):
        """
        Method is called if the sides are out of the screen.
        """ 
         
        self.pointDiv.unlink(True)
         
        self.unlinkAll()
        
        parent = self.parentNode;        

        self.musicPlayer.stop()
        
        util.startCloudFadeIn2(parent, lambda: self.main.initGame(self.parentNode,self.highscore, self.gameTime, self.gamePoints))
     
        
    
    def timeClick(self, event, time):
        """
        A Method to set the time and afterwards starting the game.
        """
        self.soundPlayer.playTune(buttonSound)
        
        if (not self.timeChosen):
            
            self.timeChosen = True
            self.time5.sensitive = False
            self.time10.sensitive = False
            self.time15.sensitive = False
            self.time30.sensitive = False
            self.timeInf.sensitive = False
            self.gameTime = time;
            
            self.time5.unlink(True)
            self.time10.unlink(True)
            self.time15.unlink(True)
            self.time30.unlink(True)
            self.timeInf.unlink(True)
           
            self.timeDiv.unlink(True)
            self.text.unlink(True)
           
            self.time5 = None
            self.time10 = None
            self.time15 = None
            self.time30 = None
            self.timeInf = None
           
            self.timeDiv = None
            self.text = None

            self.showPointMenu()
        
    
    def pointClick(self,event,points):
        """
        A Method to set the points and afterwards starting the game.
        """
        self.soundPlayer.playTune(buttonSound)
        
        if (not self.pointsChosen):
            self.pointsChosen = True   
            self.points100.sensitive = False
            self.points200.sensitive = False
            self.points300.sensitive = False
            self.points400.sensitive = False
            self.pointsInf.sensitive = False
            self.gamePoints = points
    
            self.moveMiddleMenuOut(self.introGame)
           

    def startClick(self, event):
        """"
        Method that determines what happens on click on the start button.
        """
        self.soundPlayer.playTune(buttonSound)       
        self.letHelpButtonsDisappear()
        self.moveMiddleMenuOut(self.showTimeMenu)
    
    
    def helpClick(self, event):
        """
        Method that determines what happens on click on the help button.
        """
        self.soundPlayer.playTune(buttonSound)
        self.letHelpAndCloseButtonsDisappear()
        self.moveMiddleMenuOut(self.showHelpMenu);
    
    
    def muteClick(self, event):
        """
        Method that determines what happens on click on the mute button.
        """      
        self.musicPlayer.mute()
        self.soundPlayer.mute()
        if self.musicPlayer.volume:
            self.mute.href=os.path.join(getMediaDir(__file__, "resources"), "labels/mute.png")
            self.mute.swapHref=os.path.join(getMediaDir(__file__, "resources"), "labels/mute.png")
        else:
            self.mute.href=os.path.join(getMediaDir(__file__, "resources"), "labels/unmute.png")
            self.mute.swapHref=os.path.join(getMediaDir(__file__, "resources"), "labels/unmute.png")
    
    def muteWithoutChange(self):
        """
        Method that determines what happens on click on the mute button.
        """      
        if self.musicPlayer.volume:
            self.mute.href=os.path.join(getMediaDir(__file__, "resources"), "labels/mute.png")
            self.mute.swapHref=os.path.join(getMediaDir(__file__, "resources"), "labels/mute.png")
        else:
            self.mute.href=os.path.join(getMediaDir(__file__, "resources"), "labels/unmute.png")
            self.mute.swapHref=os.path.join(getMediaDir(__file__, "resources"), "labels/unmute.png")
                    
            
    def letHelpButtonsDisappear(self):
        """
        Helper method to let the help buttons disappear.
        """
        self.help.sensitive=False
        avg.LinearAnim(self.help, "pos", 750, self.help.pos, (self.help.pos.x, -util.buttonSize[1])).start();                                                                                

        self.help2.sensitive=False
        avg.LinearAnim(self.help2, "pos", 750, self.help2.pos, (self.help2.pos.x, -util.buttonSize[1])).start();                                                                                
            

    def letHelpAndCloseButtonsDisappear(self):
        """
        Helper method to let the help and close button disappear.
        """
        self.letHelpButtonsDisappear()
        
        self.end.sensitive = False
        avg.LinearAnim(self.end, "pos", 750, self.end.pos, (self.end.pos.x, -util.buttonSize[1])).start()

        self.end2.sensitive = False
        avg.LinearAnim(self.end2, "pos", 750, self.end2.pos, (self.end2.pos.x, -util.buttonSize[1])).start()

            
             
    def scoreClick(self, event):
        """
        Method that determines what happens on a click on the score button.
        """
        self.soundPlayer.playTune(buttonSound)
        self.letHelpAndCloseButtonsDisappear()
        self.moveMiddleMenuOut(self.showScoreMenu)
  

    def fromScoreMenu(self, event):
        """
        Method is called if one clicks on the back button in highscore menu.
        """
        self.soundPlayer.playTune(buttonSound)
        self.letBackButtonDisappear()
        
        self.letHelpAndCloseButtonsAppear()                                                                             
        self.highscore.hide()   
     
        self.moveMenuIn()

    def letBackButtonDisappear(self):
        self.back.sensitive = False;
        avg.LinearAnim(self.back, "pos", 100, self.back.pos,(-util.width//4, self.back.pos.y)).start()
        

    def fromHelpMenu(self, event):
        """
        Method is called if one clicks in help menu on the back button. The div will be faded out then the main menu comes back.
        """
        self.soundPlayer.playTune(buttonSound)
        self.letBackButtonDisappear()
        
        self.hback.sensitive = False;
        self.hforward.sensitive = False;
     
        self.dragDiv.unlink(True)
        self.innerHelpDiv.unlink(True)
        self.innerHelpDivLeft.unlink(True)
        self.innerHelpDivRight.unlink(True)
        self.imageDiv.unlink(True)
        self.imageDivLeft.unlink(True)
        self.imageDivRight.unlink(True)
        self.imageOnBack.unlink(True)
        self.imageOnBackLeft.unlink(True)
        self.imageOnBackRight.unlink(True)
        self.content.unlink(True)
        self.contentLeft.unlink(True)
        self.contentRight.unlink(True)
        self.contentCentered.unlink(True)
        self.contentCenteredRight.unlink(True)
        self.contentCenteredLeft.unlink(True)
        self.text.unlink(True)        
       
        self.text = None
        self.innerHelpDiv = None
        self.backgroundRect = None
        self.itemIMG = None
        self.content = None
        self.contentCentered = None
        self.imageDiv = None
        self.imageOnBack = None
        self.innerHelpDivRight = None
        self.backgroundRectRect = None
        self.itemIMGRight = None
        self.contentRight = None
        self.contentCenteredRight = None
        self.imageDivRight = None
        self.imageOnBackRight = None
        self.innerHelpDivLeft = None
        self.backgroundRectLeft = None
        self.itemIMGLeft = None
        self.contentLeft = None
        self.contentCenteredLeft = None
        self.imageDivLeft = None
        self.imageOnBackLeft = None

     
        self.dragDiv = None
       
        def killhBackForward():
            self.hback.unlink(True)
            self.hback = None
            self.hforward.unlink(True)
            self.hforward = None
          
        avg.LinearAnim(self.hback, "opacity",1000, self.hback.opacity, 0.0).start()
        avg.LinearAnim(self.hforward, "opacity",1000, self.hforward.opacity, 0.0, False, None, killhBackForward).start()
        avg.LinearAnim(self.helpDiv, "opacity",1000, self.helpDiv.opacity, 0.0, False, None, lambda: self.killDivAndMoveMenuIn(self.helpDiv)).start()       
       
  
   
    def fromTimeMenu(self, event, div):
        """
        Method is called if one clicks in time menu on the back button. The div will be faded out then the main menu comes back.
        """
        
        self.soundPlayer.playTune(buttonSound)
        self.letBackButtonDisappear()
        
       
        self.time5.unlink(True)
        self.time10.unlink(True)
        self.time15.unlink(True)
        self.time30.unlink(True)
        self.timeInf.unlink(True)
       
        self.timeDiv.unlink(True)
        self.text.unlink(True)
       
        self.time5 = None
        self.time10 = None
        self.time15 = None
        self.time30 = None
        self.timeInf = None
       
        self.timeDiv = None
        self.text = None

       
        avg.LinearAnim(div, "opacity",1000,div.opacity, 0.0, False, None, lambda: self.killDivAndMoveMenuIn(div)).start()


    def fromPointMenu(self,event, div):
        """
        Method is called if one clicks in the point submenu on the back button. The div will be faded out and the time menu comes back.
        """
       
        self.points100.unlink(True)
        self.points200.unlink(True)
        self.points300.unlink(True)
        self.points400.unlink(True)
        self.pointsInf.unlink(True)
       
        self.pointDiv.unlink(True)
        self.text.unlink(True)
       
        self.points100 = None
        self.points200 = None
        self.points300 = None
        self.points400 = None
        self.pointsInf = None
       
        self.pointDiv = None
        self.text = None
     
        self.soundPlayer.playTune(buttonSound)
        div.unlink(True)
        self.showTimeMenu()
        
        
    def endClick(self, event):
        """
        Method that determines what happens on a click of the end button.
        """
        self.soundPlayer.playTune(buttonSound)
        self.main.quit()
        
   
   
    def unlinkAll(self):
        """
        Method that unlinks all buttons and labels.
        """        
        self.start.unlink(True)         
        self.score.unlink(True)
        self.qs1.unlink(True)
        self.qs2.unlink(True)
        self.end.unlink(True)
        self.help.unlink(True)
        self.header.unlink(True)
        self.left.unlink(True)
        self.right.unlink(True)
        self.back.unlink(True)
        if self.main.musicEnabled:
            self.mute.unlink(True)
        self.end2.unlink(True)
        self.help2.unlink(True)

    def pulsate(self, node):
        node.opacity=abs(math.sin(time.time()))
                
    def qs1Click(self,event):
        """
        Method that is responsible for starting the game directly, but only if both players pressed their button (this method indicates push of player1).
        """
        self.soundPlayer.playTune(buttonSound)

        if (self.qs1Clicked):
            self.player.clearInterval(self.pulseTimer)
            self.qs2.opacity=1.0
            self.qs1Clicked = False
            self.qs1.opacity = 1.0
        else:
            self.qs1Clicked = True
            self.qs1.opacity = 0.5
            self.qs2.pulsate = True
            self.pulseTimer = self.player.setInterval(0,lambda : self.pulsate(self.qs2))
            
            
            if (self.qs2Clicked):
                self.player.clearInterval(self.pulseTimer)
                self.unlinkAll()
                self.musicPlayer.stop()
                self.main.initGame(self.parentNode, self.highscore, -1, 200) 
    
    
    
    def qs2Click(self,event):
        """
        Method that is responsible for starting the game directly, but only if both players pressed their button (this method indicates push of player2). 
        """
        self.soundPlayer.playTune(buttonSound)
        if (self.qs2Clicked):
            self.player.clearInterval(self.pulseTimer)
            self.qs1.opacity=1.0

            self.qs2Clicked = False
            self.qs2.opacity = 1.0
        else:
            self.qs2Clicked = True
            self.qs2.opacity = 0.5            
            self.pulseTimer = self.player.setInterval(0,lambda : self.pulsate(self.qs1))

            
            if (self.qs1Clicked):
                self.player.clearInterval(self.pulseTimer)
                self.unlinkAll()
                self.musicPlayer.stop()
                self.main.initGame(self.parentNode, self.highscore, -1, 200) 
   
   
    def letHelpAndCloseButtonsAppear(self):
        self.help.sensitive = True
        self.help.href = os.path.join(getMediaDir(__file__, "resources"), "labels/qmark.png")
        self.help.swapHref = os.path.join(getMediaDir(__file__, "resources"), "labels/qmarkGlow.png")   
        avg.LinearAnim(self.help, "pos", 750, self.help.pos, (self.help.pos.x, 0)).start();                                                                                
        
        self.end.sensitive = True
        self.end.href = os.path.join(getMediaDir(__file__, "resources"), "labels/x.png")
        self.end.swapHref = os.path.join(getMediaDir(__file__, "resources"), "labels/xGlow.png")       
        avg.LinearAnim(self.end, "pos", 750, self.end.pos, (self.end.pos.x, 0)).start()                                                                              

        self.help2.sensitive = True;
        self.help2.href = os.path.join(getMediaDir(__file__, "resources"), "labels/qmark.png")
        self.help2.swapHref = os.path.join(getMediaDir(__file__, "resources"), "labels/qmarkGlow.png")
        avg.LinearAnim(self.help2, "pos", 750, self.help2.pos, (self.help2.pos.x, 0)).start();                                                                                
        
        self.end2.sensitive = True;
        self.end2.href = os.path.join(getMediaDir(__file__, "resources"), "labels/x.png")
        self.end2.swapHref = os.path.join(getMediaDir(__file__, "resources"), "labels/xGlow.png")   
        avg.LinearAnim(self.end2, "pos", 750, self.end2.pos, (self.end2.pos.x, 0)).start()                                                                              

    
    def killDivAndMoveMenuIn(self, div):
        """
        Method that unlinks the div and moves the main menu in again
        """    
        div.unlink(True)
        self.letHelpAndCloseButtonsAppear()
        self.moveMenuIn()

                  
    def showTimeMenu(self):
        """
        Method that shows the time menu.
        """
        self.pointsChosen = False
        self.timeDiv = avg.DivNode(id="timerMenu", pos = (0,util.height//16), size=(util.width, util.height//8*7), parent=self.parentNode)
        
        
        self.back.sensitive = True
        self.back.href = os.path.join(getMediaDir(__file__, "resources"), "labels/arrow.png")
        self.back.swapHref = os.path.join(getMediaDir(__file__, "resources"), "labels/arrowGlow.png")
        
        self.text = avg.ImageNode(href=os.path.join(getMediaDir(__file__, "resources"), "labels/max.png"),  parent=self.timeDiv, size=(util.width//10*8, util.height//5)) 
        self.text.pos = ((util.width-self.text.size.x)//2,util.height//20)
        

        self.createTimeMenuButtons(self.timeDiv)
        
        
        
        
    def showPointMenu(self):
        """
        Method that shows the points menu.
        """
        self.timeChosen = False
        self.pointDiv = avg.DivNode(id="pointMenu", pos = (0,util.height//16), size=(util.width, util.height //8*7), parent=self.parentNode)
        
        
        self.back.sensitive = True
        self.back.href = os.path.join(getMediaDir(__file__, "resources"), "labels/arrow.png")
        self.back.swapHref = os.path.join(getMediaDir(__file__, "resources"), "labels/arrowGlow.png")
        
        self.text = avg.ImageNode(href=os.path.join(getMediaDir(__file__, "resources"), "labels/pointsToWin.png"),  parent=self.pointDiv, size=(util.width//10*9, util.height//5)) 
        self.text.pos = ((util.width-self.text.size.x)//2,util.height//20)
            
        self.createPointMenuButtons(self.pointDiv)  
       
            
            
    def showScoreMenu(self):  
        """
        Method that shows the score-menu.
        """
        self.back.setEventHandler(avg.CURSORDOWN, avg.TOUCH | avg.MOUSE, self.fromScoreMenu)
        self.letBackButtonAppear()
        self.highscore.show(self.parentNode)  
        
 
######################  HELP MENU  ############################# 
 
        
    def showHelpMenu(self):
        """
        Method that shows the help menu.
        """
        self.captureHolderLeft=None
        self.captureHolderRight=None
        
        self.letBackButtonAppear()
                
        self.helpDiv = avg.DivNode(id="helpMenu", pos = (0,util.height//32), size=(util.width, util.height//8*7), parent=self.parentNode)
        
        self.helpCounter = 1
        
        self.createHelpMenuButtons(self.helpDiv)
        
        #self.text = avg.WordsNode(font="DejaVu Sans", color="FEFB00", fontsize=util.convertFontSize(80, 100), text = "Help ( 0" + str(self.helpCounter) + "/" + str(maxHelpCounter) + " ) ", parent=self.helpDiv)
        self.text = avg.ImageNode(href=os.path.join(getMediaDir(__file__, "resources"), "labels/help.png"),  parent=self.helpDiv, size=(util.width//3, util.height//8))
        self.text.pos = (util.width//3,0)

        self.innerHelpDiv = avg.DivNode(size = (util.width//3*2, util.height //4*3), pos = (util.width//6,util.height//20*3), parent=self.helpDiv)

        self.backgroundRect = avg.RectNode(size=(util.width//3*2, util.height // 4* 3), pos=(0,0), fillcolor="000000", fillopacity=0.8, parent=self.innerHelpDiv, color="000000")


        self.itemIMG = avg.ImageNode(id="items", sensitive=False, href= os.path.join(getMediaDir(__file__, "resources"), "labels/items.png"), size = (self.innerHelpDiv.size[0],util.height // 20*9), pos  = (0,0), opacity = 0.0, parent=self.innerHelpDiv)
        
        self.content = avg.WordsNode(font="DejaVu Sans", variant="Book", width = util.width*0.55, justify = True, color = "FEFFFF", fontsize = util.convertFontSize(22,42), pos = ((self.innerHelpDiv.size[0]-util.width*0.55)//2,util.height*0.07), parent=self.innerHelpDiv)
        self.contentCentered = avg.WordsNode(font="DejaVu Sans", variant="Book", width = util.width // 5*3, justify = True, alignment="center", color = "FEFFFF", fontsize = util.convertFontSize(25,45), pos = ((self.innerHelpDiv.size[0]-util.width // 5*3)//2,util.height//80), parent=self.innerHelpDiv)
        
         
        self.imageDiv = avg.DivNode(id="imageDiv", size = (util.height//8,util.height //8), pos = (self.innerHelpDiv.size[0]//2 - util.height//8//2,util.height//2), opacity = 0.0, parent=self.innerHelpDiv)
        
        imageBack = self.createButtonBackground(util.helpImageButtonSize)
        self.imageOnBack = self.createButton(util.helpImageMargin, util.helpImageSize, os.path.join(getMediaDir(__file__, "resources"), "circleGood.png"))

        self.imageDiv.appendChild(imageBack)
        self.imageDiv.appendChild(self.imageOnBack)
           
        self.innerHelpDivRight = avg.DivNode(size = (util.width//3*2, util.height // 20*9), pos = (util.width,util.height//20*3), parent=self.helpDiv)
        self.backgroundRectRect = avg.RectNode(size=(util.width//3*2, util.height // 4* 3), pos=(0,0), fillcolor="000000", fillopacity=0.8, parent=self.innerHelpDivRight, color="000000")

        
        self.itemIMGRight = avg.ImageNode(id="itemsRight", sensitive = False, href = os.path.join(getMediaDir(__file__, "resources"), "labels/items.png"), size = (self.innerHelpDiv.size[0],util.height // 20*9), pos=(util.width // 24,util.height//25), opacity = 0.0, parent=self.innerHelpDivRight)

        self.contentRight = avg.WordsNode(font="DejaVu Sans", variant="Book", width = util.width*0.55, justify = True, color = "FEFFFF", fontsize = util.convertFontSize(22,42), pos = ((self.innerHelpDivRight.size[0]-util.width*0.55)//2,util.height*0.07), parent=self.innerHelpDivRight)
        self.contentCenteredRight = avg.WordsNode(font="DejaVu Sans", alignment="center", variant="Book", width = util.width//5*3, justify = True, color = "FEFFFF", fontsize = util.convertFontSize(25,45), pos = ((self.innerHelpDivRight.size[0]-util.width//5*3)//2,util.height // 80), parent=self.innerHelpDivRight)


        self.imageDivRight = avg.DivNode(id="imageDivRight", size = (util.height //8, util.height //8), pos = (self.innerHelpDivRight.size[0]//2 - self.imageDiv.size.x//2,util.height//2), opacity = 0.0, parent=self.innerHelpDivRight)
        

        imageBackRight = self.createButtonBackground(util.helpImageButtonSize)
        self.imageOnBackRight = self.createButton(util.helpImageMargin, util.helpImageSize, os.path.join(getMediaDir(__file__, "resources"), "circleGood.png"))

        self.imageDivRight.appendChild(imageBackRight)
        self.imageDivRight.appendChild(self.imageOnBackRight)
           

        self.innerHelpDivLeft = avg.DivNode(size = (util.width //3*2, util.height // 16*7), pos = (-util.width//3*2,util.height//20*3), parent=self.helpDiv)
        self.backgroundRectLeft = avg.RectNode(size=(util.width//3*2, util.height // 4* 3), pos=(0,0), fillcolor="000000", fillopacity=0.8, parent=self.innerHelpDivLeft, color="000000")

        self.itemIMGLeft = avg.ImageNode(id="itemsLeft", sensitive = False, href = os.path.join(getMediaDir(__file__, "resources"), "labels/items.png"), size = (self.innerHelpDiv.size[0],util.height // 20*9), pos  = (util.width//24,util.height//25), opacity = 0.0, parent=self.innerHelpDivLeft)
        
                           
        self.contentLeft = avg.WordsNode(font="DejaVu Sans", variant="Book", width = util.width*0.55, justify = True, color = "FEFFFF", fontsize = util.convertFontSize(22,42), pos = ((self.innerHelpDivLeft.size[0]-util.width*0.55)//2,util.height*0.07), parent=self.innerHelpDivLeft)
        self.contentCenteredLeft = avg.WordsNode(font="DejaVu Sans", alignment="center", variant="Book", width = util.width // 5*3, justify = True, color = "FEFFFF", fontsize = util.convertFontSize(25,45), pos = ((self.innerHelpDivLeft.size[0]-util.width // 5*3)//2,util.height // 80), parent=self.innerHelpDivLeft)

        self.imageDivLeft = avg.DivNode(id="imageDivLeft", size = (util.height//8, util.height //8), pos = (self.innerHelpDiv.size[0]//2 - self.imageDiv.size.x//2,util.height//2), opacity = 0.0, parent=self.innerHelpDivLeft)
        
        imageBackLeft = self.createButtonBackground(util.helpImageButtonSize)
        self.imageOnBackLeft = self.createButton(util.helpImageMargin, util.helpImageSize, os.path.join(getMediaDir(__file__, "resources"), "circleGood.png"))

        self.imageDivLeft.appendChild(imageBackLeft)
        self.imageDivLeft.appendChild(self.imageOnBackLeft)
           
  
        self.dragDiv = avg.DivNode(size = (util.width, util.height//40*27), pos = (0,util.height // 5), parent=self.parentNode)
        
 
        
        self.dragDiv.setEventHandler(avg.CURSORDOWN,avg.TOUCH | avg.MOUSE, self._startDragging)
        self.dragDiv.setEventHandler(avg.CURSORMOTION,avg.TOUCH | avg.MOUSE, self._doDragging)
        self.dragDiv.setEventHandler(avg.CURSORUP,avg.TOUCH | avg.MOUSE, self._endDragging)

        
        self.displayText(self.content, self.contentCentered, self.imageDiv, self.itemIMG, self.helpCounter, self.imageOnBack)
        self.displayText(self.contentRight, self.contentCenteredRight, self.imageDivRight, self.itemIMGRight, (self.helpCounter%maxHelpCounter)+1, self.imageOnBackRight)
        self.displayText(self.contentLeft, self.contentCenteredLeft, self.imageDivLeft, self.itemIMGLeft, ((self.helpCounter-2)%maxHelpCounter)+1, self.imageOnBackLeft)


    def createButton(self, pos,size, href):
        """      
        Creates a creature field for the help menu.
        """
        return avg.ImageNode(pos=pos, size=size, href=href)


                
    def createButtonBackground(self, size):
        """
        Creates a background for the creatures in the help menu.
        """
        return self.createButton((0,0), size, os.path.join(getMediaDir(__file__, "resources"), "buttonbackground.png"))
        
   
    def displayText(self, content, contentCentered, imageDiv, itemIMG, helpCounter, imageOnBack):
        """
        Method that displays the images and the text in the help menu.
        """
        

        
        if (helpCounter == 1):
            text1 = "GeneaTD is a multi-touch tower defense game for two to four players. The goal is to earn points by increasing the number of creatures that reach your opponent's home base, whilst your opponent defends his area."
            text2 = " This can be done by touching creatures, or by building towers and touching them again so that they explode and destroy the enemy creatures. "
            text3 = " During the game you earn points for building towers, collecting items and spawning or destroying creatures. After collecting enough special items you receive a 'level up' and can use new creatures, towers or skills as described on the following pages. The game ends after a player reaches a set amount of points or after the time limit has been reached. When playing the 'quick start' mode, the goal is to reach 200 points. "
            content.text = text1+"<br/><br/>"+text2+"<br/><br/>"+text3
            itemIMG.opacity = 0.0 
            contentCentered.opacity = 0.0 
            
        elif (helpCounter==2):
            itemIMG.href=os.path.join(getMediaDir(__file__, "resources"), "labels/quickview.png")
            itemIMG.size=(util.width// 2,util.height // 16*9)
            itemIMG.pos = ((self.innerHelpDiv.size[0]-util.width//2)//2, util.height //27)
            itemIMG.opacity=1.0    
            content.text=""   
        
        elif (helpCounter == 3):
            content.text = "Touching your own home base spawns creatures. By touching for longer, you can spawn a creature with additional hit points. "
            imageDiv.opacity = 0.0
            itemIMG.opacity=0.0
            
        elif (helpCounter == 4):
            content.text = "Your standard creatures are 'warriors'. Their special ability is to have up to 8 hit points. "
            imageOnBack.href = os.path.join(getMediaDir(__file__, "resources"), "squareGood.png")
            imageDiv.opacity = 1.0
            
        elif (helpCounter == 5):
            content.text = "After gaining more experience you will be able to spawn 'scouts'. Their special ability is to run very fast, and they have up to 3 hit points. "
            imageOnBack.href = os.path.join(getMediaDir(__file__, "resources"), "triangleGood.png")
            
        elif (helpCounter == 6):
            content.text = "After gaining even more experience you will be able to spawn 'wizards'. They have the ability to teleport, and have up to 2 hit points. "
            imageOnBack.href = os.path.join(getMediaDir(__file__, "resources"), "circleGood.png")
            imageDiv.opacity = 1.0
            
        elif (helpCounter == 7):
            content.text = "Players can build towers by touching the grass field or the wasteland. Each tower requires time to construct - so you have to touch the screen for one second. After a tower is built, a touch on its center will cause an explosion, which has different effects depending on the type of the tower. "
            imageDiv.opacity = 0.0 
            
        elif (helpCounter == 8):
            content.text = unicode("Your standard tower is the 'Circle Tower'. Its explosion range is circular and deals damage to any enemy creatures that are near enough. ")
            imageOnBack.href = os.path.join(getMediaDir(__file__, "resources"), "blackball.png")
            imageDiv.opacity = 1.0      
            
        elif (helpCounter == 9):
            content.text = unicode("After gaining more experience you will be able to build 'Ice Towers'. These have a similar circular damage to the 'Circle Towers' but on explosion they also freeze the creatures around them. ")
            imageOnBack.href = os.path.join(getMediaDir(__file__, "resources"), "iceball.png")
            
        elif (helpCounter == 10):
            content.text = unicode("After gaining even more experience you will be able to build 'Fire Towers'. They have a rectangular explosion range that allows you to damage creatures even while in the opponent's field. Importantly, you can build a lot of these towers side-by-side. ")
            imageOnBack.href = os.path.join(getMediaDir(__file__, "resources"), "fireball.png")
            imageDiv.opacity = 1.0
             
        elif (helpCounter == 11):
            content.text = "The level system is easy to understand. For each 10 experience points (earned by collecting items) you will gain a level up, which unlocks new tower types (level 1 and 5), creature types (level 2 and 6) or improves your damage level (level 3, 7 and 9). "
            imageDiv.opacity = 0.0

        elif (helpCounter == 12):
            content.text = "Your current damage level is indicated by the amount of stars (0, 1, 2 or 3) in your home base. You deal (current level+1) damage to enemy creatures by touching them on your side of the field. "
            imageOnBack.href = os.path.join(getMediaDir(__file__, "resources"), "labels/star.png")
            imageDiv.opacity = 1.0

                     
        elif (helpCounter==13):
            content.text = "During the game you gain points for different actions and events. For each creature you spawn, you earn 5 points, for every one of your opponent's creatures you destroy 10 points. Every regular tower explosion gives you 25 points. In addition, you can earn additional points by collecting items as they appear (see following pages for details). After the game has ended you also get 10 points for every creature that reached your opponent's home base and another 10 points for every experience point you have. "
            imageDiv.opacity = 0.0

        elif (helpCounter == 14):
            content.text = unicode("Every few seconds an item appears somewhere on the field. You should collect all items (only the 'Armageddon' item could be harmful in some situations) to earn points and obtain special items (see next page). You can collect items by dragging them into your home base or storing them in your item bunkers for later use. ")
            itemIMG.opacity = 0.0
                     
        elif (helpCounter == 15):
            content.text = ""
            itemIMG.size = (self.innerHelpDiv.size[0],util.height // 20*9)
            itemIMG.pos  = (0,util.height // 27)

            itemIMG.opacity = 1.0
            itemIMG.href = os.path.join(getMediaDir(__file__, "resources"), "labels/items.png")    

        elif (helpCounter == 16):
            content.text = ""
            itemIMG.size =  (self.innerHelpDiv.size[0],util.height // 20*9)
            itemIMG.pos  = (0,util.height //27)

            itemIMG.opacity = 1.0
            itemIMG.href = os.path.join(getMediaDir(__file__, "resources"), "labels/items2.png")     
            
            contentCentered.opacity = 0.0

        elif (helpCounter == 17):
            content.text = ""
            contentCentered.opacity = 1.0
            contentCentered.text = """This game was written by<br/><br/>
                    <big>Frederic Kerber<br/>
                    Pascal Lessel<br/>
                    Michael Mauderer<br/>
                    <br/></big>
                    <small>
                    Support:<br/>
                    Ulrich von Zadow<br/>
                    Johannes Schöning<br/>
                    DFKI GmbH<br/>
                    University of Saarland<br/></small>
                    <br/>
                    GeneaTD is based on libavg (www.libavg.de)<br/>"""
            contentCentered.pos = (self.innerHelpDiv.size.x//2,self.innerHelpDiv.size.y -content.getMediaSize().y - contentCentered.getMediaSize().y)
            contentCentered.y = util.height*0.07
           

            itemIMG.opacity = 0.0
            
        elif (helpCounter == 18):
            content.text = unicode("There are two hotkeys in the game. Pressing 'q' while fighting will immediately end the fight and pressing 'n' will mute the sound.")

            contentCentered.opacity = 1.0
            contentCentered.text = unicode("For more information check out our web pages <br/><br/> www.geneatd.de <br/>  www.dfki.de/geneatd <br/><br/> or write us an e-mail: <br/><br/>info@geneatd.de")
            contentCentered.pos = (self.innerHelpDiv.size.x//2,self.innerHelpDiv.size.y -content.getMediaSize().y - contentCentered.getMediaSize().y)

            itemIMG.opacity = 0.0 
      
    def hbackClickWrapper(self, event):  
        self.soundPlayer.playTune(buttonSound)
        self.hbackClick(event)
        
    def hforwardClickWrapper(self, event):
        self.soundPlayer.playTune(buttonSound)
        self.hforwardClick(event)
               
    def hbackClick(self,event):
        """
        Method that determines what happens on a click on the < in the help menu.
        """
        if (self.helpCounter > 1):
            self.helpCounter -= 1
            if (self.helpCounter < 10):
                self.text.text = "Help ( 0" + str(self.helpCounter) + "/" + str(maxHelpCounter) + " ) "
            else:
                self.text.text = "Help ( " + str(self.helpCounter) + "/" + str(maxHelpCounter) + " ) "
            self.displayText(self.content, self.contentCentered, self.imageDiv, self.itemIMG, self.helpCounter, self.imageOnBack)
            self.displayText(self.contentRight, self.contentCenteredRight, self.imageDivRight, self.itemIMGRight, (self.helpCounter%maxHelpCounter)+1, self.imageOnBackRight)
            self.displayText(self.contentLeft, self.contentCenteredLeft, self.imageDivLeft, self.itemIMGLeft, ((self.helpCounter-2)%maxHelpCounter)+1, self.imageOnBackLeft)

        elif (self.helpCounter == 1):
            self.helpCounter = maxHelpCounter
            self.text.text = "Help ( " + str(self.helpCounter) + "/" + str(maxHelpCounter) + " ) "
            self.displayText(self.content, self.contentCentered, self.imageDiv, self.itemIMG, self.helpCounter, self.imageOnBack)
            self.displayText(self.contentRight, self.contentCenteredRight, self.imageDivRight, self.itemIMGRight, (self.helpCounter%maxHelpCounter)+1, self.imageOnBackRight)
            self.displayText(self.contentLeft,self.contentCenteredLeft, self.imageDivLeft, self.itemIMGLeft, ((self.helpCounter-2)%maxHelpCounter)+1, self.imageOnBackLeft)

    
    def hforwardClick(self,event):
        """
        Method that determines what happens on a click on the > in the help menu.
        """
        if (self.helpCounter < maxHelpCounter):
            self.help
            self.helpCounter += 1
            if (self.helpCounter < 10):
                self.text.text = "Help ( 0" + str(self.helpCounter) + "/" + str(maxHelpCounter) + " ) "
            else:
                self.text.text = "Help ( " + str(self.helpCounter) + "/" + str(maxHelpCounter) + " ) "
            self.displayText(self.content, self.contentCentered, self.imageDiv, self.itemIMG, self.helpCounter, self.imageOnBack)
            self.displayText(self.contentRight, self.contentCenteredRight, self.imageDivRight, self.itemIMGRight, (self.helpCounter%maxHelpCounter)+1, self.imageOnBackRight)
            self.displayText(self.contentLeft, self.contentCenteredLeft, self.imageDivLeft, self.itemIMGLeft, ((self.helpCounter-2)%maxHelpCounter)+1, self.imageOnBackLeft)

        elif (self.helpCounter == maxHelpCounter):
            self.helpCounter = 1
            self.text.text = "Help ( 0" + str(self.helpCounter) + "/" + str(maxHelpCounter) + " ) "
            self.displayText(self.content, self.contentCentered, self.imageDiv, self.itemIMG, self.helpCounter, self.imageOnBack)
            self.displayText(self.contentRight, self.contentCenteredRight, self.imageDivRight, self.itemIMGRight, (self.helpCounter%maxHelpCounter)+1, self.imageOnBackRight)
            self.displayText(self.contentLeft,  self.contentCenteredLeft, self.imageDivLeft, self.itemIMGLeft, ((self.helpCounter-2)%maxHelpCounter)+1, self.imageOnBackLeft)

        
         
    def _startDragging(self, event):
        """
        Starts the dragging of the dragging div.
        Needed for "sliding" in the help menu.
        """
        if self.captureHolderLeft is None:
            self.captureHolderLeft=event.cursorid
            self.dragOffsetXLeft = self.dragDiv.pos.x - event.pos.x
            self.dragOffsetXInner = self.innerHelpDiv.pos.x - event.pos.x
            self.dragOffsetXInnerRight = self.innerHelpDivRight.pos.x - event.pos.x
            self.dragOffsetXInnerLeft = self.innerHelpDivLeft.pos.x - event.pos.x
            event.node.setEventCapture(event.cursorid)
            
    
    def _doDragging(self, event):
        """
        Does the dragging.
        Needed for "sliding" in the help menu.
        """
        if event.cursorid==self.captureHolderLeft:
            self.dragDiv.pos=(event.pos.x+self.dragOffsetXLeft, self.dragDiv.pos.y)
            self.innerHelpDiv.pos=(event.pos.x+self.dragOffsetXInner, self.innerHelpDiv.pos.y)
            self.innerHelpDivRight.pos=(event.pos.x+self.dragOffsetXInnerRight, self.innerHelpDivRight.pos.y)
            self.innerHelpDivLeft.pos=(event.pos.x+self.dragOffsetXInnerLeft, self.innerHelpDivLeft.pos.y)
    
    def resetDivsFor(self, event):
        self.innerHelpDiv.pos = (util.width//6,util.height//20*3)
        self.innerHelpDivRight.pos = (util.width, util.height//20*3)
        self.innerHelpDivLeft.pos = (-util.width//3*2, util.height//20*3)
        self.hforwardClick(event)
        self.dragDiv.pos=(0,util.height // 5)
        self.dragDiv.sensitive=True
        self.hback.sensitive=True
        self.hforward.sensitive = True        
 
    def resetDivsBack(self, event):
        self.innerHelpDiv.pos = (util.width//6,util.height//20*3)
        self.innerHelpDivRight.pos = (util.width,util.height//20*3)
        self.innerHelpDivLeft.pos = (-util.width//3*2,util.height//20*3)
        self.hbackClick(event)
        self.dragDiv.pos=(0,util.height // 5)
        self.dragDiv.sensitive=True
        self.hback.sensitive=True
        self.hforward.sensitive = True

 
    
    def _endDragging(self, event):
        """
        End the dragging of the dragging div.
        Needed for "sliding" in the help menu.
        """
        if event.cursorid==self.captureHolderLeft:
            event.node.releaseEventCapture(event.cursorid)
            self.captureHolderLeft=None
            if self.dragDiv.pos.x < -util.width // 24:
                self.dragDiv.sensitive=False
                self.hback.sensitive=False
                self.hforward.sensitive = False
                avg.LinearAnim(self.innerHelpDiv, "pos", 500, self.innerHelpDiv.pos, (-util.width //3*2,util.height//20*3)).start()
                avg.LinearAnim(self.innerHelpDivRight, "pos", 500, self.innerHelpDivRight.pos, (util.width//6,util.height//20*3), False, None, lambda: self.resetDivsFor(event)).start()
                
            elif self.dragDiv.pos.x > util.width // 24: 
                self.dragDiv.sensitive=False
                self.hback.sensitive=False
                self.hforward.sensitive = False
                avg.LinearAnim(self.innerHelpDiv, "pos", 500, self.innerHelpDiv.pos, (util.width,util.height//20*3)).start()
                avg.LinearAnim(self.innerHelpDivLeft, "pos", 500, self.innerHelpDivLeft.pos, (util.width//6,util.height//20*3), False, None, lambda: self.resetDivsBack(event)).start()


                
