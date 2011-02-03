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
import util

class Team(object):
    """
    This class represents a team.
    """
   
      
    def __init__(self, color, name, homeArea, targetX, direction, id, baseArea, main, maxPoints):
        """ 
        Creates a  new instance of a team (including some libAVG nodes).
        color: the color of the team.
        name: the name of the team.
        homeArea: (x1, x2) begin and end of the home area.
        targetX: the beginning of the opponents home area.
        direction: 1/-1  - depending on the side of the player
        id: the id of the team.
        """
        self.maxPoints = maxPoints
        self.main = main
        self.level = 0
        self.baseArea = baseArea
        self.myOwnViewPointNode = avg.WordsNode(font="DejaVu Sans", text="000", variant="Bold", fontsize=util.convertFontSize(26), color=color, pivot=(0,0))
        self.enemyPointNode = avg.WordsNode(font="DejaVu Sans", text="000", variant="Bold", fontsize=util.convertFontSize(26), color=color, pivot=(0,0))

        if direction==1:
            self.myOwnViewPointNode.pos = (util.halfwidth + self.myOwnViewPointNode.getMediaSize()[0]//2, 2)
            self.myOwnViewPointNode.angle=math.pi/2
            
         
            
            self.enemyPointNode.pos = (util.halfwidth - self.myOwnViewPointNode.getMediaSize()[0]//2, util.height//10*9)
            self.enemyPointNode.angle=-math.pi/2

        else:
            self.myOwnViewPointNode.pos = (util.halfwidth - self.myOwnViewPointNode.getMediaSize()[0]//2, util.height-2)
            self.myOwnViewPointNode.angle=-math.pi/2

         
            self.enemyPointNode.pos = (util.halfwidth + self.myOwnViewPointNode.getMediaSize()[0]//2, util.height//10)
            self.enemyPointNode.angle=math.pi/2
 
        self.currentDamageLevel = 1
        
        self.color=color
        self.name=name
        self.homeArea = homeArea
        self.targetX = targetX
        self.direction = direction
        self._points = 0
        self._exp = 0
        self.score = 0
        self.id = id
        self.itemCounter = {}
        
        
    def appendScoreNodes(self, parentNode):
        parentNode.appendChild(self.myOwnViewPointNode)
        parentNode.appendChild(self.enemyPointNode)

        
    def _getPoints(self):
        """
        Getter for the points.
        """
        return self._points
     
    def _setPoints(self, value):
        """
        Setter for the points.
        """
        self._points=value
        self.myOwnViewPointNode.text="%03i" % self._points
        self.enemyPointNode.text="%03i" % self._points 
        if not (self.maxPoints == -1):
            if (self._points>=self.maxPoints):
                self.main.parentNode.sensitive=False
                self.main.endGame();
        
    points = property(_getPoints, _setPoints)
    
    
    
    
    def adjustScore(self, value):
        """
        Adjusts the score by the given value.
        """
        self.score = self.score + value
        
    def adjustExp(self, value):
        """
        Adjusts the experience of the player and calls the skill lock/unlock method in game.
        """
        self.adjustingExp = True
        if (self.level == 9 and value > 0):
            return
        elif (self.level == 0 and value < 0 and abs(value) > self._exp):
            value = -self._exp   #back to zero exp.
        
        oldExp = self._exp
        self._exp = self._exp + value

        if (self.id == 1):
            
            if (value > 0):
                for i in range(0, value):
                    self.main.expBar1.inc()
            else:
                for i in range(0, abs(value)):
                    self.main.expBar1.dec()
                                    
            if ((self._exp / 10) != (oldExp / 10)):
                self.level = self.level + 1 if value > 0 else self.level - 1
                self.main.expBar1.blink()
                self.main.adjustSkills(self, value>0)
                    
                    
        else:
            if (value > 0):
                for i in range(0, value):
                    self.main.expBar2.inc()
            else: 
                for i in range(0, abs(value)):
                    self.main.expBar2.dec()
                                    
            if ((self._exp / 10) != (oldExp / 10)):
                self.level = self.level + 1 if value > 0 else self.level - 1
                self.main.expBar2.blink()
                self.main.adjustSkills(self, value>0)
        
        
    
       
    def checkHomeArea(self, x, y):
        """
        Checks, if the given x coordinate is in the home area.
        """
        x1,x2 = self.homeArea
        return x>=x1 and x<=x2 and y>=util.sideBarheight and y<=util.height-util.sideBarheight


    def checkBaseArea(self, x, y):
        """
        Checks, if the given x coordinate is in the home area.
        """
        x1,x2 = self.baseArea
        return x>=x1 and x<=x2 and y>=util.sideBarheight and y<=util.height-util.sideBarheight
