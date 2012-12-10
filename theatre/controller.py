class Controller(object):
    def __init__(self, scene):
        """
            A simple Controller.
            Does not bind itself to any events.
        """

        self.scene = scene

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
        self.scene.bind("draw", self.on_draw)

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
        self.scene.bind("update", self.on_update)

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
        to inherit this class.
    """
 
    _key_press_bind   = "_theatre_key_press_binding"
    _key_release_bind = "_theatre_key_release_binding"

    def __init__(self, scene):
        super(KeyControl, self).__init__(scene)


        self.key_press_bindings   = {}
        self.key_release_bindings = {}

        self._binder(self._key_press_bind, self.key_press_bindings)
        self._binder(self._key_release_bind, self.key_release_bindings)

        self.scene.bind("keypress", self._on_key_press)
        self.scene.bind("keyrelease", self._on_key_release)
    


    def on_key_press(self, symbol, modifiers):
        """
            An overloadable function for key press events
        """
        pass

    def on_key_release(self, symbol, modifiers):
        """
            An overloadable function for key release events
        """
        pass
    
    @classmethod
    def key_press(cls, symbol, modifiers = None):
        """
            A decorator to bind a key with modifiers to a key press method
        """
        def bind(f):
            if not hasattr(f, cls._key_press_bind):
                f._theatre_key_press_binding = []
            f._theatre_key_press_binding.append( (symbol, modifiers) )
            return f
        return bind

    @classmethod
    def key_release(cls, symbol, modifiers = None):
        """
            A decorator to bind a key with modifiers to a key release method
        """
        def bind(f):
            if not hasattr(f, cls._key_release_bind):
                f._theatre_key_release_binding = []
            f._theatre_key_release_binding.append( (symbol, modifiers) )
            return f
        return bind

    def bind_key_press(self, method, key, modifiers):
        """
            Allows dynamic binding to a key with modifiers for a key press event
        """
        if key not in self.key_press_bindings:
            self.key_press_bindings[key] = []
        self.key_press_bindings[key].append( (modifiers, method) )

    def bind_key_release(self, method, key, modifiers):
        """
            Allows dynamic binding to a key with modifiers for a key release event
        """
        if key not in self.key_release_bindings:
            self.key_release_bindings[key] = []
        self.key_release_bindings[key].append( (modifiers, method) )



    def _binder(self, list_type, keydict):
        """
            Binds all members of this object that have the attribute
            'list_type' into the corresponding 'keydict'.
        """
        for name in self.__class__.__dict__:
            member = getattr(self, name)
            if not hasattr(member, list_type):
                continue
            
            for key, mod in getattr(member, list_type):
                if key not in keydict:
                    keydict[key] = []
                keydict[key].append( (mod, member) )

    def _on_key_press(self, symbol, modifiers):
        """
            The method that gets called on key press which
            then propagates that event accordingly to all
            necessary functions.
        """
        self.on_key_press(symbol, modifiers)
        if symbol in self.key_press_bindings:
            for mod, func in self.key_press_bindings[symbol]:
                if mod is None or modifiers & mod:
                    func()

        

    def _on_key_release(self, symbol, modifiers):
        """
            The method that gets called on key release which
            then propagates that event accordingly to all
            necessary functions.
        """
        self.on_key_release(symbol, modifiers)
        if symbol in self.key_release_bindings:
            for mod, func in self.key_release_bindings[symbol]:
                if mod is None or modifiers & mod:
                    func()

        

    
