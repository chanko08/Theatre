class Controller(object):
    def __init__(self, scene):
        """
            A simple Controller.
            Does not bind itself to any events.
        """
        
        self.scene = scene
        return NotImplementedError()

class Renderer(Controller):
    """
        A Render Controller.
        Binds itself to draw events with the 'on_draw'
        method.
        Controllers that need the draw event are expected
        to inherit this class.
    """

    def __init__(self, scene):
        
        super(Renderer, self).__init__(scene)
        return NotImplementedError()

    def on_draw(self):
        return NotImplementedError()


class System(Controller):
    """
        A System Controller.
        Binds itself to the update events with the 'on_update'
        method.
        Controllers that need the update event are expected
        to inherit this class.
    """

    def __init__(self, scene):
        
        super(System, self).__init__(scene)
        return NotImplementedError()

    def on_update(self, dt):
        return NotImplementedError()

class KeyControl(Controller):
    """
        A Key Controller.
        Binds itself to all 'on_key_press' and 'on_key_release'
        events, with the same names given to their respective methods.
        This also has an easier api to bind only certain keys to 
        events.
        Controllers that need keyboard event access are expected
        to inheriy this class.
    """

    def __init__(self, scene):
        super(KeyControl, self).__init__(scene)
        return NotImplementedError()

    def on_key_press(self, symbol, modifiers):
        return NotImplementedError()

    def on_key_release(self, symbol, modifiers):
        return NotImplementedError()

