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

from item import Item
import os
from libavg.AVGAppUtil import getMediaDir


class ExpItem(Item):
    """
    This class represents a experience item. 
    When player drags this item into his base, he gets experience.
    """

    def __init__(self, g_player, pos, layer, team1, team2, exp, game):
        """
        Creates a new item (including the libAVG node).
        g_player: the global player instance.
        pos: the initial position.
        layer: the layer to put the creature on.
        team1: team 1.
        team2: team 2.
        exp: the exp of the item.
        game: the game.
        """  
        Item.__init__(self, g_player, pos, layer, team1, team2, exp, game)
        
    def setAppearance(self):
        """
        This method sets the appearance of the item.
        """
        if (self.exp == 1):
            self.node.filltexhref=os.path.join(getMediaDir(__file__, "resources"), "ep.png")
        elif (self.exp == 2):
            self.node.filltexhref=os.path.join(getMediaDir(__file__, "resources"), "epp.png")
        elif (self.exp == 3):
            self.node.filltexhref=os.path.join(getMediaDir(__file__, "resources"), "eppp.png")
        
    def _executeItemEffect(self, team):
        """
        Method that adds the amount of experience for this item to the player's experience.
        """
        self.game.soundPlayer.playTune("soundfiles/sound_item_exp.mp3")
        team.adjustExp(self.exp)
        team.adjustScore(self.exp * 100)

        
    def _executeItemGraphicsEffect(self, team):
        """
        This method should be override for effect.
        Should contain the effect an item has on the GUI when collected.
        """
        #done by the adjustEXP
        pass
