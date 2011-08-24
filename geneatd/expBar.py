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
from libavg.utils import getMediaDir

class ExpBar(object):
    """
    This class represents an experience bar.
    """
    
    def __init__(self, layer, pos, color, steps, id=1):
        """
        Constructor for a new expBar object.
        layer: the layer to place the bar on.
        pos: the position to place the bar.
        color: the color of the inner rect.
        steps: nr of increases possible until the bar is full.
        id: indicates the team the bar belongs to.
        """
        self.expBarDiv = avg.DivNode(pos=pos, size=util.expBarSize, parent=layer) 
        self.underRect = avg.RectNode(fillopacity=1, strokewidth=0, fillcolor="000000", size=util.expBarSize, pos=(0,0), parent=self.expBarDiv)
        self.innerRect = avg.RectNode(fillopacity=0.8, strokewidth=0, fillcolor=color, size=(0, util.sideBarheight), parent=self.expBarDiv)
        self.borderImg = avg.ImageNode(href=os.path.join(getMediaDir(__file__, "resources"), "barrock_neu.png"), size=(util.sideBarheight,util.expBarSize[0]), parent=self.expBarDiv)
        
        self.steps = steps
        self.cnt = 0
        self.level=0
        self.id = id
        self.stepWidth = math.floor((util.expBarRightInnerDivWidth-util.levelWordsSize[0]) / steps)
        
        self.levelWords = avg.WordsNode( font="DejaVu Sans", variant="bold", fontsize=util.convertFontSize(24), text="%02i" % self.level, pivot=(0,0), alignment="center", parent=self.expBarDiv)
        
 
        if id==1:
            self.borderImg.pivot = (0,0)
            self.innerRect.pos=(util.width // 300,0)
            self.levelWords.pos=(self.borderImg.size.y+util.width//400, util.sideBarheight //2)
            self.levelWords.angle=math.pi / 2 
            self.borderImg.pos=(self.borderImg.size.y,0)
            self.borderImg.angle=math.pi /2

     
        else:
            self.borderImg.pivot = (0,0)
            self.innerRect.pos=(util.expBarSize[0],0)
            self.levelWords.pos=(-util.width//400,util.sideBarheight//2)      
            self.levelWords.angle=math.pi *3 / 2 
            self.innerRect.size=(util.expBarSize[0]-util.sideBarheight //2, util.sideBarheight)
            self.borderImg.pos=(0,util.sideBarheight)
            self.borderImg.angle=math.pi*3/2

        self.blinkAnim1 = False
        self.blinkAnim2 = False

    
    def _resetExpBar(self):
        if self.level==8:
            self.levelWords.text = "%02i" % 9
            return
        if self.id==1:
            self.incAnim1 = avg.LinearAnim(self.innerRect, "size", 500, self.innerRect.size, (self.cnt * self.stepWidth, self.innerRect.size.y))            
        else:
            self.incAnim1 = avg.LinearAnim(self.innerRect, "pos", 500, self.innerRect.pos, (util.expBarRightInnerDivWidth-self.cnt * self.stepWidth, self.innerRect.pos.y))
        self.incAnim1.start()
        self.level+=1
        self.levelWords.text = "%02i" % self.level
        

    
    def inc(self):
        """
        Increases the exp bar (inner rect).
        """
        self.cnt+=1
        if self.cnt>=self.steps:
            if self.level==8:
                self.level=8
                if self.cnt>self.steps:
                    self.cnt-=1
                    return
                
            
            if self.id==1:
                
                self.incAnim1 = avg.LinearAnim(self.innerRect, "size", 500, self.innerRect.size, (self.cnt * self.stepWidth, self.innerRect.size.y), False, None, self._resetExpBar)

               
            else:
                
                self.incAnim1 = avg.LinearAnim(self.innerRect, "pos", 500, self.innerRect.pos, (util.expBarRightInnerDivWidth-self.cnt * self.stepWidth, self.innerRect.pos.y), False, None, self._resetExpBar)
            self.incAnim1.start()
            if not self.level==8:
                self.cnt=0
            return
        
        if self.id==1:
            self.incAnim1 = avg.LinearAnim(self.innerRect, "size", 500, self.innerRect.size, (self.cnt * self.stepWidth, self.innerRect.size.y))
        else:
            self.incAnim1 = avg.LinearAnim(self.innerRect, "pos", 500, self.innerRect.pos, (util.expBarRightInnerDivWidth-self.cnt * self.stepWidth, self.innerRect.pos.y))

        self.incAnim1.start()
        
    def dec(self):
        """
        Decreases the exp bar (inner rect).
        """
        self.levelWords.text = "%02i" % self.level
        if self.cnt==0:
            if self.level==0:
                return
            self.level-=1
            self.levelWords.text = "%02i" % self.level
            if self.id==1:
                self.innerRect.size = (util.expBarSize[0]-util.levelWordsSize[0],self.innerRect.size.y)
                self.levelWords.pos=(util.expBarSize[0],util.levelWordsSize[1]//2)
            else:
                self.innerRect.pos=(util.levelWordsSize[0],0)
                self.levelWords.pos=(0,util.levelWordsSize[1]//2)      
            self.cnt=10
        self.cnt-=1
        
        if self.id==1:
            self.incAnim1 = avg.LinearAnim(self.innerRect, "size", 500, self.innerRect.size, (self.cnt * self.stepWidth, self.innerRect.size.y))
        else:
            self.incAnim1 = avg.LinearAnim(self.innerRect, "pos", 500, self.innerRect.pos, (util.expBarRightInnerDivWidth-self.cnt * self.stepWidth, self.innerRect.pos.y))

        self.incAnim1.start()
        
        
    def blink(self,i=2):
        """
        Lets the exp bar (inner rect + border img) blink.
        """
        if (self.blinkAnim1):
            if (self.blinkAnim1.isRunning()):   
                    self.blinkAnim1.abort()
        if (self.blinkAnim2):
            if (self.blinkAnim2.isRunning()):   
                    self.blinkAnim2.abort()
                    
        self.blinkAnim1=avg.LinearAnim(self.innerRect, "fillopacity", 750, 0.8, 1)
        self.blinkAnim1.start()
        self.blinkAnim2=avg.LinearAnim(self.borderImg, "opacity", 750, 1, 0.4, False, None, lambda : self._unblink(i))
        self.blinkAnim2.start()
 
    def _unblink(self,i):
        """
        Helper method for blinking.
        """
        if i>1:
            self.blinkAnim1 = avg.LinearAnim(self.innerRect, "fillopacity", 750, 1, 0.8)
            self.blinkAnim1.start()
            self.blinkAnim2 = avg.LinearAnim(self.borderImg, "opacity", 750, 0.4, 1, False, None, lambda : self.blink(i-1))
            self.blinkAnim2.start()
        else:
            self.blinkAnim1 = avg.LinearAnim(self.innerRect, "fillopacity", 750, 1, 0.8)
            self.blinkAnim1.start()
            self.blinkAnim2 = avg.LinearAnim(self.borderImg, "opacity", 750, 0.4, 1)
            self.blinkAnim2.start()
            