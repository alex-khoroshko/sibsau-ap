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

from multiprocessing import Process
import ipc, math

def callback(data):
    print(data)

def ap_core_proc(cfg):
    fg_ipc = ipc.udp_ipc(cfg);
    fg_ipc.subscribe('fg2ap')
    while True:
        data = fg_ipc.receive(['roll', 'pitch', 'yaw'])
        print (data)
        for key in data:
            data[key] = math.degrees(float(data[key]))
        print (data)
        
    
def start(cfg):
    p = Process(target=ap_core_proc, args=(cfg,))
    p.start()
    