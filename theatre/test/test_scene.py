import unittest
from theatre import Scene

class System(object):
    result = 0
    def test(self,i):
        self.result = i

class TestEntity(object):
    pass

class ComponentTest(object):
    pass

class SceneTest(unittest.TestCase):
    def test_constructor(self):
        s = Scene("this is the manager")

        self.assertEquals(s.manager, "this is the manager")
        self.assertEquals(s._event_callback, {})
        self.assertEquals(s._entities, [])
        self.assertEquals(s._system_dict, {})

    def test_entity_retrieval(self):
        s = Scene(None)
        for i in range(10):
            s.entity()

        for i in range(20):
            s.entity(components = [ComponentTest])

        for i in range(30):
            s.entity(groups=['test'])

        self.assertEquals(len(list(s.get())), 60)
        self.assertEquals(len(list(s.get(ComponentTest))), 20)
        self.assertEquals(len(list(s.get().is_member_of('test'))), 30)

    def test_entity_creation(self):
        s = Scene(None)
        e = s.entity(components = None, groups = None)

        self.assertEquals(len(s._entities), 1)


        s.add_entity(TestEntity())
        self.assertEquals(len(s._entities), 2)

        e = s.entity(components = [ComponentTest])
        self.assertEquals(len(s._entities), 3)

        e = s.entity(components = [ComponentTest], groups = ['one', 'two'])
        self.assertEquals(len(s._entities), 4)

    def test_system_registration(self):
        s = Scene(None)

        s.add_system(System())
        self.assertEquals(len(s._system_dict), 1)

    def test_system_retrieval(self):
        s = Scene(None)
        sys = System()
        s.add_system(sys)

        self.assertTrue(s.get_system("System") is sys)


    def test_event_binding(self):
        s = Scene(None)
        sys = System()

        s.bind("test", sys.test)

        s.broadcast("test", 4)
        self.assertEquals(sys.result, 4)

        s.broadcast("test", "result")
        self.assertEquals(sys.result, "result")



if __name__ == '__main__':
    unittest.main()