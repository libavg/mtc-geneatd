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
import os
from libavg.AVGAppUtil import getMediaDir

# time after which the item disappears
disappearTime = 8000

class Item(object):
    """
    This class represents a draggable item. 
    """
    
    
    
    def _startDragging(self, event):
        """
        Starts the dragging of the item.
        """
        if self.captureHolder is None:
            self.captureHolder=event.cursorid
            self.dragOffsetX = self.pos.x - event.pos.x
            self.dragOffsetY = self.pos.y - event.pos.y
            event.node.setEventCapture(event.cursorid)
            
            if not (self.itemBunker == None):
                self.itemBunker.delete()
                self.itemBunker=None
                self.node.fillopacity=1.0
                self.disappearTimer=self.player.setInterval(disappearTime, self.disappear)

    
    def _doDragging(self, event):
        """
        Does the dragging.
        """
        if event.cursorid==self.captureHolder:
            self.pos=event.pos+avg.Point2D(self.dragOffsetX,self.dragOffsetY)
    
    
    def _endDragging(self, event):
        """
        End the dragging of the item.
        """
        if event.cursorid==self.captureHolder:
            event.node.releaseEventCapture(event.cursorid)
            self.captureHolder=None
            if (util.expBarSize[0]<event.pos.x<util.expBarSize[0]+util.itemBunkerSize[0] and 0 < event.pos.y < util.itemBunkerSize[1]):
                if self.game.itemBunker1Left.dropPossible() and not self.disappeared:
                    self.game.itemBunker1Left.dropItem(self.node.filltexhref)
                    self.node.fillopacity=0.0
                    self.player.clearInterval(self.disappearTimer)
                    self.itemBunker = self.game.itemBunker1Left

            elif (util.width-(util.expBarSize[0]+util.itemBunkerSize[0])<event.pos.x<util.width-util.expBarSize[0] and util.height-util.itemBunkerSize[1] < event.pos.y < util.height):
                if self.game.itemBunker2Left.dropPossible() and not self.disappeared:
                    self.game.itemBunker2Left.dropItem(self.node.filltexhref)
                    self.node.fillopacity=0.0
                    self.player.clearInterval(self.disappearTimer)
                    self.itemBunker = self.game.itemBunker2Left

            elif (util.expBarSize[0]<event.pos.x<util.expBarSize[0]+util.itemBunkerSize[0] and util.height-util.itemBunkerSize[1] < event.pos.y < util.height):
                if self.game.itemBunker1Right.dropPossible() and not self.disappeared:
                    self.game.itemBunker1Right.dropItem(self.node.filltexhref)
                    self.node.fillopacity=0.0
                    self.player.clearInterval(self.disappearTimer)
                    self.itemBunker = self.game.itemBunker1Right

            elif (util.width-(util.expBarSize[0]+util.itemBunkerSize[0])<event.pos.x<util.width-util.expBarSize[0] and 0 < event.pos.y < util.itemBunkerSize[1]):
                if self.game.itemBunker2Right.dropPossible() and not self.disappeared:
                    self.game.itemBunker2Right.dropItem(self.node.filltexhref)
                    self.node.fillopacity=0.0
                    self.player.clearInterval(self.disappearTimer)
                    self.itemBunker = self.game.itemBunker2Right


                    
            elif self.team1.checkBaseArea(event.pos.x, event.pos.y):
                self.itemBunker = None
                self.node.sensitive = False
                self._executeItemEffect(self.team1)
                self._executeItemGraphicsEffect(self.team1)
                self.disappear()      
            elif self.team2.checkBaseArea(event.pos.x, event.pos.y): 
                self.itemBunker = None 
                self.node.sensitive = False
                self._executeItemEffect(self.team2)
                self._executeItemGraphicsEffect(self.team2)
                self.disappear()             
          

       
    
    def setAppearance(self):
        """
        This method sets the appearance of the item.
        """
        self.node.filltexhref=os.path.join(getMediaDir(__file__, "resources"), "crystal.png")            
            
                
    def __init__(self, g_player, pos, layer, team1, team2, exp, game):
        """
        DO NOT INSTANTIATE THIS ITEM
        Creates a new item (including the libAVG node).
        g_player: the global player instance.
        pos: the initial position.
        layer: the layer to put the creature on.
        team1: team 1.
        team2: team 2.
        exp: the exp of the item.
        game: the game.
        """
        self.disappeared = False
        self.node =avg.RectNode(fillopacity=0, strokewidth=0, pos=pos, size=util.itemBunkerSize, parent=layer)
        
        self.exp = exp
        self.player = g_player
        self.team1 = team1
        self.team2 = team2
        self.setAppearance()
        self.game = game
        self.node.setEventHandler(avg.CURSORDOWN,avg.TOUCH or avg.MOUSE, self._startDragging)
        self.node.setEventHandler(avg.CURSORMOTION,avg.TOUCH or avg.MOUSE, self._doDragging)
        self.node.setEventHandler(avg.CURSORUP,avg.TOUCH or avg.MOUSE, self._endDragging)
        self.itemBunker = None
        
        
        self.captureHolder=None        
        avg.LinearAnim(self.node, "fillopacity", 1000, 0,1).start()
        self.disappearTimer = self.player.setInterval(disappearTime, self.disappear)

   
    def disappear(self):
        """
        This method lets the item disappear.
        """
        self.disappeared = True
        self.player.clearInterval(self.disappearTimer)
        avg.LinearAnim(self.node, "fillopacity", 1000, 1,0, False, None, self._delete).start()

    
    def _setPos(self, value):
        """
        Setter for the position of the libAVG node.
        """
        self.node.pos = value
        
    def _getPos(self):
        """
        Getter for the position of the libAVG node.
        """
        return self.node.pos
    
    pos = property(_getPos, _setPos)
    
    
    def _delete(self):
        """
        "Deletes" the item (unlinks the libAVG node)
        """
        self.node.unlink(True)

        