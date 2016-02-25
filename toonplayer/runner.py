#!/usr/bin/env python
"""
Main entry point of the application.
"""

import os
import sys
import optparse
from twisted.internet import gtk2reactor
gtk2reactor.install() # has to be done before importing reactor and gtk
from twisted.internet import reactor
import gobject
from toonplayer import gui
from toonplayer import __version__


DEFAULT_DIRECTORY = "~/Documents/toonplayer"


def run():
    parser = optparse.OptionParser(usage="%prog [directory name]",
            version=str(__version__))
    (options, args) = parser.parse_args()
    app = gui.PlayerApp()
    dir_path = None
    if len(args) >= 1:
        dir_path = args[0]
    else:
        check_dir = os.path.expanduser(DEFAULT_DIRECTORY)
        if os.path.exists(check_dir) and os.path.isdir(check_dir):
            dir_path = check_dir
    vj = gui.VeeJay(app.player, dir_path)
    try:
        vj.load_clip_list()
    except RuntimeError, e:
        print(str(e))
        sys.exit(1)
    vj.choose_next()
    app.window.show_all()
    reactor.run()
