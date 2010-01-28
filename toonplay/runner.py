#!/usr/bin/env python
# -*- Mode: Python -*-
# vi:si:et:sw=4:sts=4:ts=4
#
# Toonloop clips player
#
# Copyright 2010 Alexandre Quessy
# http://www.toonloop.com
#
# Original idea by Alexandre Quessy
# http://alexandre.quessy.net
#
# Toonloop is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Toonloop is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the gnu general public license
# along with Toonloop.  If not, see <http://www.gnu.org/licenses/>.
#

"""
Main entry point of the application.
"""
__version__ = "0.1.0"

import os
import sys
import optparse
from twisted.internet import gtk2reactor
gtk2reactor.install() # has to be done before importing reactor and gtk
from twisted.internet import reactor
import gobject
from toonplay import gui

def run():
    parser = optparse.OptionParser(usage="%prog [directory name]", version=str(__version__))
    (options, args) = parser.parse_args()
    
    app = gui.PlayerApp()
    dir_path = None
    if len(args) >= 1:
        dir_path = args[0]
    
    vj = gui.VeeJay(app.player, dir_path)
    vj.load_clip_list()
    vj.choose_next()
    app.window.show_all()
    reactor.run()
