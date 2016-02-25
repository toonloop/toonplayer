#!/usr/bin/env python
"""
Main GUI for this application.
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
    parser.add_option("-n", "--times-each-played", type="int",
            help="How many times to play each clip.", default=2)
    parser.add_option("-d", "--clips-directory", type="string",
            help="Specifies the to directory to look in for clips to play. You can also simply specify the directory as the first argument. The default directory is %s if it exists, or the current working directory.")
    parser.add_option("-v", "--verbose", action="store_true",
            help="Enables verbose output.")
    parser.add_option("-f", "--fullscreen", action="store_true",
            help="Enables a fullscreen view.")
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
    
    app = gui.PlayerApp(fullscreen=options.fullscreen)
    vj = gui.VeeJay(app.player, dir_path=dir_path,
            times_play_each=options.times_each_played,
            verbose=options.verbose)
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
