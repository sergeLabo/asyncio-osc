#!/usr/bin/python3
# -*- coding: UTF-8 -*-

## datagram_decode.py

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
How to code and decode data sended on UDP:
3 possibilities with this script:
    - unicode
    - osc
    - json
'''

import json
from OSCcodec import OSCMessage, decodeOSC


class Decode:
    '''Decode UDP Datagram.
    Only:
        - OSC Message
        - Unicode utf-8 string
        - JSON
         https://docs.python.org/3.4/library/json.html
         http://fr.openclassrooms.com/informatique/cours/serialisez-vos-objets-au-format-json
        '''
    def __init__(self):
        pass

    def decode(self, data):
        '''Return decoded data and type:
        - data is always bytes
        types are:
        - json
        - OSC
        - Unicode string.
        .'''
        decod, typ = None, None
        decod, typ = self.json_test(data)
        if not typ:
            decod, typ = self.unicode_test(data)
        if not typ:
            decod, typ = self.osc_test(data)
        return decod, typ

    def json_test(self, data):
        '''Test if type is json, return decoded and type.'''
        typ = None
        try:
            decod = data.decode("utf-8")
            js = json.loads(decod)
            typ = "json"
        except:
            js = None
        return js, typ

    def unicode_test(self, data):
        '''Test if type is unicode string, return decoded and type.'''
        typ = None
        try:
            decod = data.decode("utf-8")
            typ = "uni"
        except:
            decod = None
        return decod, typ

    def osc_test(self, data):
        '''Test if type is OSC Message, return decoded and type.'''
        typ = None
        try:
            decod = decodeOSC(data)
            typ = "osc"
        except:
            decod = None
        return decod, typ


def comprendre():
    '''
    Création d'un message OSC:
    OSCMessage: <class 'OSCcodec.OSCMessage'> /moi [3.140000104904175]

    Message en Binaire:
        Binaire : <class 'bytes'> b'/moi\x00\x00\x00\x00,f\x00\x00@H\xf5\xc3'

    Message decodé latin-1:
        Decodé : <class 'str'> /moi,f@HõÃ

    JSON:
        json:  <class 'str'> /moi,f@HõÃ

    json encodé utf-8:
        Encodé : <class 'bytes'> b'/moi\x00\x00\x00\x00,f\x00\x00@H\xc3\xb5\xc3\x83'

    Message OSC en liste python:
        OSC : <class 'list'> ['/moi', ',f', 3.1369450092315674]
    '''

    print("Création d'un message OSC:")
    some5 = OSCMessage("/moi", 3.14)
    print("    OSCMessage:", type(some5), some5, "\n")

    print("Message en Binaire:")
    some6 = some5.getBinary()
    print("    Binaire :", type(some6), some6, "\n")

    print("Message decodé latin-1:")
    some7 = some6.decode("latin-1")
    print("    Decodé :", type(some7), some7, "\n")

    # Sérialisation
    myjson = json.dumps(some7)
    # Désérialisation
    j = json.loads(myjson)

    print("JSON:")
    print("    json: ",type(j), j, "\n")

    print("json encodé utf-8:")
    e = j.encode("utf-8")
    print("    Encodé :", type(e), e, "\n")

    print("Message OSC en liste python:")
    d = decodeOSC(e)
    print("    OSC :", type(d), d, "\n")


if __name__ == '__main__':
    r1 = b'/blender/x\x00\x00,f\x00\x00>\x99\x99\x9a'
    r = u"Mon Maître"
    r2 = r.encode("utf-8")
    r3 = b'#bundle\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x14/blender/x\x00\x00,f\x00\x00=\xcc\xcc\xcd\x00\x00\x00\x18/toto\x00\x00\x00,s\x00\x00pourquoi ?\x00\x00\x00\x00\x00\x10/test\x00\x00\x00,i\x00\x00\x00\x00\x00\x01'
    r4 = []
    r5 = b'["biroute", 1, [1, 2], {"1": 2, "3": 4}]'
    r6 = b'{"1": {"r": 56, "list": [1, 2, 3], "t": 2}}'
    r7 = b'[]'
    r8 = b''
    r9 = {}
    r10 = 1
    r11 = 2.365

    mydecoder = Decode()
    for s in [r,r1,r2,r3,r4,r5,r6,r7,r8,r9,r10,r11]:
        print("\n\n")
        print(s)
        d, t = mydecoder.decode(s)
        print(d, t)

    comprendre()
