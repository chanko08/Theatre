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
        return NotImplementedError()

    def add_components(self, components  = None):
        """
            Adds the list of components to the Entity.
            If they are classes then they are instantiated then attached to
            the entity.
            If they are objects than they are just attached as is.

            Components are attached according to their class names
        """
        return NotImplementedError()

    def add_groups(self, groups = None):
        """
            Adds the list of groups to the entity.
        """
        return NotImplementedError()