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
from os.path import expanduser

# CATEGORY = 'f8f45febbf5881de8e373f48c8bf81dc'
HOME_DIR = expanduser('~')
LAUNCHERS_DATA_PATH = HOME_DIR + '/.kodi/userdata/addon_data/plugin.program.advanced.launcher/launchers.xml'
GAME_DATA_PATH = HOME_DIR + '/game.data'
LAUNCHERS_PATH = GAME_DATA_PATH + '/launchers'
THUMBNAILS_PATH = GAME_DATA_PATH + '/thumbnails'

thumbnails_ext_list = ['.png', '.jpeg']

cur_launcher_path = ''

def get_launch_dir(game_name, value):
    str = ''
    path = LAUNCHERS_PATH + '/' + value
    if os.path.exists(path):
        str = path

    else:
        print "couldn't find {0}".format(path)
    global cur_launcher_path
    cur_launcher_path = str
    return str



def get_app_path(game_name, value):
    str = ''
    global cur_launcher_path
    path = cur_launcher_path + '/' + value
    if os.path.isfile(path):
        str = path
    else:
        print "couldn't find {0}".format(path)
    return str

def get_thumb_path(game_name, value):
    str = ''
    path = THUMBNAILS_PATH + '/' + game_name
    for ext in thumbnails_ext_list:
        if os.path.isfile(path + ext):
            str = path + ext
            break
    if len(str) == 0:
        print "unable to find thumbnail for {0}".format(game_name)
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
    print "copying from {0} to {1}".format(src, dst)
    try:
        if os.path.isfile(src):
            shutil.copyfile(src, dst)
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
        retVal = 1
    return retVal

def add_launcher(rowInFile, root, attributes, category_id):
    launcher = SubElement(root, 'launcher')
    id = SubElement(launcher, 'id')
    u = uuid.uuid1()
    id.text = str(u.hex)
    finished = SubElement(launcher, 'finished')
    finished.text = 'false'
    minimize = SubElement(launcher, 'minimize')
    minimize.text = 'false'
    cat = SubElement(launcher, 'category')
    cat.text = category_id
    set_attributes(rowInFile, launcher, attributes)

def set_attributes(rowInFile,root, attributes):
    game_name = rowInFile[0]
    root.append(Comment('Generated element for {0}'.format(game_name)))
    cnt = 0
    for attr in attributes:
        subEl = SubElement(root, attributes[cnt])
        if attributes[cnt] in auto_gen_attr:
            subEl.text = auto_gen_attr[attributes[cnt]](game_name, rowInFile[cnt])
        else:
            subEl.text = rowInFile[cnt]
        cnt += 1

def find_child_val(root, tag):
    for child in root:
        if child.tag == tag:
            return child.text
        else:
            return find_child_val(child, tag)

def run_import(xml_path, csv_path):
    # category = CATEGORY
    #create backup
    backup_path = xml_path + '.bckp'
    if backup(xml_path, backup_path) != 0:
        return
    #start import
    tree = ET.parse(xml_path)

    root = tree.getroot()

    for child in root:
        if child.tag == 'categories':
            category_id = 0
            category_id = find_child_val(child, 'id')
            if category_id == 0:
                print "unable to find games category"
                return
        if child.tag == 'launchers':
            root.remove(child)
            root = SubElement(root, 'launchers')
    try:
        cnt = 0
        with open(csv_path, 'rb') as f:
            reader = csv.reader(f)
            headers = next(reader, None)
            if headers:
                for row in reader:
                    add_launcher(row, root, headers, category_id)
                    #set_attributes(row, root)
                    cnt += 1
                print "{0} rows were imported".format(cnt)
                tree.write(xml_path)
            else:
                print "cannot import data. header row is missing"
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
        backup(backup_path, xml_path)
    except:
        print "Unexpected error:", sys.exc_info()[0]
        backup(backup_path, xml_path)
            #print(prettify(orig_root))
    else:
        #cleanup
        f.close

def main(argv):
   inputfile = ''
   outputfile = ''
   if len(argv) < 2:
       #get home directory
       # home_dir = expanduser('~')
       inputfile = GAME_DATA_PATH + '/game_info.csv'
       outputfile = LAUNCHERS_DATA_PATH
   else:
        inputfile = argv[1]
        outputfile = argv[0]
   run_import(outputfile, inputfile)
#'/home/a_krutau/launchers.xml'
#'/home/a_krutau/game_info.csv'
if ( __name__ == "__main__" ):
    main(sys.argv[1:])
