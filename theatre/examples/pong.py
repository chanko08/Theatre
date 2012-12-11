import pyglet
import pyglet.gl as gl
import pyglet.window.key as key
import theatre

#basic settings
class Settings(object):
    width = 640
    height = 480
    dim = 640,480



class Position(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y



class Velocity(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y



class Dimension(object):
    def __init__(self, w=0, h=0):
        self.w = w
        self.h = h



class Score(object):
    def __init__(self, score = 0):
        self.score = score



class DrawScore(theatre.Renderer):
    def on_draw(self):
        for e in self.scene.get(Score, Position):
            l = pyglet.text.Label(text = str(e.score.score))
            l.x = e.position.x
            l.y = e.position.y
            l.font_size = 30
            l.anchor_x = 'center'
            l.anchor_y = 'top'
            l.draw()



class DrawRect(theatre.Renderer):
    def on_draw(self):
        gl.glBegin(gl.GL_QUADS)
        gl.glColor3f(1.0, 1.0, 1.0)
        for e in self.scene.get(Position, Dimension):
            x,y = e.position.x, e.position.y
            w,h = e.dimension.w, e.dimension.h

            gl.glVertex2f(x, y)
            gl.glVertex2f(x + w, y)
            gl.glVertex2f(x + w, y + h)
            gl.glVertex2f(x, y + h)
        gl.glEnd(gl.GL_QUADS)



class PlayerControl(theatre.KeyControl):
    
    @theatre.KeyControl.key_release(key.DOWN)
    @theatre.KeyControl.key_press(key.UP)
    def move_up(self):
        player = next(self.scene.get().is_member_of('player'))
        player.velocity.y += 150

    @theatre.KeyControl.key_release(key.UP)
    @theatre.KeyControl.key_press(key.DOWN)
    def move_down(self):
        player = next(self.scene.get().is_member_of('player'))
        player.velocity.y -= 150



class ComputerControl(theatre.System):
    def on_update(self, dt):
        ball = next(self.scene.get().is_member_of('ball'))
        computer = next(self.scene.get().is_member_of('computer'))

        if ball.position.y + ball.dimension.h < computer.position.y:
            computer.velocity.y = -150
        elif ball.position.y > computer.position.y + computer.dimension.h:
            computer.velocity.y = 150



class CollisionSystem(theatre.System):
    def on_update(self, dt):
        ball = next(self.scene.get().is_member_of('ball'))
        for e in self.scene.get(Position, Dimension).exclude_members_of('ball'):
            if self.collides(ball, e):
                if e.member_of('paddle'):
                    ball.velocity.x *= -1
                elif e.member_of('wall'):
                    ball.velocity.y *= -1

    def collides(self, ent1, ent2):
        a = [
            (ent1.position.x, ent1.position.y),
            (ent1.position.x + ent1.dimension.w, ent1.position.y + ent1.dimension.h)
        ]

        b = [
            (ent2.position.x, ent2.position.y),
            (ent2.position.x + ent2.dimension.w, ent2.position.y + ent2.dimension.h)
        ]

        tests = [
            a[0][0] < b[1][0],
            a[1][0] > b[0][0],
            a[0][1] < b[1][1],
            a[1][1] > b[0][1]
        ]
        
        return all(tests)



class MovementSystem(theatre.System):
    def on_update(self, dt):
        for e in self.scene.get(Position,Velocity):
            e.position.x += e.velocity.x * dt
            e.position.y += e.velocity.y * dt

            if e.member_of('ball'): continue
            if e.position.y + e.dimension.h > Settings.height:
                e.position.y = Settings.height - e.dimension.h
            elif e.position.y < 0:
                e.position.y = 0



class ScoreSystem(theatre.System):
    def on_update(self, dt):
        ball = next(self.scene.get().is_member_of('ball'))
        p = next(self.scene.get().is_member_of('player score'))
        c = next(self.scene.get().is_member_of('computer score'))
        if ball.position.x <= 0:
            #player scored
            self.scene.broadcast('reset', p.score.score + 1, c.score.score)

        elif Settings.width <= ball.position.x + ball.dimension.w:
            #computer scored
            self.scene.broadcast('reset', p.score.score, c.score.score + 1)


class ResetController(theatre.Controller):
    def __init__(self, scene):
        super(ResetController, self).__init__(scene)
        scene.bind('reset', self.on_reset)

    def on_reset(self, player_score, computer_score):
        player = next(self.scene.get().is_member_of('player'))
        player.position.x = 20
        player.position.y = 200
        player.dimension.w = 20
        player.dimension.h = 100
        player.velocity.x = 0
        player.velocity.y = 0

        computer = next(self.scene.get().is_member_of('computer'))
        computer.position.x = Settings.width - 40
        computer.position.y = 200
        computer.dimension.w = 20
        computer.dimension.h = 100
        computer.velocity.x = 0
        computer.velocity.y = 0

        ball = next(self.scene.get().is_member_of('ball'))
        ball.position.x = 300
        ball.position.y = 100
        ball.velocity.x = 100
        ball.velocity.y = 100
        ball.dimension.w = 20
        ball.dimension.h = 20

        s = next(self.scene.get().is_member_of('player score'))
        s.score.score = player_score

        s = next(self.scene.get().is_member_of('computer score'))
        s.score.score = computer_score



class Pong(theatre.Scene):
    def __init__(self, manager):
        super(Pong, self).__init__(manager)
        player = self.entity(components = [Position, Dimension, Velocity], groups = ['player', 'paddle'])
        

        computer = self.entity(components = [Position, Dimension, Velocity], groups = ['computer', 'paddle'])
        

        player_score = self.entity(components = [Score, Position], groups = ['score', 'player score'])
        player_score.position.x = 200
        player_score.position.y = 480 - 20

        computer_score = self.entity(components = [Score, Position], groups = ['score', 'computer score'])
        computer_score.position.x = 640 - 200
        computer_score.position.y = 480 - 20


        ball = self.entity(components = [Position, Dimension, Velocity], groups = ['ball'])
        

        top = self.entity(components = [Position, Dimension], groups = ['wall'])
        top.position.x = 0
        top.position.y = Settings.height
        top.dimension.h = 20
        top.dimension.w = Settings.width

        bottom = self.entity(components = [Position, Dimension], groups = ['wall'])
        bottom.position.x = 0
        bottom.position.y = -20
        bottom.dimension.h = 20
        bottom.dimension.w = Settings.width


        self.add_system(DrawRect(self))
        self.add_system(DrawScore(self))
        self.add_system(ResetController(self))
        self.add_system(ScoreSystem(self))
        self.add_system(CollisionSystem(self))
        self.add_system(ComputerControl(self))
        self.add_system(MovementSystem(self))
        self.add_system(PlayerControl(self))

        self.broadcast('reset', 0, 0)
        

        

if __name__ == '__main__':
    window = pyglet.window.Window(*Settings.dim)
    world = theatre.PygletManager(window, Pong)
    pyglet.app.run()
        