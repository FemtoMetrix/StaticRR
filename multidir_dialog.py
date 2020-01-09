import sys
from PyQt5.QtWidgets import (QFileDialog, QAbstractItemView, QListView,
                             QTreeView, QApplication, QDialog)
import os
import re
import json

def config_handler():
    if os.path.isfile('config.json'):
        with open('config.json') as json_file:
            config_path = json.load(json_file)
            return(config_path["Default Folder"])


class getExistingDirectories(QFileDialog):
    def __init__(self, *args):
        super(getExistingDirectories, self).__init__(*args)
        self.setDirectory(config_handler())
        self.setOption(self.DontUseNativeDialog, True)
        self.setFileMode(self.Directory)
        self.setOption(self.ShowDirsOnly, True)
        self.findChildren(QListView)[0].setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.findChildren(QTreeView)[0].setSelectionMode(QAbstractItemView.ExtendedSelection)

def find_LP_SL(s): #function written to find the slot and port number and return them in int format
    ind_lp = s.find("_LP_")#load port index
    ind_lp_n  = ind_lp + 4  #index for load port number
    lp = s[ind_lp_n]
    load_port_num = int(lp) # convert a sring into
    ind_sl = s.find("_SL_") #find the index for the underscore that comes before the word SL
    ind_sl_n = ind_sl + 4; #Find the index for the slot number
    #make a copy of the substring containing the slot numbers. Because slot numbers are written in the following convention "01" - "25". The program needs to
    #create a substring
    slot_num = s[ind_sl_n:ind_sl_n + 2]
    slot_num = int(slot_num)
    print(slot_num)
    return(slot_num)

def multi_dir_dialog():
    qapp = QApplication(sys.argv)
    # Prompt the multiple directory selection UI
    dlg = getExistingDirectories()
    if dlg.exec() == QDialog.Accepted:
        dir = dlg.selectedFiles()

    file_paths = []
    f_info_list = []
    #create a dictionary where the key is the slot number and value is a list of files from that slot number
    for d in dir:
        files = os.listdir(d)
        print(files)
        #file_ninfo = 0 # list that contains the number list for
        str_list = []
        for f in files:
           str_list = []
           #if f.endswith("ref.tsv") or f.endswith("reference.tsv"):
           if f.endswith("final.tsv"): # Preprocessed data from FemtoViewer ends with final.tsv
                slot_num = find_LP_SL(f)
                str_list.append(d)
                str_list.append(f)
                file_paths.append('/'.join(str_list))
                f_info_list.append(slot_num)

    return [file_paths, f_info_list]


