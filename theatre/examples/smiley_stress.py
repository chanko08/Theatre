import theatre
import random
import pyglet
import pyglet.window.key as key
pyglet.resource.path = ['resources']
pyglet.resource.reindex()
smiley_img = pyglet.resource.image('smiley.gif')

class Sprite(object):
    def __init__(self):
        self.sprite = None

    def add_sprite(self, image):
        self.sprite = pyglet.sprite.Sprite(image)

class Velocity(object):
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

class Smiley(theatre.Entity):
    batch = pyglet.graphics.Batch()

    def __init__(self, scene):
        super(Smiley, self).__init__(scene)
        self.add_components([Sprite, Velocity])
        self.sprite.add_sprite(smiley_img)

        self.sprite.sprite.x = random.randint(0, 640 - self.sprite.sprite.width)
        self.sprite.sprite.y = random.randint(0, 480 - self.sprite.sprite.height)
        self.sprite.sprite.batch = self.batch
        self.velocity.x = random.randint(-100, 100)
        self.velocity.y = random.randint(-100, 100)



class SmileyRenderer(theatre.Renderer):
    def on_draw(self):
        e = next(self.scene.get())
        e.batch.draw()

class MoveSystem(theatre.System):
    def on_update(self, dt):
        for e in self.scene.get():
            e.sprite.sprite.x += dt * e.velocity.x
            e.sprite.sprite.y += dt * e.velocity.y

class CollisionSystem(theatre.System):
    def on_update(self, dt):
        for e in self.scene.get():
            x,y = e.sprite.sprite.x, e.sprite.sprite.y
            w,h = e.sprite.sprite.width, e.sprite.sprite.height
            dx,dy = e.velocity.x, e.velocity.y

            if x < 0:
                x = 0
                dx *= -1
            elif x + w > 640:
                x = 640 - w
                dx *= -1

            if y < 0:
                y = 0
                dy *= -1
            elif y + h > 480:
                y = 480 - h
                dy *= -1

            e.sprite.sprite.x = x
            e.sprite.sprite.y = y
            e.velocity.x = dx
            e.velocity.y = dy

class SmileyKeyControl(theatre.KeyControl):
    @theatre.KeyControl.key_press(key.SPACE)
    def add_more(self):
        for i in range(10):
            e = Smiley(self.scene)
            self.scene.add_entity(e)

    @theatre.KeyControl.key_press(key.LCTRL)
    def count(self):
        print len(self.scene._entities)


    @theatre.KeyControl.key_press(key.LSHIFT)
    def fps(self):
        print pyglet.clock.get_fps()

class SmileyScene(theatre.Scene):
    def __init__(self, manager):
        super(SmileyScene, self).__init__(manager)
        self.add_entity(Smiley(self))

        systems = [SmileyRenderer, MoveSystem, CollisionSystem, SmileyKeyControl]
        for s in systems:
            self.add_system(s(self))

if __name__ == '__main__':
    window = pyglet.window.Window(640, 480)
    world = theatre.PygletManager(window, SmileyScene)
    pyglet.app.run()
