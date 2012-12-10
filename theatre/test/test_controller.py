import unittest
from theatre import Scene, Controller, Renderer, KeyControl, System

class ControllerTest(unittest.TestCase):
    def test_controller_registration(self):
        s = Scene(None)
        c = Controller(s)
        s.add_system(c)

        self.assertTrue(c.scene is s)

        self.assertTrue(c is s.get_system('Controller'))

    def test_system_events(self):
        s = Scene(None)
        class TestSystem(System):
            test = 0
            def on_update(self, dt):
                self.test = dt + 5

        sys = TestSystem(s)
        s.broadcast('update',5)

        self.assertEquals(sys.test, 10)

    def test_renderer_events(self):
        s = Scene(None)
        class TestRenderer(Renderer):
            test = 0
            def on_draw(self):
                self.test += 1

        sys = TestRenderer(s)
        s.broadcast('draw')

        self.assertEquals(sys.test, 1)

    def test_key_controller_events(self):
        s = Scene(None)
        class TestKey(KeyControl):
            def on_key_press(self, sym, mod):
                self.sym = sym
                self.mod = mod

            def on_key_release(self, sym, mod):
                self.sym = sym
                self.mod = mod


            @KeyControl.key_press(5)
            def test(self):
                self.sym = 'works'

        sys = TestKey(s)

        s.broadcast('keypress', 13, 0)
        self.assertEquals(sys.sym, 13)
        self.assertEquals(sys.mod, 0)

        s.broadcast('keyrelease', 1, 2)
        self.assertEquals(sys.sym, 1)
        self.assertEquals(sys.mod, 2)

        s.broadcast('keypress', 5, 0)
        self.assertEquals(sys.sym, 'works')



if __name__ == '__main__':
    unittest.main()
