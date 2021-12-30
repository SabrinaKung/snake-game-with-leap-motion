import sys
import os
import math
sys.path.append(os.getcwd()+"/lib")
import Leap
import thread
import time
import random

import pygame
from pygame.locals import *
from collections import deque

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
SIZE = 25


def print_text(screen, font, x, y, text, fcolor=(255, 255, 255)):
    imgText = font.render(text, True, fcolor)
    screen.blit(imgText, (x, y))

class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']

    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

    def on_disconnect(self, controller):
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        pass
        # frame = controller.frame()

        # for gesture in frame.gestures():
        #     if gesture.type is Leap.Gesture.TYPE_SWIPE:

        #         swipe = Leap.SwipeGesture(gesture)
        #         direction = swipe.direction
        #         isHorizontal = abs(direction[0]) > abs(direction[1])
                
        #         if isHorizontal:
        #             if direction[0] < 0:
        #                 print "left"
        #                 hello = 1
        #             else:
        #                 hello = 1
        #                 print "right"
        #             print "------------"
        #         else:
        #             if direction[1] > 0:
        #                 print "up"
        #             else:
        #                 print "down"
        #             print "------------"



def main():
    listener = SampleListener()
    controller = Leap.Controller()

    controller.add_listener(listener)

    # controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE)
    controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)
    # controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP)
    # controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP)

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    pygame.display.set_caption("Snake")

    light = (100, 100, 100)  # color of snake
    dark = (200, 200, 200)  # color of food
    body = (250, 250, 250)
    pink= (255, 204, 229)

    INIT = 0
    elapsed = 5 #red dot elapsed time
    font1 = pygame.font.SysFont("SimHei", 24)  # font of score
    font2 = pygame.font.Font(None, 72)  # GAME OVER font
    red = (200, 30, 30)  # color of GAME OVER
    fwidth, fheight = font2.size("GAME OVER")
    line_width = 5  # width of gridline
    black = (0, 0, 0)  # color of gridline
    bgcolor = (89, 152, 26)  # background color

    # position, start from right
    pos_x = 1
    pos_y = 0
    # If the snake is moving to the right, then quickly click down to the left,
    # because the program refresh is not so fast, the downward event will be overwritten to the left,
    # causing the snake to retreat and go directly to GAME OVER.
    # The b variable is used to prevent this from happening
    b = True
    # scope
    scope_x = (0, SCREEN_WIDTH // SIZE - 1)
    scope_y = (2, SCREEN_HEIGHT // SIZE - 1)
    # snake
    global snake
    snake = deque()
    # food
    global food_x
    food_x = 0
    global food_y
    food_y = 0

    # initialize the snake
    def _init_snake():
        global snake
        snake.clear()
        snake.append((4, scope_y[0]))
        snake.append((3, scope_y[0]))
        snake.append((2, scope_y[0]))
        snake.append((1, scope_y[0]))
        snake.append((0, scope_y[0]))

    # create food (pink)
    def _create_food():
        global food_x, food_y
        food_x = random.randint(scope_x[0], scope_x[1])
        food_y = random.randint(scope_y[0], scope_y[1])
        while (food_x, food_y) in snake:
            # in order to prevent food out on snake
            food_x = random.randint(scope_x[0], scope_x[1])
            food_y = random.randint(scope_y[0], scope_y[1])
            
    # create random food (red)
    def _create_bonus():
        global bonus_x, bonus_y
        bonus_x = random.randint(scope_x[0], scope_x[1])
        bonus_y = random.randint(scope_y[0], scope_y[1])
        while (bonus_x, bonus_y) in snake:
            # in order to prevent food out on snake
            bonus_x = random.randint(scope_x[0], scope_x[1])
            bonus_y = random.randint(scope_y[0], scope_y[1])
        
    _init_snake()
    _create_food()
    _create_bonus()
    
    game_over = True
    start = False  # when both start = True && game_over = True, display GAME OVER
    score = 0  # score
    orispeed = 0.2  # original speed
    speed = orispeed
    last_move_time = None
    pause = False  # pauses
    
    while True:
        # leap motion gesture controller
        frame = controller.frame()
        for gesture in frame.gestures():
            if gesture.type is Leap.Gesture.TYPE_SWIPE:
                swipe = Leap.SwipeGesture(gesture)
                direction = swipe.direction
                isHorizontal = abs(direction[0]) > abs(direction[1])
                if isHorizontal:
                    if direction[0] < 0:
                        print "left"
                        if b and not pos_x:
                            pos_x = -1
                            pos_y = 0
                            b = False
                    else:
                        print "right"
                        if b and not pos_x:
                            pos_x = 1
                            pos_y = 0
                            b = False
                    print "------------"
                else:
                    if direction[1] > 0:
                        print "up"
                        if b and not pos_y:
                            pos_x = 0
                            pos_y = -1
                            b = False
                    else:
                        print "down"
                        if b and not pos_y:
                            pos_x = 0
                            pos_y = 1
                            b = False
                    print "------------"

        # Keyboard controller
        for event in pygame.event.get():
            if event.type == QUIT:
                controller.remove_listener(listener)
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    if game_over:
                        start = True
                        game_over = False
                        b = True
                        _init_snake()
                        _create_food()
                        _create_bonus()
                        pos_x = 1
                        pos_y = 0
                        # get score
                        score = 0
                        last_move_time = time.time()
                elif event.key == K_SPACE:
                    if not game_over:
                        pause = not pause
                # elif event.key in (K_w, K_UP):
                #     # In order to prevent pressing down button when snake move,
                #     # and directly lead to GAME OVER
                #     if b and not pos_y:
                #         pos_x = 0
                #         pos_y = -1
                #         b = False
                # elif event.key in (K_s, K_DOWN):
                #     if b and not pos_y:
                #         pos_x = 0
                #         pos_y = 1
                #         b = False
                # elif event.key in (K_a, K_LEFT):
                #     if b and not pos_x:
                #         pos_x = -1
                #         pos_y = 0
                #         b = False
                # elif event.key in (K_d, K_RIGHT):
                #     if b and not pos_x:
                #         pos_x = 1
                #         pos_y = 0
                #         b = False

        # fill the background color

        bgImage = pygame.image.load("./greenBackground.jpeg")
        screen.fill(bgcolor)
        screen.blit(bgImage, (0, 0))

        # column gridline
        #for x in range(SIZE, SCREEN_WIDTH, SIZE):
            #pygame.draw.line(screen, black, (x, scope_y[0] * SIZE), (x, SCREEN_HEIGHT), line_width)
        # row gridline
        #for y in range(scope_y[0] * SIZE, SCREEN_HEIGHT, SIZE):
            #pygame.draw.line(screen, black, (0, y), (SCREEN_WIDTH, y), line_width)
        pygame.draw.line(screen, black, (3, scope_y[0]+(SCREEN_HEIGHT//SIZE)*2), (3, scope_y[0]+SCREEN_HEIGHT), line_width)#left-col
        pygame.draw.line(screen, black, (0, scope_y[0]+(SCREEN_HEIGHT//SIZE)*2), (SCREEN_WIDTH, (SCREEN_HEIGHT//SIZE)*2), line_width)#up-row
        pygame.draw.line(screen, black, (0, SCREEN_HEIGHT-3), (SCREEN_WIDTH, SCREEN_HEIGHT-3), line_width)#down-row
        pygame.draw.line(screen, black, (SCREEN_WIDTH-3, scope_y[0]+(SCREEN_HEIGHT//SIZE)*2), (SCREEN_WIDTH-3, SCREEN_HEIGHT), line_width)#right-row
           
        if game_over:
            if start:
                print_text(
                    screen,
                    font2,
                    (SCREEN_WIDTH - fwidth) // 2,
                    (SCREEN_HEIGHT - fheight) // 2,
                    "GAME OVER",
                    red,
                )

        else:
            curTime = time.time()
            if curTime - last_move_time > speed:
                if not pause:
                    INIT= INIT + (curTime - last_move_time)
                    if INIT >= elapsed:
                        _create_bonus()
                        INIT = 0
                    b = True
                    last_move_time = curTime
                    next_s = (snake[0][0] + pos_x, snake[0][1] + pos_y)
                    if next_s[0] == food_x and next_s[1] == food_y:
                        # eat food
                        _create_food()
                        snake.appendleft(next_s)
                        score += 10
                        speed = orispeed - 0.03 * (score // 100)
                    elif next_s[0] == bonus_x and next_s[1] == bonus_y:
                        _create_bonus()
                        INIT = 0
                        snake.appendleft(next_s)
                        score += 30
                    else:
                        if (
                            scope_x[0] <= next_s[0] <= scope_x[1]
                            and scope_y[0] <= next_s[1] <= scope_y[1]
                            and next_s not in snake
                        ):
                            snake.appendleft(next_s)
                            snake.pop()
                        else:
                            game_over = True

        # draw food
        if not game_over:
            # To prevent that the word are covered when GAME OVER
            pygame.draw.rect(
                screen, pink, (food_x * SIZE, food_y * SIZE, SIZE, SIZE), 0
            )
            pygame.draw.rect(
                screen, red, (bonus_x * SIZE, bonus_y * SIZE, SIZE, SIZE), 0
            )

        # draw snake
        for idx, s in enumerate(snake):
            if idx == 0:
                pygame.draw.circle(
                    screen,
                    body,
                    ((s[0] + 0.5) * SIZE, (s[1] + 0.5) * SIZE),
                    SIZE / 1.2,
                )
            else:
                pygame.draw.rect(
                    screen,
                    body,
                    (
                        s[0] * SIZE + line_width,
                        s[1] * SIZE + line_width,
                        SIZE - line_width * 2,
                        SIZE - line_width * 2,
                    ),
                    0,
                )
        # else:
        #     pygame.draw.rect(
        #         screen,
        #         body,
        #         (
        #             s[0] * SIZE + line_width,
        #             s[1] * SIZE + line_width,
        #             SIZE - line_width * 2,
        #             SIZE - line_width * 2,
        #         ),
        #         0,
        #     )
        
        if score<=40:
            ev= "easy"
        elif score<=70:
            ev= "middle"
        elif score<=110:
            ev= "hard"
        else:
            ev= "SNAKE!"
        # print_text(screen, font1, 30, 7, f'Speed: {score//100}')
        print_text(screen, font1, 30, 7, "Evaluation: %s" % ev)
        # print_text(screen, font1, 450, 7, f'Score: {score}')
        print_text(screen, font1, 450, 7, "Score: %d" % (score))

        pygame.display.update()


if __name__ == "__main__":
    main()
