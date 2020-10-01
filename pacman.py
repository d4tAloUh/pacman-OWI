# Pacman in Python with PyGame
# https://github.com/hbokmann/Pacman

import pygame
from settings import *

# Call this function so the Pygame library can initialize itself
pygame.init()

clock = pygame.time.Clock()
# Create an 606x606 sized screen
screen = pygame.display.set_mode([606, 606])
font = pygame.font.Font("freesansbold.ttf", 24)


# This is a list of 'sprites.' Each block in the program is
# added to this list. The list is managed by a class called 'RenderPlain.'
def configure_initial_window():
    Trollicon = pygame.image.load('images/Trollman.png')

    # Set the title of the window
    pygame.display.set_caption('Pacman')

    # Create a surface we can draw on
    background = pygame.Surface(screen.get_size())

    # Used for converting color maps and such
    background = background.convert()

    # Fill the screen with a black background
    background.fill(black)

    pygame.display.set_icon(Trollicon)

    pygame.font.init()


class Wall(pygame.sprite.Sprite):
    # Constructor function
    def __init__(self, x, y, width, height, color):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        # Make a blue wall, of the size specified in the parameters
        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x


# This creates all the walls in room 1
def setupRoomOne(all_sprites_list):
    # Make the walls. (x_pos, y_pos, width, height)
    wall_list = pygame.sprite.RenderPlain()

    # This is a list of walls. Each is in the form [x, y, width, height]
    walls = [[0, 0, 6, 600],
             [0, 0, 600, 6],
             [0, 600, 606, 6],
             [600, 0, 6, 606],
             [300, 0, 6, 66],
             [60, 60, 186, 6],
             [360, 60, 186, 6],
             [60, 120, 66, 6],
             [60, 120, 6, 126],
             [180, 120, 246, 6],
             [300, 120, 6, 66],
             [480, 120, 66, 6],
             [540, 120, 6, 126],
             [120, 180, 126, 6],
             [120, 180, 6, 126],
             [360, 180, 126, 6],
             [480, 180, 6, 126],
             [180, 240, 6, 126],
             [180, 360, 246, 6],
             [420, 240, 6, 126],
             [240, 240, 42, 6],
             [324, 240, 42, 6],
             [240, 240, 6, 66],
             [240, 300, 126, 6],
             [360, 240, 6, 66],
             [0, 300, 66, 6],
             [540, 300, 66, 6],
             [60, 360, 66, 6],
             [60, 360, 6, 186],
             [480, 360, 66, 6],
             [540, 360, 6, 186],
             [120, 420, 366, 6],
             [120, 420, 6, 66],
             [480, 420, 6, 66],
             [180, 480, 246, 6],
             [300, 480, 6, 66],
             [120, 540, 126, 6],
             [360, 540, 126, 6]
             ]

    # Loop through the list. Create the wall, add it to the list
    for item in walls:
        wall = Wall(item[0], item[1], item[2], item[3], blue)
        wall_list.add(wall)
        all_sprites_list.add(wall)

    # return our new list
    return wall_list


def setupGate(all_sprites_list):
    gate = pygame.sprite.RenderPlain()
    gate.add(Wall(282, 242, 42, 2, white))
    all_sprites_list.add(gate)
    return gate


# This class represents the ball
# It derives from the "Sprite" class in Pygame
class Circle(pygame.sprite.Sprite):

    # Constructor. Pass in the color of the block, 
    # and its x and y position
    def __init__(self, color=yellow, width=4, height=4):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([width, height])
        self.image.fill(white)
        self.image.set_colorkey(white)
        pygame.draw.ellipse(self.image, color, [0, 0, width, height])

        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values 
        # of rect.x and rect.y
        self.rect = self.image.get_rect()


class Player(pygame.sprite.Sprite):
    # Set speed vector
    change_x = 0
    change_y = 0

    # Constructor function
    def __init__(self, x, y, filename):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        # Set height, width
        self.image = pygame.image.load(filename).convert()

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x
        self.prev_x = x
        self.prev_y = y

    def set_speed_null(self):
        self.change_x = 0
        self.change_y = 0

    def moveUp(self):
        self.changespeed(0, -30)

    def moveDown(self):
        self.changespeed(0, 30)

    def moveRight(self):
        self.changespeed(30, 0)

    def moveLeft(self):
        self.changespeed(-30, 0)

    def check_y_open(self, walls, vel):
        old_y = self.rect.top
        new_y = old_y + vel
        self.rect.top = new_y
        y_collide = pygame.sprite.spritecollide(self, walls, False)
        if y_collide:
            self.rect.top = old_y
            return False
        self.rect.top = old_y
        return True

    def check_x_open(self, walls, vel):
        old_x = self.rect.left
        new_x = old_x + vel
        self.rect.left = new_x
        x_collide = pygame.sprite.spritecollide(self, walls, False)
        if x_collide:
            self.rect.left = old_x
            return False
        self.rect.left = old_x
        return True

    def up_is_open(self, walls):
        return self.check_y_open(walls, -30)

    def down_is_open(self, walls):
        return self.check_y_open(walls, 30)

    def right_is_open(self, walls):
        return self.check_x_open(walls, 30)

    def left_is_open(self, walls):
        return self.check_x_open(walls, -30)

    # Change the speed of the player
    def changespeed(self, x, y):
        self.change_x += x
        self.change_y += y

    # Find a new position for the player
    def update(self, walls, gate):

        old_x = self.rect.left
        new_x = old_x + self.change_x
        self.rect.left = new_x

        old_y = self.rect.top
        new_y = old_y + self.change_y

        # Did this update cause us to hit a wall?
        x_collide = pygame.sprite.spritecollide(self, walls, False)
        if x_collide:
            self.rect.left = old_x
        else:
            self.rect.top = new_y
            y_collide = pygame.sprite.spritecollide(self, walls, False)
            if y_collide:
                self.rect.top = old_y

        if gate:
            gate_hit = pygame.sprite.spritecollide(self, gate, False)
            if gate_hit:
                self.rect.left = old_x
                self.rect.top = old_y


