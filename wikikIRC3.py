#!/usr/bin/python3
# -*- coding: utf8 -*-

## wikikIRC3.py

# WikikIRC by Olivier Baudu, Anthony Templier for Labomedia September 2011.
# Modified by Sylvain Blocquaux 2012.
# Modified for Le Bit de Dieu by SergeBlender for Labomedia November 2013.
# Improved by SergeBlender for Labomedia June 2014.
# olivier arobase labomedia point net // http://lamomedia.net
# Published under License GPLv3: http://www.gnu.org/licenses/gpl-3.0.html


import os
import subprocess
from time import sleep
import re
import urllib.request
from irc.bot import SingleServerIRCBot

try:
    import lxml
except ImportError:
    import subprocess
    print("Vous devez instaler python3-lxml")
    print("sudo apt-get install python3-lxml")
    subprocess.call('sudo apt-get install python3-lxml', shell=True)
    import lxml

try:
    from bs4 import BeautifulSoup
except ImportError:
    import subprocess
    print("Vous devez instaler python3-bs4")
    print("sudo apt-get install python3-bs4")
    subprocess.call('sudo apt-get install python3-bs4', shell=True)
    from bs4 import BeautifulSoup

REPLACE =   [
            "=", "*", "|", "''", "<", ">", "{", "}", "[", "]", "•", "/",
            "listeRecents", "/noinclude",
            "  ", "   ",
            "align ", "left", "valign", "top", "<br", "_"
            ]

FIRST = [
            "=", "[", "{", "#", "<", ":", "!"
        ]

BLACK = [
            "Discussion Utilisateur", "small","#", "rowspan", "liste1",
            "galerie web"
        ]

class MyBot(SingleServerIRCBot):
    '''Bot qui récupère les modifications sur Wikipedia,
    en ne retournant que les phrases jolies.'''
    def __init__(self, server_list, nickname, realname, bavard=True):
        '''Doc de SingleServerIRCBot
        - irc_list -- A list of ServerSpec objects or tuples of
                       parameters suitable for constructing ServerSpec
                       objects. Defines the list of servers the bot will
                       use (in order).
        - nickname -- The bot's nickname.
        - realname -- The bot's realname.
        '''
        SingleServerIRCBot.__init__(self, server_list, nickname, realname)
        self.wiki_out = ''
        self.bavard = bavard
        self.address = ""

    def on_welcome(self, serv, ev):
        '''Connection à l'IRC.'''
        print ("\n Connexion on IRC...\n")
        serv.join("#fr.wikipedia")

    def on_pubmsg(self, serv, ev):
        '''Si message reçu sur l'IRC, met à jour self.wiki_out.'''
        self.get_address(ev)
        if self.address:
            # Liste de str avec les modifs de la page
            liste = self.modifs_in_page()
            self.filtre(liste)
        return self.wiki_out

    def modifs_in_page(self):
        '''Retourne une liste de modifications dans la page de
        comparaison de version de wikipedia.
        '''
        page = self.get_page() # unicode
        data = lxml.etree.HTML(page)
        # tag = '<td class="diff-context"><div>'
        liste = data.xpath('//td[@class="diff-context"]/div/text()')
        return liste

    def filtre(self, liste):
        '''Filtre la liste de lignes récupérées pour avoir un beau texte.'''
        good = []
        for line in liste:
            # Suppression des petites lignes et des lignes vides
            if len(line) > 0:
                if not line[0] in FIRST:
                    for i in REPLACE:
                        line = line.replace(i, ' ')
                        # Suppression d'un expace en premier caractère
                        if len(line) > 0:
                            if line[0] == ' ':
                                line = line[1:]
                    # Suppression des lignes techniques
                    ok = 1
                    for b in BLACK:
                        if b in line:
                            ok = 0
                    if ok:
                        good.append(line)
        if len(good) > 0:
            if len(good[0]) > 40:
                self.wiki_out = good[0]
                if self.bavard:
                    if self.wiki_out:
                        print(self.wiki_out, "\n\n")

    def get_page(self):
        '''Retourne le html de la page.'''
        try:
            req = urllib.request.Request(self.address)
            # Add header becauce wikipedia expected a navigator
            req.add_header('User-agent', 'WikikIRC-0.4')
            handle = urllib.request.urlopen(req)
            page = handle.read()
            page = page.decode('utf-8')
            handle.close()
        except:
            print(('Page {0} introuvable'.format(self.url)))
            page = ''
        return page

    def get_address(self, ev):
        '''Met à jour l'adresse de la page modifiée.'''
        try:
            msg = ev.arguments[0]
            # Delete color codes codes and get only text
            message = re.compile("\x03[0-9]{0,2}").sub('', msg)
            # Position de http://
            debut = re.search("http://fr.wikipedia.org", message)
            # Je coupe le début inutile
            message = message[debut.start():]
            # Position du premier espace après debut
            fin = re.search(" ", message)
            # Je coupe la fin
            self.address = message[:fin.start()]
        except:
            self.address = None
            if self.bavard:
                print("Adresse introuvable")
        if self.bavard:
            print("Récupération des modifications à l'adresse : {0}".format(
                                                                self.address))


if __name__ == "__main__":
    server_list = [("irc.wikimedia.org", 6667)]
    nickname = "Labomedia-test"
    realname = "Syntaxis analysis in Python with bot"
    print("Test", "\n", server_list, "\n", nickname, "\n", realname)
    mybot = MyBot(server_list, nickname, realname, bavard=True)
    mybot.start()
