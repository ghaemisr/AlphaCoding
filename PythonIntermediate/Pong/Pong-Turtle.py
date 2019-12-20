import turtle
import random
import math


class Paddle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 18
        self.going_up = False
        self.going_down = False
        self.turtle = turtle.Pen()
        self.turtle.shape("turtle")
        self.turtle.color("white")
        self.turtle.speed(0)
        self.turtle.penup()
        self.turtle.setposition(self.x, self.y)

    def update(self):
        # Update turtle position coordinate
        if self.going_up:
            self.y += self.speed
        elif self.going_down:
            self.y -= self.speed

        # Limit movement to screen size
        if self.y > screen_size[1]:
            self.y = screen_size[1]
        elif self.y < -screen_size[1]:
            self.y = -screen_size[1]

        self.turtle.goto(self.x, self.y)

    def up(self):
        self.going_up = True
        self.going_down = False

    def down(self):
        self.going_down = True
        self.going_up = False

    def clear_keys_up(self):
        self.going_up = False

    def clear_keys_down(self):
        self.going_down = False


class Ball:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.speed = 18
        self.dir = [random.choice([-self.speed, self.speed]),
                    random.randint(-self.speed, self.speed)]
        self.turtle = turtle.Pen()
        self.turtle.shape("circle")
        self.turtle.color("white")
        self.turtle.speed(1)
        self.turtle.penup()

    def update(self):
        global finished
        self.x += self.dir[0]
        self.y += self.dir[1]
        self.turtle.goto(self.x, self.y)
        if self.y > screen_size[1] or self.y < -screen_size[1]:
            self.dir[1] = -self.dir[1]

        if self.x > screen_size[0]:
            env.screen.bye()
            print("GAME OVER!! RIGHT WON")

        if self.y < -screen_size[0]:
            env.screen.bye()
            print("GAME OVER!! LEFT WON")

        if math.hypot(left_paddle.x - self.x, self.y - left_paddle.y) < 20:
            print("")
            self.dir[0] = -self.dir[0]

        if math.hypot(right_paddle.x - self.x, self.y - right_paddle.y) < 20:
            self.dir[0] = -self.dir[0]


def update_game():
    the_ball.update()
    left_paddle.update()
    right_paddle.update()
    env.screen.ontimer(update_game, 50)


finished = False
env = turtle.Pen()
env.hideturtle()
env.screen.bgcolor("black")
env.color("white")
screen_size = env.screen.screensize()
env.speed(0)
env.penup()
env.goto(-screen_size[0], -screen_size[1])
env.pendown()
env.forward(2 * screen_size[0])
env.left(90)
env.forward(2 * screen_size[1])
env.left(90)
env.forward(2 * screen_size[0])
env.left(90)
env.forward(2 * screen_size[1])

right_result = turtle.Pen()
right_result.color("White")
right_result.hideturtle()
right_result.penup()
right_result.goto(-screen_size[0], screen_size[1] + 20)
right_result.write("0")

left_result = turtle.Pen()
left_result.color("White")
left_result.hideturtle()
left_result.penup()
left_result.goto(screen_size[0], screen_size[1] + 20)
left_result.write("0")

right_paddle = Paddle(screen_size[0], 0)
right_paddle.turtle.left(180)
left_paddle = Paddle(-screen_size[0], 0)
the_ball = Ball()

env.screen.onkeypress(right_paddle.up, "Up")
env.screen.onkeypress(right_paddle.down, "Down")
env.screen.onkeypress(left_paddle.up, "w")
env.screen.onkeypress(left_paddle.down, "s")

env.screen.onkeyrelease(right_paddle.clear_keys_up, "Up")
env.screen.onkeyrelease(right_paddle.clear_keys_down, "Down")
env.screen.onkeyrelease(left_paddle.clear_keys_up, "w")
env.screen.onkeyrelease(left_paddle.clear_keys_down, "s")

update_game()
env.screen.listen()

turtle.done()