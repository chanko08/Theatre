import pyglet
from pyglet.window import key
import theatre


class Label(object):
    def __init__(self):
        super(Label, self).__init__()
        self.label = pyglet.text.Label("Hello World")
        self.label.anchor_x = 'center'
        self.label.anchor_y = 'center'
        self.label.x = 640 / 2
        self.label.y = 480 / 2
        self.label.font_size = 40

        self.dx = 20

class LabelDraw(theatre.Renderer):
    def on_draw(self):
        for e in self.scene.get():
            e.label.label.draw()



class LabelMove(theatre.System):
    def on_update(self, dt):
        for e in self.scene.get():
            e.label.label.x += e.label.dx * dt
            


class LabelKey(theatre.KeyControl):
    @theatre.KeyControl.key_release(key.SPACE)
    @theatre.KeyControl.key_press(key.SPACE)
    def switch_directions(self):
        for e in self.scene.get():
            e['label'].dx *= -1



class HelloWorld(theatre.Scene):
    def __init__(self, manager):
        super(HelloWorld, self).__init__(manager)
        self.entity(components = [Label])
        
        self.add_system(LabelDraw(self))
        self.add_system(LabelMove(self))
        self.add_system(LabelKey(self))


if __name__ == '__main__':
    window = pyglet.window.Window(640, 480)
    world = theatre.PygletManager(window, HelloWorld)
    pyglet.app.run()