def move_left_algorithm(pacman, walls):
    if pacman.left_is_open(walls):
        print("left is open")
        pacman.moveLeft()

def start_game_loop(playAlgorithm=None):
    Pacman = Player(PACMAN_X, PACMAN_Y, "images/Trollman.png")

    # Creation of all sprite lists
    all_sprites_list = pygame.sprite.RenderPlain()
    circle_list = pygame.sprite.RenderPlain()
    pacman_collide = pygame.sprite.RenderPlain()
    wall_list = setupRoomOne(all_sprites_list)
    gate = setupGate(all_sprites_list)
    pacman_collide.add(Pacman)
    all_sprites_list.add(Pacman)

    current_amount_of_circles = 0

    for row in range(19):
        for column in range(19):
            if current_amount_of_circles >= AMOUNT_OF_CIRCLES:
                break
            # ghosts place, gate is closing entrance
            if (row == 7 or row == 8) and (column == 8 or column == 9 or column == 10):
                continue
            else:
                block = Circle()

                block.rect.x = (30 * column + 6) + 26
                block.rect.y = (30 * row + 6) + 26

                b_collide = pygame.sprite.spritecollide(block, wall_list, False)
                p_collide = pygame.sprite.spritecollide(block, pacman_collide, False)

                if b_collide:
                    continue
                elif p_collide:
                    continue
                else:
                    # Add the block to the list of objects
                    circle_list.add(block)
                    all_sprites_list.add(block)
                    current_amount_of_circles += 1

    score = 0

    while True:
        # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    Pacman.moveLeft()
                if event.key == pygame.K_RIGHT:
                    Pacman.moveRight()
                if event.key == pygame.K_UP:
                    Pacman.moveUp()
                if event.key == pygame.K_DOWN:
                    Pacman.moveDown()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    Pacman.moveRight()
                if event.key == pygame.K_RIGHT:
                    Pacman.moveLeft()
                if event.key == pygame.K_UP:
                    Pacman.moveDown()
                if event.key == pygame.K_DOWN:
                    Pacman.moveUp()
        # ALL EVENT PROCESSING SHOULD GO ABOVE THIS COMMENT

        # ALL GAME LOGIC SHOULD GO BELOW THIS COMMENT
        try:
            playAlgorithm(Pacman, wall_list)
        except TypeError:
            pass

        Pacman.update(wall_list, gate)

        # Remove Pacman speed if algorithm is set
        if playAlgorithm is not None:
            Pacman.set_speed_null()

        blocks_hit_list = pygame.sprite.spritecollide(Pacman, circle_list, True)

        # Check the list of collisions.
        if blocks_hit_list:
            score += len(blocks_hit_list)

        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        screen.fill(black)
        all_sprites_list.draw(screen)

        text = font.render("Score: " + str(score) + "/" + str(current_amount_of_circles), True, red)
        screen.blit(text, [10, 10])

        if score == current_amount_of_circles:
            game_ended("Congratulations, you won!", 145)

        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

        pygame.display.flip()
        clock.tick(10)


def game_ended(message, left):
    while True:
        # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return
                if event.key == pygame.K_RETURN:
                    start_game_loop()

        # Grey background
        w = pygame.Surface((400, 200))  # the size of your rect
        w.set_alpha(10)  # alpha level
        w.fill((128, 128, 128))  # this fills the entire surface
        screen.blit(w, (100, 200))  # (0,0) are the top-left coordinates

        # Won or lost
        text1 = font.render(message, True, white)
        screen.blit(text1, [left, 233])

        text2 = font.render("To play again, press ENTER.", True, white)
        screen.blit(text2, [135, 303])
        text3 = font.render("To quit, press ESCAPE.", True, white)
        screen.blit(text3, [165, 333])

        pygame.display.flip()

        clock.tick(10)


if __name__ == '__main__':
    configure_initial_window()
    start_game_loop(move_left_algorithm)
    pygame.quit()
