###!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# tulipserver.py

import sys
import asyncio
try:
    import signal
except ImportError:
    signal = None

from OSCcodec import decodeOSC, OSCMessage, OSCBundle
import random


class MyServerUdpProtocol:

    def connection_made(self, transport):
        print('start', transport)
        self.transport = transport

    def datagram_received(self, data, addr):
        #print('Data received:', data, "type", type(data), "from", addr)
        res = decodeOSC(data)
        print("OSC message receiced: {0}".format(res))

        # echo
        self.transport.sendto(data, addr)

        msg = OSCMessage("/blender/x")
        msg.append(10*random.random())
        self.transport.sendto(msg.getBinary(), ("127.0.0.1", 9999))


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
    port = 8888

    loop = asyncio.get_event_loop()
    if signal is not None:
        loop.add_signal_handler(signal.SIGINT, loop.stop)

    server = start_server(loop, (host, port))
    try:
        loop.run_forever()
    finally:
        server.close()
        loop.close()
