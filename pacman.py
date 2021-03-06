import os
import random
import time

import pygame
import psutil

import settings
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
    def __init__(self, color=settings.yellow, width=4, height=4):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([width, height])
        self.image.fill(settings.white)
        self.image.set_colorkey(settings.white)
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

    def set_start_pos(self, x, y):
        self.rect.left = x
        self.rect.top = y

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
    PACMAN_X = 0
    PACMAN_Y = 0
    circles_coords = []

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode([570, 570])
        self.font = pygame.font.Font("freesansbold.ttf", 24)

        self.gate = pygame.sprite.RenderPlain()

        self.wall_list = pygame.sprite.RenderPlain()
        self.circle_list = pygame.sprite.RenderPlain()
        self.all_sprites_list = pygame.sprite.RenderPlain()

        self.parse_map_from_file(settings.map)

        self.Pacman = Player(self.PACMAN_X, self.PACMAN_Y, "images/tacopng.png")
        self.all_sprites_list.add(self.Pacman)

        self.pacman_collide = pygame.sprite.RenderPlain()
        self.pacman_collide.add(self.Pacman)

        # self.setup_random_circles()

    def get_circle_coords(self):
        return self.circles_coords[0][0] - 12, self.circles_coords[0][1] - 12

    def refresh(self):
        del self.all_sprites_list
        del self.circle_list
        del self.wall_list
        del self.Pacman
        del self.pacman_collide

        self.PACMAN_X = 0
        self.PACMAN_Y = 0
        self.score = 0

        self.all_sprites_list = pygame.sprite.RenderPlain()
        self.circle_list = pygame.sprite.RenderPlain()
        self.wall_list = pygame.sprite.RenderPlain()

        self.parse_map_from_file(settings.map)

        self.Pacman = Player(self.PACMAN_X, self.PACMAN_Y, "images/tacopng.png")
        self.all_sprites_list.add(self.Pacman)

        self.pacman_collide = pygame.sprite.RenderPlain()
        self.pacman_collide.add(self.Pacman)

    def parse_map_from_file(self, filename):
        lines = []
        settings.AMOUNT_OF_CIRCLES = 0
        with open(filename) as my_file:
            for line in my_file:
                lines.append(line)
        for l in range(len(lines)):
            k = (lines[l])
            for i in range(len(k)):
                if k[i] == "W":
                    wall_object = Wall(30 * i, 30 * l, 30, 30,
                                       random.choice([settings.blue, settings.green_yellow]))
                    self.wall_list.add(wall_object)
                    self.all_sprites_list.add(wall_object)
                elif k[i] == "P":
                    self.PACMAN_X = 30 * i
                    self.PACMAN_Y = 30 * l
                elif k[i] == "O":
                    self.create_circle(i * 30 + 12, l * 30 + 12)
                    self.circles_coords.append((i * 30 + 12, l * 30 + 12))
                    settings.AMOUNT_OF_CIRCLES += 1

    def setup_random_circles(self):
        current_amount_of_circles = 0
        while current_amount_of_circles != settings.AMOUNT_OF_CIRCLES:
            column = random.randint(0, 18)
            row = random.randint(0, 18)

            block = Circle()

            block.rect.x = 30 * column + 12
            block.rect.y = 30 * row + 12

            wall_collide = pygame.sprite.spritecollide(block, self.wall_list, False)
            pacman_collide = pygame.sprite.spritecollide(block, self.pacman_collide, False)
            circles_collide = pygame.sprite.spritecollide(block, self.circle_list, False)

            if wall_collide or pacman_collide or circles_collide:
                continue
            print(block.rect)
            self.circle_list.add(block)
            self.all_sprites_list.add(block)
            current_amount_of_circles += 1

    def setup_circles(self):
        current_amount_of_circles = 0
        for row in range(19):
            for column in range(19):
                if current_amount_of_circles == settings.AMOUNT_OF_CIRCLES:
                    break
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

    def create_circle(self, x, y):
        block = Circle()

        block.rect.x = x
        block.rect.y = y

        self.circle_list.add(block)
        self.all_sprites_list.add(block)

    def setup_initial_window(self):
        Taco = pygame.image.load('images/taco.png')

        # Set the title of the window
        pygame.display.set_caption('Pacman')

        # Create a surface we can draw on
        background = pygame.Surface(self.screen.get_size())

        # Used for converting color maps and such
        background = background.convert()

        # Fill the screen with a black background
        background.fill(settings.black)

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
        self.screen.fill(settings.black)
        self.all_sprites_list.draw(self.screen)

        text = self.font.render("Score: " + str(self.score) + "/" + str(settings.AMOUNT_OF_CIRCLES), True, settings.red)
        self.screen.blit(text, [10, 10])

        if self.won():
            self.show_won_menu("Congratulations, you won!", 145)

        pygame.display.flip()
        self.clock.tick(settings.GAME_TICK)

    def won(self):
        if self.score == settings.AMOUNT_OF_CIRCLES:
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
                        self.refresh()
                        self.start_game()
                        break

            # Grey background
            w = pygame.Surface((400, 200))  # the size of your rect
            w.set_alpha(10)  # alpha level
            w.fill((128, 128, 128))  # this fills the entire surface
            self.screen.blit(w, (100, 200))  # (0,0) are the top-left coordinates

            # Won or lost
            text1 = self.font.render(message, True, settings.white)
            self.screen.blit(text1, [left, 233])
            text2 = self.font.render("To play again, press ENTER.", True, settings.white)
            self.screen.blit(text2, [135, 303])
            text3 = self.font.render("To quit, press ESCAPE.", True, settings.white)
            self.screen.blit(text3, [165, 333])

            pygame.display.flip()

            self.clock.tick(settings.GAME_TICK)


