import random

import pygame
from settings import *
import collections


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


class Circle(pygame.sprite.Sprite):

    # Constructor. Pass in the color of the block, 
    # and its x and y position
    def __init__(self, color=yellow, width=4, height=4):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([width, height])
        self.image.fill(white)
        self.image.set_colorkey(white)
        pygame.draw.ellipse(self.image, color, [0, 0, width, height])

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
        self.image = pygame.image.load(filename)

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

    def get_neighbours(self, wall_list):
        result = []
        if self.up_is_open(wall_list):
            result.append(("U", (self.rect.left, self.rect.top - 30)))
        if self.down_is_open(wall_list):
            result.append(("D", (self.rect.left, self.rect.top + 30)))
        if self.left_is_open(wall_list):
            result.append(("L", (self.rect.left - 30, self.rect.top)))
        if self.right_is_open(wall_list):
            result.append(("R", (self.rect.left + 30, self.rect.top)))
        return result

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


class Game:
    score = 0
    pygame.init()

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode([606, 606])
        self.font = pygame.font.Font("freesansbold.ttf", 24)

        self.Pacman = Player(PACMAN_X, PACMAN_Y, "images/taco.png")
        self.all_sprites_list = pygame.sprite.RenderPlain()

        self.all_sprites_list.add(self.Pacman)

        self.gate = pygame.sprite.RenderPlain()
        self.wall_list = pygame.sprite.RenderPlain()
        self.circle_list = pygame.sprite.RenderPlain()

        self.pacman_collide = pygame.sprite.RenderPlain()
        self.pacman_collide.add(self.Pacman)

        # self.setup_gate()
        self.setup_walls_room_one()
        self.setup_circles()

    def setup_gate(self):
        self.gate.add(Wall(282, 242, 42, 2, white))
        self.all_sprites_list.add(self.gate)

    def setup_walls_room_one(self):
        for wall in WALLS_ROOM_ONE:
            wall_object = Wall(wall[0], wall[1], wall[2], wall[3], pink)
            self.wall_list.add(wall_object)
            self.all_sprites_list.add(wall_object)

    def setup_random_circles(self):
        current_amount_of_circles = 0
        while current_amount_of_circles != AMOUNT_OF_CIRCLES:
            column = random.randint(0, 19)
            row = random.randint(0, 19)

            block = Circle()

            block.rect.x = (30 * column + 6) + 26
            block.rect.y = (30 * row + 6) + 26

            wall_collide = pygame.sprite.spritecollide(block, self.wall_list, False)
            pacman_collide = pygame.sprite.spritecollide(block, self.pacman_collide, False)
            circles_collide = pygame.sprite.spritecollide(block, self.circle_list, False)

            if wall_collide or pacman_collide or circles_collide:
                continue

            self.circle_list.add(block)
            self.all_sprites_list.add(block)
            current_amount_of_circles += 1

    def setup_circles(self):
        current_amount_of_circles = 0
        for row in range(19):
            for column in range(19):
                if current_amount_of_circles == AMOUNT_OF_CIRCLES:
                    break
                # ghosts place, gate is closing entrance
                # if (row == 7 or row == 8) and (column == 8 or column == 9 or column == 10):
                #     continue
                # else:
                block = Circle()

                block.rect.x = (30 * column + 6) + 26
                block.rect.y = (30 * row + 6) + 26

                wall_collide = pygame.sprite.spritecollide(block, self.wall_list, False)
                pacman_collide = pygame.sprite.spritecollide(block, self.pacman_collide, False)

                if wall_collide or pacman_collide:
                    continue

                self.circle_list.add(block)
                self.all_sprites_list.add(block)
                current_amount_of_circles += 1

    def setup_initial_window(self):
        Taco = pygame.image.load('images/taco.png')

        # Set the title of the window
        pygame.display.set_caption('Pacman')

        # Create a surface we can draw on
        background = pygame.Surface(self.screen.get_size())

        # Used for converting color maps and such
        background = background.convert()

        # Fill the screen with a black background
        background.fill(black)

        pygame.display.set_icon(Taco)

        pygame.font.init()

    def start_game(self):
        self.play_standart_game()

    def play_standart_game(self):
        while True:
            # HANDLING KEY EVENTS
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.Pacman.moveLeft()
                    if event.key == pygame.K_RIGHT:
                        self.Pacman.moveRight()
                    if event.key == pygame.K_UP:
                        self.Pacman.moveUp()
                    if event.key == pygame.K_DOWN:
                        self.Pacman.moveDown()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.Pacman.moveRight()
                    if event.key == pygame.K_RIGHT:
                        self.Pacman.moveLeft()
                    if event.key == pygame.K_UP:
                        self.Pacman.moveDown()
                    if event.key == pygame.K_DOWN:
                        self.Pacman.moveUp()

            # UPDATE PACMAN POSITION
            self.Pacman.update(self.wall_list, self.gate)

            # CHECK IF PACMAN HITS CIRCLE
            if self.hit_circle():
                self.score += 1

            # DRAW SCORE AND SPRITES
            self.draw_screen()

    def hit_circle(self):
        if pygame.sprite.spritecollide(self.Pacman, self.circle_list, True):
            return True
        return False

    def draw_screen(self):
        self.screen.fill(black)
        self.all_sprites_list.draw(self.screen)

        text = self.font.render("Score: " + str(self.score) + "/" + str(AMOUNT_OF_CIRCLES), True, red)
        self.screen.blit(text, [10, 10])

        if self.won():
            self.show_won_menu("Congratulations, you won!", 145)

        pygame.display.flip()
        self.clock.tick(60)

    def won(self):
        if self.score == AMOUNT_OF_CIRCLES:
            return True
        return False

    def show_won_menu(self, message, left):
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
                        self.start_game()
                        break

            # Grey background
            w = pygame.Surface((400, 200))  # the size of your rect
            w.set_alpha(10)  # alpha level
            w.fill((128, 128, 128))  # this fills the entire surface
            self.screen.blit(w, (100, 200))  # (0,0) are the top-left coordinates

            # Won or lost
            text1 = self.font.render(message, True, white)
            self.screen.blit(text1, [left, 233])
            text2 = self.font.render("To play again, press ENTER.", True, white)
            self.screen.blit(text2, [135, 303])
            text3 = self.font.render("To quit, press ESCAPE.", True, white)
            self.screen.blit(text3, [165, 333])

            pygame.display.flip()

            self.clock.tick(60)


