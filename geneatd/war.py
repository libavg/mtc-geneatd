#!/usr/bin/env python
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
from team import Team
from tower import Tower
from armageddonItem import ArmageddonItem
from expItem import ExpItem
from musicPlayer import MusicPlayer
from ultimaItem import UltimaItem
from towerKillItem import TowerKillItem
from levelDecreaseItem import LevelDecreaseItem
from creatureKillItem import CreatureKillItem
from preventTowerBuildingItem import PreventTowerBuildingItem
from indyTower import IndyTower
from iceTower import IceTower
from wizardCreature import WizardCreature
from scoutCreature import ScoutCreature
from mainMenu import MainMenu
from keyboard import Keyboard
from timeBar import TimeBar
from expBar import ExpBar
from itemBunker import ItemBunker
from preventCreatureBuildingItem import PreventCreatureBuildingItem
from freezeCreatureItem import FreezeCreatureItem
import util
import random
import os
import math
from libavg.AVGAppUtil import getMediaDir
from optparse import OptionParser 


# the global  player
g_player = avg.Player.get()

# tower creation time
towerCreationTime = 500

# map for event starting times - event id --> starting time
eventStartTimes = {}

# time span between item appearance
itemTimerTime = 2000

# indicates whether we run standalone
standAlone = False

# action layer
actionLayer = avg.DivNode(id="actionLayer", size=(util.width, util.height), pos=(0,0))

# creature layer
creatureLayer = avg.DivNode(id="creatureLayer", size=(util.width, util.height), pos=(0,0))

activeCreatureLayer = avg.DivNode(id="activeCreatureLayer", size=(util.width, util.height), pos=(0,0))

inActiveCreatureLayer = avg.DivNode(id="inActiveCreatureLayer", size=(util.width, util.height), pos=(0,0), sensitive=False)




