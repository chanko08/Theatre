from entity import Entity

class Scene(object):
    def __init__(self, manager):
        """
            Initialize the scene so that systems can tie their events to the
            scene.

        """
        super(Scene, self).__init__()
        self.manager = manager
        self._event_callback = {}
        self._entities = []
        self._system_dict = {}

        self.bind("update", self._clean_entities)


    def _clean_entities(self, dt):
        entity_list = []
        for e in self._entities:
            if not e._dead:
                entity_list.append(e)
        self._entities = entity_list


    

    def entity(self, components=None, groups=None):
        """
            Creates an entity based on the list of component classes passed in
            and the group identifiers passed in, and registers it with this
            scene.

            Returns an initialized Entity object
        """
        e = Entity(self, components, groups)
        return self.add_entity(e)
        

    def add_entity(self, entity):
        """
            Registers the given entity object with the scene
        """
        self._entities.append(entity)
        return entity


    def add_system(self, system):
        """
            The object is placed in the systems dictionary
            with its given name

            The object is then inspected to see what events it is bound to.

            Note: You do not need to add the system to the scene in order to bind
            systems to events in the scene.
        """
        self._system_dict[system.__class__.__name__] = system

    def get_system(self, system_name):
        """
            Access a system registered with the scene by its class
            name.
        """
        return self._system_dict[system_name]


    def get(self, *components):
        """
            Returns an iterator for searching entities. If arguments
            are given it passes these to the iterator for processing
            of the list of entities.
        """
        it = EntityIterator(self._entities)
        it.contains(*components)
        return it


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
        self.entities = iter(entities)

        self.andables    = set()
        self.someables   = set()
        self.excludables = set()
        self.groups      = set()
        self.excludable_groups = set()

    def contains(self, *andables):
        """
            Ensure that all entities that are returned from the iterator
            have these components.
        """
        self.andables.update(self._class_names(andables))
        return self

    def has_one_of(self, *someables):
        """
            Ensure that all entities that are returned from the iterator
            have at least one of these components
        """
        self.someables.update(self._class_names(someables))
        return self

    def excludes(self, *excludables):
        """
            Ensure that all entities that are returned from the iterator
            do not have any of these components
        """
        self.excludables.update(self._class_names(excludables))
        return self

    def is_member_of(self, *groups):
        """
            Ensure that all entities that are returned from the iterator
            are a member of any of the given group identifiers.
        """
        self.groups.update(groups)
        return self

    def exclude_members_of(self, *groups):
        self.excludable_groups.update(groups)
        return self

    def first(self):
        """
            Returns the first match for this iterator.
        """
        return next(self)

    def __iter__(self):
        """
            Returns itself as an iterator
        """
        return self

    def next(self):
        """
            Goes through all entities and returns only the ones that
            match the parameters specified by the user.
        """
        for e in self.entities:
            components = e._components.keys()
            groups = e._groups
            if self.andables and not self.andables.issubset(components):
                continue

            if self.someables and not self.someables.intersection(components):
                continue

            if self.excludables and self.excludables.intersection(components):
                continue

            if self.groups and not self.groups.intersection(groups):
                continue

            if self.excludable_groups and self.excludable_groups.intersection(groups):
                continue

            return e
        raise StopIteration
    
    def _class_names(self, classes):
        """
            A helper method for getting all component names
        """
        return [c.__name__.lower() for c in classes]
