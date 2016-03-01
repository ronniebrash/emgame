__author__ = 'akrutau'

import logging
import os.path
from os.path import expanduser
import xbmc, xbmcgui
from xbmcaddon import Addon

HOME_DIR = expanduser('~')
LAUNCHERS_DATA_PATH = os.path.join(HOME_DIR, '.kodi/userdata/addon_data/plugin.program.advanced.launcher/launchers.xml')
GAME_DATA_PATH = os.path.join(HOME_DIR, 'game.data')
LAUNCHERS_PATH = os.path.join(GAME_DATA_PATH, 'launchers')
THUMBNAILS_PATH = os.path.join(GAME_DATA_PATH, 'thumbnails')
FORMAT = '[%(asctime)-15s][%(levelname)s][%(funcName)s] - %(message)s'

LANGUAGES = ['English', 'French']
DEBUG = False

def getLogger(name):
    log_path = os.path.join(GAME_DATA_PATH, 'logs')
    if not os.path.exists(log_path):
        os.mkdir(log_path)
    logging.basicConfig(level=logging.DEBUG, filename=os.path.join(log_path, name), filemode = 'a', \
                        format=FORMAT)
    return logging.getLogger(name)



#get actioncodes from https://github.com/xbmc/xbmc/blob/master/xbmc/guilib/Key.h
ACTION_PREVIOUS_MENU = 10

# class MyClass(xbmcgui.Window):
#   def __init__(self):
#     self.strActionInfo = xbmcgui.ControlLabel(250, 80, 200, 200, '', 'font14', '0xFFBBBBFF')
#     self.addControl(self.strActionInfo)
#     self.strActionInfo.setLabel('Push BACK to quit')
#     self.list = xbmcgui.ControlList(200, 150, 300, 400)
#     self.addControl(self.list)
#     self.list.addItem('English')
#     self.list.addItem('French')
#     self.setFocus(self.list)
#
#   def onAction(self, action):
#     if action == ACTION_PREVIOUS_MENU:
#       self.close()
#
#   def onControl(self, control):
#     if control == self.list:
#       item = self.list.getSelectedItem()
#       self.message('You selected : ' + item.getLabel())
#       self.close()
#
#   def message(self, message):
#     dialog = xbmcgui.Dialog()
#     dialog.ok(" My message title", message)
def main(argv):
	__settings__ = Addon(id="plugin.program.advanced.launcher")
	__settings__.openSettings()
	xbmc.executebuiltin("XBMC.ReloadSkin()")
	
if ( __name__ == "__main__" ):
    main(sys.argv[1:])
