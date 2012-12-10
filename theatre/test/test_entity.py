import unittest
from theatre import Entity

class EntityTest(unittest.TestCase):
    def test_constructor(self):
        e = Entity('scene')
        self.assertEquals(e.scene, 'scene')

    def test_add_groups(self):
        e = Entity('scene', groups = ['test'])
        self.assertTrue('test' in e._groups)

        e.add_groups(['test2'])
        self.assertTrue('test2' in e._groups)

    def test_add_components(self):
        e = Entity('scene', components = ['this is a component'])
        self.assertEquals(e.str, 'this is a component')

        self.assertEquals(e['str'], 'this is a component')

        e.add_components([12])
        self.assertEquals(e.int, 12)
        self.assertEquals(e['int'], 12)

        
if __name__ == '__main__':
    unittest.main()
