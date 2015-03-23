#    Copyright 2015 Alexander Khoroshko

#    This file is part of sibsau-ap.
#    sibsau-ap is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#    sibsau-ap is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#    You should have received a copy of the GNU General Public License
#    along with sibsau-ap.  If not, see <http://www.gnu.org/licenses/>.

global_cfg = {}

import json, sys, os
from optparse import OptionParser
parser = OptionParser()
parser.add_option("-c", "--config", dest="settings_path", help="set path to config files folder (mandatory).")
(options, args) = parser.parse_args()

#test for path to global settings file
if not options.settings_path:
    print('No global config path given. Exiting.')
    sys.exit(0)

print ('Trying to load global config from path: "' + options.settings_path + '"')

#parsing config file  
import os.path
if not os.path.isdir(options.settings_path):
    print('Specified config folder doesn\'t exist. Exiting.')
    sys.exit(0)
print('Specified config folder exists')

settings_file_path = options.settings_path + 'sibsau_ap_cfg.json'
print('Trying to open global config file: "' + settings_file_path + '"' )
if not os.path.isfile(settings_file_path):
    print('Global config file doesn\'t exist. Exiting')
    sys.exit(0)
print('Global config file exists' )    
try:
    with open(settings_file_path) as settings_file:    
        global_cfg = json.load(settings_file)
except:
    print('Failed to parse global config file with error:\n\t' + str(sys.exc_info()) + '\n\tExiting.')
    sys.exit(0)
print('Global config file parsed successfully')

#Check if tmp files folder exists and create if not
try:
    tmp_files_folder = global_cfg['tmp_files_folder']
except:
    print('Critical error: global config file doesn\'t have mandatory field "tmp_files_folder". Exiting.')
    sys.exit(0)
if os.path.isdir(tmp_files_folder):
    print('Temporary files folder exists.')
else:
    print('Temporary files folder doesn\'t exist. Trying to create.')
    try:
        os.makedirs(tmp_files_folder)
        print('Temporary files folder create success.')
    except:
        print('Critical: failed to create dir. Exiting.')
        sys.exit(0)  
        
#Clean-up tmp folder
print('Cleaning-up the tmp files folder:')
for the_file in os.listdir(tmp_files_folder):
    file_path = os.path.join(tmp_files_folder, the_file)
    print('\tremoving file: "' + file_path + '"')
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
    except:
        print ('Error occured while removing files:\n\t' + str(sys.exc_info()) )
print ('\tdone.')                  

import ipc
pub_cfg = {
           'name': "testPub"
           }
try:
    ipc.publish(pub_cfg)
except:
    pass