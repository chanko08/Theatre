class Scene(object):
    def __init__(self, manager):
        """
            Initialize the scene so that systems can tie their events to the
            scene.
        """
        self.manager = manager
        self._event_callback = {}
        self._entities = []

    

    def entity(self, components=None, groups=None):
        """
            Creates an entity based on the list of component classes passed in
            and the group identifiers passed in.

            Returns an initialized Entity object
        """
        raise NotImplementedError()


    def system(self, system):
        """
            Takes a class or object as an input.
            If the input is a class then the object is initialized and placed in
            the systems dictionary with its given name

            If the input is an object, the object is placed in the systems dictionary
            with its given name

            Either way, the object is then inspected to see what events it is bound to.
        """
        raise NotImplementedError()


    def get(self, *components):
        """
            Returns an iterator for searching entities. If arguments
            are given it passes these to the iterator for processing
            of the list of entities.
        """
        raise NotImplementedError()


    def bind(self, event, callback):
        """
            Bind a given function to a given event in the scene
        """
        if event not in self._event_callback:
            self._event_callback[event] = []

        self._event_callback[event].append(callback)


    def broadcast(self, event, *args, **kwargs):
        """
            Have the scene alert all systems that are listening to the
            given event that the event occurred with the given arguments

            Systems can call this to help communicate with one another if 
            they do not like the normal way.
        """
        if event not in self._event_callback:
            return

        for callback in self._event_callback[event]:
            callback(*args, **kwargs)


class EntityIterator(object):
    """
        The EntityIterator is an iterator designed to allow
        users to filter what entities they recieve.
    """

    def __init__(self, entities):
        raise NotImplementedError()

    def contains(self, *andables):
        """
            Ensure that all entities that are returned from the iterator
            have these components.
        """
        raise NotImplementedError()

    def has_one_of(self, *someables):
        """
            Ensure that all entities that are returned from the iterator
            have at least one of these components
        """
        raise NotImplementedError()

    def excludes(self, *excludables):
        """
            Ensure that all entities that are returned from the iterator
            do not have any of these components
        """
        raise NotImplementedError()        

    def is_member_of(self, *groups):
        """
            Ensure that all entities that are returned from the iterator
            are a member of the given group identifiers.
        """
        raise NotImplementedError()

    def __iter__(self):
        """
            Returns itself as an iterator
        """
        raise NotImplementedError()

    def next(self):
        """
            Goes through all entities and returns only the ones that
            match the parameters specified by the user.
        """
        raise NotImplementedError()
