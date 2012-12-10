import pyglet
import theatre

class HelloWorld(theatre.Scene):
    def __init_(self):
        super(theatre.Scene).__init__()


if __name__ == '__main__':
    window = pyglet.window.Window()
    world = theatre.PygletManager(window, HelloWorld)
    pyglet.app.run()