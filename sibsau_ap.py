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

import json, sys
from optparse import OptionParser
parser = OptionParser()
parser.add_option("-s", "--settings", dest="settings_path", help="set path to settings files folder (mandatory)")
(options, args) = parser.parse_args()

#test for path to global settings file
try:
    print (options.settings_path)
except:
    print('No settings path given. Exiting')
    sys.exit(0)

#parsing config file  
import os.path
if not os.path.isdir(options.settings_path):
    print('Specified settings folder doesn\'t exist. Exiting')
    sys.exit(0)
settings_file_path = options.settings_path + 'settings.json'

try:
    with open(settings_file_path) as settings_file:    
        data = json.load(settings_file)
except:
    print('Failed to parse global config file. Exiting')
    sys.exit(0)
            
from pprint import pprint  