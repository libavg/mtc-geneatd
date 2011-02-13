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
from libavg.AVGAppUtil import getMediaDir
from creature import Creature
import os
import util

class Tower(object):
    """
    This class represents a normal tower object.
    """
    
    # A Map of all towers: id --> object.
    towers = {}
       
    # All creatures of player 1.
    tower1 = []
    
    # All creatures of player 2.
    tower2 = []
        
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

            del Tower.towers[id(self)]
            self.towerDiv.unlink(True)
            self.tower.unlink(True)
            self.team.adjustScore(25)

    def getDistance(self, creature):
        """
        Returns the distance from the given creature to the tower.
        """
        return mathutil.getDistance(self.pos, creature.getCirclePos())
    
    def getCreaturesInExplosionRange(self):
        """
        A getter for the creatures in range that should be affected.
        """
        creatureList = Creature.creatures2
        if self.team.id == 2:
            creatureList = Creature.creatures1
        return creatureList[:]

    def executeTowerEffect(self, creatureList):
        """
        Executes the special tower effect on the creatures that are given.
        """
        for creature in creatureList:
            dist = self.getDistance(creature)
            if dist > self.towerCircle.r + creature.r:
                continue
            else:
                creature.damage(2)
    
    def executeTowerDestroyAnimation(self):
        """
        The animation that happens if tower is clicked. Should call the die method afterwards.
        """
        self.explosionCircle = avg.CircleNode(fillopacity=0.0, strokewidth=2, color=self.destroyCircleColor, pos=(self.towerDiv.size.x // 2, self.towerDiv.size.x // 2), parent=self.towerDiv)

        anim = avg.LinearAnim(self.explosionCircle, "r", 300 , self.tower.size.x // 2, self.towerCircle.r, False, None, self.die)
        anim.start()
        
    def towerExplosion(self, event):
        """
        Boom.
        """
        if not self.alreadyExploded:
            self.alreadyExploded = True
            self.towerDiv.sensitive = False
            creatureList = self.getCreaturesInExplosionRange()
            self.executeTowerEffect(creatureList)
            self.executeTowerDestroyAnimation()
        
    
    def setAppearance(self):
        """
        A setter for the appearance of the tower.
        """
        self.towerDiv = avg.DivNode(size=util.towerDivSize, pos=(self.pos.x - util.towerDivSize[0] // 2, self.pos.y - util.towerDivSize[1] // 2))
        
        #sets the explosion radius
        self.towerCircle = avg.CircleNode(fillopacity=0.3, strokewidth=0, fillcolor=self.team.color, r=self.towerDiv.size.x // 2, pos = (self.towerDiv.size.x // 2, self.towerDiv.size.y // 2), parent=self.towerDiv)

        self.tower = avg.RectNode(fillopacity=1, strokewidth=0, filltexhref=os.path.join(getMediaDir(__file__, "resources"), "blackball.png"), size=util.towerSize, pos=(self.pos.x - util.towerSize[0] // 2, self.pos.y - util.towerSize[1] // 2))
        
         
        
    def __init__(self, team, pos, layer, creatureLayer):
        """
        Creates a new tower instance (including libAVG nodes).
        g_player: the global libAVG player.
        team: the team, the tower belongs to.
        pos: the position of the tower.
        layer: the layer the tower should be placed on.
        """
        self.living = True
        self.pos = pos
        self.team = team
        self.layer = layer
        self.setAppearance()
        self.alreadyExploded =False
     
        self.destroyCircleColor="FFA500"
     
        tid = id(self)
        self.towerDiv.id = str(tid)
        Tower.towers[tid] = self
        
        if self.team.name == "Team2":
            Tower.tower2.append(self)
        else:
            Tower.tower1.append(self)
       
         
        self.tower.setEventHandler(avg.CURSORDOWN, avg.TOUCH | avg.MOUSE, self.towerExplosion)   
        
        creatureLayer.appendChild(self.tower)
        layer.appendChild(self.towerDiv)
