import os

from war import Main
from libavg.AVGAppUtil import getMediaDir, createImagePreviewNode

__all__ = [ 'apps',]

def createPreviewNode(maxSize):
    
    filename = os.path.join(getMediaDir(__file__, "resources"), 'preview.png')
    return createImagePreviewNode(maxSize, absHref = filename)

apps = ({'class': Main,
            'createPreviewNode': createPreviewNode},
            )

