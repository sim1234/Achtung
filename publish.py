# coding: utf-8
import sys, os, shutil
sys.path.append(os.path.abspath("../Pipe"))
sys.path.append(os.path.abspath("../Updater"))
sys.path.append(os.path.abspath("../Exec_server"))

from update import Updater
from client import EClient, get_t

def ip(x):
    if x == "":
        return EClient("192.168.0.186", 666) 
    r = x.split(":")
    for z in r[0].split("."):
        if not (0 <= int(z) <= 255):
            raise Exception
    return EClient(r[0], int(r[1]))

def main():
    c = get_t("Polacz z 192.168.0.168:666 lub z: ", ip)
    f = raw_input("Folder z programem lub '': ")
    m = raw_input("Plik do wykonania lub '2exe.py': ") or "2exe.py"
    print "\nFolder:", os.path.abspath(f)
    print "Plik:", m
    r = raw_input("Potwierdzasz? (t/n/q)").lower()
    if r.startswith("t"):
        c.send_code(f, m)
        print "Wyslano! Prosze czekac, wykonywanie moze potrwac"
        raw_input("Kontynuuj...")
        print "Moving", os.path.abspath("excecuted/dist")
        shutil.move("executed/dist", "publish")
        print "Deleting", os.path.abspath("excecuted")
        shutil.rmtree("executed", 1)
        print "cd publish"
        os.chdir("publish")
        print "Pchnij:"
        Updater("", raw_input("Haslo: ")).push(raw_input("Wersia: "))
        print "cd .."
        os.chdir("..")
        if raw_input("Delete 'publish'?"):
            print "Deleting", os.path.abspath("publish")
            shutil.rmtree("publish", 1)
        raw_input("Zakoncz...")
        c.stop()
    elif r.startswith("q"):
        pass
    else:
        main()
    



if __name__ == "__main__":
    main()