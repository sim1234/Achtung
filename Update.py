# coding:utf-8

import os, sys, shutil
sys.path.append(os.path.abspath("../Pipe"))
sys.path.append(os.path.abspath("../Updater"))
from update import Updater


 
if __name__ == "__main__":
    u = Updater()
    u.update(u.get_l_version() == "0" or "force" in sys.argv)
    #raw_input("Enter by zakończyć...")
    time.sleep(3)
    