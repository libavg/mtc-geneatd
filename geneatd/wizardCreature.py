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
from creature import Creature
import random
import os
from libavg.AVGAppUtil import getMediaDir
import util


moveTime = 3000 
opacityTime = 1000



class WizardCreature(Creature):      
    """
    This class represents a wizard creature.
    """
    
    def __init__(self, g_player, team, enemy,  pos, layer, when, main, inActiveLayer, maxHitPoints = 8):
        """
        Creates a new wizard creature (including the libAVG nodes).
        g_player: the global player instance.
        team: the team, the creature should belong to.
        pos: the initial position.
        layer: the layer to put the creature on.
        when: the moment, the creation has been started.
        """
        self.maxJumpDistance = util.halfwidth // 2
        self.goalXPos = self.maxJumpDistance
        self.freezed = False
        self.shouldDie = False
        self.firstJump = True
        self.appearAnim = None
        self.disappearAnim = None
        Creature.__init__(self, g_player, team, enemy, pos, layer, when, main, inActiveLayer, maxHitPoints)
        if self.team.name == "Team2":
            self.creature.filltexhref = os.path.join(getMediaDir(__file__, "resources"), "circleEvil.png")
        else:
            self.creature.filltexhref = os.path.join(getMediaDir(__file__, "resources"), "circleGood.png")

        
        
    def _delete(self):
        """
        Removes the creature from the creature "lists" and unlinks the libAVG node.
        """              
        if self.team.id==1:
            self.creatures1.remove(self)
        else:
            self.creatures2.remove(self)
        del Creature.creatures[id(self)]
        self.creatureDiv.unlink(True) 


    def die(self):
        """
        This method is called if a creatures is destroyed on the field.
        """

        if self.state=="RUNNING":
            self.state="DEAD" 
            if (self.disappearAnim != None):
                self.disappearAnim.abort()
            
            if (self.appearAnim != None):
                self.appearAnim.abort()
            
            del self.disappearAnim    
            del self.appearAnim 
            
            self.player.clearInterval(self.portTimer)
            
            
            self.team.adjustScore(10)
            self._delete()  


        
    def _appear(self):
        """
        This method lets the wizard appear on the new position.
        """
        
        if self.state=="RUNNING":
            if self.firstJump:
                self.firstJump = False
                self.creatureDiv.unlink(False)
                self.inActiveLayer.appendChild(self.creatureDiv)
    
    
            oldXPos = self.goalXPos- self.maxJumpDistance
            self.goalXPos = self.creatureDiv.pos.x+3*self.speed*self.team.direction
            self.goalXPos-=random.randint(0, self.maxJumpDistance//4)
            newXPos = self.goalXPos-self.maxJumpDistance

            if oldXPos * newXPos < 0:
                self.creatureDiv.unlink(False)
                self.activeLayer.appendChild(self.creatureDiv)
    
    
            if -self.team.direction* self.goalXPos < -self.team.direction*self.targetX:
                self.creatureDiv.pos= (self.targetX,random.randint(util.sideBarheight,util.height-util.sideBarheight-self.creatureDiv.size.y))
                if not self.freezed:
                    self.appearAnim = avg.LinearAnim(self.creatureDiv, "opacity", opacityTime, 0,1, False, None, self._runningStopped)
                else:
                    self.appearAnim = avg.LinearAnim(self.creatureDiv, "opacity", opacityTime, 0,1)
                    self.shouldDie = True
                self.appearAnim.start()
                self.player.clearInterval(self.portTimer)
            else:
                self.creatureDiv.pos= (self.goalXPos,random.randint(util.sideBarheight,util.height-util.sideBarheight-self.creatureDiv.size.y))
                self.appearAnim = avg.LinearAnim(self.creatureDiv, "opacity", opacityTime, 0,1)
                self.appearAnim.start()

        
    def _disappear(self):
        """
        This method lets the wizard disappear.
        """
        if not self.freezed:
            self.disappearAnim = avg.LinearAnim(self.creatureDiv, "opacity", opacityTime, 1,0, False, None, self._appear)
            self.disappearAnim.start()
 
    
    def _startRunning(self):
        """
        Starts the movement of the creature.
        """
        self.targetX = self.team.targetX-(2*self.creature.r if self.team.direction==1 else 0)
        self.state="RUNNING"
        self.portTimer = self.player.setInterval(moveTime, self._disappear) 
        self._disappear()
        
        
    def _startMoving(self):
        """
        Starts the linear running anim after a freezing.
        """
        self.freezed=False
        if self.shouldDie:
            self._runningStopped()
        
        
    def freeze(self, time):
        """
        Freezes the creature for the given time.
        """
        self.freezed=True
        self.freezeTimer = self.player.setInterval(time, self._startMoving) 
        
