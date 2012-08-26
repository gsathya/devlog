import sys
import utils
import optparse 
import shutil
from publish import *

def parse_args(options):
    parser = optparse.OptionParser()
    parser.add_option('-s','--create-skeleton', action="store_true", default=False)
    parser.add_option('-p','--publish', action="store_true", default=False)
    options, rem = parser.parse_args(options)
    return options

def create_skeleton():
    newpath = 'site/posts'
    if not os.path.exists(newpath): os.makedirs(newpath)
    shutil.copytree('assets', 'site/assets')

if __name__ == '__main__':
    options = parse_args(sys.argv[1:])

    if options.create_skeleton:
        create_skeleton()
    if options.publish:
        publish()
