#!/usr/bin/python3
# -*- coding: UTF-8 -*-

## blenderOSC_always.py

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

'''
This script run at all frame.
'''

import textwrap
from bge import logic as gl
from bge import events

note_dict = {   '0':0,  '1':35,  '2':2,  '3':34,  '4':4,  '5':33,
                'a':6,  'b':7,  'c':8,  'd':9,  'e':10, 'f':11,
                'g':12, 'h':13, 'i':14, 'j':15, 'k':16, 'l':17,
                'm':18, 'n':19, 'o':20, 'p':21, 'q':22, 'r':23,
                's':24, 't':25, 'u':26, 'v':27, 'w':28, 'x':29,
                'y':30, 'z':31, '6':32, '7':1, '8':3, '9':5}


# Listen every frame
gl.data = gl.my_receiver.get_data()


if isinstance(gl.data, list):
    if "/blender/x" in gl.data:
        gl.x = gl.data[2]
    if "/blender/y" in gl.data:
        gl.y = gl.data[2]

if isinstance(gl.data, str):
    if gl.text != gl.data:
        gl.text_change = True
        gl.text = gl.data
        #gl.text.encode("utf-8").decode("latin-1")
        #print(gl.text)

# Move the Cube
controller = gl.getCurrentController()
owner = controller.owner
owner.localPosition = [0.3*gl.x, 0.3*gl.y, 0]

#
owner["Text"] = textwrap.fill(gl.text, 80)
# Bonne résolution au max
owner.resolution = 4

# Send
gl.my_sender.simple_send_to("/moi", 1, (gl.ip_out, gl.port_out))


################################### MUSIC
gl.frame_counter += 1
# If new message, reinit
if gl.text_change:
    gl.position = -1
    gl.text_change = False

text = gl.text
# Every "every" frame, play note
# Plus le texte est long, plus je joue vite
every = 12
if len(text) < 30:
    every = 18
if 31 < len(text) < 100:
    every = 16
if 101 < len(text) < 200:
    every = 14
if 201 < len(text) < 300:
    every = 12
if 301 < len(text) < 400:
    every = 10
if 400 < len(text) < 800:
    every = 7
if 801 < len(text):
    every = 3

if gl.frame_counter % every == 0:
    if gl.position < len(text) -1:
        gl.position += 1
        if text[gl.position] in list(note_dict.keys()):
            note = str(note_dict[text[gl.position]])
            gl.note_piano[note].play()
            # le volume varie en fonction de la longueur du texte
            n = min(len(text), 500)
            vol = 0.4 + 0.5 * n/500
            gl.note_piano[note].set_volume(vol)
            #print("gl.position", gl.position, "note", note)
