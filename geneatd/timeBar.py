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
import math
import os
from libavg.AVGAppUtil import getMediaDir

class TimeBar(object):
    """
    This class represents a time bar.
    """
    
    def __init__(self, layer, pos, color, gameTime, id=1):
        """
        Constructor for a new timeBar object.
        layer: the layer to place the bar on.
        pos: the position to place the bar.
        color: the color of the inner rect.
        gameTime: time in minutes or -1 if infinity.
        id: indicates the team the bar belongs to.
        """
        self.timeBarDiv = avg.DivNode(pos=pos, size=util.expBarSize, parent=layer)
        
        self.underRect = avg.RectNode(fillopacity=1, strokewidth=0, fillcolor="000000", size=util.expBarSize, pos=(0,0), parent=self.timeBarDiv)
 
        self.innerRect = avg.RectNode(fillopacity=0.8, strokewidth=0, fillcolor=color, size=(util.expBarSize[0]-util.levelWordsSize[0], util.sideBarheight), parent=self.timeBarDiv)
        
        self.borderImg = avg.ImageNode(href=os.path.join(getMediaDir(__file__, "resources"), "barrock_neu.png"), pivot=(0,0), size=(util.sideBarheight,util.expBarSize[0]), parent=self.timeBarDiv)
        
        self.clockImg = avg.ImageNode(href=os.path.join(getMediaDir(__file__, "resources"), "clock.png"), size=util.clockSize, parent=self.timeBarDiv)
        
        if id==1:
 
            self.clockImg.pos=(util.expBarSize[0]-util.levelWordsSize[0]-util.width//600,util.width//250)
            self.clockImg.angle=math.pi/2
            self.innerRect.pos=(0,0)
            self.borderImg.pos=(util.expBarSize[0],0)
            self.borderImg.angle=math.pi /2
            
            if not gameTime==-1:
                avg.LinearAnim(self.innerRect, "size", gameTime*60*1000, (self.innerRect.size.x, self.innerRect.size.y), (1,self.innerRect.size.y)).start()
        else:

            self.clockImg.pos=(util.width//800,util.width//250)
            self.clockImg.angle=math.pi/2*3
            self.innerRect.pos=(util.sideBarheight//4*3,0)
            self.borderImg.angle=math.pi *3 /2
            self.borderImg.pos=(0,util.sideBarheight)
           
            if not gameTime==-1:
                avg.LinearAnim(self.innerRect, "pos", gameTime*60*1000, (self.innerRect.pos.x, self.innerRect.pos.y), (util.expBarSize[0],self.innerRect.pos.y)).start()
                
                