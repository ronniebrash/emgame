from _elementtree import SubElement

__author__ = 'a_krutau'

import csv
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
import datetime
from xml.etree import ElementTree
from xml.dom import minidom
import uuid
import sys
import shutil
import os.path
from aux import getLogger
from aux import HOME_DIR, LAUNCHERS_DATA_PATH, THUMBNAILS_PATH, LAUNCHERS_PATH, GAME_DATA_PATH, DEBUG

from os.path import expanduser

log = getLogger("launcher.log")

CATEGORY = 'f8f45febbf5881de8e373f48c8bf81dc'


thumbnails_ext_list = ['.png', '.jpeg', '.jpg']

cur_launcher_path = ''

def get_launch_dir(game_name, value):
    str = ''
    path = os.path.join(LAUNCHERS_PATH, value)
    if os.path.exists(path) or DEBUG:
        str = path
    else:
        log.error("couldn't find {0}".format(path))
    global cur_launcher_path
    cur_launcher_path = str
    return str

def get_app_path(game_name, value):
    str = ''
    global cur_launcher_path
    path = os.path.join(cur_launcher_path, value)
    if os.path.isfile(path) or DEBUG:
        str = path
    else:
        log.error("couldn't find {0}".format(path))
    return str

def get_thumb_path(game_name, value):
    str = ''
    path = os.path.join(THUMBNAILS_PATH, game_name)
    for ext in thumbnails_ext_list:
        if os.path.isfile(path + ext):
            str = path + ext
            break
    if len(str) == 0:
        log.error("unable to find thumbnail for {0}".format(game_name))
    return str


auto_gen_attr = {
    'launcherdir': get_launch_dir,
    'application': get_app_path,
    'thumb': get_thumb_path,
    }





def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def backup(src, dst):
    retVal = 0
    log.info("copying from {0} to {1}".format(src, dst))
    try:
        if os.path.isfile(src):
            shutil.copyfile(src, dst)
    except IOError as e:
        log.error("I/O error({0}): {1}".format(e.errno, e.strerror))
        retVal = 1
    return retVal

def add_launcher(rowInFile, attributes, fin):
        fin.write('<launcher>\n')
        u = uuid.uuid1()
        fin.write('<id>{0}</id>\n'.format(str(u.hex)))
        fin.write('<finished>false</finished>\n')
        fin.write('<minimize>false</minimize>\n')
        fin.write('<category>{0}</category>\n'.format(CATEGORY))
        set_attributes(rowInFile, fin, attributes)
        fin.write('</launcher>\n')
    # 	 <launcher>
		# 		 <id>c685f57cdd6311e5967e4fe1a7ea7b1c</id>
		# 		 <finished>false</finished>
		# 		 <minimize>false</minimize>
		# 		 <category>f8f45febbf5881de8e373f48c8bf81dc</category>
		# 		 <!--Generated element for supermeatboy-->
		# 		 <name>SuperMeatBoy</name>
		# 		 <launcherdir>/home/akrutau/game.data/launchers/supermeatboy</launcherdir>
		# 		 <application>/home/akrutau/game.data/launchers/supermeatboy/SuperMeatBoy</application>
		# 		 <args />
		# 		 <rompath />
		# 		 <tumbpath />
		# 		 <fanartpath />
		# 		 <trailerpath />
		# 		 <custompath />
		# 		 <romext />
		# 		 <platform>Linux</platform>
		# 		 <thumb />
		# 		 <fanart />
		# 		 <genre>Platform</genre>
		# 		 <release />
		# 		 <publisher>Team Meat</publisher>
		# 		 <launcherplot>Super Meat Boy is a platform game in which players control a small, dark red, cube-shaped character named Meat Boy, who must save his cube-shaped, heavily bandaged girlfriend Bandage Girl from the evil scientist Dr. Fetus. The game is divided into chapters, which together contain over 300 levels.[2][3] Players attempt to reach the end of each level, represented by Bandage Girl, while avoiding crumbling blocks, saw blades, and various other fatal obstacles. The player can jump and run on platforms, and can jump off or slide down walls. The core gameplay requires fine control and split-second timing, and has been compared to, regarding both gameplay and level of difficulty, traditional platform games such as Super Mario Bros. and Ghosts'n Goblins</launcherplot>
		# 		 <lnk />
		# 		 <roms />
		# 	</launcher>



