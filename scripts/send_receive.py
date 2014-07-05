#!/usr/bin/python3
# -*- coding: UTF-8 -*-

## send_receive.py

#############################################################################
# Copyright (C) Labomedia July 2014
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franproplin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
#############################################################################

import socket
try:
    from OSCcodec import OSCMessage, decodeOSC
except:
    from scripts.OSCcodec import OSCMessage, decodeOSC


class Receive:
    '''.'''
    def __init__(self, ip, port, buffer_size, verbose=False):
        '''Plug a socket.'''
        self.ip = ip
        self.port = port
        self.buffer_size = buffer_size
        self.verb = verbose
        self.data = None


        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            self.sock.bind((self.ip, self.port))
            self.sock.setblocking(0)
            self.sock.settimeout(0.01)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, buffer_size)
            if self.verb:
                print('Plug : IP = {} Port = {} Buffer Size = {}'.
                      format(ip, port, buffer_size))
        except:
            if self.verb:
                print('No connected on {0}:{1}'.format(self.ip, self.port))

    def listen(self):
        '''Return decoded OSC data, or None.'''
        try:
            raw_data = self.sock.recv(self.buffer_size)
            if self.verb:
                print("Receive from {0}:{1} : {2}".format(self.ip,
                                                self.port, raw_data))
            self.convert_data(raw_data)
        except:
            if self.verb:
                print('Nothing from {0}:{1}'.format(self.ip, self.port))
        return self.data

    def convert_data(self, raw_data):
        try:
            self.data = decodeOSC(raw_data)
            if self.verb:
                print("Decoded OSC message: {0}".format(self.data))
        except:
            if self.verb:
                print('Impossible to decode {0}'.format(raw_data))

class Send():
    '''Create your OSC messge with OSCcodec,
    example:
    msg = OSCMessage("/my/osc/address")
    msg.append('something')
    See OSCcodec documentation
    '''

    def __init__(self, verbose=True):
        '''Create an UDP socket.'''
        self.verb = verbose
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def _sendto(self, msg, address):
        '''Send msg to ip:port
        msg is an OSC message create with OSCMessage()
        address is a tuple.
        '''
        self.sock.sendto(msg.getBinary(), address)
        if self.verb:
            print("OSC message sended: {0}".format(msg))

    def simple_send_to(self, title, value, address):
        '''Send osc message: example
        simple_send_to((127.0.0.1, 8000), "/spam", 1.023)
        '''
        msg = OSCMessage(title, value)
        self._sendto(msg, address)
        if self.verb:
            print("OSC message sended: {0}".format(msg))

    def send_list_to(self, title, liste, address):
        '''Send osc message: example
        simple_send_to((127.0.0.1, 8000), "spam", [1, 2, 3])
        '''
        msg = OSCMessage(title)
        for l in liste:
            msg.append(l)
        self._sendto(msg, address)
        if self.verb:
            print("OSC message sended: {0}".format(msg))

# only to test this script standalone with pure data
if __name__ == "__main__":
    from time import sleep

    buffer_size = 1024

    ip_in = "127.0.0.1"
    port_in = 8000

    ip_out = "127.0.0.1"
    port_out = 9000

    my_receiver = Receive(ip_in, port_in, buffer_size, verbose=True)

    my_sender = Send(verbose=True)

    a = 0
    while True:
        a += 1
        sleep(0.01)

        data = my_receiver.listen()
        print(decodeOSC(b'/blender/x\x00\x00,f\x00\x00>\xaf\xbcf'))
        msg = OSCMessage("/test/rien")

        my_sender.send_list_to("/spam", [1, 2.01, "toto"], (ip_out, port_out))

        my_sender.simple_send_to("/toto", 3.14, (ip_out, port_out))
