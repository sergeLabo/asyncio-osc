#!/usr/bin/python3
# -*- coding: utf8 -*-

# etherpad3.py

#############################################################################
# Copyright (C) Labomedia June 2014
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


from time import sleep
import sys, os
import subprocess
import re
import json
import urllib.request, urllib.error, urllib.parse

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("Vous devez instaler python3-bs4")
    print("sudo apt-get install python3-bs4")
    subprocess.call('sudo apt-get install python3-bs4', shell=True)
    from bs4 import BeautifulSoup


class EtherPad:
    '''Retourne les nouvelles lignes écrites dans le Pad
       à la fin du texte existant.
    '''

    def __init__(self, url, bavard=False):
        '''Définir l' address de l'etherpad, bavard informe en terminal.'''
        self.url = url
        self.bavard = bavard
        self.nbl_new = 0
        self.nbl_old = 0
        self.set_inital_text_lenght()
        self.new_lines = None
        self.text = ""

    def get_text(self):
        '''Met à jour la variable self.text avec
        tout le texte contenu dans le pad.
        '''
        page = self.get_page()
        script = self.get_script_var(page)
        text = self.get_text_in_js_var(script)
        self.text = self.suppression_des_lignes_vides_a_la_fin(text)
        if self.bavard:
            # clear remonte les lignes
            # reset est bien aussi pour effacer vraiment toutes les lignes
            subprocess.call('reset', shell=True)
            print("Le texte entier est:\n{0}".format(self.text))
        return self.text

    def suppression_des_lignes_vides_a_la_fin(self, text):
        # Suppression des lignes vides à la fin
        texte_en_liste = text.splitlines()

        n = len(texte_en_liste)
        for i in reversed(range(n)):
            if len(texte_en_liste[i]) == 0:
                texte_en_liste.remove(texte_en_liste[i])
            else:
                break
        # Reforme le text en un string
        le_texte = '\n'.join(texte_en_liste)
        return le_texte

    def suppression_des_fins_de_lignes(self, text):
        # Cette fonction ne sert à rien
        le_texte = [x for x in texte_en_liste if x != 0]
        # Suppression de toutes les fin de lignes
        le_texte = text.replace('\n', '')

    def set_inital_text_lenght(self):
        '''Définit le nombre total de lignes initiales.'''
        page = self.get_page()  # html in unicode
        script = self.get_script_var(page)  # pretty unicode
        text = self.get_text_in_js_var(script)  # liste de lignes
        text = text.splitlines()
        self.nbl_old = len(text) - 1
        if self.bavard:
            print(("Nombre de lignes initiales = {0}".format(self.nbl_old+1)))

    def get_new_finished_lines(self):
        '''Retourne toutes les nouvelles lignes sauf la dernière.'''
        page = self.get_page()
        script = self.get_script_var(page)
        text = self.get_text_in_js_var(script)  # liste de lignes
        self.new_finished_lines_filter(text)
        if self.new_lines:
            nbla = len(self.new_lines)
        else:
            nbla = 0
        if self.bavard:
            print(('''Nonbre total d'anciennes lignes: {0}
Nombre total de nouvelles lignes: {1}
Nombre de nouvelles lignes affichées: {2}'''.format(self.nbl_old,
                                                    self.nbl_new, nbla)))
            self.print_new_lines()
        return self.new_lines

    def print_new_lines(self):
        '''Imprime en terminal les nouvelles lignes.'''
        if self.new_lines:
            print('Les nouvelles lignes sont:\n')
            for l in self.new_lines:
                print(('{0}'.format(l)))

    def new_finished_lines_filter(self, text):
        '''Retourne une liste des lignes filtrées.'''
        self.nbl_new = len(text)
        self.new_lines = None
        # Si au moins 2 lignes nouvelles en plus
        if self.nbl_new >= self.nbl_old + 2:
            # Je cherche combien de ligne vides à la fin du texte
            for i in reversed(list(range(self.nbl_new))):
                nbl_cut = 1
                if text[i] != '':
                    # Je ne garde pas les lignes vides, ni la dernière non vide
                    nbl_cut = self.nbl_new - i
                    break
            self.new_lines = text[self.nbl_old:-nbl_cut]
            self.nbl_old = self.nbl_new - nbl_cut
        # Des lignes sont effacées dans le pad
        if self.nbl_new < self.nbl_old:
            self.nbl_old = self.nbl_new

    def get_page(self):
        '''Retourne le html de la page.'''
        try:
            req = urllib.request.Request(self.url)
            handle = urllib.request.urlopen(req)
            page = handle.read()
            page = page.decode('utf-8')
            handle.close()
        except IOError:
            print(('Page Etherpad {0} introuvable'.format(self.url)))
            page = 'Page'
        return page

    def get_script_var(self, page):
        '''Retourne le code entre les balises "script" avec la belle soupe.'''
        soup = BeautifulSoup(page)
        try:
            script = soup.script.prettify()  # unicode
        except:
            script = 'Pas de tag script'
        return script

    def get_text_in_js_var(self, script):
        '''Retourne le texte du pad en liste de lignes.'''
        try:
            jsonValue = '{%s}' % (script.split('{', 1)[1].rsplit('}', 1)[0],)
            ##jsonValue = '{0}{1}{2}'.format(u'{',
                                ##textValue.split('{', 1)[1].rsplit('}', 1)[0],
                                ##u'}')
            # Dictionnaire obtenu avec le code javascript
            decoded = json.loads(jsonValue, encoding='utf-8')
            # Le texte est là
            text = decoded['collab_client_vars']['initialAttributedText']['text']
        except:
            text = 'Le texte contient des caractères interdits !'
        return text  # str


if __name__ == "__main__":
    #url = "http://etherpad.pingbase.net/ServietteFarcie"
    url = "http://etherpad.pingbase.net/MhYHGouMuX"
    my_pad = EtherPad(url, False)

    while True:
        sleep(2)
        text = my_pad.get_text() # liste de lignes
        new_lines = my_pad.get_new_finished_lines()
        print(new_lines)
