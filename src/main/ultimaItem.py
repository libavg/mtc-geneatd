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
from item import Item
from creature import Creature
from tower import Tower
import os
from libavg.AVGAppUtil import getMediaDir
import util

class UltimaItem(Item):
    """
    This class represents an ultima item. 
    When player drags this item into his base, he destroys all creatures and towers of the enemy.
    """

    def __init__(self, g_player, pos, layer, team1, team2, exp, game, graphicsLayer):
        """
        Creates a new item (including the libAVG node).
        g_player: the global player instance.
        pos: the initial position.
        layer: the layer to put the creature on.
        team1: team 1.
        team2: team 2.
        exp: the exp of the item.
        game: the game.
        graphicslayer: the layer where the graphical effect should be executed.
        """
        self.graphicsLayer = graphicsLayer
        Item.__init__(self, g_player, pos, layer, team1, team2, exp, game)
        
    def setAppearance(self):
        """
        This method sets the appearance of the item.
        """
        self.node.filltexhref=os.path.join(getMediaDir(__file__, "resources"), "ultimate.png")     
        
        
    def _executeItemEffect(self, team):
        """
        Method that kills all creatures and towers of the opponent.
        """
        
        self.game.soundPlayer.playTune("soundfiles/sound_item_ultima.mp3")
        
        if (team.id == 1):
            #player 1 got the item.
            creatureKillList = Creature.creatures2[:]
            towerKillList = Tower.tower2[:]
        else: 
            creatureKillList = Creature.creatures1[:]
            towerKillList = Tower.tower1[:]
            
        for creature in creatureKillList:
            creature.die()
        
        for tower in towerKillList:
            tower.die()
            
        team.adjustExp(self.exp)
        team.adjustScore(1000)
            
            
    def _removeLight(self):
        """
        Unlinks the lightning node.
        """
        self.lightning.unlink(True)     
          
        
    def _executeItemGraphicsEffect(self, team):
        """
        This method should be override for effect.
        Should contain the effect an item has on the GUI when collected.
        """
        self.lightning = avg.RectNode(fillopacity=0.01, strokewidth=0, sensitive=False, size=util.playingFieldSize, pos=util.playingFieldPos, parent=self.graphicsLayer)
       
        if (team.id == 1):
            self.lightning.fillcolor = self.team2.color
        else:
            self.lightning.fillcolor = self.team1.color
                

            
        avg.LinearAnim(self.lightning,"fillopacity", 250, 0.01, 1.0, False, None, self._removeLight).start()
