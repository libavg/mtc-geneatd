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

class ItemBunker(object):
    """
    This class represents an experience bar.
    """
    
    def __init__(self, layer, pos):
        
        self.node = avg.ImageNode(href=os.path.join(getMediaDir(__file__, "resources"), "itembunker.png"), size=util.itemBunkerSize, pos=pos, parent=layer)
        self.imgNode = avg.ImageNode(href="", size=(util.itemBunkerSize[0] //4 *3 , util.itemBunkerSize[1] // 4 * 3), pos=(pos.x+(self.node.size.x - util.itemBunkerSize[0] //4 *3)//2, pos.y+(self.node.size.y - util.itemBunkerSize[1] // 4 * 3)//2), parent=layer)
        self.hasItem = False
        
    def dropPossible(self):
        return not self.hasItem
    
    def dropItem(self, image):
        self.hasItem=True
        self.imgNode.href=image
        
    def delete(self):
        self.hasItem = False
        self.imgNode.href=""