class Algorithm:
    def __init__(self, Game):
        self.game = Game
        self.moves = 0

    def move_to_v(self, path_to_v):
        while path_to_v is not '':
            self.moves += 1
            current_move = path_to_v[0]
            if current_move == "R":
                self.game.Pacman.moveRight()
            if current_move == "D":
                self.game.Pacman.moveDown()
            if current_move == "U":
                self.game.Pacman.moveUp()
            if current_move == "L":
                self.game.Pacman.moveLeft()

            path_to_v = path_to_v[1:]
            self.game.Pacman.update(self.game.wall_list, self.game.gate)
            self.game.Pacman.set_speed_null()
            self.game.draw_screen()

    def reverse_move(self, path):
        result: str = ""
        for letter in path:
            if letter == "R":
                result += "L"
            if letter == "D":
                result += "U"
            if letter == "U":
                result += "D"
            if letter == "L":
                result += "R"
        return result

    def get_move(self, path1, path2):
        '''
        :param path1: current path from start
        :param path2: path to next node
        :return: path from current node to next
        '''
        i = 0
        maxi = min(len(path1), len(path2))
        result = ''
        try:
            while i < maxi and path1[i] == path2[i]:
                i += 1
            result += self.reverse_move(path1[i:len(path1)][::-1])
            result += path2[i:len(path2)]
        except IndexError:
            result = path2
        return result

    def depth_search(self):
        self.moves = 0
        stack = collections.deque()
        stack.append(("", (self.game.Pacman.rect.left, self.game.Pacman.rect.top)))
        visited = []
        path = ""
        while stack:
            # V = path to current block
            # (x,y) - current coordinates
            v, (x, y) = stack.pop()

            if (x, y) in visited:
                continue
            path_to_v = self.get_move(path, v)

            self.move_to_v(path_to_v)

            if self.game.hit_circle():
                print("Path: ", v)
                print("Amount of moves: ", self.moves)
                return v

            neighbours = self.game.Pacman.get_neighbours(self.game.wall_list)

            for neighbour, (x1, y1) in neighbours:
                stack.append((v + neighbour, (x1, y1)))

            visited.append((x, y))
            path = v

        return "No PATH"

    def breadth_search(self):
        self.moves = 0
        queue = collections.deque()
        queue.append(("", (self.game.Pacman.rect.left, self.game.Pacman.rect.top)))
        visited = []
        path = ""
        while queue:
            # V = path to current block
            # (x,y) - current coordinates
            v, (x, y) = queue.popleft()

            if (x, y) in visited:
                continue
            path_to_v = self.get_move(path, v)

            self.move_to_v(path_to_v)

            if self.game.hit_circle():
                print("Path: ", v)
                print("Amount of moves: ", self.moves)
                return v

            neighbours = self.game.Pacman.get_neighbours(self.game.wall_list)

            for neighbour, (x1, y1) in neighbours:
                queue.append((v + neighbour, (x1, y1)))

            visited.append((x, y))
            path = v

        return "No PATH"


if __name__ == '__main__':
    pacman = Game()
    # pacman.start_game()
    algo = Algorithm(pacman)
    # algo.depth_search()
    algo.breadth_search()