class GeneaTD(gameapp.GameApp):   
    """
    The main class.
    """
    multitouch=True
    
    def __init__(self, parentNode):
        g_player.setOGLOptions(False, False, True, 4)
        util.updateSizes(parentNode.size.x, parentNode.size.y)
        
        avg.WordsNode.addFontDir(getMediaDir(__file__, "fonts"))
        self.musicEnabled = True
        super(GeneaTD, self).__init__(parentNode)


    def ownLeave(self):
        if standAlone:
            g_player.stop()
        else:
            util.clear()
            self.leave()

    def init(self):
        util.init()
        self._gameOver = True        
        self.parentNode = avg.DivNode(size=(self._parentNode.size.x, self._parentNode.size.y), pos=(0,0), parent= self._parentNode)

        self.team1TowerBlock = False;
        self.team2TowerBlock = False;
        
        self.timer1 = None
        self.timer2 = None

        self.team1CreatureBlock = False;
        self.team2CreatureBlock = False;

 
        self.timerCreature1 = None
        self.timerCreature2 = None
        
        self.soundPlayer = MusicPlayer(self._parentNode, self.musicEnabled)
        self.musicPlayer = MusicPlayer(self._parentNode, self.musicEnabled)
        
        self._mm = MainMenu(self.parentNode, g_player, self)
        
    def initialOption(self):
        """
        A method for init the left and right options. If not called in constructor, all options are available.
        """
        self.op = 0.4
                
        self.player1OptionsLeftWizardBack.opacity = self.op
        self.player1OptionsLeftWizardBack.sensitive = False
        self.player1OptionsLeftWizard.opacity = self.op
        self.player1OptionsLeftWizard.sensitive = False
        self.player1OptionsLeftScoutBack.opacity = self.op
        self.player1OptionsLeftScoutBack.sensitive = False
        self.player1OptionsLeftScout.opacity = self.op
        self.player1OptionsLeftScout.sensitive = False


        self.player2OptionsLeftWizardBack.opacity = self.op
        self.player2OptionsLeftWizardBack.sensitive = False
        self.player2OptionsLeftWizard.opacity = self.op
        self.player2OptionsLeftWizard.sensitive = False
        self.player2OptionsLeftScoutBack.opacity = self.op
        self.player2OptionsLeftScoutBack.sensitive = False
        self.player2OptionsLeftScout.opacity = self.op
        self.player2OptionsLeftScout.sensitive = False
        
        
        self.player1OptionsRightIceBack.opacity = self.op
        self.player1OptionsRightIceBack.sensitive = False
        self.player1OptionsRightIce.opacity = self.op
        self.player1OptionsRightIce.sensitive = False
        self.player1OptionsRightIndyBack.opacity = self.op
        self.player1OptionsRightIndyBack.sensitive = False
        self.player1OptionsRightIndy.opacity = self.op
        self.player1OptionsRightIndy.sensitive = False


        self.player2OptionsRightIceBack.opacity = self.op
        self.player2OptionsRightIceBack.sensitive = False
        self.player2OptionsRightIce.opacity = self.op
        self.player2OptionsRightIce.sensitive = False
        self.player2OptionsRightIndyBack.opacity = self.op
        self.player2OptionsRightIndyBack.sensitive = False
        self.player2OptionsRightIndy.opacity = self.op
        self.player2OptionsRightIndy.sensitive = False
       
        

    def showStars(self, id, amount):
        if (id==1):
            # adjust team1
            if amount ==0:
                self.homeBaseStar1.opacity=0.0
                self.homeBaseStar21.opacity=0.0
                self.homeBaseStar22.opacity=0.0
                self.homeBaseStar31.opacity=0.0
                self.homeBaseStar32.opacity=0.0
                self.homeBaseStar33.opacity=0.0
            if amount ==1:
                self.homeBaseStar1.opacity=0.7
                self.homeBaseStar21.opacity=0.0
                self.homeBaseStar22.opacity=0.0
                self.homeBaseStar31.opacity=0.0
                self.homeBaseStar32.opacity=0.0
                self.homeBaseStar33.opacity=0.0
            elif amount==2:
                self.homeBaseStar1.opacity=0.0
                self.homeBaseStar21.opacity=0.7
                self.homeBaseStar22.opacity=0.7
                self.homeBaseStar31.opacity=0.0
                self.homeBaseStar32.opacity=0.0
                self.homeBaseStar33.opacity=0.0                
            elif amount==3:
                self.homeBaseStar1.opacity=0.0
                self.homeBaseStar21.opacity=0.0
                self.homeBaseStar22.opacity=0.0
                self.homeBaseStar31.opacity=0.7
                self.homeBaseStar32.opacity=0.7
                self.homeBaseStar33.opacity=0.7

        else:
            # adjust team2
            if amount == 0:
                self.homeBase2Star1.opacity=0.0
                self.homeBase2Star21.opacity=0.0
                self.homeBase2Star22.opacity=0.0
                self.homeBase2Star31.opacity=0.0
                self.homeBase2Star32.opacity=0.0
                self.homeBase2Star33.opacity=0.0
            if amount ==1:
                self.homeBase2Star1.opacity=0.7
                self.homeBase2Star21.opacity=0.0
                self.homeBase2Star22.opacity=0.0
                self.homeBase2Star31.opacity=0.0
                self.homeBase2Star32.opacity=0.0
                self.homeBase2Star33.opacity=0.0
            elif amount==2:
                self.homeBase2Star1.opacity=0.0
                self.homeBase2Star21.opacity=0.7
                self.homeBase2Star22.opacity=0.7
                self.homeBase2Star31.opacity=0.0
                self.homeBase2Star32.opacity=0.0
                self.homeBase2Star33.opacity=0.0                
            elif amount==3:
                self.homeBase2Star1.opacity=0.0
                self.homeBase2Star21.opacity=0.0
                self.homeBase2Star22.opacity=0.0
                self.homeBase2Star31.opacity=0.7
                self.homeBase2Star32.opacity=0.7
                self.homeBase2Star33.opacity=0.7
     

    
    def adjustSkills(self, team, levelup):
        """
        Method that locks and unlocks skills for a player, regarding his level. 
        levelup: a boolean that indicates whether the team has a level up or a level down.
        """
        if (levelup):
            self.soundPlayer.playTune("soundfiles/sound_levelup.mp3")
        else:
            self.soundPlayer.playTune("soundfiles/sound_leveldown.mp3")
        
        if (team.id == 1):
            
            self.adjustSkillsTeam1(levelup)
        else:
            
            self.adjustSkillsTeam2(levelup)
    
    
    def adjustSkillsTeam1(self, levelup):
        """ 
        A helper method that adjust the skills for team1.
        """  
        if (self.oldLevelTeam1 == 0):
            if (levelup):
                self.player1OptionsRightIceBack.opacity = 1.0
                self.player1OptionsRightIceBack.sensitive = True
                self.player1OptionsRightIce.opacity = 1.0
                self.player1OptionsRightIce.sensitive = True
                self.oldLevelTeam1 = 1
                return
            else:
                return

       
                   
        if (self.oldLevelTeam1 == 1):
            if (levelup):
                self.player1OptionsLeftScoutBack.opacity = 1.0
                self.player1OptionsLeftScoutBack.sensitive = True
                self.player1OptionsLeftScout.opacity = 1.0
                self.player1OptionsLeftScout.sensitive = True
                self.oldLevelTeam1 = 2
                return
            else:
                self.player1OptionsRightIceBack.opacity = self.op
                self.player1OptionsRightIceBack.sensitive = False
                self.player1OptionsRightIce.opacity = self.op
                self.player1OptionsRightIce.sensitive = False
                self.activeTowerPlayer1 = 0
                self.clickMethodTowerPlayer1(self.activeTowerPlayer1)
                self.oldLevelTeam1 = 0
                return
           
           
        if (self.oldLevelTeam1 == 2):
            if (levelup):
                self.team1.currentDamageLevel = 2
                self.showStars(1, 1)
                self.oldLevelTeam1 = 3
                return
            else:
                self.player1OptionsLeftScoutBack.opacity = self.op
                self.player1OptionsLeftScoutBack.sensitive = False
                self.player1OptionsLeftScout.opacity = self.op
                self.player1OptionsLeftScout.sensitive = False
                self.activeCreaturePlayer1 = 0
                self.clickMethodCreaturePlayer1(self.activeCreaturePlayer1)
                self.oldLevelTeam1 = 1
                return  
           
             
       
        if (self.oldLevelTeam1 == 3):
            if (levelup):
                self.oldLevelTeam1 = 4
                return
            else: 
                self.team1.currentDamageLevel = 1
                self.showStars(1, 0)
                self.oldLevelTeam1 = 2
                return


        if (self.oldLevelTeam1 == 4):
            if (levelup):
                self.player1OptionsRightIndyBack.opacity = 1.0
                self.player1OptionsRightIndyBack.sensitive = True
                self.player1OptionsRightIndy.opacity = 1.0
                self.player1OptionsRightIndy.sensitive = True
                self.oldLevelTeam1 = 5
                return
            else:
                self.oldLevelTeam1 = 3
          
        if (self.oldLevelTeam1 == 5):
            if (levelup):   
                self.player1OptionsLeftWizardBack.opacity = 1.0
                self.player1OptionsLeftWizardBack.sensitive = True
                self.player1OptionsLeftWizard.opacity = 1.0
                self.player1OptionsLeftWizard.sensitive = True
                self.oldLevelTeam1 = 6
                return
            else:
                self.player1OptionsRightIndyBack.opacity = self.op
                self.player1OptionsRightIndyBack.sensitive = False
                self.player1OptionsRightIndy.opacity = self.op
                self.player1OptionsRightIndy.sensitive = False
                if (self.activeTowerPlayer1 == 2):
                    self.activeTowerPlayer1 = 1
                self.clickMethodTowerPlayer1(self.activeTowerPlayer1)
                self.oldLevelTeam1 = 4
                return         
           
        if (self.oldLevelTeam1 == 6):
            if (levelup): 
                self.team1.currentDamageLevel = 3
                self.showStars(1, 2)
                self.oldLevelTeam1 = 7
                return
            else:
                self.player1OptionsLeftWizardBack.opacity = self.op
                self.player1OptionsLeftWizardBack.sensitive = False
                self.player1OptionsLeftWizard.opacity = self.op
                self.player1OptionsLeftWizard.sensitive = False
                if (self.activeCreaturePlayer1 == 2):
                    self.activeCreaturePlayer1 = 1
                self.clickMethodCreaturePlayer1(self.activeCreaturePlayer1)
                self.oldLevelTeam1 = 5
                return
               
        if (self.oldLevelTeam1 == 7):
            if (levelup):
                self.oldLevelTeam1 = 8
                return 
            else:
                self.team1.currentDamageLevel = 2
                self.showStars(1, 1)
                self.oldLevelTeam1 = 6
                return
       
        if  (self.oldLevelTeam1  == 8):
            if (levelup):
                self.oldLevelTeam1  = 9
                self.showStars(1, 3)
                self.team1.currentDamageLevel = 4
                return
            else: 
                self.oldLevelTeam1 = 7
                return

          
        if (self.oldLevelTeam1  == 9):
            if (levelup):
                return
            else:
                self.oldLevelTeam1 = 8
                self.team1.currentDamageLevel = 3
                self.showStars(1, 2)
                return

    def adjustSkillsTeam2(self, levelup):
        """ 
        A helper method that adjust the skills for team2.
        """  
        if (self.oldLevelTeam2 == 0):
            if (levelup):
                self.player2OptionsRightIceBack.opacity = 1.0
                self.player2OptionsRightIceBack.sensitive = True
                self.player2OptionsRightIce.opacity = 1.0
                self.player2OptionsRightIce.sensitive = True
                self.oldLevelTeam2 = 1
                return
            else:
                return

       
                   
        if (self.oldLevelTeam2 == 1):
            if (levelup):
                self.player2OptionsLeftScoutBack.opacity = 1.0
                self.player2OptionsLeftScoutBack.sensitive = True
                self.player2OptionsLeftScout.opacity = 1.0
                self.player2OptionsLeftScout.sensitive = True
                self.oldLevelTeam2 = 2
                return
            else:
                self.player2OptionsRightIceBack.opacity = self.op
                self.player2OptionsRightIceBack.sensitive = False
                self.player2OptionsRightIce.opacity = self.op
                self.player2OptionsRightIce.sensitive = False
                self.activeTowerPlayer2 = 0
                self.clickMethodTowerPlayer2(self.activeTowerPlayer2)
                self.oldLevelTeam2 = 0
                return
           
           
        if (self.oldLevelTeam2 == 2):
            if (levelup):
                self.team2.currentDamageLevel = 2
                self.showStars(2, 1)
                self.oldLevelTeam2 = 3
                return
            else:
                self.player2OptionsLeftScoutBack.opacity = self.op
                self.player2OptionsLeftScoutBack.sensitive = False
                self.player2OptionsLeftScout.opacity = self.op
                self.player2OptionsLeftScout.sensitive = False
                self.activeCreaturePlayer2 = 0
                self.clickMethodCreaturePlayer2(self.activeCreaturePlayer2)
                self.oldLevelTeam2 = 1
                return  
           
             
       
        if (self.oldLevelTeam2 == 3):
            if (levelup):
                self.oldLevelTeam2 = 4
                return
            else: 
                self.team2.currentDamageLevel = 1
                self.oldLevelTeam2 = 2
                self.showStars(2, 0)
                return


        if (self.oldLevelTeam2 == 4):
            if (levelup):
                self.player2OptionsRightIndyBack.opacity = 1.0
                self.player2OptionsRightIndyBack.sensitive = True
                self.player2OptionsRightIndy.opacity = 1.0
                self.player2OptionsRightIndy.sensitive = True
                self.oldLevelTeam2 = 5
                return
            else:
                self.oldLevelTeam2 = 3
          
        if (self.oldLevelTeam2 == 5):
            if (levelup):   
                self.player2OptionsLeftWizardBack.opacity = 1.0
                self.player2OptionsLeftWizardBack.sensitive = True
                self.player2OptionsLeftWizard.opacity = 1.0
                self.player2OptionsLeftWizard.sensitive = True
                self.oldLevelTeam2 = 6
                return
            else:
                self.player2OptionsRightIndyBack.opacity = self.op
                self.player2OptionsRightIndyBack.sensitive = False
                self.player2OptionsRightIndy.opacity = self.op
                self.player2OptionsRightIndy.sensitive = False
                if (self.activeTowerPlayer2 == 2):
                    self.activeTowerPlayer2 = 1
                self.clickMethodTowerPlayer2(self.activeTowerPlayer2)
                self.oldLevelTeam2 = 4
                return         
           
        if (self.oldLevelTeam2 == 6):
            if (levelup): 
                self.team2.currentDamageLevel = 3
                self.showStars(2,2)
                self.oldLevelTeam2 = 7
                return
            else:
                self.player2OptionsLeftWizardBack.opacity = self.op
                self.player2OptionsLeftWizardBack.sensitive = False
                self.player2OptionsLeftWizard.opacity = self.op
                self.player2OptionsLeftWizard.sensitive = False
                if (self.activeCreaturePlayer2 == 2):
                    self.activeCreaturePlayer2 = 1
                self.clickMethodCreaturePlayer2(self.activeCreaturePlayer2)
                self.oldLevelTeam2 = 5
                return
               
        if (self.oldLevelTeam2 == 7):
            if (levelup):
                self.oldLevelTeam2 = 8
                return 
            else:
                self.team2.currentDamageLevel = 2
                self.showStars(2, 1)
                self.oldLevelTeam2 = 6
                return
       
        if  (self.oldLevelTeam2  == 8):
            if (levelup):
                self.oldLevelTeam2  = 9
                self.showStars(2, 3)
                self.team2.currentDamageLevel = 4
                return
            else: 
                self.oldLevelTeam2 = 7
                return

          
        if (self.oldLevelTeam2  == 9):
            if (levelup):

                return
            else:
                self.oldLevelTeam2 = 8
                self.showStars(2, 2)
                self.team2.currentDamageLevel = 3
                return
    
 
    def tossCoin(self):
        """
        A method that returns true or false.
        """
        return random.randint(0,1)
    
    
    
    def _itemTimerEvent(self):
        """
        Factory-Method - produces a new item.
        """
        # probabilities for the items.
        #p_expItem_1 = 20 / 106
        #p_expItem_2 = 10 / 106
        #p_expItem_3 = 5 / 106
        #p_creatureKillItem = 5 / 106
        #p_towerKillItem = 5 / 106
        #p_armageddonItem = 3 / 106
        #p_preventTowerBuildingItem = 3 / 106
        #p_preventCreatureBuildingItem = 3 / 106
        #p_freezeCreatureItem = 3/106
        #p_levelDecreaseItem = 2 / 106
        #p_ultimaItem = 1 / 106
            
        if not self._gameOver:
            randInt = random.randint(0,106)
 
            if (randInt > 59):
                return
            elif (56 < randInt <=59):
                FreezeCreatureItem(g_player, (random.randint(util.basewidth,util.width-util.basewidth-util.itemBunkerSize[0]), random.randint(util.sideBarheight, util.height-2*util.sideBarheight)), creatureLayer, self.team1, self.team2,  0, self, inActiveCreatureLayer)
            elif (53 < randInt <=56):
                PreventCreatureBuildingItem(g_player, (random.randint(util.basewidth,util.width-util.basewidth-util.itemBunkerSize[0]), random.randint(util.sideBarheight, util.height-2*util.sideBarheight)), creatureLayer, self.team1, self.team2, 0, self)   
            elif (0 <= randInt <= 19):
                ExpItem(g_player, (random.randint(util.basewidth,util.width-util.basewidth-util.itemBunkerSize[0]), random.randint(util.sideBarheight, util.height-2*util.sideBarheight)), creatureLayer, self.team1, self.team2, 1, self)
            
            elif (20 <= randInt <= 29):
                ExpItem(g_player, (random.randint(util.basewidth,util.width-util.basewidth-util.itemBunkerSize[0]), random.randint(util.sideBarheight, util.height-2*util.sideBarheight)), creatureLayer, self.team1, self.team2, 2, self)
            
            elif (30 <= randInt <= 34):
                ExpItem(g_player, (random.randint(util.basewidth,util.width-util.basewidth-util.itemBunkerSize[0]), random.randint(util.sideBarheight, util.height-2*util.sideBarheight)), creatureLayer, self.team1, self.team2, 3, self)
            
            elif (35 <= randInt <= 39):
                if self.tossCoin():
                    CreatureKillItem(g_player, (random.randint(util.basewidth,util.width-util.basewidth-util.itemBunkerSize[0]), random.randint(util.sideBarheight, util.height-2*util.sideBarheight)), creatureLayer, self.team1, self.team2, 2, 1, self, inActiveCreatureLayer)
                else:
                    CreatureKillItem(g_player, (random.randint(util.basewidth,util.width-util.basewidth-util.itemBunkerSize[0]), random.randint(util.sideBarheight, util.height-2*util.sideBarheight)), creatureLayer, self.team1, self.team2, 2, 2, self, inActiveCreatureLayer)    
                
            elif (40 <= randInt <= 44):
                if self.tossCoin():
                    TowerKillItem(g_player, (random.randint(util.basewidth,util.width-util.basewidth-util.itemBunkerSize[0]), random.randint(util.sideBarheight, util.height-2*util.sideBarheight)), creatureLayer, self.team1, self.team2, 2, 1, self, inActiveCreatureLayer)
                else:
                    TowerKillItem(g_player, (random.randint(util.basewidth,util.width-util.basewidth-util.itemBunkerSize[0]), random.randint(util.sideBarheight, util.height-2*util.sideBarheight)), creatureLayer, self.team1, self.team2, 2, 2, self, inActiveCreatureLayer)    
                
            elif (45 <= randInt <= 47):
                ArmageddonItem(g_player, (random.randint(util.basewidth,util.width-util.basewidth-util.itemBunkerSize[0]), random.randint(util.sideBarheight, util.height-2*util.sideBarheight)), creatureLayer, self.team1, self.team2, 2, self, inActiveCreatureLayer)
            
            elif (48 <= randInt <= 50):
                PreventTowerBuildingItem(g_player, (random.randint(util.basewidth,util.width-util.basewidth-util.itemBunkerSize[0]), random.randint(util.sideBarheight, util.height-2*util.sideBarheight)), creatureLayer, self.team1, self.team2, 0, self)
            
            elif (51 <= randInt <= 52):
                LevelDecreaseItem(g_player, (random.randint(util.basewidth,util.width-util.basewidth-util.itemBunkerSize[0]), random.randint(util.sideBarheight, util.height-2*util.sideBarheight)), creatureLayer, self.team1, self.team2, 0, self)
            
            elif (53 == randInt):
                UltimaItem(g_player, (random.randint(util.basewidth,util.width-util.basewidth-util.itemBunkerSize[0]), random.randint(util.sideBarheight, util.height-2*util.sideBarheight)), creatureLayer, self.team1, self.team2, 5, self, inActiveCreatureLayer)

    def clickMethodCreaturePlayer1(self, id):
        self.activeCreaturePlayer1=id
        self.hoverCreaturePlayer1.pos=((2-id)*util.sideBarheight, 0)

    def clickMethodCreaturePlayer2(self, id):
        self.activeCreaturePlayer2=id
        self.hoverCreaturePlayer2.pos=(id*util.sideBarheight, 0)


    def clickMethodTowerPlayer1(self, id):
        self.activeTowerPlayer1=id
        self.hoverTowerPlayer1.pos=((2-id)*util.sideBarheight, 0)

    def clickMethodTowerPlayer2(self, id):
        self.activeTowerPlayer2=id
        self.hoverTowerPlayer2.pos=(id*util.sideBarheight, 0)


    def gameTimeOver(self):
        self.parentNode.sensitive=False
        self.endGame();

    
    def blockAllTowers(self,id, block):
        """
        Method that prevents changing the right player options.
        id: the id of the player, who should be blocked/unblocked.
        block: True, if the player should be blocked. False, otherwise.
        """
        if (id == 1):
            if (block):
                self.player1OptionsRight.sensitive = False;
                self.player1OptionsRight.opacity = self.op
            else:
                self.player1OptionsRight.sensitive = True;
                self.player1OptionsRight.opacity = 1.0
        else:
            if (block):
                self.player2OptionsRight.sensitive = False;
                self.player2OptionsRight.opacity = self.op
            else:
                self.player2OptionsRight.sensitive = True;
                self.player2OptionsRight.opacity = 1.0

    def blockAllCreatures(self,id, block):
        """
        Method that prevents changing the right player options.
        id: the id of the player, who should be blocked/unblocked.
        block: True, if the player should be blocked. False, otherwise.
        """
        if (id == 1):
            if (block):
                self.homeBaseImg.opacity=1.0
                self.homeBaseImg.href=os.path.join(getMediaDir(__file__, "resources"), "baseStoned2.png")
            else:
                self.homeBaseImg.opacity=0.0
                self.homeBaseImg.href=os.path.join(getMediaDir(__file__, "resources"), "baseStoned2.png")
        else:
            if (block):
                self.homeBaseImg2.opacity=1.0
                self.homeBaseImg2.href=os.path.join(getMediaDir(__file__, "resources"), "baseStoned2.png")
            else:
                self.homeBaseImg2.opacity=0.0
                self.homeBaseImg2.href=os.path.join(getMediaDir(__file__, "resources"), "baseStoned2.png")


    
    def initGame(self, parentNode, highscore, gameTime = -1, maxPoints = -1):
        """
        Creates a new instance of the main class.
        """    
        
        
        global actionLayer
        actionLayer = avg.DivNode(id="actionLayer", size=(util.width, util.height), pos=(0,0))

        global creatureLayer    
        creatureLayer = avg.DivNode(id="creatureLayer", size=(util.width, util.height), pos=(0,0))

        global activeCreatureLayer
        activeCreatureLayer = avg.DivNode(id="activeCreatureLayer", size=(util.width, util.height), pos=(0,0))

        global inActiveCreatureLayer
        inActiveCreatureLayer = avg.DivNode(id="inActiveCreatureLayer", size=(util.width, util.height), pos=(0,0), sensitive=False)


        if not (gameTime == -1):
            self.gameTimer = g_player.setInterval(gameTime*60*1000, self.gameTimeOver) 
        
        self.gameTime = gameTime
        self.activeCreaturePlayer1=0
        self.activeCreaturePlayer2=0
        self.activeTowerPlayer1=0
        self.activeTowerPlayer2=0    
        self.overallField = avg.DivNode(pos=(0,0), size=(util.width, util.height), parent=parentNode)

        parentNode = self.overallField
        
        self._gameOver = False    
        self.highscore = highscore 
        self.team1 = Team("00008b","Team1", (0,(util.width-util.middleLinewidth)/2), util.width-util.basewidth, 1,1, (0,util.basewidth), self, maxPoints)
        self.team2 = Team("8b0000","Team2", ((util.width+util.middleLinewidth)/2, util.width),util.basewidth, -1,2, (util.width-util.basewidth, util.width), self, maxPoints)
        self.oldLevelTeam1 = 0
        self.oldLevelTeam2 = 0

        self.timeBar1=TimeBar(actionLayer,  avg.Point2D(0, util.height-util.menuAreaheight), self.team1.color,gameTime)
        self.timeBar2=TimeBar(actionLayer, avg.Point2D(util.width-util.expBarSize[0], 0), self.team2.color,gameTime,2)

        self.expBar1 = ExpBar(actionLayer,  avg.Point2D(0, 0), self.team1.color,10)
        self.expBar2 = ExpBar(actionLayer,  avg.Point2D(util.width-util.expBarSize[0], util.height-util.menuAreaheight), self.team2.color,10,2)
        
        self.itemBunker1Left = ItemBunker(actionLayer, avg.Point2D(util.expBarSize[0],0));
        self.itemBunker2Left = ItemBunker(actionLayer, avg.Point2D(util.width-(util.expBarSize[0]+util.itemBunkerSize[0]),util.height-util.menuAreaheight));

        self.itemBunker1Right = ItemBunker(actionLayer, avg.Point2D(util.expBarSize[0],util.height-util.menuAreaheight));
        self.itemBunker2Right = ItemBunker(actionLayer, avg.Point2D(util.width-(util.expBarSize[0]+util.itemBunkerSize[0]),0));

        
        def homeBaseTeam1Down(event):
            """
            Cursor click on home base --> creates a new creature.
            """
            if not self.team1CreatureBlock:
                if self.activeCreaturePlayer1==0:
                    Creature(g_player, self.team1, self.team2, event.pos, activeCreatureLayer, event.when, self, inActiveCreatureLayer, 8)
                elif self.activeCreaturePlayer1==1:
                    ScoutCreature(g_player, self.team1, self.team2, event.pos, activeCreatureLayer, event.when, self, inActiveCreatureLayer, 3)
                else:
                    WizardCreature(g_player, self.team1, self.team2, event.pos, activeCreatureLayer, event.when, self, inActiveCreatureLayer, 2)

        def homeBaseTeam2Click(event):
            """
            Cursor click on home base --> creates a new creature.
            """
            if not self.team2CreatureBlock:
                if self.activeCreaturePlayer2==0:
                    Creature(g_player, self.team2, self.team1, event.pos, activeCreatureLayer, event.when, self, inActiveCreatureLayer, 8)
                elif self.activeCreaturePlayer2==1:
                    ScoutCreature(g_player, self.team2, self.team1, event.pos, activeCreatureLayer, event.when, self, inActiveCreatureLayer,3)
                else:
                    WizardCreature(g_player, self.team2, self.team1, event.pos, activeCreatureLayer, event.when, self, inActiveCreatureLayer, 2)

        def createActionDown(event):
            """
            Starts the tower creation animation.
            """
            global eventStartTimes
            
            
            if event.node.id == "player1Field":
                if self.team1.checkBaseArea(event.pos.x, event.pos.y):
                    homeBaseTeam1Down(event)
                    return;
            
            if event.node.id == "player2Field":
                if self.team2.checkBaseArea(event.pos.x, event.pos.y):
                    homeBaseTeam2Click(event)
                    return;
            
            if (event.node.id == "player1Field" and not self.team1TowerBlock and util.sideBarheight<event.pos.y<util.height-util.sideBarheight):
                creationCircle = avg.CircleNode(fillopacity=0.3, strokewidth=0, pos=event.pos, parent=actionLayer)
                
                creationCircle.setEventHandler(avg.CURSORUP,avg.TOUCH | avg.MOUSE, createActionUp); 
                creationCircle.setEventHandler(avg.CURSOROUT,avg.TOUCH | avg.MOUSE, createActionUp); 
    
                anim = avg.LinearAnim(creationCircle,"r", towerCreationTime, util.creationCircleRadius//6, util.creationCircleRadius, False, None, lambda : createActionUp(event))
                anim.start()
            
                eventStartTimes[event.cursorid]=(anim, creationCircle)
            
            if event.node.id == "player2Field" and not self.team2TowerBlock and util.sideBarheight<event.pos.y<util.height-util.sideBarheight:
                
                creationCircle = avg.CircleNode(fillopacity=0.3, strokewidth=0, pos=event.pos, parent=actionLayer)
                creationCircle.setEventHandler(avg.CURSORUP,avg.TOUCH | avg.MOUSE, createActionUp); 
                creationCircle.setEventHandler(avg.CURSOROUT,avg.TOUCH | avg.MOUSE, createActionUp); 
    
                anim = avg.LinearAnim(creationCircle,"r", towerCreationTime, util.creationCircleRadius // 6, util.creationCircleRadius, False, None, lambda : createActionUp(event))
                anim.start()
            
                eventStartTimes[event.cursorid]=(anim, creationCircle)
  
            
        def createActionUp(event):
            """
            Called if the tower creation circle generation is finished.
            If finished successful, a new tower is created. Otherwise an action will take place.
            """
            if event.cursorid in eventStartTimes:
                anim, circle = eventStartTimes[event.cursorid]
                if not anim.isRunning():
                    
                    team = self.team2
                
                    if event.node.id == "player1Field":
                        team=self.team1
                        
                        if self.activeTowerPlayer1==0:
                            Tower(team, event.pos, actionLayer, creatureLayer)
                        elif self.activeTowerPlayer1==1:
                            IceTower(team, event.pos, actionLayer, creatureLayer)
                        else:
                            IndyTower(team, event.pos, actionLayer,  creatureLayer)
                            
                    else:
                        if self.activeTowerPlayer2==0:
                            Tower(team, event.pos, actionLayer,  creatureLayer)
                        elif self.activeTowerPlayer2==1:
                            IceTower(team, event.pos, actionLayer,  creatureLayer)
                        else:
                            IndyTower(team, event.pos, actionLayer,  creatureLayer)
                        
                        
                                
                            
                else:
                    anim.setStopCallback(None)
                    anim.abort()
                    
                circle.unlink(True)
                del eventStartTimes[event.cursorid]
                   
            
        

        self.field = avg.RectNode(id="field", fillopacity=1, strokewidth=0, filltexhref=os.path.join(getMediaDir(__file__, "resources"), "backgroundHRes.jpg"), pos=(0,0), size=(util.width, util.height))
        
         
        self.player1Field = avg.DivNode(id="player1Field", pos=(0,0), size=(((util.width-util.middleLinewidth)/2),util.height))

        self.player1Field.setEventHandler(avg.CURSORDOWN,avg.TOUCH | avg.MOUSE, createActionDown);
        self.player1Field.setEventHandler(avg.CURSORUP,avg.TOUCH | avg.MOUSE, createActionUp); 
        

        self.player2Field = avg.DivNode(id="player2Field", pos=(((util.width+util.middleLinewidth)/2),0), size=(((util.width-util.middleLinewidth)/2),util.height))
        self.player2Field.setEventHandler(avg.CURSORDOWN,avg.TOUCH | avg.MOUSE, createActionDown);
        self.player2Field.setEventHandler(avg.CURSORUP,avg.TOUCH | avg.MOUSE, createActionUp); 
    
        
        starPath = os.path.join(getMediaDir(__file__, "resources"), "labels/star.png")
        
        self.homeBaseStar1 = avg.ImageNode(href=starPath, size=util.starSize, pos=((util.basewidth-util.starSize[0])//2, (util.height-util.starSize[1])//2), opacity=0.0)
        
        self.homeBaseStar21 = avg.ImageNode(href=starPath, size=util.starSize, pos=((util.basewidth-util.starSize[0])//2, (util.height-util.starSize[1])//2-util.starSize[1]), opacity=0.0)
 
        self.homeBaseStar22 = avg.ImageNode(href=starPath, size=util.starSize, pos=((util.basewidth-util.starSize[0])//2, (util.height-util.starSize[1])//2+util.starSize[1]), opacity=0.0)
        
        self.homeBaseStar31 = avg.ImageNode(href=starPath, size=util.starSize, pos=((util.basewidth-util.starSize[0])//2, (util.height-util.starSize[1])//2-util.starSize[1]), opacity=0.0)

        self.homeBaseStar32 = avg.ImageNode(href=starPath, size=util.starSize, pos=(util.basewidth//2, (util.height-util.starSize[1])//2), opacity=0.0)
        
        self.homeBaseStar33 = avg.ImageNode(href=starPath, size=util.starSize, pos=((util.basewidth-util.starSize[0])//2, (util.height-util.starSize[1])//2+util.starSize[1]), opacity=0.0)
        
        
        self.homeBaseNode = avg.RectNode(id="team1BaseArea", fillopacity=0.3, strokewidth=0, pos=(0, util.menuAreaheight), fillcolor=self.team1.color, size=(util.basewidth, util.height-2*util.menuAreaheight))

        self.homeBaseNode.setEventHandler(avg.CURSORDOWN,avg.TOUCH | avg.MOUSE,homeBaseTeam1Down)
        
        self.homeBaseImg = avg.ImageNode(href=os.path.join(getMediaDir(__file__, "resources"), "baseStoned2.png"), pos=(0, util.menuAreaheight), opacity=0.0, size = (util.basewidth, util.height-2*util.menuAreaheight))
        

        starPath = os.path.join(getMediaDir(__file__, "resources"), "labels/star2.png")

        self.homeBase2Star1 = avg.ImageNode(href=starPath, size=util.starSize, pos=(util.width-(util.basewidth+util.starSize[0])//2,  (util.height-util.starSize[1])//2), opacity=0.0)
        
        self.homeBase2Star21 = avg.ImageNode(href=starPath, size=util.starSize, pos=(util.width-(util.basewidth+util.starSize[0])//2, (util.height-util.starSize[1])//2-util.starSize[1]), opacity=0.0)
        
        self.homeBase2Star22 = avg.ImageNode(href=starPath, size=util.starSize, pos=(util.width-(util.basewidth+util.starSize[0])//2,(util.height-util.starSize[1])//2+util.starSize[1]), opacity=0.0)
        
        self.homeBase2Star31 = avg.ImageNode(href=starPath, size=util.starSize, pos=(util.width-(util.basewidth+util.starSize[0])//2, (util.height-util.starSize[1])//2-util.starSize[1]), opacity=0.0)
        
        self.homeBase2Star32 = avg.ImageNode(href=starPath, size=util.starSize, pos=(util.width-util.basewidth//2-util.starSize[0],  (util.height-util.starSize[1])//2), opacity=0.0)
        
        self.homeBase2Star33 = avg.ImageNode(href=starPath, size=util.starSize, pos=(util.width-(util.basewidth+util.starSize[0])//2, (util.height-util.starSize[1])//2+util.starSize[1]), opacity=0.0)
        
        
        self.homeBaseNode2 = avg.RectNode(id="team2BaseArea", fillopacity=0.3, strokewidth=0, pos=(util.width-util.basewidth,util.menuAreaheight), fillcolor=self.team2.color, size=(util.basewidth, util.height-2*util.menuAreaheight))

        self.homeBaseNode2.setEventHandler(avg.CURSORDOWN,avg.TOUCH | avg.MOUSE,homeBaseTeam2Click)
        
        self.homeBaseImg2 = avg.ImageNode(href=os.path.join(getMediaDir(__file__, "resources"), "baseStoned2.png"), pos=(util.width-util.basewidth,util.menuAreaheight), opacity=0.0, size = (util.basewidth, util.height-2*util.menuAreaheight))

        
   
       
        self.middleLine = avg.RectNode(id="border", fillopacity=0.0, fillcolor="FFFFFF", strokewidth=0, pos=((util.width-util.middleLinewidth)/2,0), size=(util.middleLinewidth, util.height))

        
        def createButton(pos,size, href):
            return avg.ImageNode(pos=pos, size=size, href=href)

                
        def createButtonBackground(pos):
            return createButton(pos, (util.sideBarheight, util.sideBarheight), os.path.join(getMediaDir(__file__, "resources"), "buttonbackground.png"))
        
       
        self.player1OptionsLeft = avg.DivNode(pos=(util.expBarSize[0] + util.sideBarheight,0), size=(3*util.menuAreaheight, util.menuAreaheight))

        self.player1OptionsLeftWizardBack = createButtonBackground((0,0))
        self.player1OptionsLeftWizard = createButton((util.imageMargin,util.imageMargin), util.imageSize, os.path.join(getMediaDir(__file__, "resources"), "circleGood.png"))
         
        self.player1OptionsLeftWizardBack.setEventHandler(avg.CURSORDOWN, avg.TOUCH | avg.MOUSE, lambda event : self.clickMethodCreaturePlayer1(2)) 
        self.player1OptionsLeftWizard.setEventHandler(avg.CURSORDOWN, avg.TOUCH | avg.MOUSE, lambda event : self.clickMethodCreaturePlayer1(2)) 

 
        self.player1OptionsLeftScoutBack = createButtonBackground((util.sideBarheight,0))
        self.player1OptionsLeftScout = createButton((util.sideBarheight+util.imageMargin,util.imageMargin), util.imageSize, os.path.join(getMediaDir(__file__, "resources"), "triangleGood.png"))      
        
        self.player1OptionsLeftScoutBack.setEventHandler(avg.CURSORDOWN, avg.TOUCH | avg.MOUSE, lambda event : self.clickMethodCreaturePlayer1(1)) 
        self.player1OptionsLeftScout.setEventHandler(avg.CURSORDOWN, avg.TOUCH | avg.MOUSE, lambda event : self.clickMethodCreaturePlayer1(1)) 


        self.player1OptionsLeftNormalBack = createButtonBackground((2*util.sideBarheight,0))
        self.player1OptionsLeftNormal = createButton((2*util.sideBarheight+util.imageMargin,util.imageMargin), util.imageSize, os.path.join(getMediaDir(__file__, "resources"), "squareGood.png"))      
  
        self.player1OptionsLeftNormalBack.setEventHandler(avg.CURSORDOWN, avg.TOUCH | avg.MOUSE, lambda event : self.clickMethodCreaturePlayer1(0)) 
        self.player1OptionsLeftNormal.setEventHandler(avg.CURSORDOWN, avg.TOUCH | avg.MOUSE, lambda event : self.clickMethodCreaturePlayer1(0)) 
  
        
        self.player1OptionsLeft.appendChild(self.player1OptionsLeftWizardBack)       
        self.player1OptionsLeft.appendChild(self.player1OptionsLeftScoutBack)        
        self.player1OptionsLeft.appendChild(self.player1OptionsLeftNormalBack)
        
        self.hoverCreaturePlayer1 = createButton((2*util.sideBarheight,0), (util.sideBarheight,util.sideBarheight), os.path.join(getMediaDir(__file__, "resources"), "greymask.png"))
        self.hoverCreaturePlayer1.blendmode = "add"
        self.player1OptionsLeft.appendChild(self.hoverCreaturePlayer1)
        
        self.player1OptionsLeft.appendChild(self.player1OptionsLeftWizard)
        self.player1OptionsLeft.appendChild(self.player1OptionsLeftScout)
        self.player1OptionsLeft.appendChild(self.player1OptionsLeftNormal)



        self.player1OptionsRight = avg.DivNode(pos=((util.expBarSize[0]+util.sideBarheight),util.height-util.menuAreaheight), size=(3*util.menuAreaheight, util.menuAreaheight))

        self.player1OptionsRightIndyBack = createButtonBackground((0,0))
        self.player1OptionsRightIndy = createButton((util.imageMargin,util.imageMargin), util.imageSize, os.path.join(getMediaDir(__file__, "resources"), "fireball.png"))
                
        
        self.player1OptionsRightIndyBack.setEventHandler(avg.CURSORDOWN, avg.TOUCH | avg.MOUSE, lambda event : self.clickMethodTowerPlayer1(2)) 
        self.player1OptionsRightIndy.setEventHandler(avg.CURSORDOWN, avg.TOUCH | avg.MOUSE, lambda event : self.clickMethodTowerPlayer1(2)) 


        self.player1OptionsRightIceBack = createButtonBackground((util.sideBarheight,0))
        self.player1OptionsRightIce = createButton((util.sideBarheight+util.imageMargin,util.imageMargin), util.imageSize, os.path.join(getMediaDir(__file__, "resources"), "iceball.png"))      
        

        self.player1OptionsRightIceBack.setEventHandler(avg.CURSORDOWN, avg.TOUCH | avg.MOUSE, lambda event : self.clickMethodTowerPlayer1(1)) 
        self.player1OptionsRightIce.setEventHandler(avg.CURSORDOWN, avg.TOUCH | avg.MOUSE, lambda event : self.clickMethodTowerPlayer1(1)) 



        self.player1OptionsRightNormalBack = createButtonBackground((2*util.sideBarheight,0))
        self.player1OptionsRightNormal = createButton((2*util.sideBarheight+util.imageMargin,util.imageMargin), util.imageSize, os.path.join(getMediaDir(__file__, "resources"), "blackball.png"))     
        
        self.player1OptionsRightNormalBack.setEventHandler(avg.CURSORDOWN, avg.TOUCH | avg.MOUSE, lambda event : self.clickMethodTowerPlayer1(0)) 
        self.player1OptionsRightNormal.setEventHandler(avg.CURSORDOWN, avg.TOUCH | avg.MOUSE, lambda event : self.clickMethodTowerPlayer1(0)) 

        self.player1OptionsRight.appendChild(self.player1OptionsRightIndyBack)      
        self.player1OptionsRight.appendChild(self.player1OptionsRightIceBack)       
        self.player1OptionsRight.appendChild(self.player1OptionsRightNormalBack)
        
        self.hoverTowerPlayer1 = createButton((2*util.sideBarheight,0), (util.sideBarheight, util.sideBarheight), os.path.join(getMediaDir(__file__, "resources"), "greymask.png"))
        self.hoverTowerPlayer1.blendmode = "add"
        self.player1OptionsRight.appendChild(self.hoverTowerPlayer1)
        
        self.player1OptionsRight.appendChild(self.player1OptionsRightIndy)        
        self.player1OptionsRight.appendChild(self.player1OptionsRightIce)        
        self.player1OptionsRight.appendChild(self.player1OptionsRightNormal)




        self.player2OptionsLeft = avg.DivNode(pos=(util.width-3*util.menuAreaheight-(util.expBarSize[0]+util.sideBarheight),util.height-util.menuAreaheight), size=(3*util.menuAreaheight, util.menuAreaheight))
        

        

        self.player2OptionsLeftNormalBack = createButtonBackground((0,0))
        self.player2OptionsLeftNormal = createButton((util.imageMargin,util.imageMargin), util.imageSize, os.path.join(getMediaDir(__file__, "resources"), "squareEvil.png"))      
        
        self.player2OptionsLeftNormalBack.setEventHandler(avg.CURSORDOWN, avg.TOUCH | avg.MOUSE, lambda event : self.clickMethodCreaturePlayer2(0)) 
        self.player2OptionsLeftNormal.setEventHandler(avg.CURSORDOWN, avg.TOUCH | avg.MOUSE, lambda event : self.clickMethodCreaturePlayer2(0)) 
       

        self.player2OptionsLeftScoutBack = createButtonBackground((util.sideBarheight,0))
        self.player2OptionsLeftScout = createButton((util.sideBarheight+util.imageMargin,util.imageMargin), util.imageSize, os.path.join(getMediaDir(__file__, "resources"), "triangleEvil.png"))      
        
        self.player2OptionsLeftScoutBack.setEventHandler(avg.CURSORDOWN, avg.TOUCH | avg.MOUSE, lambda event : self.clickMethodCreaturePlayer2(1)) 
        self.player2OptionsLeftScout.setEventHandler(avg.CURSORDOWN, avg.TOUCH | avg.MOUSE, lambda event : self.clickMethodCreaturePlayer2(1)) 
 

        self.player2OptionsLeftWizardBack = createButtonBackground((2*util.sideBarheight,0))
        self.player2OptionsLeftWizard = createButton((2*util.sideBarheight+util.imageMargin,util.imageMargin), util.imageSize, os.path.join(getMediaDir(__file__, "resources"), "circleEvil.png"))

        self.player2OptionsLeftWizardBack.setEventHandler(avg.CURSORDOWN, avg.TOUCH | avg.MOUSE, lambda event : self.clickMethodCreaturePlayer2(2)) 
        self.player2OptionsLeftWizard.setEventHandler(avg.CURSORDOWN, avg.TOUCH | avg.MOUSE, lambda event : self.clickMethodCreaturePlayer2(2)) 
                

        self.player2OptionsLeft.appendChild(self.player2OptionsLeftNormalBack)
        self.player2OptionsLeft.appendChild(self.player2OptionsLeftScoutBack)
        self.player2OptionsLeft.appendChild(self.player2OptionsLeftWizardBack)
        
        self.hoverCreaturePlayer2 = createButton((0,0), (util.sideBarheight, util.sideBarheight), os.path.join(getMediaDir(__file__, "resources"), "greymask.png"))
        self.hoverCreaturePlayer2.blendmode = "add"
        self.player2OptionsLeft.appendChild(self.hoverCreaturePlayer2)
 
        self.player2OptionsLeft.appendChild(self.player2OptionsLeftNormal)
        self.player2OptionsLeft.appendChild(self.player2OptionsLeftScout)
        self.player2OptionsLeft.appendChild(self.player2OptionsLeftWizard)



        self.player2OptionsRight = avg.DivNode(pos=(util.width-3*util.menuAreaheight-(util.expBarSize[0]+util.sideBarheight),0), size=(3*util.menuAreaheight, util.menuAreaheight)) 

        self.player2OptionsRightNormalBack = createButtonBackground((0,0))
        self.player2OptionsRightNormal = createButton((util.imageMargin,util.imageMargin), util.imageSize, os.path.join(getMediaDir(__file__, "resources"), "blackball.png"))      

        self.player2OptionsRightNormalBack.setEventHandler(avg.CURSORDOWN, avg.TOUCH | avg.MOUSE, lambda event : self.clickMethodTowerPlayer2(0)) 
        self.player2OptionsRightNormal.setEventHandler(avg.CURSORDOWN, avg.TOUCH | avg.MOUSE, lambda event : self.clickMethodTowerPlayer2(0)) 
        
       

        self.player2OptionsRightIceBack = createButtonBackground((util.sideBarheight,0))
        self.player2OptionsRightIce = createButton((util.sideBarheight+util.imageMargin, util.imageMargin), util.imageSize, os.path.join(getMediaDir(__file__, "resources"), "iceball.png"))      
        
        self.player2OptionsRightIceBack.setEventHandler(avg.CURSORDOWN, avg.TOUCH | avg.MOUSE, lambda event : self.clickMethodTowerPlayer2(1)) 
        self.player2OptionsRightIce.setEventHandler(avg.CURSORDOWN, avg.TOUCH | avg.MOUSE, lambda event : self.clickMethodTowerPlayer2(1)) 
 

        self.player2OptionsRightIndyBack = createButtonBackground((2*util.sideBarheight,0))
        self.player2OptionsRightIndy = createButton((2*util.sideBarheight+util.imageMargin,util.imageMargin), util.imageSize, os.path.join(getMediaDir(__file__, "resources"), "fireball.png"))


        self.player2OptionsRightIndyBack.setEventHandler(avg.CURSORDOWN, avg.TOUCH | avg.MOUSE, lambda event : self.clickMethodTowerPlayer2(2)) 
        self.player2OptionsRightIndy.setEventHandler(avg.CURSORDOWN, avg.TOUCH | avg.MOUSE, lambda event : self.clickMethodTowerPlayer2(2)) 


        self.player2OptionsRight.appendChild(self.player2OptionsRightNormalBack)                
        self.player2OptionsRight.appendChild(self.player2OptionsRightIceBack)
        self.player2OptionsRight.appendChild(self.player2OptionsRightIndyBack)


        
        self.hoverTowerPlayer2 = createButton((0,0), (util.sideBarheight,util.sideBarheight), os.path.join(getMediaDir(__file__, "resources"), "greymask.png"))
        self.hoverTowerPlayer2.blendmode = "add"
        self.player2OptionsRight.appendChild(self.hoverTowerPlayer2)
        
        self.player2OptionsRight.appendChild(self.player2OptionsRightNormal)        
        self.player2OptionsRight.appendChild(self.player2OptionsRightIce)        
        self.player2OptionsRight.appendChild(self.player2OptionsRightIndy)

        creatureLayer.appendChild(self.homeBaseStar1)
        creatureLayer.appendChild(self.homeBaseStar21)
        creatureLayer.appendChild(self.homeBaseStar22)
        creatureLayer.appendChild(self.homeBaseStar31)
        creatureLayer.appendChild(self.homeBaseStar32)
        creatureLayer.appendChild(self.homeBaseStar33)

        creatureLayer.appendChild(self.homeBase2Star1)
        creatureLayer.appendChild(self.homeBase2Star21)
        creatureLayer.appendChild(self.homeBase2Star22)
        creatureLayer.appendChild(self.homeBase2Star31)
        creatureLayer.appendChild(self.homeBase2Star32)
        creatureLayer.appendChild(self.homeBase2Star33)


        creatureLayer.appendChild(self.homeBaseNode)
        creatureLayer.appendChild(self.homeBaseNode2)
        creatureLayer.appendChild(self.homeBaseImg)
        creatureLayer.appendChild(self.homeBaseImg2)
    
        
        self.overallField.appendChild(self.field)    
        self.team1.appendScoreNodes(self.overallField)
        self.team2.appendScoreNodes(self.overallField)

        self.overallField.appendChild(creatureLayer)  
        creatureLayer.appendChild(inActiveCreatureLayer)  
        creatureLayer.appendChild(activeCreatureLayer)

        activeCreatureLayer.appendChild(actionLayer)      
        actionLayer.appendChild(self.player1Field)
        actionLayer.appendChild(self.player2Field)
        creatureLayer.appendChild(self.middleLine)

        self.overallField.appendChild(self.player1OptionsLeft)
        self.overallField.appendChild(self.player2OptionsLeft)
        self.overallField.appendChild(self.player1OptionsRight)
        self.overallField.appendChild(self.player2OptionsRight)
        
        self.initialOption()
        
        
        self.itemTimer = g_player.setInterval(itemTimerTime, self._itemTimerEvent)
        
        
         
          
    def onKeyDown(self, event):
        if event.keystring == 'q':
            if not self._gameOver:
                self.endGame()
                
        if event.keystring == 'n':
            self._mm.muteClick(None)
        
            



    def showKeyboard(self):
        global actionLayer, activeCreatureLayer, inActiveCreatureLayer, creatureLayer
        self.itemBunker1Left.node.unlink(True)
        self.itemBunker1Right.node.unlink(True)
        self.itemBunker2Left.node.unlink(True)
        self.itemBunker2Right.node.unlink(True)
        self.overallField.unlink(True)
        actionLayer.unlink(True)
        self.player1Field.unlink(True)
        self.player2Field.unlink(True)
        self.homeBaseNode.unlink(True)
        self.homeBaseNode2.unlink(True)
        self.middleLine.unlink(True)
        activeCreatureLayer.unlink(True)
        inActiveCreatureLayer.unlink(True)
        creatureLayer.unlink(True)
        self.field.unlink(True)
        self.player1OptionsLeft.unlink(True)
        self.player2OptionsLeft.unlink(True)
        self.player1OptionsRight.unlink(True)
        self.player2OptionsRight.unlink(True)
        self.timeBar1.timeBarDiv.unlink(True)
        self.timeBar2.timeBarDiv.unlink(True)
        self.expBar1.expBarDiv.unlink(True)
        self.expBar2.expBarDiv.unlink(True)
        self.homeBase2Star1.unlink(True)
        self.homeBase2Star21.unlink(True)
        self.homeBase2Star22.unlink(True)
        self.homeBase2Star31.unlink(True)
        self.homeBase2Star32.unlink(True)
        self.homeBase2Star33.unlink(True)
        self.homeBaseStar1.unlink(True)
        self.homeBaseStar21.unlink(True)
        self.homeBaseStar22.unlink(True)
        self.homeBaseStar31.unlink(True)
        self.homeBaseStar32.unlink(True)
        self.homeBaseStar33.unlink(True)
       
        actionLayer = None
        creatureLayer = None
        activeCreatureLayer = None
        inActiveCreatureLayer = None
        

        self.overallField = None
        self.timeBar1=None
        self.timeBar2=None

        self.expBar1 = None
        self.expBar2 = None
        
        self.itemBunker1Left = None
        self.itemBunker2Left = None

        self.itemBunker1Right = None
        self.itemBunker2Right = None
        
        
        self.field = None
        
         
        self.player1Field = None
        self.player2Field = None

        self.homeBaseStar1 = None
        self.homeBaseStar21 = None
        self.homeBaseStar22 = None
        self.homeBaseStar31 = None
        self.homeBaseStar32 = None
        self.homeBaseStar33 = None
        
        self.homeBaseNode = None
        self.homeBaseImg = None
        

        self.homeBase2Star1 = None
        self.homeBase2Star21 = None
        self.homeBase2Star22 = None
        self.homeBase2Star31 = None
        self.homeBase2Star32 = None
        self.homeBase2Star33 = None
        
        
        self.homeBaseNode2 = None
        self.homeBaseImg2 = None

        self.middleLine = None


        self.player1OptionsLeft = None

        self.player1OptionsLeftWizardBack = None
        self.player1OptionsLeftWizard = None
         
        self.player1OptionsLeftScoutBack = None
        self.player1OptionsLeftScout = None    
        
        self.player1OptionsLeftNormalBack = None
        self.player1OptionsLeftNormal = None      
          
        self.hoverCreaturePlayer1 = None
        
        self.player1OptionsRight = None

        self.player1OptionsRightIndyBack = None
        self.player1OptionsRightIndy = None
                       
        self.player1OptionsRightIceBack = None
        self.player1OptionsRightIce = None
        
        self.player1OptionsRightNormalBack = None
        self.player1OptionsRightNormal = None
        
        self.hoverTowerPlayer1 = None

        self.player2OptionsLeft = None

        

        self.player2OptionsLeftNormalBack = None
        self.player2OptionsLeftNormal = None
        

        self.player2OptionsLeftScoutBack = None
        self.player2OptionsLeftScout = None 
        
       

        self.player2OptionsLeftWizardBack = None
        self.player2OptionsLeftWizard = None
        
        self.hoverCreaturePlayer2 = None

        self.player2OptionsRight = None
        self.player2OptionsRightNormalBack = None
        self.player2OptionsRightNormal = None
       

        self.player2OptionsRightIceBack = None
        self.player2OptionsRightIce = None

        self.player2OptionsRightIndyBack = None
        self.player2OptionsRightIndy = None


        
        self.hoverTowerPlayer2 = None
        g_player.clearInterval(self.itemTimer)
        
        
        self.victoryScoreLeft =   None 
        self.victoryScoreRight =  None
        self.victoryWordsLeft = None
        self.victoryWordsRight = None


       
        lowestEntry = (int) (self.highscore.getLowestEntry())
     
        Keyboard(self.parentNode, self.team1.score>=lowestEntry, self.team2.score>=lowestEntry, self.highscore, (self.team1.score, self.team2.score), self)
 
        self.parentNode.sensitive=True
        self.team1 = None
        self.team2 = None
        
       
    

    def endGame(self):
        self._gameOver = True
        if not self.gameTime == -1:
            g_player.clearInterval(self.gameTimer)
    
        if not self.itemTimer == -1:
            g_player.clearInterval(self.itemTimer)
            
        self.team1.score += self.team1.points*10
        self.team2.score += self.team2.points*10
        self.team1.score += self.team1._exp*10
        self.team2.score += self.team2._exp*10
        
        
        
        self.victoryLeft = avg.DivNode(pos=(0, util.halfwidth), size = (util.height, util.halfwidth), pivot =(util.halfwidth,0), angle = math.pi/2)

        self.victoryRight = avg.DivNode(pos=(util.halfwidth,util.height), size = (util.height, util.halfwidth), pivot =(0,0), angle = -math.pi/2)
        

        
        self.victoryScoreLeft =   avg.WordsNode(font="DejaVu Sans", variant="Bold", opacity=0.0, fontsize=util.convertFontSize(32), text="Score: "+str(self.team1.score), parent=self.victoryLeft)
        self.victoryScoreLeft.pos = ((util.height-self.victoryScoreLeft.getMediaSize()[0])//2,util.width//7)

        self.victoryScoreRight =  avg.WordsNode(font="DejaVu Sans", variant="Bold", opacity=0.0, fontsize=util.convertFontSize(32), text="Score: "+str(self.team2.score), parent=self.victoryRight)
        self.victoryScoreRight.pos = ((util.height-self.victoryScoreRight.getMediaSize()[0])//2,util.width//7)
 

        self.victoryWordsLeft = avg.WordsNode(font="DejaVu Sans", variant="Bold", opacity=0.0, fontsize=util.convertFontSize(32), parent=self.victoryLeft)
        
        self.victoryWordsRight = avg.WordsNode(font="DejaVu Sans", variant="Bold", opacity=0.0, fontsize=util.convertFontSize(32), parent=self.victoryRight)

        if (self.team1.points > self.team2.points):
            self.victoryWordsLeft.text = "Team Blue has won the fight!"
            self.victoryWordsRight.text = "Team Blue has won the fight!"
            self.musicPlayer.playTune("soundfiles/music_goodwins.mp3")

 
        elif (self.team1.points < self.team2.points):
            self.victoryWordsLeft.text = "Team Red has won the fight!"
            self.victoryWordsRight.text = "Team Red has won the fight!"
            self.musicPlayer.playTune("soundfiles/music_badwins.mp3") 

        else:
            self.victoryWordsLeft.text = "Draw"
            self.victoryWordsRight.text = "Draw"
            self.musicPlayer.playTune("soundfiles/music_draw.mp3")

   
            
        self.victoryWordsLeft.pos = ((util.height-self.victoryWordsLeft.getMediaSize()[0])//2,util.width//10)
        self.victoryWordsRight.pos = ((util.height-self.victoryWordsRight.getMediaSize()[0])//2,util.width//10)


                                                    
        self.overallField.appendChild(self.victoryLeft)
        self.overallField.appendChild(self.victoryRight)


        def test():
            
            for i in xrange(0, self.overallField.getNumChildren()):
                child = self.overallField.getChild(i)
                if (child is not self.field):
                    avg.fadeOut(child, 1000)
            g_player.setTimeout(1000, lambda: util.startCloudFadeOut2(self.parentNode,self.showKeyboard ))         


        avg.LinearAnim(self.victoryWordsLeft,"opacity", 9000, 0, 1).start()
        avg.LinearAnim(self.victoryWordsRight,"opacity", 9000, 0, 1).start()
        avg.LinearAnim(self.victoryScoreLeft,"opacity", 9000, 0, 1).start()
        avg.LinearAnim(self.victoryScoreRight,"opacity", 9000, 0, 1, False, None, test).start()

  
        
            
        
        
    def isGameOver(self):
        return self._gameOver
            
           
  
if __name__ == '__main__':
    width = avg.Player.get().getScreenResolution().x
    height = avg.Player.get().getScreenResolution().y
    standAlone = True
    GeneaTD.start(resolution=(width,height))

