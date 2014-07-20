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
import util
import time
from hp import HP
import os
from libavg.utils import getMediaDir



class Creature(object):      
    """
    This class represents a creature.
    """

    # Map of all creatures id --> object.
    creatures = {}
    
    # All creatures of player 1.
    creatures1 = []
    
    # All creatures of player 2.
    creatures2 = []
    


    def _runningStopped(self):
        """
        This method is called, if the linearAnim that moves the creature stops.
        """
        if self.state == "RUNNING" and self.pos.x == self.targetX :
            self.state="DEAD"
            duration = 1000
    
            if not self.main.isGameOver(): 
                self.team.points+=self.hitPoints

            self.creatureDiv.sensitive=False
            middlepoint = (self.pos.x +self.creatureDiv.size.x//2, self.pos.y +self.creatureDiv.size.y//2) 
            self.creatureDiv.size = (self.creatureDiv.size.x*3, self.creatureDiv.size.y*3)
            self.creature.pos = (self.creatureDiv.size.x//2,self.creatureDiv.size.y//2)

            self.pos = (middlepoint[0]-self.creatureDiv.size.x//2,middlepoint[1]-self.creatureDiv.size.y//2) 

            self._hp.hide()
            avg.LinearAnim(self.creatureDiv, "pos", duration, self.creatureDiv.pos , (self.pos.x + self.team.direction * 3*self.creature.r, self.pos.y)).start()
            avg.LinearAnim(self.creature, "r", duration, self.creature.r, self.creature.r*3).start()
            avg.LinearAnim(self.creature, "fillopacity", duration,   self.creature.fillopacity, 0, False, None, self._delete).start()       
   
  
        
    def _delete(self):
        """
        Removes the creature from the creature "lists" and unlinks the libAVG node.
        """
        if self.team.id==1:
            self.creatures1.remove(self)
        else:
            self.creatures2.remove(self)
        del Creature.creatures[id(self)]
        del self.runningAnim
        if (self.freezeTimer is not None):
            self.player.clearInterval(self.freezeTimer)

        self.creatureDiv.unlink(True) 
 
 
    def _switchToActiveLayer(self):
        """
        Changes the layer the creature is running on.
        """
        if self.state=="RUNNING" and self.pos.x==util.halfwidth:
            self.targetX = self.team.targetX-(2*self.creature.r if self.team.direction==1 else 0)
            runningTime = self._calcTime()
            self.creatureDiv.unlink(False)
            self.activeLayer.appendChild(self.creatureDiv)
            self.runningAnim = avg.LinearAnim(self.creatureDiv, "pos", runningTime, (self.pos.x,self.pos.y), (self.targetX,self.pos.y),False, None, self._runningStopped)
            self.runningAnim.start()

        
    def _switchToInActiveLayer(self):
        """
        Changes the layer the creature is running on.
        """
        if self.team.id==1:
            self.testX = util.basewidth
        else:
            self.testX = util.rightBasePos[0]-self.creatureDiv.size.x
        
        if self.pos.x == self.testX:
            self.creatureDiv.unlink(False)
            self.inActiveLayer.appendChild(self.creatureDiv)
            self.targetX = util.halfwidth
            
            runningTime = self._calcTime()
            self.runningAnim = avg.LinearAnim(self.creatureDiv, "pos", runningTime, (self.pos.x,self.pos.y), (self.targetX,self.pos.y),False, None, self._switchToActiveLayer)
            self.startTime = time.time()
            self.runningAnim.start()
 
        
    
    def _startRunning(self):
        """
        Starts the movement of the creature.
        """
        if(self.state == "BIRTH"):
            self.state = "RUNNING"
          
            if self.team.id==1:
                self.targetX = util.basewidth
            else:
                self.targetX = util.rightBasePos[0]-self.creatureDiv.size.x
            runningTime = self._calcTime()
            self.runningAnim = avg.LinearAnim(self.creatureDiv, "pos", runningTime, (self.pos.x,self.pos.y), (self.targetX,self.pos.y),False, None, self._switchToInActiveLayer)
            self.startTime = time.time()
            self.runningAnim.start()
  
    
    def _mouseUp(self,event):
        """
        Stops the birth process.
        """
        if self.state == "BIRTH":
            self.player.clearInterval(self.timer)
            self._startRunning()
            
     
    def _setPos(self, value):
        """
        Setter for the position of the libAVG node.
        """
        self.creatureDiv.pos = value
    
    def  _getPos(self):
        """
        Getter for the position of the libAVG node.
        """
        return self.creatureDiv.pos
    
    pos = property(_getPos, _setPos)   
    
    
    def _setHP(self, value):
        """
        Setter for the HP of the creature.
        """
        self._hp.hp = value
    
    def  _getHP(self):
        """
        Getter for the HP of the creature.
        """
        return self._hp.hp
    
    hitPoints = property(_getHP, _setHP)

    
    
    
    def _hitPointTimer(self):
        """
        This method is called by the timer for the creation of the creature.
        Increases the amount of pie pieces and the hit points.
        """
        if self.i<self.maxHitPoints-2: 
            self.i+=1
            self.hitPoints += 1
        else:
            self.hitPoints += 1
            self.player.clearInterval(self.timer)
            self._startRunning() 
        
        
        
    
    def __init__(self, g_player, team, enemy,  pos, layer, when, main, inActiveLayer, maxHitPoints = 8):
        """
        Creates a new creature (including the libAVG nodes).
        g_player: the global player instance.
        team: the team, the creature should belong to.
        pos: the initial position.
        layer: the layer to put the creature on.
        when: the moment, the creation has been started.
        """
        global creatures
        self.runningAnim = None
        self.enemy = enemy
        self.circlePos=pos 
        self.activeLayer = layer
        self.inActiveLayer = inActiveLayer
        self.main = main
        self.maxHitPoints = maxHitPoints
        self.layer = layer
        self.speed = util.width //20
        self.state = "BIRTH" 
        self.when = when 
        self.team = team
        self.i = 0
        self.freezeTimer = None


        cid = id(self)
        self.creatureDiv = avg.DivNode(id = str(cid), size = util.creatureDivSize, pos = (pos.x-util.creatureDivSize[0]//2, pos.y-util.creatureDivSize[1]//2), parent=layer)
        
        self.creatureDiv.subscribe(Node.CURSOR_UP, self._mouseUp)
        self.creatureDiv.subscribe(Node.CURSOR_OUT, self._mouseUp)

        self.creatureDiv.subscribe(Node.CURSOR_DOWN, self.creatureCursorDown)

        self.team.score = self.team.score + 5
        
        self.creature = avg.CircleNode(fillopacity=1, pos=(self.creatureDiv.size.x // 2, self.creatureDiv.size.y // 2), r=util.creatureRadius, strokewidth=0, parent=self.creatureDiv)
        
        self.player = g_player
               
        if self.team.name == "Team2":
            self.creature.filltexhref = os.path.join(getMediaDir(__file__, "resources"), "squareEvil.png")
            Creature.creatures2.append(self)
        else:
            self.creature.filltexhref = os.path.join(getMediaDir(__file__, "resources"), "squareGood.png")
            Creature.creatures1.append(self)
               
        Creature.creatures[cid] = self
        
        self._hp = HP(1, self.creatureDiv)

        self.timer = self.player.setInterval(500, self._hitPointTimer)

            
    def _getR(self):
        """
        Getter for the radius of libAVG node.
        """
        return self.creature.r
        
    r = property(_getR)

 
 
      
    def die(self):
        """
        This method is called if a creatures is destroyed on the field.
        """
     
        if self.state=="RUNNING": 
            self.state="DEAD" 
            self.team.adjustScore(10)
            self.runningAnim.abort()     
            self._delete()  

        
    def damage(self, value=1):
        """
        Gives method gives damage to the creature. (value if specified, 1 otherwise).
        """
        self.hitPoints -=value
        
        if self.hitPoints<=0:
            self.die()
            
            
    def creatureCursorDown(self,event):
        """
        Cursor down event handler for the creature.
        Checks for damage.
        """               
        if not self.team.checkHomeArea(event.x, event.y):
            creatureNode = event.node
            creature = Creature.creatures[int(creatureNode.id)]
            creature.damage(self.enemy.currentDamageLevel)
            
    def _calcTime(self):
        """
        Helper method to calculate the time for the running linear anim.
        """
        return (int) (abs(self.targetX - self.pos.x) / self.speed * 1000)
        
    def _startMoving(self):
        """
        Starts the linear running anim after a freezing.
        """
        if not self.state =="DEAD":
            if self.team.id==1:
                if self.pos.x <=util.basewidth:
                    self.targetX=util.basewidth
                    stopAnim = self._switchToInActiveLayer
                elif self.pos.x <=util.halfwidth:
                    self.targetX=util.halfwidth
                    stopAnim = self._switchToActiveLayer
                else:
                    self.targetX= self.team.targetX-(2*self.creature.r if self.team.direction==1 else 0)
                    stopAnim = self._runningStopped
            else:
                if self.pos.x >=util.rightBasePos[0]-self.creatureDiv.size.x:
                    self.targetX=util.rightBasePos[0]-self.creatureDiv.size.x
                    stopAnim = self._switchToInActiveLayer
                elif self.pos.x>=util.halfwidth:
                    self.targetX=util.halfwidth
                    stopAnim = self._switchToActiveLayer
                else:
                    self.targetX= self.team.targetX-(2*self.creature.r if self.team.direction==1 else 0)
                    stopAnim = self._runningStopped
                
                
                
            self.player.clearInterval(self.freezeTimer)
            self.runningAnim = avg.LinearAnim(self.creatureDiv, "pos", self._calcTime(), (self.pos.x,self.pos.y), (self.targetX,self.pos.y),False, None, stopAnim)            
            self.runningAnim.start()
        
        
    def freeze(self, time):
        """
        Freezes the creature for the given time.
        """
        if not (self.runningAnim == None):
            self.runningAnim.abort()
            self.freezeTimer = self.player.setInterval(time, self._startMoving) 
            
    def getCirclePos(self):
        return avg.Point2D(self.pos.x + self.creatureDiv.size.x//2, self.pos.y + self.creatureDiv.size.y//2) 
        

