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
import os
from libavg.utils import getMediaDir

class FreezeCreatureItem(Item):
    """
    This class represents a creature kill item. 
    When player drags this item into his base, he destroys all creatures of the enemy.
    """

    def __init__(self, g_player, pos, layer, team1, team2,exp, game,graphicsLayer):
        """
        Creates a new item (including the libAVG node).
        g_player: the global player instance.
        pos: the initial position.
        layer: the layer to put the creature on.
        team1: team 1.
        team2: team 2.
        exp: the exp of the item.
        game: the game.
        kill: which player should loose his creature.
        graphicsLayer: where to append graphic nodes.
        """
        self.game = game
        self.graphicsLayer = graphicsLayer
        Item.__init__(self, g_player, pos, layer, team1, team2, exp, game)
        
    def setAppearance(self):
        """
        This method sets the appearance of the item.
        """
        self.node.filltexhref=os.path.join(getMediaDir(__file__, "resources"), "freezeItem.png")     
        
    def _executeItemEffect(self, team):
        """
        Method that kills all creatures.
        """
        self.game.soundPlayer.playTune("soundfiles/sound_item_creaturefreeze.mp3") 
        if team.id == 1: 
            killList = Creature.creatures2[:]
        else:
            killList = Creature.creatures1[:]
            
        for creature in killList:
            creature.freeze(3000)
        
        team.adjustScore(200)
        
    def _executeItemGraphicsEffect(self, team):
        pass