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

#the width of the whole application
width = 1280

#the height of the whole application
height = 800

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


    