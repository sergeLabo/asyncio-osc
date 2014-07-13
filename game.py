###!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# game.py

from time import sleep
import threading
from OSCcodec import decodeOSC, OSCMessage, OSCBundle
from wikikIRC3 import MyBot
from etherpad3 import EtherPad
import asyncio
try:
    import signal
except ImportError:
    signal = None


class Game:
    def __init__(self):
        # Etherpad
        url = "http://etherpad.pingbase.net/MhYHGouMuX"
        # on va hériter de self.new_lines et self.text
        self.mypad = EtherPad(url, bavard=False)
        print("Routine to get new lines at etherpad.pingbase.net/MhYHGouMuX")
        self.text = u""
        # Pad thread
        self.pad()

        # IRC
        server_list = [("irc.wikimedia.org", 6667)]
        nickname = "Labomedia-test"
        realname = "Syntaxis analysis in Python with bot"
        print("Test", "\n", server_list, "\n", nickname, "\n", realname)
        # self.wiki_out
        self.mybot = MyBot(server_list, nickname, realname, bavard=False)
        self.wiki = self.mybot.wiki_out
        # IRC thread
        self.irc()

        # Mouvement
        self.x = 0
        self.sens = 1

    def OSC_x_position(self):
        msg = OSCMessage("/blender/x")
        if self.x > 10:
            self.sens = -1
        if self.x < -10:
            self.sens = 1
        self.x += self.sens/10
        msg.append(self.x) # de -10 à 10
        return msg.getBinary()

    def pad(self):
        # Thread qui tourne pour le bot
        thread1 = threading.Thread(target=self.get_diff_etherpad)
        thread1.start()

    def get_diff_etherpad(self):
        while True:
            self.text = self.mypad.get_text() # liste de lignes
            self.wiki = self.mybot.wiki_out
            sleep(2)

    def irc(self):
        # Thread qui tourne pour le bot
        thread2 = threading.Thread(target=self.mybot.start)
        thread2.start()

if __name__ == '__main__':
    mygame = Game()


    ##loop = asyncio.get_event_loop()
    ##@asyncio.coroutine
    ##def get_diff_etherpad_every_2s(self):
        ##while True:
            ##print("J'attends la réponse de etherpad")
            ##self.text = self.mypad.get_text() # liste de lignes
            ##print("Etherpad diff =", new_lines)
            ##yield from asyncio.sleep(2)
            ##loop.run_until_complete(mygame.get_diff_etherpad_every_2s())
