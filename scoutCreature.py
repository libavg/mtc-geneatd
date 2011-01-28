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
import os
from libavg.AVGAppUtil import getMediaDir

moveTime = 3000 
opacityTime = 1000



class ScoutCreature(Creature):      
    """
    This class represents a scout creature.
    """
    
    def __init__(self, g_player, team, enemy,  pos, layer, when, main, inActiveLayer, maxHitPoints = 8):
        """
        Creates a new scout creature (including the libAVG nodes).
        g_player: the global player instance.
        team: the team, the creature should belong to.
        pos: the initial position.
        layer: the layer to put the creature on.
        when: the moment, the creation has been started.
        """
        Creature.__init__(self, g_player, team, enemy, pos, layer, when, main, inActiveLayer, maxHitPoints)
        self.speed = self.speed * 2
        
        if self.team.name == "Team2":
            self.creature.filltexhref = os.path.join(getMediaDir(__file__, "resources"), "triangleEvil.png")
        else:
            self.creature.filltexhref = os.path.join(getMediaDir(__file__, "resources"), "triangleGood.png")
