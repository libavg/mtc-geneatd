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
from libavg.utils import getMediaDir

class PreventCreatureBuildingItem(Item):
    """
    This class represents an item that prevents the building of creatures.
    When player drags this item into his base, the other player isn't able to build creatures for a specific time.
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
        self.blockTime = 7000
    

        Item.__init__(self, g_player, pos, layer, team1, team2, exp, game)
        
    def setAppearance(self):
        """
        This method sets the appearance of the item.
        """
        self.node.filltexhref=os.path.join(getMediaDir(__file__, "resources"), "preventCreatureBuilding.png")    
        
    
    def releaseBlock(self,id):
        """
        This method checks whether the item has still an effect or not.
        id: which team should be released of the block.
        """
        if (id == 1): #release player 1.
            self.player.clearInterval(self.game.timerCreature1)
            
            self.game.timerCreature1 = None
            self.game.team1CreatureBlock = False
            self.game.blockAllCreatures(1, False)
        else:
            self.player.clearInterval(self.game.timerCreature2)
            self.game.timerCreature2 = None
            self.game.team2CreatureBlock = False
            self.game.blockAllCreatures(2, False)
        

    def releaseBlockHalf(self,id):
        """
        This method checks whether the item has still an effect or not.
        id: which team should be released of the block.
        """
        if (id == 1): #release player 1.
            self.player.clearInterval(self.game.timerCreature1)
            self.game.homeBaseImg.href=os.path.join(getMediaDir(__file__, "resources"), "baseStoned1.png")
            self.game.timerCreature1 = self.player.setInterval(self.blockTime/2, lambda: self.releaseBlock(1))
        else:
            self.player.clearInterval(self.game.timerCreature2)
            self.game.homeBaseImg2.href=os.path.join(getMediaDir(__file__, "resources"), "baseStoned1.png")        
            self.game.timerCreature2 = self.player.setInterval(self.blockTime/2, lambda: self.releaseBlock(2))

    
    def _executeItemEffect(self, team):
        """
        Method that decreases the level of the other player by 1.
        """
        
        self.game.soundPlayer.playTune("soundfiles/sound_item_preventcreaturebuilding.mp3") 
        
        if (team.id == 1):  #player 1 collects it.
            self.game.team2CreatureBlock = True
            self.game.blockAllCreatures(2, True)
            if not (self.game.timerCreature2 == None):
                self.player.clearInterval(self.game.timerCreature2)
            self.game.timerCreature2 = self.player.setInterval(self.blockTime/2, lambda: self.releaseBlockHalf(2))
                
        else:
            self.game.team1CreatureBlock = True
            self.game.blockAllCreatures(1, True)
            if not (self.game.timerCreature1 == None):
                self.player.clearInterval(self.game.timerCreature1)
            self.game.timerCreature1 = self.player.setInterval(self.blockTime/2, lambda: self.releaseBlockHalf(1))
                
       
        team.adjustScore(200)    
            
        
   
          
        
    def _executeItemGraphicsEffect(self, team):
        """
        This method should be override for effect.
        Should contain the effect an item has on the GUI when collected.
        """
        pass
        