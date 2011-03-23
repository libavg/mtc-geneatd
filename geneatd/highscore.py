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

import sys
from libavg import *
import util
import os

class Highscore(object):
    """
    Highscore object manages the highscore data and how it is showed.
    """
    
    def __init__(self, path, player, length = 10):
   
        self._path = os.path.join(path,".geneatd")
        if not os.path.exists(self._path): 
            os.mkdir(self._path)


        self._path = os.path.join(self._path,"score.src")
        
       
        
        if not os.path.exists(self._path):
            
            try:
                fobj = open(self._path,"w")
                
    
                for i in xrange(10,0,-1): 
                    fobj.write("User" + "\t" + str((i*1000)) + "\n") 
            finally:
                fobj.close()
            
        self._player = player
        self._length = length
        self.readHighscore()
        
    
    def readHighscore(self):
        
        self.entries = []
           
        try:
            f = open(self._path,"r")
            for line in f:
                self.entries.append(line.strip().split("\t"))
        except IOError: 
            f.close()
            print "IOError while reading highscore file"
            sys.exit()
            
        f.close()
            
 

    
    def addEntry(self, name, score):
        """
        Adds an entry in the highscore
        """
        if self.entries:
            for i, entry in enumerate(self.entries):
                if int(entry[1]) <=  score:
                    self.entries.insert(i, [name, score])
                    break
            else:
                self.entries.append([name, str(score)])
        else:
            self.entries.append([name, str(score)])
             
             
        if len(self.entries) > self._length:
            del self.entries[self._length:]
           
               
        try:
            f = open(self._path, "w")
            global c            
            c=""
            for entry in self.entries:
                f.write(c)
                f.write(unicode(entry[0]) + "\t" +  str(entry[1]))
                c="\n"
        finally:
            f.close()
        
        
    
    def show(self, parentNode=None):
        """
        Displays the highscore.
        """
        self.highscoreDiv = avg.DivNode(id="highscore")
      
        
        
        if not self.entries:
            
            self.highscoreDiv.pos = (util.width//10,util.height//4)
            self.highscoreDiv.size=(util.width//10*8,util.height//4)
            
            backgroundRect = avg.RectNode(size=self.highscoreDiv.size, pos=(0,0), fillcolor="000000", fillopacity=0.8, color="000000")
            self.highscoreDiv.appendChild(backgroundRect)
            text = avg.WordsNode(font="DejaVu Sans", color="FEFB00", fontsize=util.convertFontSize(100), text="No entries here", parent=self.highscoreDiv) 

            text.pos = ((util.width//10*8-text.getMediaSize()[0])//2, 0)
            
        else:
            self.highscoreDiv.pos = (util.width//10,util.height//15)
            self.highscoreDiv.size=(util.width//10*8,util.height//15*13)
            backgroundRect = avg.RectNode(size=(self.highscoreDiv.size.x,self.highscoreDiv.size.y*99//100), pos=(-util.width//200,0), fillcolor="000000", fillopacity=0.8, color="000000")
            self.highscoreDiv.appendChild(backgroundRect)
            for i, entry in enumerate(self.entries):
                avg.WordsNode(font="DejaVu Sans", text=("%02i" % (i+1))+". "+unicode(entry[0]), color="FEFB00", fontsize=util.convertFontSize(40), pos=(0, i*util.height//12), parent=self.highscoreDiv)
                avg.WordsNode(font="DejaVu Sans", text=str(entry[1]) +" ", color="FEFB00", fontsize=util.convertFontSize(40), pos=(util.width // 5*4, i*util.height//12), alignment="right", parent=self.highscoreDiv)
                

            
        if not parentNode:
            self._player.getRootNode().appendChild(self.highscoreDiv)
        else:
           
            
            parentNode.appendChild(self.highscoreDiv)
              
        
    
    def hide(self):
        """
        Hides the highscore
        """
        self.highscoreDiv.unlink(True)
        self.highscoreDiv = None

        
    def getLowestEntry(self):
        if not self.entries or len(self.entries)<self._length:
            return -1
        return self.entries[-1][1]
    


