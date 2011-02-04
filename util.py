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
from libavg.AVGAppUtil import getMediaDir
from libavg import avg
import os
import math

#the width of the whole application
width = 800

#the height of the whole application
height = 600

#the width of one side of the playing field
halfwidth = width // 2

#the width of the home base
basewidth = width // 10

#the height of the sidebar area
sideBarheight = height // 20

#the size of playing field
playingFieldSize = (width-2*basewidth, height-2*sideBarheight)

#the position of the playingfield
playingFieldPos = (basewidth, sideBarheight)

#the position of the right home base
rightBasePos = (width-basewidth, sideBarheight)

#the position of the left home base
leftBasePos = (0,sideBarheight)

#the size of the div surrounding a creature
creatureDivSize = (width // 25, width // 25)

#the size of a creatur
creatureRadius = creatureDivSize[0] // 2

#the size of the experience bar
expBarSize = (width // 6, sideBarheight)

#the size of the inner div of the experience bar
expBarRightInnerDivWidth = expBarSize[0]

#the size of the level counter
levelWordsSize = (expBarSize[0] // 7, sideBarheight)

#the size of the div surrounding a tower
towerDivSize = (width // 6,width // 6)

#the size of a tower
towerSize = (width // 20, width // 20)

#the size of the div surrounding an indyTower
indyTowerDivSize = (width // 4, width // 20)

#the size of the item bunker
itemBunkerSize = (sideBarheight,sideBarheight)

#the size of the clock
clockSize=(sideBarheight//4*3,sideBarheight//4*3)

#the size of the images in the sidebar 
imageSize = (sideBarheight//4*3,sideBarheight//4*3) 

#the margin of the images in the sidebar 
imageMargin = (sideBarheight - sideBarheight//4*3) // 2

#the size of an image button in the help menu
helpImageButtonSize= (height // 8, height // 8)

#the size of an image  in the help menu
helpImageSize = (height // 100*9, height // 100*9)

#the margin of the image buttons in the help menu
helpImageMargin = ((height//8-height//100*9)//2,(height//8-height//100*9)//2); 

#the width of the middle line
middleLinewidth = width // 25

#the height of the menu area
menuAreaheight = sideBarheight

#the radius of the tower creation circle
creationCircleRadius = width//20

#the size of the damage level stars
starSize = (sideBarheight*3//2,sideBarheight*3//2)

#the size of a button in the main menu.
buttonSize = (width // 2.5, height // 7.5)

#the size of the help / close button.
helpAndCloseButtonSize = (width // 10, height // 15)

#the margin of the buttons from top.
buttonMarginTop = height // 10 * 3

#the margin of the buttons from the bottom.
buttonMarginBottom = height // 10 * 9

#the space between the buttons.
buttonSpace = height // 100 * 5

#the height of a key.
keyHeight = height //13



def convertFontSize(incomingSize, maxSize=140):
    '''
    Method to adjust the font size depending on the current width.
    '''
    return max(1, min(maxSize, ((int) (incomingSize / 800.0 *width)-(width//100))))



def updateSizes(width2, height2):
    '''
    Method to adjust all the above sizes depending on the new width and height.
    '''    
    global width, height, halfwidth, basewidth, sideBarheight, playingFieldSize, playingFieldPos
    global rightBasePos, leftBasePos, creatureDivSize, creationCircleRadius, expBarSize, expBarRightInnerDivWidth
    global creatureRadius, levelWordsSize, towerDivSize, towerSize, indyTowerDivSize, itemBunkerSize, clockSize
    global imageSize, imageMargin, helpImageButtonSize, helpImageSize, helpImageMargin, middleLinewidth, menuAreaheight
    global creatureCircleRadius, starSize, buttonSize, helpAndCloseButtonSize, buttonMarginTop, buttonMarginBottom, buttonSpace
    global keyHeight
    
    width = width2
    height = height2
    
    
    halfwidth = width // 2
    
    basewidth = width // 10
    sideBarheight = height // 20
    
    playingFieldSize = (width-2*basewidth, height-2*sideBarheight)
    playingFieldPos = (basewidth, sideBarheight)
    
    rightBasePos = (width-basewidth, sideBarheight)
    leftBasePos = (0,sideBarheight)
    
    
    creatureDivSize = (width // 25, width // 25)
    creatureRadius = creatureDivSize[0] // 2
    
    expBarSize = (width // 6, sideBarheight)
    expBarRightInnerDivWidth = expBarSize[0]
    levelWordsSize = (expBarSize[0] // 7, sideBarheight)
    
    
    towerDivSize = (width // 6,width // 6)
    towerSize = (width // 20, width // 20)
    
    indyTowerDivSize = (width // 4, width // 20)
    
    itemBunkerSize = (sideBarheight,sideBarheight)
    clockSize=(sideBarheight//4*3,sideBarheight//4*3)
    
    imageSize = (sideBarheight//4*3,sideBarheight//4*3) 
    imageMargin = (sideBarheight - sideBarheight//4*3) // 2
    
    helpImageButtonSize= (height // 8, height // 8)
    helpImageSize = (height // 100*9, height // 100*9)
    helpImageMargin = ((height//8-height//100*9)//2,(height//8-height//100*9)//2); 
    
    middleLinewidth = width // 25
    menuAreaheight = sideBarheight
    
    
    creationCircleRadius = width//20
    
    
    starSize = (sideBarheight*3//2,sideBarheight*3//2)
    
    buttonSize = (width // 2.5, height // 7.5)
    helpAndCloseButtonSize = (width // 10, height // 15)
    buttonMarginTop = height // 10 * 3
    buttonMarginBottom = height // 10 * 9
    buttonSpace = height // 100 * 5
    
    
    keyHeight = height //13
    
    
    
__new = avg.ImageNode(id="p2", opacity=1, href=os.path.join(getMediaDir(__file__, "resources"), "backgroundHRes.jpg"), pos=(0,0) )              
__c1 =  avg.ImageNode(id="c1", opacity=1, href=os.path.join(getMediaDir(__file__, "resources"), "c1.png")) 
__c2 =  avg.ImageNode(id="c2", opacity=1, href=os.path.join(getMediaDir(__file__, "resources"), "c2.png"))
__c3 =  avg.ImageNode(id="c3", opacity=1, href=os.path.join(getMediaDir(__file__, "resources"), "c3.png"))
__c4 =  avg.ImageNode(id="c4", opacity=1, href=os.path.join(getMediaDir(__file__, "resources"), "c4.png"))        
__old = avg.ImageNode(id="p1", opacity=1, href=os.path.join(getMediaDir(__file__, "resources"), "MainBackground.jpg"), pos=(0,0))
       
       
def __activateNode(parent, node):
    parent.appendChild(node)
    node.active = True
    node.opacity = 1
       
def __deactivateNode(node):
    node.unlink(False)
    node.active = False
    
    
def startCloudFadeIn(parentNode, endAction=None):
     
    __activateNode(parentNode,__new )
    __activateNode(parentNode,__c1 )
    __activateNode(parentNode,__c2 )
    __activateNode(parentNode,__c3 )
    __activateNode(parentNode,__c4 )
    __activateNode(parentNode,__old )

    __old.pos = (0,0)
    __old.size= parentNode.size
    __new.pos=(0,0)
    __new.size= parentNode.size
    
    __c1.pos =( 0 - parentNode.width ,0 - parentNode.height )
    __c1.size = (parentNode.width * 2, parentNode.height * 2)
    
    __c2.pos =(0, -parentNode.height ) 
    __c2.size= (parentNode.width * 2, parentNode.height * 2)
    
    __c3.pos =(0,0)
    __c3.size = (parentNode.width * 2, parentNode.height * 2)
    
    __c4.pos = (-parentNode.width , 0)
    __c4.size = (parentNode.width * 2, parentNode.height * 2)
    
    
   
   
        
    ca1 = avg.LinearAnim(__c1, "pos", 4000, __c1.pos, (0,0)                                   ,False, None, lambda: __deactivateNode(__c1))
    ca2 = avg.LinearAnim(__c2, "pos", 4000, __c2.pos, (0,0)                                   ,False, None, lambda: __deactivateNode(__c2))
    ca3 = avg.LinearAnim(__c3, "pos", 4000, __c3.pos, (-parentNode.width ,-parentNode.height ),False, None, lambda: __deactivateNode(__c3))
    ca4 = avg.LinearAnim(__c4, "pos", 4000, __c4.pos, (0 ,0 - parentNode.height )             ,False, None ,lambda: __deactivateNode(__c4))
    
    ra2 = avg.LinearAnim(__old, "opacity", 4000, 1, 0 ,False, None,lambda: __deactivateNode(__old))
    
    ra2.start()
    ca1.start()
    ca2.start()
    ca3.start()
    ca4.start()
    avg.fadeOut(__c1, 4000)
    avg.fadeOut(__c2, 4000)
    avg.fadeOut(__c3, 4000, lambda: __deactivateNode(__new))
    avg.fadeOut(__c4, 4000, endAction)
    
    
def startCloudFadeIn2(parentNode, endAction=None):
     
    __activateNode(parentNode,__new )
    __activateNode(parentNode,__c3 )
    __activateNode(parentNode,__c4 )
    __activateNode(parentNode,__old )

    __old.pos = (0,0)
    __old.size= parentNode.size
    __new.pos=(0,0)
    __new.size= parentNode.size
    
    __c1.pos =( 0 - parentNode.width ,0 - parentNode.height )
    __c1.size = (parentNode.width * 2, parentNode.height * 2)
    
    __c2.pos =(0, -parentNode.height )
    __c2.size= (parentNode.width * 2, parentNode.height * 2)
    
    __c3.pos =(0,0)
    __c3.size = (parentNode.width , parentNode.height )
    
    __c4.pos = (0,0)
    __c4.size = (parentNode.width , parentNode.height )
    
    
   
   
        
    ca1 = avg.LinearAnim(__c1, "pos", 10000, __c1.pos, (0,0)                                   ,False, None, lambda: __deactivateNode(__c1))
    ca2 = avg.LinearAnim(__c2, "pos", 10000, __c2.pos, (0,0)                                   ,False, None, lambda: __deactivateNode(__c2))
    ca3 = avg.LinearAnim(__c3, "pos", 10000, __c3.pos, (-parentNode.width ,-parentNode.height ),False, None, lambda: __deactivateNode(__c3))
    ca32 = avg.LinearAnim(__c3, "size", 10000, __c3.size, (parentNode.width*3 ,parentNode.height*3 ))
   
    ca4 = avg.LinearAnim(__c4, "pos", 10000, __c4.pos, (-2*parentNode.width ,-2*parentNode.height )             ,False, None ,lambda: __deactivateNode(__c4))
    ca41 = avg.LinearAnim(__c4, "size", 10000, __c4.size, (5*parentNode.width ,5*parentNode.height ))
    
    ra2 = avg.LinearAnim(__old, "opacity", 5000, 1, 0 ,False, None,lambda: __deactivateNode(__old))
    
    ra2.start()
    ca1.start()
    ca2.start()
    ca3.start()
    ca32.start()
    ca4.start()
    ca41.start()
    
    def textAnim():
        
        def fancyWords():
            place2 = avg.WordsNode(font="DejaVu Sans", variant="Bold", fontsize=convertFontSize(32), color = "111111", text = "Take your side now!", parent=parentNode)
            place2.pivot = (place2.getMediaSize()[0], 0)
            place2.pos = (width // 2 - width//8,height//2-place.getMediaSize()[0]//2)
        
            avg.LinearAnim(place, "angle", 3000, 0, math.pi / 2, False, None, lambda: avg.LinearAnim(place, "opacity", 1000, 1, 0 ,False, None, lambda: place.unlink(True)).start()).start()
            avg.LinearAnim(place2, "angle", 3000, 0, -math.pi / 2, False, None, lambda: avg.LinearAnim(place2, "opacity", 1000, 1, 0 ,False, None, lambda: place2.unlink(True)).start()).start()
           
        
        place = avg.WordsNode(font="DejaVu Sans", opacity=0, variant="Bold", fontsize=convertFontSize(40), pivot = (0, 0), color = "111111", text = "Take your side now!", parent=parentNode)  
        place.pos = ((width-place.getMediaSize()[0])//2, height//2-place.getMediaSize()[0]//2)
        avg.LinearAnim(place, "opacity", 6000, 0, 1 ,False, None, lambda: avg.LinearAnim(place, "opacity", 2000, 1, 0 ,False, None, None).start() ).start()


       
    
    avg.fadeOut(__c1, 2000, textAnim)
    avg.fadeOut(__c2, 8000 )
    avg.fadeOut(__c3, 10000, lambda: __deactivateNode(__new))
    avg.fadeOut(__c4, 10000, endAction)
    
    
def startCloudFadeOut(parentNode, endAction=None):
     
    __activateNode(parentNode,__old )
    __activateNode(parentNode,__c1 )
    __activateNode(parentNode,__c2 )
    __activateNode(parentNode,__c3 )
    __activateNode(parentNode,__c4 )
    __activateNode(parentNode,__new )

    __old.pos = (0,0)
    __old.size= parentNode.size
    __new.pos=(0,0)
    __new.size= parentNode.size
    
    __c1.pos =( 0 - parentNode.width ,0 - parentNode.height )
    __c1.size = (parentNode.width * 2, parentNode.height * 2)
    
    __c2.pos =(0, -parentNode.height ) 
    __c2.size= (parentNode.width * 2, parentNode.height * 2)
    
    __c3.pos =(0,0)
    __c3.size = (parentNode.width * 2, parentNode.height * 2)
    
    __c4.pos = (-parentNode.width , 0)
    __c4.size = (parentNode.width * 2, parentNode.height * 2)
    
    
   
   
        
    ca1 = avg.LinearAnim(__c1, "pos", 4000, (0,0), __c1.pos                                    ,False, None, lambda: __deactivateNode(__c1))
    ca2 = avg.LinearAnim(__c2, "pos", 4000, (0,0) , __c2.pos                                   ,False, None, lambda: __deactivateNode(__c2))
    ca3 = avg.LinearAnim(__c3, "pos", 4000, (-parentNode.width ,-parentNode.height ), __c3.pos,False, None, lambda: __deactivateNode(__c3))
    ca4 = avg.LinearAnim(__c4, "pos", 4000,(0 ,0 - parentNode.height ) , __c4.pos             ,False, None ,lambda: __deactivateNode(__c4))
    
    ra2 = avg.LinearAnim(__new, "opacity", 4000, 1, 0 ,False, None,lambda: __deactivateNode(__new))
    
    ra2.start()
    ca1.start()
    ca2.start()
    ca3.start()
    ca4.start()
    avg.fadeOut(__c1, 4000)
    avg.fadeOut(__c2, 4000)
    avg.fadeOut(__c3, 4000, lambda: __deactivateNode(__old) )
    avg.fadeOut(__c4, 4000, endAction)
    
def startCloudFadeOut2(parentNode, endAction=None):
     
    __activateNode(parentNode,__old )
    __activateNode(parentNode,__c3 )
    __activateNode(parentNode,__c4 )
    __activateNode(parentNode,__new )

    __old.pos = (0,0)
    __old.size= parentNode.size
    __new.pos=(0,0)
    __new.size= parentNode.size
    
    __c1.pos =( 0 - parentNode.width ,0 - parentNode.height )
    __c1.size = (parentNode.width * 2, parentNode.height * 2)
    
    __c2.pos =(0, -parentNode.height ) 
    __c2.size= (parentNode.width * 2, parentNode.height * 2)
    
    __c3.pos =(0,0)
    __c3.size = (parentNode.width , parentNode.height )
    
    __c4.pos = (0,0)
    __c4.size = (parentNode.width , parentNode.height )
    
    
   
   
        
    ca1 = avg.LinearAnim(__c1, "pos", 10000, (0,0), __c1.pos                                    ,False, None, lambda: __deactivateNode(__c1))
    ca2 = avg.LinearAnim(__c2, "pos", 10000, (0,0), __c2.pos                                   ,False, None, lambda: __deactivateNode(__c2))
    ca3 = avg.LinearAnim(__c3, "pos", 10000, (-parentNode.width ,-parentNode.height ),__c3.pos,False, None, lambda: __deactivateNode(__c3))
    ca32 = avg.LinearAnim(__c3, "size", 10000, (parentNode.width*3 ,parentNode.height*3 ), __c3.size)
   
    ca4 = avg.LinearAnim(__c4, "pos", 10000, (-2*parentNode.width ,-2*parentNode.height ),__c4.pos             ,False, None ,lambda: __deactivateNode(__c4))
    ca41 = avg.LinearAnim(__c4, "size", 10000, (5*parentNode.width ,5*parentNode.height ), __c4.size)
    
    ra2 = avg.LinearAnim(__new, "opacity", 5000, 1, 0 ,False, None,lambda: __deactivateNode(__new))
    
    ra2.start()
    ca1.start()
    ca2.start()
    ca3.start()
    ca32.start()
    ca4.start()
    ca41.start()
        
    avg.fadeOut(__c1, 2000)
    avg.fadeOut(__c2, 8000 )
    avg.fadeOut(__c3, 10000, lambda: __deactivateNode(__old))
    avg.fadeOut(__c4, 10000, endAction)
    

def clear():
    global __new, __c1, __c2, __c3, __c4,__old

    __new = None
    __c1 =  None
    __c2 =  None
    __c3 =  None
    __c4 =  None
    __old = None    
    
def init():
    global __new, __c1, __c2, __c3, __c4,__old

    __new = avg.ImageNode(id="p2", opacity=1, href=os.path.join(getMediaDir(__file__, "resources"), "backgroundHRes.jpg"), pos=(0,0) )              
    __c1 =  avg.ImageNode(id="c1", opacity=1, href=os.path.join(getMediaDir(__file__, "resources"), "c1.png")) 
    __c2 =  avg.ImageNode(id="c2", opacity=1, href=os.path.join(getMediaDir(__file__, "resources"), "c2.png"))
    __c3 =  avg.ImageNode(id="c3", opacity=1, href=os.path.join(getMediaDir(__file__, "resources"), "c3.png"))
    __c4 =  avg.ImageNode(id="c4", opacity=1, href=os.path.join(getMediaDir(__file__, "resources"), "c4.png"))        
    __old = avg.ImageNode(id="p1", opacity=1, href=os.path.join(getMediaDir(__file__, "resources"), "MainBackground.jpg"), pos=(0,0))
          

    