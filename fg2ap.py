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

import socket
from multiprocessing import Process
import ipc
import os
import math


def fg_proc(cfg):
    fg_ipc = ipc.udp_ipc(cfg);
    fg_ipc.publish('fg2ap')
    port = cfg['ipc_udp_starting_port']
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        try:
            sock.bind(('127.0.0.1', port))
            break
        except:
            port+=1
    print('fg incoming port is ' + str(port))
    fg_string = 'fgfs --generic=socket,out,10,localhost,'+str(port)+',udp,fg2ap &'
    os.system(fg_string)
    q = {}
    while True:
        packet, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        data = packet.split('\t')
        for elem in data:
            name, val = elem.split('=')
            q[name]=float(val)
        ground_speed = math.sqrt(q['speed-east']*q['speed-east'] + q['speed-north']*q['speed-north'])
        state = {
                 'altitude':        q['alt'],
                 'ground-elev':     q['ground-elev'],
                 'lat':             q['lat'],
                 'lon':             q['lon'],
                 'roll':            q['roll'],
                 'pitch':           q['pitch'],
                 'yaw':             q['yaw'],
                 'rate-roll':       q['rate-roll'],
                 'rate-pitch':      q['rate-pitch'],
                 'rate-yaw':        q['rate-yaw'],
                 'vert-speed':      q['vert-speed'],
                 'ground_speed':    ground_speed,
                 'airspeer':        q['airspeed'],  
                 'x-accel':         q['x-accel'],
                 'y-accel':         q['y-accel'],
                 'z-accel':         q['z-accel'],
                 }
        fg_ipc.post(state)

def start(cfg):
    p = Process(target=fg_proc, args=(cfg,))
    p.start()
    
 
            