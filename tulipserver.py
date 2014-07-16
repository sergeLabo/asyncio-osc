###!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# tulipserver.py

import asyncio
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

    loop = asyncio.get_event_loop()
    if signal is not None:
        loop.add_signal_handler(signal.SIGINT, loop.stop)

    server = start_server(loop, (host, port))


    try:
        print("Le serveur UDP tourne")
        loop.run_forever()
    finally:
        server.close()
        loop.close()




##
##@asyncio.coroutine
##def wait_2s():
    ##while True:
        ##print("tempo 2s")
        ##yield from asyncio.sleep(2)
        ##
#res = decodeOSC(data)
#print("OSC message receiced: {0}".format(res))
# echo
#rep = "Ö été ê ç ^ Œ œ 合久必分 分久必合".encode('utf-8')
#self.transport.sendto(rep, addr)
#self.transport.sendto(rep, ("127.0.0.1", 9000))

    ##asyncio.Task(wait_2s())

        ##print('Data received:', data, "type", type(data), "from", addr)
        ##msg_x = self.mygame.OSC_x_position()
        ###print("msg_x =", msg_x)
        ##self.datagram_send(msg_x, ("127.0.0.1", 9000))
        ##if time() - self.t0 > 2:
            ##self.t0 = time()
            ##sleep(0.02)
            ##t = self.mygame.text
            ##w = self.mygame.wiki
            ##self.datagram_send(w.encode("utf-8"), ("127.0.0.1", 9000))
