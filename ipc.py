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

import socket
import json
import sys


def detect_own_ip():
    #find out our own ip
    
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

class udp_ipc:
    def __init__(self, cfg):
        self.tmp_folder = cfg['tmp_files_folder']
        self.start_port = cfg['ipc_udp_starting_port']
     
    def publish(self, name):
        self.pub_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.pub_sock.setblocking(0)
        #own_ip = detect_own_ip()
        pub_port = self.start_port
        while True:
            try:
                self.pub_sock.bind(('127.0.0.1', pub_port))
                break
            except:
                pub_port+=1
        print('Module ' + name + ' managed to bind request port number ' + str(pub_port) )
        self.pub_port = pub_port
        pub_cfg = { 
                   "name":          name,
                   "request_port":  pub_port
                  }    
        cfg_filename = self.tmp_folder + '/publisher_' + name + '.json'
        print('Creating publisher file: "' + cfg_filename + '"')
        try:
            file_obj =  open(cfg_filename, 'w')
            cfg_file = json.dumps(pub_cfg)
            file_obj.write(cfg_file)   
        except:
            print('Publisher file write failed with error:\n\t' + str(sys.exc_info()))
            return
        print('Publisher file write is successful')
        

    
    def subscribe(self, name):
        from time import sleep
        cfg_filename = self.tmp_folder + '/publisher_' + name + '.json'
        
        while True:
            try:
                print('Trying to open publisher file: "' + cfg_filename + '"')
                with open(cfg_filename) as settings_file:
                    cfg_data = json.load(settings_file)  
                break  
            except:
                print('file: "' + cfg_filename + '" failure:' + str(sys.exc_info()) + ' Retrying')
                sleep(0.5)
        
        self.pub_port = cfg_data['request_port']
        self.sub_sock = socket.socket(socket.AF_INET, # Internet
                          socket.SOCK_DGRAM) # UDP
        sub_port = self.start_port
        while True:
            try:
                self.sub_sock.bind(('127.0.0.1', sub_port))
                break
            except:
                sub_port+=1
        self.sub_port = sub_port
        print ('subscriber to' + name + 'managed to bind at port ' + str(sub_port))
        #self.sub_sock.sendto(pkt, (addr, port)) 
           
    def receive(self, req):
        string = ''
        for var in req:
            string += str(var) + '\t'
        self.sub_sock.sendto(string, ('127.0.0.1', self.pub_port))
        data, addr = self.sub_sock.recvfrom(1024) # buffer size is 1024 bytes
        resp = {}
        data_arr = data.split('\t')
        for word in data_arr:
            try:
                name, val = word.split('=')
                resp[name] = val
            except:
                pass
        return resp
                                         
  
    def post(self, data):
        while True:
            try:
                req_string, addr = self.pub_sock.recvfrom(1024) # buffer size is 1024 bytes
            except:
                return
            request = req_string.split('\t')
            pkt = ''
            for word in request:
                try:
                    pkt += word + '=' + str(data[word]) + '\t'
                except:
                    pass
            self.pub_sock.sendto(pkt, (addr[0], addr[1]))    
                    
