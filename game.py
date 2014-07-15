###!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# game.py

from time import sleep
import threading
import json
from OSCcodec import decodeOSC, OSCMessage, OSCBundle, OSCError
from wikikIRC3 import MyBot
from etherpad3 import EtherPad
try:
    import signal
except ImportError:
    signal = None


class Game:
    def __init__(self):
        '''.'''
        self.mybot = None
        self.wiki = u""
        self.mypad = None
        self.text = u""

        # connect
        ##self.connect_pad()
        ##self.connect_irc()

        # Mouvement
        self.x = 0
        self.sens = 1

    def connect_pad(self):
        # Etherpad
        url = "http://etherpad.pingbase.net/MhYHGouMuX"
        # on va hériter de self.new_lines et self.text
        self.mypad = EtherPad(url, bavard=False)
        print("Routine to get new lines at etherpad.pingbase.net/MhYHGouMuX")
        # Pad thread
        self.pad()

    def connect_irc(self):
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

    def request(self, data, addr):
        '''Je reçois data de addr, data est toujours un message OSC.'''
        dec, typ = self.is_bundle_or_uni(data)
        print("Raw =", data)
        print("Data = ", dec ,"de type ", typ, " from ", addr)
        resp = None
        ##if typ == "osc":
            ##tag_dict = self.get_all_tag_in_bundle(dec)
            ##if "/moi" in tag_dict:
                ##self.set_x_possiton()
                ##d = {
                ##"text": u"@ là forêt, païen, où À la fête ! {} []",
                ##"/blender/x": self.x
                ##}
                ##resp = json.dumps(d).encode("utf-8")
                ##if typ == "osc":
            ##tag_dict = self.get_all_tag_in_bundle(dec)

        self.set_x_possiton()
        d = {
        "text": u"@ là forêt, païen, où À la fête ! {} []",
        "/blender/x": self.x
        }
        resp = json.dumps(d).encode("utf-8")
        return resp

    def set_x_possiton(self):
        if self.x > 10:
            self.sens = -1
        if self.x < -10:
            self.sens = 1
        self.x += self.sens/10

    def get_all_tag_in_bundle(self, dec):
        '''Recherche de tag dans la liste des messages.'''
        tag_dict = {}
        for d in dec:
            tag_dict[d[0]] = d[2]
        print(tag_dict)
        return tag_dict

    def is_bundle_or_uni(self, data):
        '''test si bundle ou unicode sinon None.'''
        bund = True
        typ = None
        try:
            dec = decodeOSC(data)
            if len(dec) > 0:
                typ = "osc"
                # test bundle
                if len(dec) > 0:
                    if dec[0] != "#bundle":
                        dec = None
                        typ = None
                        bund = None
                    else:
                        # je coupe les 2 premiers
                        dec = dec[2:]
            else:
                typ = None
        except OSCError:
            bund = None

        if not bund:
            try:
                dec = data.decode("utf-8")
                typ = "uni"
            except:
                print("Data received incompréhensible")
                dec, typ = None, None
        return dec, typ

    def OSC_x_position(self):
        msg = OSCMessage("/blender/x")

        msg.append(self.x) # de -10 à 10
        bnd = OSCBundle()
        bnd.append(msg)

        msg1 = OSCMessage("/toto")
        msg1.append("pourquoi ?")
        bnd.append(msg1)

        msg2 = OSCMessage("/test")
        msg2.append(1)
        bnd.append(msg2)
        return bnd.getBinary()

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

    data = b'#budle\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x10/moi\x00\x00\x00\x00,i\x00\x00\x00\x00\x00\x01\x00\x00\x00\x14/test\x00\x00\x00,s\x00\x00toto\x00\x00\x00\x00'

    dec = ['#bundle', 0.0, ['/moi', ',i', 1]]
    addr = ('127.0.0.1', 53860)
    resp = mygame.request(data, addr)


    ##loop = asyncio.get_event_loop()
    ##@asyncio.coroutine
    ##def get_diff_etherpad_every_2s(self):
        ##while True:
            ##print("J'attends la réponse de etherpad")
            ##self.text = self.mypad.get_text() # liste de lignes
            ##print("Etherpad diff =", new_lines)
            ##yield from asyncio.sleep(2)
            ##loop.run_until_complete(mygame.get_diff_etherpad_every_2s())
