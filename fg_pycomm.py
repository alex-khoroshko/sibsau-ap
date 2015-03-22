#    Copyright 2015 Alexander Khoroshko

#    This file is part of fg-pycomm.
#    fg-pycomm is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#    fg-pycomm is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#    You should have received a copy of the GNU General Public License
#    along with fg-pycomm.  If not, see <http://www.gnu.org/licenses/>.

def parse_settings():

    return

if __name__ == '__main__':
    pass

import json, sys
from optparse import OptionParser
parser = OptionParser()
parser.add_option("-s", "--settings", dest="settings_path", help="set path to settings files folder")
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
from pprint import pprint
try:
    with open(settings_file_path) as settings_file:    
        data = json.load(settings_file)
except:
    print('Failed to parse global config file. Exiting')
    sys.exit(0)
            
    
    
pprint(data)

#"export" means from flightgear to our application
fg_export_cfg_path = options.settings_path + data['config_files']['fg_export_cfg']
from xml.dom import minidom
doc = minidom.parse(fg_export_cfg_path)
# doc.getElementsByTagName returns NodeList
#value_field = doc.getElementsByTagName("chunk")
#for chunk in value_field:
#    print(chunk.getElementsByTagName(''))

import ipc
cfg = {
       'name': 'nav',
       'path': '/tmp/sibsau-ap/',
       'start_port': 30000
       }
ipc.subscribe(cfg)

import socket
UDP_IP = "127.0.0.1"
UDP_PORT = 12345
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

from datetime import datetime
time_prev = datetime.now()
q = {}
while True:
    packet, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    data = packet.split('\t')
    for elem in data:
        name, val = elem.split('=')
        q[name]=float(val)
    #print(chr(27) + "[2J")
    #print ("received message:"), data
    #print ("q:"), q
    
    time = datetime.now()
    time_diff = time - time_prev
    time_prev = time
    print ("time_difference:\t" + str(time_diff.microseconds) + 'us')
    
