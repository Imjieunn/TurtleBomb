# This example is not working in Spyder directly (F5 or Run)
# Please type '!python turtle_runaway.py' on IPython console in your Spyder.
import turtle, random

class RunawayGame:
    def __init__(self, canvas, runner, bomb, chaser, score=0, timer=200, playing=True, catch_radius=50):
        self.canvas = canvas
        self.runner = runner
        self.bomb = bomb
        self.chaser = chaser
        self.catch_radius2 = catch_radius**2

        # runner : you should meet runner! if you meet runner, you get 1 score
        self.runner.shape('turtle')
        self.runner.color('#FFCC00')
        self.runner.shapesize(2,2)
        self.runner.penup()
        
        # bomb : avoid! if you meet bomb, the game is over
        self.bomb.shape('circle')
        self.bomb.color('#663300')
        self.bomb.shapesize(3,3)
        self.bomb.penup()
        
        # chaser : user cntrol character
        self.chaser.shape('turtle')
        self.chaser.color('#99CC66')
        self.chaser.shapesize(2,2)
        self.chaser.penup()

        # final score drawer
        self.drawer = turtle.RawTurtle(canvas)
        self.drawer.hideturtle()
        self.drawer.penup()
        
        # timer & score drawer
        self.drawer2 = turtle.RawTurtle(canvas)
        self.drawer2.hideturtle()
        self.drawer2.penup()
        
        # score
        self.score = score

        # timer
        self.timer = timer
        
        # Whether the game is played or not
        self.playing = playing
        
    def is_catched(self):
        p = self.runner.pos()
        q = self.chaser.pos()
        dx, dy = p[0] - q[0], p[1] - q[1]
        return dx**2 + dy**2 < self.catch_radius2 # True/False
    
    def is_bombCatched(self):
        p = self.bomb.pos()
        q = self.chaser.pos()
        dx, dy = p[0] - q[0], p[1] - q[1]
        return dx**2 + dy**2 < self.catch_radius2 # True/False
    
    def start(self, init_dist=400, ai_timer_msec=100): 
        if self.playing == True:
            self.runner.setpos((-init_dist / 2, 0))
            self.runner.setheading(0)
            self.bomb.setpos((0, 0))
            self.bomb.setheading(90)
            self.chaser.setpos((+init_dist / 2, 0))
            self.chaser.setheading(180)
        
            self.ai_timer_msec = ai_timer_msec
            self.canvas.ontimer(self.step, self.ai_timer_msec)
        else:
            self.end

    def step(self): 
        if self.playing == True:
            self.runner.run_ai(self.chaser.pos(), self.chaser.heading())
            self.bomb.run_ai(self.chaser.pos(), self.chaser.heading())
            self.chaser.run_ai(self.runner.pos(), self.runner.heading())
        
            is_catched = self.is_catched()
            is_bombCatched = self.is_bombCatched()
        
            # game's boundary
            if self.runner.xcor() > 300 or self.runner.xcor() < -300:
                self.runner.right(180)
            if self.runner.ycor() > 300 or self.runner.ycor() < -300:
                self.runner.right(180)            
            if self.bomb.xcor() > 300 or self.bomb.xcor() < -300:
                self.bomb.right(180)
            if self.bomb.ycor() > 300 or self.bomb.ycor() < -300:
                self.bomb.right(180)       
            if self.chaser.xcor() > 300 or self.chaser.xcor() < -300:
                self.chaser.right(180)
            if self.chaser.ycor() > 300 or self.chaser.ycor() < -300:
                self.chaser.right(180)                   
                    
            if is_catched == True:
                self.score += 1
            
            # if you meet bomb, the game is over!
            if is_bombCatched == True:
                self.playing = False
                return self.end()
        
            self.timer -= 1
            
            # if the timer is less than zero, the game is over!
            if self.timer<=0:
                self.playing = False
                return self.end()
                
            self.drawer2.undo()
            self.drawer2.penup()
            self.drawer2.setpos(300, 300) # (가로, 세로)
            self.drawer2.write(f'score : {self.score}\ntimer : {self.timer//10}', font=("Arial", 10, "bold"))

            self.canvas.ontimer(self.step, self.ai_timer_msec)
        
    def end(self):
        if self.playing == False:
            # Remove existing screen
            self.canvas.clear()
            self.drawer.undo()
            self.drawer.penup()
            self.drawer.setpos(0, 0) # (가로, 세로)
            self.drawer.write(f'final score : {self.score}', align="center", font=("Arial", 30, "bold"))  
            
            input = self.canvas.textinput("AGAIN", "Do you want again?(Y/N) ")
            
            # Again Game
            if input == "Y":
                self.playing = True
                self.score = 0
                self.timer = 200
                self.canvas.clear()
                
                self.runner = RandomMover(canvas)
                self.bomb = BombMover(canvas)
                self.chaser = ManualMover(canvas)
                
                self.runner.shape('turtle')
                self.runner.color('blue')
                self.runner.shapesize(2,2)
                self.runner.penup()
                
                self.bomb.shape('circle')
                self.bomb.color('purple')
                self.bomb.shapesize(3,3)
                self.bomb.penup()
                
                self.chaser.shape('turtle')
                self.chaser.color('red')
                self.chaser.shapesize(2,2)
                self.chaser.penup()
                
                canvas.title("Turtle Runaway")
                canvas.bgcolor("#FFFFCC")
                
                return self.start()
                
class ManualMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=10, step_turn=10):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn

        # Register event handlers
        canvas.onkeypress(lambda: self.forward(self.step_move), 'Up')
        canvas.onkeypress(lambda: self.backward(self.step_move), 'Down')
        canvas.onkeypress(lambda: self.left(self.step_turn), 'Left')
        canvas.onkeypress(lambda: self.right(self.step_turn), 'Right')
        canvas.listen()

    def run_ai(self, opp_pos, opp_heading):
        pass

class RandomMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=20, step_turn=10):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn

    def run_ai(self, oop_pos, opp_heading):
        mode = random.randint(0, 2)
        if mode == 0:
            self.forward(self.step_move)
        elif mode == 1:
            self.left(self.step_turn)
        elif mode == 2:
            self.right(self.step_turn)
            
class BombMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=100, step_turn=10):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn

    def run_ai(self, opp_pos, opp_heading):
        mode = random.randint(0, 2)
        if mode == 0:
            self.forward(self.step_move)
        elif mode == 1:
            self.left(self.step_turn)
        elif mode == 2:
            self.right(self.step_turn)

if __name__ == '__main__':
        canvas = turtle.Screen()
        runner = RandomMover(canvas)
        bomb = BombMover(canvas)
        chaser = ManualMover(canvas)

        game = RunawayGame(canvas, runner, bomb, chaser)
        while game.playing == True:
            canvas.title("Turtle Runaway")
            canvas.bgcolor("#FFFFCC")
            
            game.start()
            canvas.mainloop()