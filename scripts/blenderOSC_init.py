#!/usr/bin/python3
# -*- coding: UTF-8 -*-

## blenderOSC_init.py

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


from bge import logic as gl
from scripts.sound import EasyAudio

'''send_receive.py is in scripts directory'''
from scripts.send_receive import Client


'''
This script run only once at the first frame
to initialize some variable that they are attributs of GameLogic
and used always during the game.
'''

gl.ip_in = "127.0.0.1"
gl.ip_out = "127.0.0.1"
gl.port_in = 9000
gl.port_out = 8000
gl.buffer_size = 1024

gl.text = "Test init Ö été ê ç ^ Œ œ "
gl.x, gl.y = 0, 0

# Listener python object
gl.myclient= Client(gl.ip_in, gl.port_in, gl.buffer_size, verbose=False)

def init_note():
    gl.musicsources = "wiki"
    gl.frame_counter = 0
    gl.text_change = False
    gl.position = 0

def init_audio():
    note_list = []
    for i in range(36):
        note_list.append(str(i))
    gl.note_piano = EasyAudio(note_list, "//samples/")

init_audio()
init_note()
