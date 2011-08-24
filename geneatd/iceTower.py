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
import random
import math
import util
import os
from libavg import *
from libavg.utils import getMediaDir


class IceTower(Tower):
    """
    This class represents an ice tower object.
    """
    
    snowballTime = 5000
    freezeDuration = 5000
    
    
    
    
    def die(self):
        """
        This method destroys the tower (unlinks the libAVG node).
        """
        if self.living:
            self.living = False        
            if self.team.id==1:
                self.tower1.remove(self)
            else:
                self.tower2.remove(self)

            for x in self.snowballAnimsList:
                x.abort()
                self.snowballAnimsList.remove(x)
                del x
    
            del Tower.towers[id(self)]
            self.towerDiv.unlink(True)
            self.tower.unlink(True)
            self.team.adjustScore(25)
    
    def executeTowerEffect(self, creatureList):
        """
        Executes the special tower effect on the creatures that are given.
        """
        for creature in creatureList:
            dist = self.getDistance(creature)
            if dist > self.towerCircle.r + creature.r:
                continue
            else:
                creature.freeze(self.freezeDuration)
                creature.damage(1)

    
    def snowballAnim(self,xPos, yPos, snowball):
        """
        A method that is responsible for the snow ball movement.
        """
        size = self.towerDiv.size
       
        newXPos = random.randint(0 + math.floor(snowball.r), math.ceil(size.x - snowball.r))
        newYPos = random.randint(0 + math.floor(snowball.r), math.ceil(size.y - snowball.r))
        anim = avg.LinearAnim(snowball, "pos", self.snowballTime, (xPos,yPos), (newXPos, newYPos), False, None, lambda: self.snowballAnim(newXPos, newYPos, snowball))
        
        self.snowballAnimsList.append(anim)
        anim.start()
        

    def setAppearance(self):
        """
        A setter for the appearance of the tower.
        """
        self.towerDiv = avg.DivNode(size=util.towerDivSize, pos=(self.pos.x - util.towerDivSize[0]//2, self.pos.y-util.towerDivSize[1]//2))
        
        #sets the explosion radius
        self.towerCircle = avg.CircleNode(fillopacity=0.3, strokewidth=0, fillcolor=self.team.color, r=self.towerDiv.size.x//2, pos=(self.towerDiv.size.x//2,self.towerDiv.size.y//2), parent=self.towerDiv)
        
        
        #sets the fancy snow balls
        
        for i in xrange(5):
            radius = self.towerDiv.size[0]//10
            xPos = random.randint(0 + math.floor(radius), math.ceil(self.towerDiv.size.x - radius))
            yPos = random.randint(0 + math.floor(radius), math.ceil(self.towerDiv.size.y - radius))
            
            snowball = avg.CircleNode(fillopacity=0.5, strokewidth=0, filltexhref=os.path.join(getMediaDir(__file__, "resources"), "snowflakes.png"), r=radius, pos=(xPos,yPos), parent=self.towerDiv)
            
            self.snowballAnim(xPos,yPos,snowball)
            
        
        self.tower = avg.RectNode(fillopacity=1, strokewidth=0, size=util.towerSize, pos=(self.pos.x  - util.towerSize[0] // 2, self.pos.y - util.towerSize[1] // 2))
        
        
        if self.team.name == "Team2":
            self.tower.filltexhref = os.path.join(getMediaDir(__file__, "resources"), "iceball.png")
        else:
            self.tower.filltexhref = os.path.join(getMediaDir(__file__, "resources"), "iceball.png")
            
        

    def __init__(self, team, pos, layer, creatureLayer):
        """
        Creates a new ice tower instance (including libAVG nodes).
        team: the team, the tower belongs to.
        pos: the position of the tower.
        layer: the layer the tower should be placed on.
        """
        self.snowballAnimsList = []
        Tower.__init__(self, team, pos, layer,  creatureLayer)
        self.destroyCircleColor = "00BFFF"
        
        
        
