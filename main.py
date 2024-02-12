import pygame
import random

# uses the pointsToWin var, used both across menu and game loop
global pointsToWin

# initializes all pygame functions
pygame.init()

# loading, playing, infinitely looping music
pygame.mixer.music.load("sound/Blippy Trance from Incompetech.mp3")
pygame.mixer.music.play(-1)


# main menu
def menu():
    # pygame setup
    pygame.init()

    global pointsToWin
    pointsToWin = 0

    screenwidth = 1280
    screenheight = 720

    # display surface for drawing objects on
    screen = pygame.display.set_mode((screenwidth, screenheight))
    # names the window the game is played in
    pygame.display.set_caption("Pong Clone by Nelson Henriquez")
    # clock function for keeping track of real time
    clock = pygame.time.Clock()
    running = True
    # means yes, we are currently on the main menu, used for moving to the score selector menu
    main_menu = True
    # delta time, time since last frame used for framerate independent physics
    dt = 0

    # sound loading
    select_sound = pygame.mixer.Sound("sound/select sound.mp3")

    # font loading for text
    title_font = pygame.font.Font('font/Barlow-Regular.ttf', 100)
    button_font = pygame.font.Font('font/Barlow-Regular.ttf', 50)

    # creating all text surfaces to display or "blit" on top of the screen surface
    title_surf = title_font.render('Pong', True, (0, 0, 0))
    start_surf = button_font.render('Start', True, (0, 0, 0))
    quit_surf = button_font.render('Quit', True, (0, 0, 0))

    # copy of ball from the game loop, but able to initialize both x and y velocity on creation
    class Ball:
        # position
        x = 0
        y = 0

        # velocity
        vx = 0
        vy = 0

        # constructor. pass these parameters to the attributes of the instance
        def __init__(self, init_x, init_y, init_v):
            self.x = init_x
            self.y = init_y
            self.vx = init_v
            self.vy = init_v

        # updates ball position
        def update(self):
            # multiply velocity by time since last frame, then add that value to position
            self.x += self.vx * dt
            self.y += self.vy * dt

        # draw ball to screen
        def draw(self):
            pygame.draw.circle(screen, "black", (self.x, self.y), 20, 3)

    # creating object named ball from class/type Ball
    ball = Ball(random.randint(20, screenwidth - 20), random.randint(20, screenheight - 20), random.randint(900, 1500))

    while running:  # RUNS EVERY FRAME
        # pygame.QUIT event means the user clicked X to close the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                '''this is normally "running = False," but some bug in returning to the main menu after a game 
                completes, if you clicked the x button after completing a game, it would keep showing a win message 
                instead of actually closing the game. something is technically broken here but idrc and this works 
                pretty much the same anyway.'''
                pygame.quit()

        # checking ball collision with ceiling and floor
        if ball.y < 20 or ball.y > screenheight - 20:
            ball.vy = ball.vy * -1
        # checking ball collision with walls
        if ball.x < 20 or ball.x > screenwidth - 20:
            ball.vx = ball.vx * -1

        # wipes away last frame with white screen
        screen.fill("white")

        # update ball's position then draw it to screen
        ball.update()
        ball.draw()

        # if we are on the main menu (main_menu == True), run this code
        if main_menu:
            # get mouse position every frame
            mouse_x = pygame.mouse.get_pos()[0]
            mouse_y = pygame.mouse.get_pos()[1]

            # draw these white rectangles behind the buttons so the ball isn't visible behind them (looks ugly)
            pygame.draw.rect(screen, "white", (490, 340, 300, 100))
            pygame.draw.rect(screen, "white", (490, 520, 300, 100))

            # if the mouse pointer is over the button,
            if 790 > mouse_x > 490 and 440 > mouse_y > 340:
                # color in the button,
                pygame.draw.rect(screen, "gray", (490, 340, 300, 100))
                # check every frame is the mouse is clicked, to click the button
                if pygame.mouse.get_pressed(3)[0]:
                    # play the select sound
                    pygame.mixer.Sound.play(select_sound)
                    # move to the submenu code next frame
                    main_menu = False

            if 790 > mouse_x > 490 and 620 > mouse_y > 520:
                pygame.draw.rect(screen, "gray", (490, 520, 300, 100))
                if pygame.mouse.get_pressed(3)[0]:
                    # game quits on next frame, it's unnecessary to play any sound
                    pygame.quit()

            # draw the outlines for the buttons
            pygame.draw.rect(screen, "black", (490, 340, 300, 100), 2)
            pygame.draw.rect(screen, "black", (490, 520, 300, 100), 2)
            # draw the text for the buttons
            screen.blit(title_surf, (525, 100))
            screen.blit(start_surf, (580, 355))
            screen.blit(quit_surf, (590, 535))

        # if we have already pressed start, and gone to the score goal menu, run this code
        else:
            mouse_x = pygame.mouse.get_pos()[0]
            mouse_y = pygame.mouse.get_pos()[1]

            pygame.draw.rect(screen, "white", (250, 300, 300, 100))
            pygame.draw.rect(screen, "white", (750, 300, 300, 100))
            pygame.draw.rect(screen, "white", (500, 500, 300, 100))

            # points select menu
            if 550 > mouse_x > 250 and 400 > mouse_y > 300:
                pygame.draw.rect(screen, "gray", (250, 300, 300, 100))
                if pygame.mouse.get_pressed(3)[0]:
                    pygame.mixer.Sound.play(select_sound)
                    # you have selected to play until 5 points
                    pointsToWin = 5
                    # start the game ^u^
                    game_loop()

            if 1050 > mouse_x > 750 and 400 > mouse_y > 300:
                pygame.draw.rect(screen, "gray", (750, 300, 300, 100))
                if pygame.mouse.get_pressed(3)[0]:
                    pygame.mixer.Sound.play(select_sound)
                    pointsToWin = 10
                    game_loop()

            if 800 > mouse_x > 500 and 600 > mouse_y > 500:
                pygame.draw.rect(screen, "gray", (500, 500, 300, 100))
                if pygame.mouse.get_pressed(3)[0]:
                    pygame.mixer.Sound.play(select_sound)
                    pointsToWin = 20
                    game_loop()

            pygame.draw.rect(screen, "black", (250, 300, 300, 100), 2)
            pygame.draw.rect(screen, "black", (750, 300, 300, 100), 2)
            pygame.draw.rect(screen, "black", (500, 500, 300, 100), 2)

            title_surf = title_font.render('# of points to win?', True, (0, 0, 0))
            number_one = button_font.render('Five', True, (0, 0, 0))
            number_two = button_font.render('Ten', True, (0, 0, 0))
            number_three = button_font.render('Twenty', True, (0, 0, 0))

            screen.blit(title_surf, (255, 100))
            screen.blit(number_one, (350, 320))
            screen.blit(number_two, (855, 320))
            screen.blit(number_three, (570, 520))

        # show everything you have drawn to the screen!
        pygame.display.flip()

        # calculate time in milliseconds since last frame, then divide it by 1000 to get seconds
        dt = clock.tick(60) / 1000


# main game loop
def game_loop():
    # pygame setup
    pygame.init()

    global pointsToWin

    screenwidth = 1280
    screenheight = 720
    screen = pygame.display.set_mode((screenwidth, screenheight))
    clock = pygame.time.Clock()
    running = True
    dt = 0

    # sound loading
    hit_sound = pygame.mixer.Sound("sound/ball hit.mp3")
    win_sound = pygame.mixer.Sound("sound/success sound.mp3")

    # loading font again for win message
    title_font = pygame.font.Font('font/Barlow-Regular.ttf', 100)

    # score display
    score1 = 0
    score2 = 0
    my_font = pygame.font.Font('font/Barlow-Regular.ttf', 60)
    player_score = my_font.render(str(score1), True, (0, 0, 0))
    opp_score = my_font.render(str(score2), True, (0, 0, 0))
    player_ball = False

    # respawning variables
    respawning = False
    timer = 0

    # paddle class used for players 1 and 2
    class Paddle:
        x = 0
        y = 0
        w = 0
        h = 0

        # initializing rect to use in draw function
        rect = 0
        velocity = 0

        def __init__(self, init_x, init_y, init_w, init_h):
            self.x = init_x
            self.y = init_y
            self.w = init_w
            self.h = init_h

            # paddle speed
            self.velocity = 600

            # stores the 4 points of the rectangle in an object, necessary for draw
            self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

        # update paddle position
        def update(self):
            self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

        # draw this paddle object to the screen
        def draw(self):
            pygame.draw.rect(screen, "black", self.rect)

    # ball class from menu function, but no y velocity parameter, is not necessary
    class Ball:
        x = 0
        y = 0

        vx = 0
        vy = 0

        def __init__(self, init_x, init_y, init_vx):
            self.x = init_x
            self.y = init_y

            # ball speed
            self.vx = init_vx
            self.vy = 0

        def update(self):
            # dt so speed isn't tied to fps
            self.x += self.vx * dt
            self.y += self.vy * dt

        def draw(self):
            pygame.draw.circle(screen, "white", (self.x, self.y), 20, )
            pygame.draw.circle(screen, "black", (self.x, self.y), 20, 3)

    # create player 1 and 2 paddles
    player = Paddle(64, screenheight / 2 - 60, 20, 120)
    player2 = Paddle(screenwidth - 84, screenheight / 2 - 60, 20, 120)
    # create ball
    ball = Ball(screenwidth / 2, screenheight / 2, 850)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # if player 1 or 2 reach the score limit:
        if score1 == pointsToWin:
            # reset the score
            pointsToWin = 0
            # wipe the screen
            screen.fill("white")
            # use the title surface to draw the win text
            title_surf = title_font.render('Player 1 Wins!', True, (0, 0, 0))
            screen.blit(title_surf, (380, 270))
            pygame.display.flip()
            # play that sweet victory sound
            pygame.mixer.Sound.play(win_sound)
            # stop the program for a second just to chill and show off the text
            pygame.time.delay(5000)
            # return to the main menu
            menu()

        elif score2 == pointsToWin:
            pointsToWin = 0
            screen.fill("white")
            title_surf = title_font.render('Player 2 Wins!', True, (0, 0, 0))
            screen.blit(title_surf, (380, 270))
            pygame.display.flip()
            pygame.mixer.Sound.play(win_sound)
            pygame.time.delay(5000)
            menu()

        else:
            # ball collision logic

            # if ball is between the top and bottom of the paddle and is in front of the paddle:
            if player.y <= ball.y <= player.y + 140 and player.x <= ball.x <= player.x + 40:
                # find center of the paddle
                center = player.y + 60
                # modify the y velocity based on the difference between the paddle's and the ball's center
                ball.vy = (center - ball.y) * -5
                # increase the velocity a little every successful return
                ball.vx -= 30
                # reverse the ball's x velocity when it is reflected off the paddle
                ball.vx = ball.vx * -1
                # play that hit sound!!!
                pygame.mixer.Sound.play(hit_sound)

            if player2.y <= ball.y <= player2.y + 140 and player2.x + 20 >= ball.x >= player2.x - 20:
                center = player2.y + 60
                ball.vy = (center - ball.y) * -5
                ball.vx += 30
                ball.vx = ball.vx * -1
                pygame.mixer.Sound.play(hit_sound)

            # if ball hits ceiling or floor
            if ball.y < 20 or ball.y > screenheight - 20:
                # reflect the y velocity
                ball.vy = ball.vy * -1
                # play that hit sound again!!!
                pygame.mixer.Sound.play(hit_sound)

            # ball goes off-screen
            if ball.x < 0:
                # add a point to the player who scored
                score2 += 1
                # return the ball to the center and reset its velocity to zero
                ball.x = screenwidth / 2
                ball.y = screenheight / 2
                ball.vx = 0
                ball.vy = 0
                # put the new score on screen
                opp_score = my_font.render(str(score2), True, (0, 0, 0))
                # the player who scored gets first hit. in this case player 2
                player_ball = False
                # begin respawning logic
                respawning = True

            elif ball.x > screenwidth:
                score1 += 1
                ball.x = screenwidth / 2
                ball.y = screenheight / 2
                ball.vx = 0
                ball.vy = 0
                player_score = my_font.render(str(score1), True, (0, 0, 0))
                player_ball = True
                respawning = True

            # fill the screen with a color to wipe away anything from last frame
            screen.fill("white")
            # draw the net in the middle
            pygame.draw.line(screen, "black", (screenwidth / 2, 0), (screenwidth / 2, screenheight), 3)

            # updating all objects and drawing them to the screen
            player.update()
            player.draw()

            player2.update()
            player2.draw()

            ball.update()
            ball.draw()

            # drawing score to the screen
            screen.blit(player_score, (10, 10))
            screen.blit(opp_score, (1230, 10))

            # input handling
            keys = pygame.key.get_pressed()
            # dt uses real time so speed isn't tied to framerate

            # left paddle movement
            if keys[pygame.K_w] and player.y > 0:
                player.y -= player.velocity * dt
            elif keys[pygame.K_s] and player.y < 615:
                player.y += player.velocity * dt

            # right paddle movement
            if keys[pygame.K_UP] and player2.y > 0:
                player2.y -= player2.velocity * dt
            elif keys[pygame.K_DOWN] and player2.y < 615:
                player2.y += player2.velocity * dt

            # flip() to put all that business on screen
            pygame.display.flip()

            dt = clock.tick(60) / 1000

            # respawning logic: if respawning is now true, start a timer for 80 frames (a little over one second)
            if respawning and timer < 80:
                timer += 1

            # if last check fails, respawning is now over, check how long it's been and then,
            elif timer == 80:
                # stop the respawning logic
                respawning = False
                # set the respawn timer back to zero for next time
                timer = 0
                # if player 1 scored, he gets first hit
                if player_ball:
                    ball = Ball(screenwidth / 2, screenheight / 2, -850)
                # if player 2 scored, he gets second hit
                else:
                    ball = Ball(screenwidth / 2, screenheight / 2, 850)


# run the game
menu()
