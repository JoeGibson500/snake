import random
from tkinter import *

GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 100
# size of individual cells
SPACE_SIZE = 50
BODY_PARTS = 10
SNAKE_COLOUR = "green"
FOOD_COLOUR = "red"
BACKGROUND_COLOUR = "black"

class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill = SNAKE_COLOUR, tag = "snake")
            self.squares.append(square)

class Food:
    def __init__(self):
        # generate a random coordinates 
        # multiply by space size to align with grid
        x = random.randint(0, int((GAME_WIDTH/SPACE_SIZE)-1) * SPACE_SIZE)
        y = random.randint(0, int((GAME_HEIGHT/SPACE_SIZE)-1) * SPACE_SIZE)

        self.coordinates = [x,y]

        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill = FOOD_COLOUR, tag ="food")
    
def next_turn(snake, food):
    
    x, y = snake.coordinates[0]

# this is confusing - the standard coordinates system for graphical programmes
# starts with the origin in the top left corner. The Y value increases as you move down the screen 
    
    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    # after updating the x coordinate change the 0th index (the head) to the new coordinates 
    snake.coordinates.insert(0, (x, y))

    # create a new rectangle representing the snakes head on the canvas
    square = canvas.create_rectangle(x, y , x + SPACE_SIZE, y+ SPACE_SIZE, fill = SNAKE_COLOUR)

    # update the list of squares representing the snake's body on the canvas
    snake.squares.insert(0, square)

    # if x == food.coordinates[0] and y == food.coordinates[1]:
    if (
    x >= food.coordinates[0] - SPACE_SIZE
    and x <= food.coordinates[0] + SPACE_SIZE
    and y >= food.coordinates[1] - SPACE_SIZE
    and y <= food.coordinates[1] + SPACE_SIZE
):
        global score 
        score += 1

        label.config(text = "Score:{}".format(score))

        canvas.delete("food")

        food = Food()

    else: # remove the last coordinates and corresponding square (tail) of the snake 
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    
    else:
        # params : after(delay, callback, *args)
        window.after(SPEED, next_turn, snake, food)


def change_direction(new_direction):
    
    # without the global function this function would create a new variable called direction
    # this isnt needed if you are not modifying the variable
    global direction

    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction

def check_collisions(snake):
    
    x, y = snake.coordinates[0]
    # check if snake is out of bounds 
    if x < 0 or x >= GAME_WIDTH:
        return True
    
    if y < 0 or y >= GAME_HEIGHT:
            return True
    
    # check if snake collides with itself
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
    
    return False

def game_over():
    
    global canvas

    canvas.delete(ALL)

    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2, font = ('consolas', 70), text = "GAME OVER!!", fill = "red", tag = "game")



window = Tk()
window.title("Snake game")

score = 0
direction = "down"

# create a label widget
label = Label(window, text = "Score:{}".format(score), font = ('consolas', 40 ))

# pack means it adjusts the size and placement of the label within the window according to its content and the specified font size.
label.pack()

# a canvas is an area for drawing graphics
canvas = Canvas(window, bg=BACKGROUND_COLOUR, height = GAME_HEIGHT, width = GAME_WIDTH)
canvas.pack()

# this will process any pending events and update the GUI
# ensures immediate reflection of changes made to the interface 
window.update()

# retrieve the height and width of window and screen
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
 
# calculate the x coordinates for placing the window at the centre of the screen
x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

# takes a string input specifying the size (widthxheight) and the position(+x+y)
window.geometry('%dx%d+%d+%d' % (window_width, window_height, x, y))


# think of the 'bind' function like it generates a signal when a certain event happens 
# In Python, lambda is a keyword that allows you to create small, anonymous functions.
# These functions are often used for short, one-time operations
# syntax=   lambda arguments: expression. So in this case, event is
window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))


snake = Snake()
food = Food()

next_turn(snake, food)

window.mainloop() 