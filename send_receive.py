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


'''
Only to be used in the Blender 3D Game Engine.

Send class send UDP OSC message,
Receive class receive OSC message.
Build with python3 socket standard module.


OSC message are created and decoded with OSCcodec.py in pyOSCcodec at
https://github.com/sergeLabo/pyOSCcodec

pyOSCcodec is a part of OSC.py, from
https://gitorious.org/pyosc/devel/source/6aaf78b0c1e89942a9c5b1952266791b7ae16012:

See documentation in send_receive.html.

The aim of this script is to be used in the
Blender Game Engine in python script.

Blender Game engine don't accept thread, twisted, socketserver, asyncio ...

String are latin-1 encoded and decoded.
    ISO 8859-1 = ISO/CEI 8859-1 = Latin-1

To receive or send unicode string, don't use OSC.

Use listen_unicode() in send_receive.py to receive UDP data without OSC.
Send with socket.sendto(data, address)

and data = "your unicode string".encode('utf-8')

'''


import socket

try:
    # to run standalone
    from OSCcodec import OSCMessage, decodeOSC
except:
    # to run in blender scripts directory
    from scripts.OSCcodec import OSCMessage, decodeOSC

class Receive:
    '''Receive, decode Message with a socket .'''

    def __init__(self, ip, port, buffer_size=1024, verbose=False):
        '''Plug an UDP socket.
        ip example: "localhost", "127.0.0.1", "10.0.0.100"
        port = integer
        buffer_size = integer, used to clear out the buffer at each reading
        verbose = True is very verbose in terminal
        '''
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
            # This option set buffer size
            # Every self.sock.recv() empty the buffer,
            # so we have always the last incomming value
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, buffer_size)
            if self.verb:
                print('Plug : IP = {} Port = {} Buffer Size = {}'.
                      format(ip, port, buffer_size))
        except:
            if self.verb:
                print('No connected on {0}:{1}'.format(self.ip, self.port))

    def send_with_receiver_socket(self, data, addr):
        '''Send data with this socket.'''
        self.sock.sendto(data, addr)

    def listen_from(self):
        '''Get decoded received data, OSC in a list or string unicode.'''
        raw_data = None
        try:
            # bytes, address
            raw_data, addr = self.sock.recvfrom(self.buffer_size)
            if self.verb:
                print("Binary received from {0}:{1} : {2}".format(self.ip,
                                                self.port, raw_data))
        except:
            if self.verb:
                print('Nothing from {0}:{1}'.format(self.ip, self.port))
        if raw_data:
            self.data = self.convert_data(raw_data)

    def get_data(self):
        '''Get received data.'''
        self.listen()
        return self.data

    def listen(self):
        '''Get decoded received data, OSC in a list or string unicode.'''
        raw_data = None
        try:
            raw_data = self.sock.recv(self.buffer_size)
            if self.verb:
                print("Binary received from {0}:{1} : {2}".format(self.ip,
                                                self.port, raw_data))
        except:
            if self.verb:
                print('Nothing from {0}:{1}'.format(self.ip, self.port))
        if raw_data:
            self.data = self.convert_data(raw_data)

    def convert_data(self, raw_data):
        '''From raw binary data, return decoded OSC data in a list,
        or unicode string .
        '''
        data = None
        try:
            data = decodeOSC(raw_data)
            if self.verb:
                print("Decoded OSC message: {0}".format(self.data))
        except:
            data = raw_data.decode('utf-8')
            if self.verb:
                print('No OSC message in {0}'.format(raw_data))
        return data

    def listen_unicode(self):
        '''Only to receive data without OSC.
        Sended data must be encoded with 'utf-8'.
        Return raw data decoded with 'utf-8', or None.'''
        try:
            raw_data = self.sock.recv(self.buffer_size)
            if self.verb:
                print("Receive from {0}:{1} : {2}".format(self.ip,
                                                self.port, raw_data))
            self.data = raw_data.decode('utf-8')
        except:
            self.data = None
            if self.verb:
                print('Nothing from {0}:{1}'.format(self.ip, self.port))
        return self.data


class Send:
    '''Create your OSC messge with OSCcodec,
    example:
    msg = OSCMessage("/my/osc/address")
    msg.append('something')
    See OSCcodec documentation in OSCcodec.html.
    '''

    def __init__(self, verbose=True):
        '''Create an UDP socket.'''
        self.verb = verbose
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_str_to(self, string, address):
        '''Send unicode string to address = (ip, port).'''
        self.sock.sendto(string.encode("utf-8"), address)

    def send_to(self, msg, address):
        '''Send msg to address = tuple = (ip, port)
        msg is an OSC message create with OSCMessage().
        '''
        self.sock.sendto(msg.getBinary(), address)

    def simple_send_to(self, title, value, address):
        '''Create and send OSC message:

        tille: string beginning with "/
        value: int, str, list, dict,
                dict are conert to list

        example:
        simple_send_to((127.0.0.1, 8000), "/spam", 1.023)
        '''
        msg = OSCMessage(title, value)
        self.send_to(msg, address)
        if self.verb:
            print("OSC message sended: {0}".format(msg))


class Client:
    '''Send and Receive with the same socket.

    Send a request, and get the response of a sever.
    datas aren't encoded and decoded in this class.
    Use datagram_decode.py to decode.
    '''

    def __init__(self, ip, port, buffer_size=1024, verbose=False):
        '''Plug an UDP socket.
        ip example: "localhost", "127.0.0.1", "10.0.0.100"
        port = integer
        buffer_size = integer, used to clear out the buffer at each reading
        verbose = True is very verbose in terminal
        '''
        self.ip = ip
        self.port = port
        self.buffer_size = buffer_size
        self.verb = verbose
        self.conn = False
        self.data = None

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            self.sock.bind((self.ip, self.port))
            self.sock.setblocking(False)
            self.sock.settimeout(0.01)
            # This option set buffer size
            # Every self.sock.recv() empty the buffer,
            # so we have always the last incomming value
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, buffer_size)
            if self.verb:
                print('Plug : IP = {} Port = {} Buffer Size = {}'.
                      format(ip, port, buffer_size))
        except:
            if self.verb:
                print('No connected on {0}:{1}'.format(self.ip, self.port))

    def send(self, req):
        '''Send request to connected socket.'''
        addr = self.ip, self.port
        self.sock.connect(addr)
        self.sock.send(req)
        if self.verb:
            print('{0} sended'.format(req))

    def send_to(self, req, address):
        '''Send request to address = (ip, port)
        '''
        self.sock.sendto(req, address)
        if self.verb:
            print('{0} sended'.format(req))

    def listen(self):
        '''Return received data and address from.'''
        raw_data, addr = None, None
        try:
            raw_data, addr = self.sock.recvfrom(self.buffer_size)
            if self.verb:
                print("Binary received from {0}: {1}".format(addr, raw_data))
        except:
            if self.verb:
                print('Received nothing')
        return raw_data, addr
