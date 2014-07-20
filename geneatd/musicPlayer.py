# geneaTD - A multi-touch tower defense game.
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


class MusicPlayer(object):
    """
    This class represents a music player.
    """


    def __init__(self, parentNode, enabled):
        """
        Creates a new music player object.
        """
        self.parent = parentNode
        self.enabled = enabled
        self.musicPlayer = avg.SoundNode(parent=parentNode)
        self.musicPlayer.volume = 1
        self.volume = 1

    def playTune(self, name, loopEnabled=False, path=getMediaDir(__file__, "resources")):
        """
        Plays a new tune.
        name: The reference to the new tune.
        path: The path.
        """
        if self.enabled:
            self.musicPlayer.stop()
            self.musicPlayer.href = os.path.join(path, name)

            try:
                if loopEnabled:
                    self.musicPlayer.setEOFCallback(lambda: self._setLoop(name, path))

                self.musicPlayer.play()
            except RuntimeError:
                pass

    def stop(self):
        """
        Stops the playback.
        """
        if self.enabled:
            self.musicPlayer.stop()
            self.musicPlayer.subscribe(SoundNode.END_OF_FILE, self.noFunc)

    def noFunc(self):
        pass

    def _setLoop(self, name, path):
        """
        After playback has come to an end start again.
        name: The reference to the new tune.
        path: The path.
        """
        self.playTune(name, path)

    def mute(self):
        """
        A method that mute or unmute the sound, depending whether the sound is
        """
        if self.musicPlayer.volume == 0:
            self.musicPlayer.volume = 1
            self.volume = 1
        else:
            self.musicPlayer.volume = 0
            self.volume = 0
