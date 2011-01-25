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

from tower import Tower
import math
import os
import util
from libavg import *
from libavg.AVGAppUtil import getMediaDir

class IndyTower(Tower):
    """
    This class represents an indy tower object.
    """

    def executeTowerDestroyAnimation(self):
        """
        The animation that happens if tower is clicked. Should call the die method afterwards.
        """
        self.explosionRect = avg.RectNode(fillopacity=0.0, color="FF4500", strokewidth=2, pos=(self.tower.size.x//2, util.towerSize[0]//10), size=(0, self.towerDiv.size.y-util.towerSize[0] //5), parent=self.towerDiv)
        
        anim = avg.LinearAnim(self.explosionRect,"size" ,300, (0,self.explosionRect.size.y), (self.towerSquare.size.x - util.towerSize[0] // 10, self.towerSquare.size.y), False, None, self.die)
        anim.start()

    def executeTowerEffect(self, creatureList):
        """
        Executes the special tower effect on the creatures that are given.
        """
        side = 1
        if self.team.id==2:
            side = -1
        for creature in creatureList:

            if (self.checkCreatureInAreaOfEffect(creature,side)):
                creature.damage(3)
                
          
    
    def checkCreatureInAreaOfEffect(self, creature, side):
        """
        Checks whether a creature is in range of the area of effect.
        """
        xPos = self.towerDiv.pos.x + self.tower.size.x/2
        yPos = self.towerDiv.pos.y
        
        
        x=0
        if side==-1:
            x = creature.creature.r*2
       
        checkX = (side * xPos <= side * creature.pos.x-x  <= side * (xPos + side * self.towerDiv.size.x-util.towerSize[0] //2))
        checkY = (yPos-creature.creatureDiv.size.y <= creature.pos.y  <= yPos + self.towerDiv.size.y)
        
        return checkX and checkY


    def setAppearance(self):
        """
        A setter for the appearance of the tower.
        """
             
              
        self.tower = avg.RectNode(fillopacity=1, strokewidth=0, size=util.towerSize, pos=(self.pos.x-util.towerSize[0]//2, self.pos.y-util.towerSize[1]//2),filltexhref = os.path.join(getMediaDir(__file__, "resources"), "fireball.png"))
        
    
        
        if self.team.name == "Team2":
            self.towerDiv = avg.DivNode(size=util.indyTowerDivSize, pos=(self.pos.x - self.tower.size.x//2, self.pos.y - self.tower.size.y//2), pivot=(self.tower.size.x//2,self.tower.size.y//2), angle = math.pi)
            self.towerSquare = avg.RectNode(fillopacity=0.3, strokewidth=0, fillcolor=self.team.color, size = (self.towerDiv.size.x,self.towerDiv.size.y-util.towerSize[0] // 5), pos = (self.tower.size.x//2, util.towerSize[0] // 10), parent=self.towerDiv)

        else:
            
            self.towerDiv = avg.DivNode(size = util.indyTowerDivSize, pos = (self.pos.x - self.tower.size.x//2, self.pos.y - self.tower.size.y//2))
            self.towerSquare = avg.RectNode(fillopacity=0.3, strokewidth=0, fillcolor = self.team.color, size = (self.towerDiv.size.x,self.towerDiv.size.y-util.towerSize[0] // 5), pos = (self.tower.size.x//2, util.towerSize[0] // 10), parent=self.towerDiv)



    def __init__(self, team, pos, layer, creatureLayer):
        """
        Creates a new ice tower instance (including libAVG nodes).
        team: the team, the tower belongs to.
        pos: the position of the tower.
        layer: the layer the tower should be placed on.
        """
        Tower.__init__(self, team, pos, layer, creatureLayer)
        