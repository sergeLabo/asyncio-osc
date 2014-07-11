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

from bge import logic as gl

# Listen every frame
gl.data = gl.my_receiver.get_data()

# Default position
x, y = 0, 0

if isinstance(gl.data, list):
    if "/blender/x" in gl.data:
        x = gl.data[2]
    if "/blender/y" in gl.data:
        y = gl.data[2]

if isinstance(gl.data, str):
    gl.text = u"always \n" + gl.data
    print(gl.text)

# Move the Cube
controller = gl.getCurrentController()
owner = controller.owner
owner.localPosition = [0.3*x, 0.3*y, 0]

#
owner["Text"] = gl.text
# Send
gl.my_sender.simple_send_to("/toto", 3.14, (gl.ip_out, gl.port_out))
