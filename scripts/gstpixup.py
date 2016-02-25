from twisted.internet import gtk2reactor
gtk2reactor.install()
from twisted.internet import reactor
import gst
import time
pipeline = gst.Pipeline('test_pipeline')
source = gst.element_factory_make('videotestsrc', 'source_1')
pixbuffer = gst.element_factory_make('gdkpixbufsink', 'snapshot')
pipeline.add(source, pixbuffer)
gst.element_link_many(source, pixbuffer)
bus = pipeline.get_bus()
bus.add_signal_watch()
def on_message(bus, message):
    print "bus,mess:", bus, message
    t = message.type
    if t == gst.MESSAGE_ELEMENT and message.structure.get_name() == 'pixbuf':
        pixbuf = message.structure['pixbuf']
        print "size:", pixbuf.get_width(), pixbuf.get_height()

bus.connect('message', on_message)
pipeline.set_state(gst.STATE_PLAYING)
def _later():
    pipeline.set_state(gst.STATE_NULL)
    reactor.stop()
    
reactor.callLater(1, _later)
reactor.run()