def set_attributes(rowInFile,fin, attributes):
    game_name = rowInFile[1]
    fin.write('<!--Generated element for {0}-->'.format(game_name))
    cnt = 0
    attr_text = ''
    for attr in attributes:
        attr_text = ''
        if attr in auto_gen_attr:
            attr_text = auto_gen_attr[attr](game_name, rowInFile[cnt])
        else:
            attr_text = rowInFile[cnt]
        fin.write('<{0}>{1}</{0}>\n'.format(attr, attr_text))
        cnt += 1



def find_child_val(root, tag):
    for child in root:
        if child.tag == tag:
            return child.text
        else:
            return find_child_val(child, tag)

def add_launchers(fin, csv_path):
        cnt = 0
        with open(csv_path, 'rb') as f:
            reader = csv.reader(f)
            headers = next(reader, None)
            if headers:
                for row in reader:
                    add_launcher(row, headers, fin)
                    #set_attributes(row, root)
                    cnt += 1
                log.info("{0} rows were imported".format(cnt))
                # tree.write(xml_path)
            else:
                log.info("cannot import data. header row is missing")


def run_import(xml_path, csv_path):
    #create backup
    backup_path = xml_path + '.bckp'
    if backup(xml_path, backup_path) != 0:
        return
    #start import
    os.remove(xml_path)
    try:
        with open(xml_path, 'a') as fin:
            fin.write('<advanced_launcher version="1.0">\n')
            fin.write('<categories>\n')
            fin.write('<category>\n')
            fin.write('<id>{0}</id>\n'.format(CATEGORY))
            fin.write('<name>Games</name>\n')
            fin.write('<thumb />\n')
            fin.write('<fanart />\n')
            fin.write('<genre />\n')
            fin.write('<description />\n')
            fin.write('<finished>false</finished>\n')
            fin.write('</category>\n')
            fin.write('</categories>\n')
            fin.write('<launchers>\n')
            add_launchers(fin, csv_path)
            fin.write('</launchers>\n')
            fin.write('</advanced_launcher>')
            fin.close()
    except IOError as e:
        log.error("I/O error({0}): {1}".format(e.errno, e.strerror))
        backup(backup_path, xml_path)
    except:
        log.error("Unexpected error:", sys.exc_info()[0])
        backup(backup_path, xml_path)
            #print(prettify(orig_root))
    else:
        #cleanup
        fin.close


    # tree = ET.parse(xml_path)
    # root = tree.getroot()
    # for child in root:
    #     if child.tag == 'categories':
    #         category_id = find_child_val(child, 'id')
    #         if category_id == 0:
    #             log.error("unable to find games category")
    #             return
    #     if child.tag == 'launchers':
    #         root.remove(child)
    #         root = SubElement(root, 'launchers')


def main(argv):
   inputfile = ''
   outputfile = ''
   if len(argv) < 2:
       #get home directory
       # home_dir = expanduser('~')
       # inputfile = os.path.join(home_dir, 'emgame/copy_of_working_csv.csv')
       # outputfile = os.path.join(home_dir, 'emgame/launchers.xml')
       inputfile = os.path.join(GAME_DATA_PATH, 'game_info.csv')
       outputfile = LAUNCHERS_DATA_PATH
   else:
        inputfile = argv[1]
        outputfile = argv[0]
   run_import(outputfile, inputfile)
#'/home/a_krutau/launchers.xml'
#'/home/a_krutau/game_info.csv'
if ( __name__ == "__main__" ):
    main(sys.argv[1:])
