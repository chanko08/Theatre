import unittest
from theatre import Manager, Scene

class TestScene(Scene):
    def broadcast(self, ev, *args, **kwargs):
        self.ev_called = ev
        self.args = args
        self.kwargs = kwargs

class ManagerTest(unittest.TestCase):
    def test_constructor(self):
        m = Manager(2)
        self.assertEquals(m.current_scene, 2)

        m = Manager(Scene)
        self.assertTrue(isinstance(m.current_scene, Scene))

    def test_broadcast(self):
        m = Manager(TestScene)

        m.broadcast("test", 1, 2, test='this is test')

        self.assertEquals(m.current_scene.ev_called, "test")
        self.assertEquals(m.current_scene.args, (1,2))
        self.assertEquals(m.current_scene.kwargs, {'test':'this is test'})

if __name__ == '__main__':
    unittest.main()