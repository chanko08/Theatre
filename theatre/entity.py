class Entity(object):
    """
        The container that holds components.
        This class is designed to be usable without
        creating entity classes, but you are able to do that
        if you need extra functionality.
    """

    def __init__(self, scene, components=None, groups=None):
        """
            Creates an entity, attaches the given components to the entity,
            gives the entity the given group qualifiers.
        """
        self.scene = scene
        self._components = {}
        self._groups = []
        self._dead = False

        self.add_components(components)
        self.add_groups(groups)

    def add_components(self, components  = None):
        """
            Adds the list of components to the Entity.
            If they are classes then they are instantiated then attached to
            the entity.
            If they are objects than they are just attached as is.

            Components are attached according to their class names
        """
        if components is None:
            return

        for c in components:
            if isinstance(c, type):
                self._components[c.__name__.lower()] = c()
            else:
                self._components[c.__class__.__name__.lower()] = c

    def add_groups(self, groups = None):
        """
            Adds the list of groups to the entity.
        """
        if groups is None:
            return
        self._groups.extend(groups)

    def __getitem__(self, key):
        """
            Allows easy access to components via
                entity['all lower case component class name']
        """
        return self._components[key]

    def __getattr__(self, name):
        """
            If there is no attribute attached to the entity with this
            name, then check if any component has this name, and access it.
            This specifically will work for component class names in all lowercase.
        """
        if name in self._components:
            return self._components[name]
        raise AttributeError("Couldn't find component with name:{0}".format(name))

    def member_of(self, group):
        """
            A test of whether the entity holds a given group identifier
        """
        return group in self._groups

    def delete(self):
        """
            Marks the entity for deletion for the scene.
            If an entity needs to clean anything up prior to deletion
            it is recommended to overload this method, and in the overloaded
            method to call the Entity version of the method via super
        """
        self._dead = True