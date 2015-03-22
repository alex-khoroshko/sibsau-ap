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

def publish(n):
    pass

import os.path
import json

def detect_own_ip():
    #find out our own ip
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        s.connect(('8.8.8.8', 9))
        client = s.getsockname()[0]
    except socket.error:
        client = "Unknown IP"
    finally:
        del s
    print ('own ip address: ' + client)
    return client


def subscribe(cfg):
    try:
        cfg['name']
        cfg['path']
        cfg['start_port']
    except:
        print('wrong config')
        return
    try:
        cfg['ip_addr']
    except:
        cfg['ip_addr']=detect_own_ip()
    path = cfg['path']
    if not os.path.isdir(path):
        print('Config directory doesn\'t exist. Creating')
        try:
            os.makedirs(path)
        except:
            print('Failed to create dir. Critical: failed to publish data')
            return
    
    cfg_filename = path + cfg['name'] + '.json'
    if os.path.isfile(cfg_filename):
        print('Settings file already exist. Critical: failed to publish data')
        return
    file_obj =  open(cfg_filename, 'w')
    cfg_file = json.dumps(cfg)
    file_obj.write(cfg_file)   
