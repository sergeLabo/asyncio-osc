###!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# tulipserver.py

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

import asyncio
import subprocess
try:
    import signal
except ImportError:
    signal = None

from time import time, sleep
from game import Game
from OSCcodec import decodeOSC, OSCMessage, OSCBundle

class MyServerUdpProtocol:
    def __init__(self):
        self.mygame = Game()

    def connection_made(self, transport):
        print('start', transport)
        self.transport = transport
        self.t0 = time()

    def datagram_received(self, data, addr):
        '''Le serveur répond à chaque requête du client,
        la réponse dépend de la question,
        et de la gestion du jeu par le serveur
        Doc:
        ephemeral port: Many Linux kernels use the port range 32768 to 61000
        Game étudie la question, ouah, joli ça.
        '''
        resp = self.mygame.request(data, addr)
        if resp:
            ##self.transport.sendto(resp, ("127.0.0.1", 9000))
            self.transport.sendto(resp, addr)

    def datagram_send(self, data, addr):
        #print('Data sended:', data, "to", addr)
        self.transport.sendto(data, addr)

    def error_received(self, exc):
        print('Error received:', exc)

    def connection_lost(self, exc):
        print('stop', exc)

def start_server(loop, addr):
    t = asyncio.Task(loop.create_datagram_endpoint(
        MyServerUdpProtocol, local_addr=addr))
    transport, server = loop.run_until_complete(t)
    return transport


if __name__ == '__main__':
    host = "127.0.0.1"
    port = 8000

    #subprocess.Popen(['blenderplayer','asyncio-osc.blend'],
                        #stdout=subprocess.PIPE)

    loop = asyncio.get_event_loop()
    if signal is not None:
        loop.add_signal_handler(signal.SIGINT, loop.stop)
    server = start_server(loop, (host, port))

    subprocess.Popen(['blenderplayer','asyncio-osc.blend'],
                        stdout=subprocess.PIPE)
    try:
        print("Le serveur UDP tourne")
        loop.run_forever()
    finally:
        server.close()
        loop.close()
