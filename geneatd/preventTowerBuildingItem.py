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

class PreventTowerBuildingItem(Item):
    """
    This class represents an item that prevents the building of towers.
    When player drags this item into his base, the other player isn't able to build towers for a specific time.
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
        game: The reference to the game.
        """
        self.blockTime = 10000
    

        Item.__init__(self, g_player, pos, layer, team1, team2, exp, game)
        
    def setAppearance(self):
        """
        This method sets the appearance of the item.
        """
        self.node.filltexhref=os.path.join(getMediaDir(__file__, "resources"), "notower.png")     
        
    
    def releaseBlock(self,id):
        """
        This method checks whether the item has still an effect or not.
        id: which team should be released of the block.
        """
        if (id == 1): #release player 1.
            self.player.clearInterval(self.game.timer1)
            
            self.game.timer1 = None
            self.game.team1TowerBlock = False
            self.game.blockAllTowers(1, False)
        else:
            self.player.clearInterval(self.game.timer2)
            self.game.timer2 = None
            self.game.team2TowerBlock = False
            self.game.blockAllTowers(2, False)
        
        
        
    
    def _executeItemEffect(self, team):
        """
        Method that decreases the level of the other player by 1.
        """
        
        self.game.soundPlayer.playTune("soundfiles/sound_item_preventtowerbuilding.mp3") 
        
        if (team.id == 1):  #player 1 collects it.
            self.game.team2TowerBlock = True
            self.game.blockAllTowers(2, True)
            if not (self.game.timer2 == None):
                self.player.clearInterval(self.game.timer2)
            self.game.timer2 = self.player.setInterval(self.blockTime, lambda: self.releaseBlock(2))
                
        else:
            self.game.team1TowerBlock = True
            self.game.blockAllTowers(1, True)
            if not (self.game.timer1 == None):
                self.player.clearInterval(self.game.timer1)
            self.game.timer1 = self.player.setInterval(self.blockTime, lambda: self.releaseBlock(1))
                
       
        team.adjustScore(200)    
            
        
   
          
        
    def _executeItemGraphicsEffect(self, team):
        """
        This method should be override for effect.
        Should contain the effect an item has on the GUI when collected.
        """
        pass
        