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
import os
from libavg.utils import getMediaDir

class HP(object):
    
    def __init__(self, number, parent):
       
        self._node = avg.ImageNode(size=parent.size, parent=parent)
        self._anim = avg.ContinuousAnim(self._node, "angle",0, 3, False, None, None)

        self._anim.start()
        self.hp= number
    
    def __del__(self):
        self._anim.abort()
        
    def _getHP(self):
        return self._hp
    
    def _setHP(self, number):
        if number < 1:
            self._hp = 0
            self.hide()                       
        elif number > 8:
            self._hp = 8
            self._node.href = os.path.join(getMediaDir(__file__, "resources"), "hp/" + str(self._hp) + ".png")
        else:
            self._hp = number
            self._node.href = os.path.join(getMediaDir(__file__, "resources"), "hp/" + str(self._hp) + ".png")
            

                
    def hide(self):
        self._node.opacity = 0
        
        
    
    hp = property(_getHP, _setHP)