class Algorithm:
    def __init__(self, Game):
        self.game = Game
        self.game_played = False
        self.pacman_moves = 0
        self.start_time = time.time()

    def move_to_v(self, path_to_v):
        while path_to_v is not '':
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break
            self.pacman_moves += 1
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

    def search(self, method):
        self.start_time = time.time()
        self.game_played = True
        self.pacman_moves = 0
        algo_moves = 0

        stack = collections.deque()

        stack.append(("", (self.game.Pacman.rect.left, self.game.Pacman.rect.top)))

        visited = []
        path = ""

        while stack:
            # V = path to current block
            # (x,y) - current coordinates
            if method == "DFS":
                v, (x, y) = stack.pop()
            #     else BFS
            else:
                v, (x, y) = stack.popleft()

            if (x, y) in visited:
                continue

            algo_moves += 1

            path_to_v = self.get_move(path, v)

            self.move_to_v(path_to_v)

            if self.game.hit_circle():
                self.print_result(v, algo_moves, method)
                return v

            neighbours = self.game.Pacman.get_neighbours(self.game.wall_list)

            for neighbour, (x1, y1) in neighbours:
                stack.append((v + neighbour, (x1, y1)))

            visited.append((x, y))
            path = v

        return "No PATH"

    def depth_search(self):
        if self.game_played:
            self.game.refresh()
        return self.search("DFS")

    def breadth_search(self):
        if self.game_played:
            self.game.refresh()
        return self.search("BFS")

    def manhattan_length(self, x1: int, y1: int, x2: int, y2: int):
        return abs(x1 - x2) + abs(y1 - y2)

    def greedy_search(self):
        if self.game_played:
            self.game.refresh()
        else:
            self.game_played = True
        self.heuristic_search("Greedy", self.manhattan_length, lambda obj: obj[2])

    def a_star_search(self):
        if self.game_played:
            self.game.refresh()
        self.game_played = True
        self.heuristic_search("A*", self.manhattan_length, lambda obj: obj[2])

    def print_result(self, path, algo_moves, algo_name):
        print("\n\n-----------------------------Result-------------------------------")
        print("Algorithm: ", algo_name)
        print("Path: ", path)
        print("Game TICK: ", settings.GAME_TICK)
        print("Amount of PACMAN moves: ", self.pacman_moves)
        print("Amount of ALGO moves: ", algo_moves)
        print("TIME IN SECONDS: ", (time.time() - self.start_time))
        process = psutil.Process(os.getpid())
        print(f"MEMORY USAGE: {process.memory_info().rss / 1000} KB")
        print("-------------------------------------------------------------------\n")

    def heuristic_search(self, method, heuristic, sortBy):
        # Heuristic must take 4 arguments x1,y1 x2,y2
        self.start_time = time.time()
        self.game_played = True
        self.pacman_moves = 0
        algo_moves = 0
        # Start and End positions for heuristic
        circle_x, circle_y = self.game.get_circle_coords()
        start_x, start_y = self.game.Pacman.rect.left, self.game.Pacman.rect.top

        queue = collections.deque()
        if method == "Greedy":
            queue.append(("", (self.game.Pacman.rect.left, self.game.Pacman.rect.top), 0))
        else:
            queue.append(("", (start_x, start_y), heuristic(start_x, start_y, circle_x, circle_y), 0))
        visited = []
        path = ""

        while queue:
            if method == "Greedy":
                v, (x, y), cost = queue.popleft()
            else:
                v, (x, y), _, cost = queue.popleft()

            if (x, y) in visited:
                continue

            path_to_v = self.get_move(path, v)

            self.move_to_v(path_to_v)
            algo_moves += 1

            if self.game.hit_circle():
                self.print_result(v, algo_moves, method)
                return v

            neighbours = self.game.Pacman.get_neighbours(self.game.wall_list)

            for neighbour, (x1, y1) in neighbours:
                if method == "Greedy":
                    queue.append((v + neighbour, (x1, y1), self.manhattan_length(circle_x, circle_y, x1, y1)))
                else:
                    queue.append(
                        (v + neighbour, (x1, y1), cost + self.manhattan_length(circle_x, circle_y, x1, y1),
                         self.manhattan_length(start_x, start_y, x1, y1)))

            queue = collections.deque(sorted(queue, key=sortBy))
            visited.append((x, y))
            path = v

    def test_a_star(self, method, sortBy):
        self.start_time = time.time()
        self.game_played = True
        self.pacman_moves = 0
        algo_moves = 0
        # Start and End positions for heuristic
        circle_x, circle_y = self.game.get_circle_coords()
        start_x, start_y = self.game.Pacman.rect.left, self.game.Pacman.rect.top

        queue = list()
        queue.append({"path": "",
                      "coord": (start_x, start_y),
                      "cost": 0,
                      "depth": 0})
        visited = []
        path = ""
        while len(queue) > 0:

            cell = queue[0]
            del queue[0]
            # Look if we visited this cell, if so, continue with next cell
            if (cell["coord"][0], cell["coord"][1]) in visited:
                continue

            # get path looking "LRDU" to move from prev cell, to current cell
            path_to_v = self.get_move(path, cell["path"])

            # algorithm to vizualize moving
            self.move_to_v(path_to_v)
            algo_moves += 1
            # Is this cell is final destination
            if self.game.hit_circle():
                # Print benchmarks
                self.print_result(cell["path"], algo_moves, method)
                # return path from start to result cell
                return cell["path"]

            # get all possible neighbours
            neighbours = self.game.Pacman.get_neighbours(self.game.wall_list)

            for neighbour, (x1, y1) in neighbours:
                # check if we already added to queue or visited this node
                exists, existing_cell = self.cell_exists_in_list((x1, y1), queue)
                if not exists and (x1, y1) not in visited:
                    # If it is new cell, add it to the queue
                    queue.append(
                        {"path": cell["path"] + neighbour,
                         "coord": (x1, y1),
                         "cost": cell["depth"] + self.manhattan_length(circle_x, circle_y, x1, y1)/30,
                         "depth": cell["depth"] + 1})
                #     check if returned not null cell from algorithm
                elif existing_cell is not None:
                    # If depth of this exsiting cell is deeper, than it will have from current mvoe
                    # remove it from queue, and add it with new path
                    if existing_cell["depth"] > cell["depth"] + 1:
                        existing_cell["depth"] = cell["depth"] + 1
                        queue = self.remove_existing_cell_in_list((x1, y1), queue)
                        queue.append(
                            {"path": cell["path"] + neighbour,
                             "coord": (x1, y1),
                             "cost": cell["depth"] + self.manhattan_length(circle_x, circle_y, x1, y1)/30,
                             "depth": cell["depth"] + 1})
                        # remove this cell from visited, because now it has less depth, then previously
                        if existing_cell["coord"] in visited:
                            visited.remove(existing_cell["coord"])
            # Sort queue
            queue = collections.deque(sorted(queue, key=sortBy))
            # add current cell to visited list
            visited.append((cell["coord"][0], cell["coord"][1]))
            # remember path from start to current node
            path = cell["path"]

    def remove_existing_cell_in_list(self, node, list_n: list):
        for item in list_n:
            if item["coord"] == node:
                list_n.remove(item)
                return list_n
        return list_n

    def cell_exists_in_list(self, node, list_n):
        for item in list_n:
            if item["coord"] == node:
                return True, item
        return False, None


if __name__ == '__main__':
    pacman = Game()
    # # pacman.start_game()
    algo = Algorithm(pacman)
    # algo.test_a_star("A* Test", lambda x: x["cost"])
    # algo.a_star_search()
    # algo.greedy_search()
    # algo.breadth_search()
    # algo.depth_search()
