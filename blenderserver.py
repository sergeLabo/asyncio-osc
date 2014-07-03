#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# blenderserver.py

from bge import logic as gl
import sys, threading, time
import asyncio
try:
    import signal
    #print("signal module imported")
except ImportError:
    signal = None

class MyServerUdpEchoProtocol:

    def connection_made(self, transport):
        #print('start', transport)
        self.transport = transport

    def datagram_received(self, data, addr):
        print('Data received:', data, addr)
        self.transport.sendto(data, addr)

    def error_received(self, exc):
        print('Error received:', exc)

    def connection_lost(self, exc):
        print('stop', exc)


def start_server(loop, addr):
    t = asyncio.Task(loop.create_datagram_endpoint(
        MyServerUdpEchoProtocol, local_addr=addr))
    transport, server = loop.run_until_complete(t)
    return transport


if __name__ == '__main__':


    ##host = "127.0.0.1"
    ##port = 8888
##
    ##gl.loop = asyncio.get_event_loop()
    ##if signal is not None:
        ##gl.loop.add_signal_handler(signal.SIGINT, gl.loop.stop)
    ##gl.server = start_server(gl.loop, (host, port))
##
##
    ##t0 = time.time()
    ##while time.time() - t0 < 0.008:
        ##gl.loop.run_forever()
    ##gl.server.close()
    ##gl.loop.close()

    if not gl.connected:
        host = "127.0.0.1"
        port = 8888

        gl.loop = asyncio.get_event_loop()
        if signal is not None:
            gl.loop.add_signal_handler(signal.SIGINT, gl.loop.stop)
        gl.server = start_server(gl.loop, (host, port))

    if gl.connected:
        t0 = time.time()
        while time.time() - t0 < 0.008:
            gl.loop.run_forever()
        gl.server.close()
        gl.loop.close()

    ##thread3 = threading.Thread(target=gl.loop.run_forever)
    ##thread3.start()
    ##print("gl.loop.run_forever ok")

