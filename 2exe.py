try:
    from distutils.core import setup
    import py2exe, pygame
    from modulefinder import Module
    import glob, fnmatch
    import sys, os, shutil
    import operator
    import re
except ImportError, message:
    raise SystemExit,  "Unable to load module. %s" % message

pygame.font.init()


def find_pygame_dlls():
    dlls = []
    pygamedir = os.path.split(pygame.base.__file__)[0]
    for r,d,f in os.walk(pygamedir):
        for files in f:
            if files.lower().endswith(".dll"):
                dlls.append(os.path.join(r, files))
    #l = os.path.join(pygamedir, "libogg-0.dll")
    #if not l in dlls:
    #    dlls.append(l)
    return dlls

PYGAME_DLLS = find_pygame_dlls()

#hack which fixes the pygame mixer and pygame font
origIsSystemDLL = py2exe.build_exe.isSystemDLL # save the orginal before we edit it
def isSystemDLL(pathname):
    # checks if the freetype and ogg dll files are being included

    if (pathname in PYGAME_DLLS) or re.match(".*python\d\d\.dll$", pathname):#("libfreetype-6.dll", "libogg-0.dll", "msvcp71.dll", "dwmapi.dll", "SDL_ttf.dll"):#, "SDL_ttf.dll"):        
        return 0
    elif pathname.lower().startswith("c:\\windows"):
        return 1
    return origIsSystemDLL(pathname) # return the orginal function
py2exe.build_exe.isSystemDLL = isSystemDLL # override the default function with this one


class pygame2exe(py2exe.build_exe.py2exe): #This hack make sure that pygame default font is copied: no need to modify code for specifying default font
    def copy_extensions(self, extensions):
        #Get pygame default font
        pygamedir = os.path.split(pygame.base.__file__)[0]
        pygame_default_font = os.path.join(pygamedir, pygame.font.get_default_font())
 
        #Add font to list of extension to be copied
        extensions.append(Module("pygame.font", pygame_default_font))
        
        # Copy all pygame dll's
        for dll in PYGAME_DLLS:
            try:
                m = Module("pygame", dll)
                m.__pydfile__ = ".".join(dll.split(".")[:-1]) + ".pyd"
                extensions.append(m)
            except Exception:
                print "Warning, couldn't load", dll
            
        py2exe.build_exe.py2exe.copy_extensions(self, extensions)
 
class BuildExe:
    def __init__(self):
        #Name of starting .py
        self.script = "main.py"
 
        #Name of program
        self.project_name = "Achtung"
 
        #Project url
        self.project_url = "None"
 
        #Version of program
        self.project_version = "0.1"
 
        #License of the program
        self.license = "Open"
 
        #Auhor of program
        self.author_name = "Sim1234"
        self.author_email = "None"
        self.copyright = "None"
 
        #Description
        self.project_description = "Simple 2D game"
 
        #Icon file (None will use pygame default icon)
        self.icon_file = None
         
        #Extra files/dirs copied to game
        self.extra_datas = ['data']
 
        #Extra/excludes python modules
        self.extra_modules = []
        self.exclude_modules = []
        
        #DLL Excludes
        self.exclude_dll = []
        #python scripts (strings) to be included, seperated by a comma
        self.extra_scripts = []
 
        #Zip file name (None will bundle files in exe instead of zip file)
        self.zipfile_name = "gamedata.dll"#"sdl.zip"
 
        #Dist directory
        #self.dist_dir = 'dist'
 
    ## Code from DistUtils tutorial at http://wiki.python.org/moin/Distutils/Tutorial
    ## Originally borrowed from wxPython's setup and config files
    def opj(self, *args):
        path = os.path.join(*args)
        return os.path.normpath(path)
 
    def find_data_files(self, srcdir, *wildcards, **kw):
        # get a list of all files under the srcdir matching wildcards,
        # returned in a format to be used for install_data
        def walk_helper(arg, dirname, files):
            if '.svn' in dirname:
                return
            names = []
            lst, wildcards = arg
            for wc in wildcards:
                wc_name = self.opj(dirname, wc)
                for f in files:
                    filename = self.opj(dirname, f)
 
                    if fnmatch.fnmatch(filename, wc_name) and not os.path.isdir(filename):
                        names.append(filename)
            if names:
                lst.append( (dirname, names ) )
 
        file_list = []
        recursive = kw.get('recursive', True)
        if recursive:
            os.path.walk(srcdir, walk_helper, (file_list, wildcards))
        else:
            walk_helper((file_list, wildcards),
                        srcdir,
                        [os.path.basename(f) for f in glob.glob(self.opj(srcdir, '*'))])
        return file_list
 
    def run(self):
        if os.path.isdir("dist"): #Erase previous destination dir
            print "Removing", os.path.abspath("dist")
            shutil.rmtree("dist")
        
        #Use the default pygame icon, if none given
        if self.icon_file == None:
            path = os.path.split(pygame.__file__)[0]
            self.icon_file = os.path.join(path, 'pygame.ico')
 
        #List all data files to add
        extra_datas = []
        for data in self.extra_datas:
            if os.path.isdir(data):
                extra_datas.extend(self.find_data_files(data, '*'))
            else:
                extra_datas.append(('.', [data]))
        extra_datas.append(('.', glob.glob('*.dll')))
        extra_datas.append(('.', PYGAME_DLLS))
        self.extra_modules += [ "pygame.font", "pygame", "pygame._view", "pygame.mixer"]
        
        setup(
            cmdclass = {'py2exe': pygame2exe},
            version = self.project_version,
            description = self.project_description,
            name = self.project_name,
            url = self.project_url,
            author = self.author_name,
            author_email = self.author_email,
            license = self.license,
 
            # targets to build
            windows = [{
                'script': self.script,
                'icon_resources': [(0, self.icon_file)],
                'copyright': self.copyright
            }],
            options = {'py2exe': {'optimize': 2, 'bundle_files': 3, 'compressed': True, \
                                  'excludes': self.exclude_modules, 'packages': self.extra_modules, \
                                  'dll_excludes': self.exclude_dll,
                                  'includes': self.extra_scripts} },
            zipfile = self.zipfile_name,
            data_files = extra_datas,
            #dist_dir = self.dist_dir
            )
        
        if os.path.isdir('build'): #Clean up build dir
            print "Removing", os.path.abspath("build")
            shutil.rmtree('build')
 
if __name__ == '__main__':
    if operator.lt(len(sys.argv), 2):
        sys.argv.append('py2exe')
    BuildExe().run() #Run generation
    print "Done!"
    #raw_input("Press any key to continue") #Pause to let user see that things ends 
