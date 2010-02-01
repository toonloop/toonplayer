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
__version__ = "0.1.2"

import os
import sys
import optparse
from twisted.internet import gtk2reactor
gtk2reactor.install() # has to be done before importing reactor and gtk
from twisted.internet import reactor

DEFAULT_DIRECTORY = "~/Documents/toonplayer"

def run():
    parser = optparse.OptionParser(usage="%prog [directory name]", version=str(__version__))
    parser.add_option("-n", "--times-each-played", type="int", help="How many times to play each clip.", default=2)
    parser.add_option("-d", "--clips-directory", type="string", help="Specifies the to directory to look in for clips to play. You can also simply specify the directory as the first argument. The default directory is %s if it exists, or the current working directory.")
    parser.add_option("-v", "--verbose", action="store_true", help="Enables verbose output.")
    (options, args) = parser.parse_args()
    dir_path = None
    if options.clips_directory:
        dir_path = options.clips_directory
    elif len(args) == 1: 
        dir_path = args[0]
    else:
        check_dir = os.path.expanduser(DEFAULT_DIRECTORY)
        if os.path.exists(check_dir) and os.path.isdir(check_dir):
            dir_path = check_dir
    
    from toonplay import gui
    app = gui.PlayerApp()
    vj = gui.VeeJay(app.player, dir_path=dir_path, times_play_each=options.times_each_played, verbose=options.verbose)
    try:
        vj.load_clip_list()
    except RuntimeError, e:
        print(str(e))
        sys.exit(1)
    vj.choose_next()
    app.window.show_all()
    try:
        reactor.run()
    except KeyboardInterrupt:
        pass
