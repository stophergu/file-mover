import time
import os
import shutil
from datetime import datetime

DATE_FORMAT = '%m/%d/%Y'
    
#possible addition of refining search by time
TIME_FORMAT ='%a %b %d %H:%M:%S %Y'
   

def find_files(path, ext):
    '''
    return a list of all files that end with extension(s) from root directory
    and all subdirectories of given root.

    path is valid path of existing directory
    ext is string of single extensoin, or multiple extensions seperated by comma
    '''
    filez = []
    extensions = ext.split(',')
    if not os.path.isdir(path):
        raise AttributeError('Invalid Source Path Provided')
        
     
    path += '\\'
    walk = os.walk(path)
    for block in walk:
        root, dir, files = block
        for fn in files:
            for ext in extensions:
                if fn.endswith(ext.strip()):
                    fn = os.path.join(root, fn)
                    if os.path.isfile(fn):
                        filez.append(fn)
    return filez
def parse(files, min_date, max_date, created = False, modified = False):
    '''
    Return a list of files parsed according to date file was created
    and/or modified
    '''
    PARSED = []
    date_min = datetime.strptime(min_date, DATE_FORMAT).date()
    date_max = datetime.strptime(max_date, DATE_FORMAT).date() 

    
    
    for fn in files:
        ###if/when additon of search by time function added###
        #ctime = time.ctime(os.path.getctime(fn))
        #ctime = datetime.strptime(ctime, TIME_FORMAT).date()
        #mtime = time.ctime(os.path.getmtime(fn))
        #modtime = datetime.strptime(mtime, TIME_FORMAT).date()

        if created:
            if date_min <=  date_max:
                PARSED.append(fn)
        if modified:
            if date_min <=  date_max:
                PARSED.append(fn)
    return PARSED

def move(files, target, copy = False, cut = False):
    '''
    Transfer parsed files to target location, create target directory if 
    directory does not exist.
    '''
    if not os.path.isdir(target):
        os.mkdir(target)

    for fn in files:
        if copy:
            try:
                shutil.copy(fn, target)
            except:
                pass    
        elif cut:
            try:
                shutil.move(fn, target)
            except:
                raise AttributeError('%s was not moved' % (fn))
