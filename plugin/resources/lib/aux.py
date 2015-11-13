__author__ = 'akrutau'

import logging
import os.path
from os.path import expanduser

HOME_DIR = expanduser('~')
LAUNCHERS_DATA_PATH = os.path.join(HOME_DIR, '.kodi/userdata/addon_data/plugin.program.advanced.launcher/launchers.xml')
GAME_DATA_PATH = os.path.join(HOME_DIR, 'game.data')
LAUNCHERS_PATH = os.path.join(GAME_DATA_PATH, 'launchers')
THUMBNAILS_PATH = os.path.join(GAME_DATA_PATH, 'thumbnails')
FORMAT = '[%(asctime)-15s][%(levelname)s][%(funcName)s] - %(message)s'


def getLogger(name):
    log_path = os.path.join(GAME_DATA_PATH, 'logs')
    if not os.path.exists(log_path):
        os.mkdir(log_path)
    logging.basicConfig(level=logging.DEBUG, filename=os.path.join(log_path, name), filemode = 'a', \
                        format=FORMAT)
    return logging.getLogger(name)