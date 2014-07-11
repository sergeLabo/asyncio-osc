###!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# tulipserver.py

import sys
import threading
import asyncio
try:
    import signal
except ImportError:
    signal = None

import random
from time import time, sleep
from OSCcodec import decodeOSC, OSCMessage, OSCBundle
from wikikIRC3 import MyBot
from etherpad3 import EtherPad  # revoir class de ?

TEST = "Ö été ê ç ^ Œ œ 合久必分 分久必合"

class MyServerUdpProtocol:
    def connection_made(self, transport):
        print('start', transport)
        self.transport = transport
        self.t0 = time()

    def datagram_received(self, data, addr):
        # ephemeral port: Many Linux kernels use the port range 32768 to 61000
        #print('Data received:', data, "type", type(data), "from", addr)
        x = OSC_x_position()
        self.datagram_send(x, ("127.0.0.1", 9000))
        sleep(0.02)
        if time() - self.t0 > 2:
            self.t0 = time()
            self.datagram_send(TEST.encode("utf-8"), ("127.0.0.1", 9000))

    def datagram_send(self, data, addr):
        print('Data sended:', data, "to", addr)
        self.transport.sendto(data, addr)

    def error_received(self, exc):
        print('Error received:', exc)

    def connection_lost(self, exc):
        print('stop', exc)

def OSC_x_position():
    msg = OSCMessage("/blender/x")
    msg.append(20*random.random() - 15)
    return msg.getBinary()

def send_cube_position():
    send_to_blender()

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

    # Thread qui tourne pour le bot IRC
    server_list = [("irc.wikimedia.org", 6667)]
    nickname = "Labomedia-test"
    realname = "Syntaxis analysis in Python with bot"
    print("Test", "\n", server_list, "\n", nickname, "\n", realname)
    mybot = MyBot(server_list, nickname, realname, bavard=True)
    thread3 = threading.Thread(target=mybot.start)
    #thread3.start()

    try:
        print("Le serveur UDP tourne")
        loop.run_forever()
    finally:
        server.close()
        loop.close()




##@asyncio.coroutine
##def get_diff_etherpad_every_2s():
    ##url = "http://etherpad.pingbase.net/MhYHGouMuX"
    ##my_pad = EtherPad(url, False)
    ##print("Routine to get new lines in http://etherpad.pingbase.net/MhYHGouMuX")
    ##while True:
        ##print("j'attends la réponse de etherpad")
        ##new_lines = my_pad.get_text() # liste de lignes
        ##print("etherpad diff", new_lines)
        ##yield from asyncio.sleep(2)
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
    ##asyncio.Task(get_diff_etherpad_every_2s())
