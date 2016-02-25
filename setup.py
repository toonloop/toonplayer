#!/usr/bin/env python
from distutils.core import setup
from toonplayer import __version__


setup(
    name="toonplayer",
    version=__version__,
    description="The Toonplayer Looping Video Player",
    author="Alexandre Quessy",
    author_email="alexandre@quessy.net",
    url="http://www.toonloop.com",
    packages=["toonplayer"],
    scripts=["scripts/toonplayer"]
    )
