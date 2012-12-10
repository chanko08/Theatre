import pyglet
from manager import Manager

class PygletManager(Manager):
    def __init__(self, window, scene, fps=60):
        super(PygletManager, self).__init__(scene)
        self.window = window
        self._pyglet_event_handler = PygletManagerEventHandler(self, window, fps)
        self.window.push_handlers(self._pyglet_event_handler)



class PygletManagerEventHandler(object):
    def __init__(self, manager, window, fps):
        self.manager = manager
        self.window = window

        ev_handler = self._event_handler
        self.on_key_press   = ev_handler("keypress")
        self.on_key_release = ev_handler("keyrelease")

        self.on_mouse_press   = ev_handler("mousepress")
        self.on_mouse_release = ev_handler("mouserelease")
        self.on_mouse_motion  = ev_handler("mousemotion")
        self.on_mouse_drag    = ev_handler("mousedrag")
        self.on_mouse_enter   = ev_handler("mouseenter")
        self.on_mouse_leave   = ev_handler("mouseleave")
        self.on_mouse_scroll  = ev_handler("mousescroll")

        self.on_update = ev_handler("update")

        pyglet.clock.schedule_interval(self.on_update, 1.0/fps)


    def on_draw(self):
        self.window.clear()
        f = self._event_handler("draw")
        return f()


    def _event_handler(self, ev):
        return lambda *args, **kwargs: self.manager.broadcast(ev, *args, **kwargs)