class Manager(object):
    """
        The Manager class is what passes information to scenes.
        Any events that are triggered are first given to the
        manager, which will then pass it to the corresponding
        scene.
        This layer makes it easier to switch scenes.
    """
    def __init__(self, scene):
        if isinstance(scene, type):
            self.current_scene = scene(self)
        else:
            self.current_scene = scene


    def broadcast(self, event, *args, **kwargs):
        """
            Passes a specific message along to the current scene running.
        """
        self.current_scene.broadcast(event, *args, **kwargs)

