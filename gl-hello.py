#!/usr/bin/env python
"""
Testing OpenGL in a GTK Window.
"""
import sys
import pygtk
pygtk.require('2.0')
import gtk
import gtk.gtkgl
from OpenGL.GL import *
from OpenGL.GLU import *

WIDTH = 640
HEIGHT = 480

def draw_square():
    """
    Draws a square of 2 x 2 size centered at 0, 0
    
    Make sure to call glDisable(GL_TEXTURE_RECTANGLE_ARB) first.
    """
    glBegin(GL_QUADS)
    glVertex2f(-1.0, -1.0) # Bottom Left of Quad
    glVertex2f(1.0, -1.0) # Bottom Right of Quad
    glVertex2f(1.0, 1.0) # Top Right Of Quad
    glVertex2f(-1.0, 1.0) # Top Left Of Quad
    glEnd()


# Create OpenGL-capable gtk.DrawingArea by subclassing
# gtk.gtkgl.Widget mixin.

class SimpleDrawingArea(gtk.DrawingArea, gtk.gtkgl.Widget):
    """
    OpenGL drawing area for simple demo.
    """
    def __init__(self, glconfig):
        gtk.DrawingArea.__init__(self)
        # Set OpenGL-capability to the drawing area
        self.set_gl_capability(glconfig)
        # Connect the relevant signals.
        self.connect_after('realize',   self._on_realize)
        self.connect('configure_event', self._on_configure_event)
        self.connect('expose_event',    self._on_expose_event)

    def _on_realize(self, *args):
        # Obtain a reference to the OpenGL drawable
        # and rendering context.
        gldrawable = self.get_gl_drawable()
        glcontext = self.get_gl_context()
        # OpenGL begin.
        if not gldrawable.gl_begin(glcontext):
            return

        glClearColor(0.0, 0.0, 0.0, 1.0)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        glOrtho(-4.0, 4.0, -3.0, 3.0, -1.0, 1.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        #glMatrixMode(GL_MODELVIEW)

        #TODO:
        #GL.glEnable(GL.GL_TEXTURE_RECTANGLE_ARB) # 2D)
        #GL.glEnable(GL.GL_BLEND)
        #GL.glShadeModel(GL.GL_SMOOTH)
        #GL.glClearColor(0.0, 0.0, 0.0, 0.0) # black background
        #GL.glColor4f(1.0, 1.0, 1.0, 1.0) # self.config.playback_opacity) # for now we use it for all
        #GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)

        # OpenGL end
        gldrawable.gl_end()

    def _on_configure_event(self, *args):
        # Obtain a reference to the OpenGL drawable
        # and rendering context.
        gldrawable = self.get_gl_drawable()
        glcontext = self.get_gl_context()
        # OpenGL begin
        if not gldrawable.gl_begin(glcontext):
            return False
        glViewport(0, 0, self.allocation.width, self.allocation.height)
        # OpenGL end
        gldrawable.gl_end()
        return False

    def _on_expose_event(self, *args):
        # Obtain a reference to the OpenGL drawable
        # and rendering context.
        gldrawable = self.get_gl_drawable()
        glcontext = self.get_gl_context()
        # OpenGL begin
        if not gldrawable.gl_begin(glcontext):
            return False
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        #glCallList(1)

        glColor4f(1.0, 0.8, 0.2, 1.0)
        draw_square()
        if gldrawable.is_double_buffered():
            gldrawable.swap_buffers()
        else:
            glFlush()
        # OpenGL end
        gldrawable.gl_end()
        return False


class SimpleDemo(gtk.Window):
    """Simple demo application."""

    def __init__(self):
        gtk.Window.__init__(self)
        self.set_title('Testing OpenGL')
        if sys.platform != 'win32':
            self.set_resize_mode(gtk.RESIZE_IMMEDIATE)
        self.set_reallocate_redraws(True)
        self.connect('delete_event', self.on_delete_event)

        # VBox to hold everything.
        vbox = gtk.VBox()
        self.add(vbox)
        # Query the OpenGL extension version.
        print "OpenGL extension version - %d.%d\n" % gtk.gdkgl.query_version()
        # Configure OpenGL framebuffer.
        # Try to get a double-buffered framebuffer configuration,
        # if not successful then try to get a single-buffered one.
        display_mode = (gtk.gdkgl.MODE_RGB    |
                        gtk.gdkgl.MODE_DEPTH  |
                        gtk.gdkgl.MODE_DOUBLE)
        try:
            glconfig = gtk.gdkgl.Config(mode=display_mode)
        except gtk.gdkgl.NoMatches:
            display_mode &= ~gtk.gdkgl.MODE_DOUBLE
            glconfig = gtk.gdkgl.Config(mode=display_mode)
        print "is RGBA:",                 glconfig.is_rgba()
        print "is double-buffered:",      glconfig.is_double_buffered()
        print "is stereo:",               glconfig.is_stereo()
        print "has alpha:",               glconfig.has_alpha()
        print "has depth buffer:",        glconfig.has_depth_buffer()
        print "has stencil buffer:",      glconfig.has_stencil_buffer()
        print "has accumulation buffer:", glconfig.has_accum_buffer()
        # SimpleDrawingArea
        drawing_area = SimpleDrawingArea(glconfig)
        drawing_area.set_size_request(WIDTH, HEIGHT)
        vbox.pack_start(drawing_area)

        # A quit button.
        button = gtk.Button('Quit')
        button.connect('clicked', gtk.main_quit)
        vbox.pack_start(button, expand=False)

    def on_delete_event(self, widget, event):
        gtk.main_quit()

if __name__ == '__main__':
    app = SimpleDemo()
    app.show_all()
    gtk.main()
