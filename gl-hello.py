#!/usr/bin/env python
"""
Testing OpenGL in a GTK Window.

This is quite long to startup, though.
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

def draw_line(from_x, from_y, to_x, to_y):
    glBegin(GL_LINES)
    glVertex2f(from_x, from_y) 
    glVertex2f(to_x, to_y) 
    glEnd()
    

class SimpleDrawingArea(gtk.DrawingArea, gtk.gtkgl.Widget):
    """
    OpenGL drawing area for simple demo.
    
    OpenGL-capable gtk.DrawingArea by subclassing
    gtk.gtkgl.Widget mixin.
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

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        glOrtho(-4.0, 4.0, -3.0, 3.0, -1.0, 1.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glEnable(GL_TEXTURE_RECTANGLE_ARB) # 2D)
        glEnable(GL_BLEND)
        glShadeModel(GL_SMOOTH)
        glClearColor(0.0, 0.0, 0.0, 1.0) # black background
        glColor4f(1.0, 1.0, 1.0, 1.0) # default color is white
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # OpenGL end
        gldrawable.gl_end()

    def _on_configure_event(self, *args):
        # Obtain a reference to the OpenGL drawable
        # and rendering context.
        gldrawable = self.get_gl_drawable()
        glcontext = self.get_gl_context()
        if gldrawable is None:
            return False
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
        if gldrawable is None:
            return False
        # OpenGL begin
        if not gldrawable.gl_begin(glcontext):
            return False
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        self.draw()

        # DONE
        if gldrawable.is_double_buffered():
            gldrawable.swap_buffers()
        else:
            glFlush()
        # OpenGL end
        gldrawable.gl_end()
        return False

    def draw(self):
        # DRAW STUFF HERE
        glColor4f(1.0, 0.8, 0.2, 1.0)
        draw_square()

        glColor4f(1.0, 1.0, 0.0, 0.8)
        for x in [4, 3.5, 3, 2.5, 2, 1.5, 1, 0.5,  0, -0.5, -1, -1.5, -2, -2.5, -3, -3.5, -4]:
            draw_line(float(x), -4.0, float(x), 4.0)
            draw_line(-4.0, float(x), 4.0, float(x))

class SimpleApp(object):
    """
    Simple demo application.
    """
    def __init__(self):
        self.is_fullscreen = False
        self.verbose = True
        self.window = gtk.Window()
        self.window.set_title('Testing OpenGL')
        self.window.set_reallocate_redraws(True)
        self.window.connect('delete_event', self.on_delete_event)
        self.window.connect("key-press-event", self.on_key_pressed)
        self.window.connect("window-state-event", self.on_window_state_event)

        # VBox to hold everything.
        vbox = gtk.VBox()
        self.window.add(vbox)
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
        # Drawing Area
        self.drawing_area = SimpleDrawingArea(glconfig)
        self.drawing_area.set_size_request(WIDTH, HEIGHT)
        vbox.pack_start(self.drawing_area)

        # A quit button.
        button = gtk.Button('Quit')
        button.connect('clicked', self.on_quit_clicked)
        vbox.pack_start(button, expand=False)
        
        self.drawing_area.show()
        button.show()
        vbox.show()
        self.window.show()
        #self.window.show_all()

    def on_delete_event(self, widget, event=None):
        gtk.main_quit()

    def on_quit_clicked(self, widget, event=None):
        gtk.main_quit()
        
    def on_key_pressed(self, widget, event):
        name = gtk.gdk.keyval_name(event.keyval)
        if name == "Escape":
            self.toggle_fullscreen()
        return True

    def toggle_fullscreen(self):
        if self.is_fullscreen:
            self.window.unfullscreen()
            self._showhideWidgets(self.drawing_area, False)
        else:
            self.window.fullscreen()
            self._showhideWidgets(self.drawing_area, True)

    def on_window_state_event(self, widget, event):
        #print 'window state event', event.type, event.changed_mask, 
        #print event.new_window_state
        if event.new_window_state == gtk.gdk.WINDOW_STATE_FULLSCREEN:
            if self.verbose:
                print('fullscreen on')
            self.is_fullscreen = True
        elif event.new_window_state == 0: #gtk.gdk.WINDOW_STATE_WITHDRAWN:
            if self.verbose:
                print('fullscreen off')
            self.is_fullscreen = False
        return True
    
    def _showhideWidgets(self, widget, hide=True):
        """
        Show or hide all widgets in the window except the given
        widget. Used for going fullscreen: in fullscreen, you only
        want the clutter embed widget and the menu bar etc.
        """
        parent = widget.get_parent()

        for c in parent.get_children():
            if c != widget:
                #print "toggle %s visibility %s" % (c, hide)
                if hide:
                    c.hide()
                else:
                    c.show()
        if parent == self.window:
            return
        self._showhideWidgets(parent, hide)

if __name__ == '__main__':
    app = SimpleApp()
    gtk.main()
