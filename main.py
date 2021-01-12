import os
import random
import sys
import socket
from pygame.locals import *
import pygame
pygame.init()
step_of_user = 0
c = 0
sock = socket.socket()
server = ''
port = 5050
# 0 - вода
# 1 - выделенная клетка
# 2 - земля
# 3 - железо(6)
# 4 - дерево(10)
# 5 - нефть(4)
# 6 - вольфрам(3)
# 10 - артиллерия
# 20 - пехота
# 30 - мотопехота
# 40 - танк
# 100 - дом лесника
# 200 - рудник железа
# 300 - нефтекачалка
# 400 - рудник вольфрама
all_sprites = pygame.sprite.Group()
units_sprites = pygame.sprite.Group()
builds_sprites = pygame.sprite.Group()
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT = pygame.font.Font(None, 32)
pygame.mixer.music.load('data/Agression.mp3')
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Red:
    def __init__(self):
        self.resource = {3: 100, 4: 100, 5: 100, 6: 100}

    def res(self):
        return self.resource


class Blue:
    def __init__(self):
        self.resource = {3: 100, 4: 100, 5: 100, 6: 100}

    def res(self):
        return self.resource


class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False
        if x == 1700:
            nick = open('data/cfg.txt', mode='r').readlines()[0].split()[2]
        else:
            nick = ''
        self.txt_surface = FONT.render(nick[1:-1], True, self.color)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def register(self):
        nick = open('data/cfg.txt', mode='r').readlines()[0].split()
        nick[2] = "'" + self.text + "'"
        f = open('data/cfg.txt', mode='w')
        f.write(' '.join(nick))

    def connect(self):
        host = self.text
        port = 5050
        try:
            sock.connect((host, port))
        except:
            self.answer()

    def answer(self):
        self.txt_surface = FONT.render('Connection down', True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)


class Button:
    def create_button(self, surface, color, x, y, length, height, width, text, text_color):
        surface = self.draw_button(surface, color, length, height, x, y, width)
        surface = self.write_text(surface, text, text_color, length, height, x, y)
        self.rect = pygame.Rect(x, y, length, height)
        return surface

    def write_text(self, surface, text, text_color, length, height, x, y):
        font_size = int(length//len(text))
        myfont = pygame.font.SysFont("Calibri", font_size)
        mytext = myfont.render(text, 1, text_color)
        surface.blit(mytext, ((x+length/2) - mytext.get_width()/2, (y+height/2) - mytext.get_height()/2))
        return surface

    def draw_button(self, surface, color, length, height, x, y, width):
        for i in range(1, 10):
            s = pygame.Surface((length + (i * 2), height + (i * 2)))
            s.fill(color)
            alpha = (255 / (i + 2))
            if alpha <= 0:
                alpha = 1
            s.set_alpha(alpha)
            pygame.draw.rect(s, color, (x - i, y - i, length + i, height + i), width)
            surface.blit(s, (x - i, y - i))
        pygame.draw.rect(surface, color, (x, y, length, height), 0)
        pygame.draw.rect(surface, (190, 190, 190), (x, y, length, height), 1)
        return surface

    def pressed(self, mouse):
        if mouse[0] > self.rect.topleft[0]:
            if mouse[1] > self.rect.topleft[1]:
                if mouse[0] < self.rect.bottomright[0]:
                    if mouse[1] < self.rect.bottomright[1]:
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False


step = Button()
class Board:
    # создание поля
    def __init__(self, width, height):
        self.b = 0
        self.width = width
        self.height = height
        self.board = []
        self.resources1_1 = {3: 12, 4: 30, 5: 3, 6: 4}
        self.resources1_2 = {3: 12, 4: 30, 5: 3, 6: 4}
        self.resources2_1 = {3: 12, 4: 30, 5: 3, 6: 4}
        self.resources2_2 = {3: 12, 4: 30, 5: 3, 6: 4}
        self.resources3_1 = {3: 12, 4: 30, 5: 3, 6: 4}
        self.resources3_2 = {3: 12, 4: 30, 5: 3, 6: 4}
        for i in range(height):
            if i < 5 or i > 29:
                self.board.append([0] * width)
            elif 5 <= i < 10 or 24 < i <= 29:
                col = []
                for j in range(width):
                    if j < 5 or j > 57:
                        col.append(0)
                    elif 5 <= j < 20:
                        a = random.choice([0, 0, 0, 2])
                        if a == 2:
                            a = random.choice([2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 4, 4, 4])
                            if a != 2 and self.resources1_1[a] != 0:
                                self.resources1_1[a] -= 1
                            else:
                                a = 2
                        col.append(a)
                    elif 42 < j <= 57:
                        a = random.choice([0, 0, 0, 2])
                        if a == 2:
                            a = random.choice([2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 4, 4, 4])
                            if a != 2 and self.resources1_2[a] != 0:
                                self.resources1_2[a] -= 1
                            else:
                                a = 2
                        col.append(a)
                    elif 20 <= j < 33:
                        a = random.choice([0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2])
                        if a == 2:
                            a = random.choice([2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 5, 6, 6, 5, 4, 4])
                            if a != 2 and self.resources1_1[a] != 0:
                                self.resources1_1[a] -= 1
                            else:
                                a = 2
                        col.append(a)
                    elif 33 <= j < 42:
                        a = random.choice([0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2])
                        if a == 2:
                            a = random.choice([2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 5, 6, 6, 5, 4, 4])
                            if a != 2 and self.resources1_2[a] != 0:
                                self.resources1_2[a] -= 1
                            else:
                                a = 2
                        col.append(a)
                col.append(0)
                self.board.append(col)
            elif 10 <= i < 15 or 19 < i <= 24:
                col = []
                for j in range(width):
                    if j < 5 or j > 57:
                        col.append(0)
                    elif 5 <= j < 20:
                        a = random.choice([0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2])
                        if a == 2:
                            a = random.choice([2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 4, 4, 4])
                            if a != 2 and self.resources2_1[a] != 0:
                                self.resources2_1[a] -= 1
                            else:
                                a = 2
                        col.append(a)
                    elif 42 < j <= 57:
                        a = random.choice([0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2])
                        if a == 2:
                            a = random.choice([2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 4, 4, 4])
                            if a != 2 and self.resources2_2[a] != 0:
                                self.resources2_2[a] -= 1
                            else:
                                a = 2
                        col.append(a)
                    elif 20 <= j < 25:
                        a = random.choice([0, 2, 2, 2, 2, 2, 2, 2])
                        if a == 2:
                            a = random.choice([2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 4, 4, 4])
                            if a != 2 and self.resources2_1[a] != 0:
                                self.resources2_1[a] -= 1
                            else:
                                a = 2
                        col.append(a)
                    elif 37 < j <= 42:
                        a = random.choice([0, 2, 2, 2, 2, 2, 2, 2])
                        if a == 2:
                            a = random.choice([2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 4, 4, 4])
                            if a != 2 and self.resources2_2[a] != 0:
                                self.resources2_2[a] -= 1
                            else:
                                a = 2
                        col.append(a)
                    elif 25 <= j < 31:
                        a = random.choice([0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2])
                        if a == 2:
                            a = random.choice([2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 5, 6, 6, 5, 4, 4])
                            if a != 2 and self.resources2_1[a] != 0:
                                self.resources2_1[a] -= 1
                            else:
                                a = 2
                        col.append(a)
                    elif 31 <= j < 37:
                        a = random.choice([0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2])
                        if a == 2:
                            a = random.choice([2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 5, 6, 6, 5, 4, 4])
                            if a != 2 and self.resources2_2[a] != 0:
                                self.resources2_2[a] -= 1
                            else:
                                a = 2
                        col.append(a)
                col.append(0)
                self.board.append(col)
            else:
                col = []
                for j in range(width):
                    if j < 5 or j > 57:
                        col.append(0)
                    elif 5 <= j < 20:
                        a = random.choice([0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2])
                        if a == 2:
                            a = random.choice([2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 4, 4, 4])
                            if a != 2 and self.resources3_1[a] != 0:
                                self.resources3_1[a] -= 1
                            else:
                                a = 2
                        col.append(a)
                    elif 42 < j <= 57:
                        a = random.choice([0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2])
                        if a == 2:
                            a = random.choice([2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 4, 4, 4])
                            if a != 2 and self.resources3_2[a] != 0:
                                self.resources3_2[a] -= 1
                            else:
                                a = 2
                        col.append(a)
                    elif 20 <= j < 25:
                        a = random.choice([0, 2, 2, 2, 2, 2, 2, 2])
                        if a == 2:
                            a = random.choice([2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 4, 4, 4])
                            if a != 2 and self.resources3_1[a] != 0:
                                self.resources3_1[a] -= 1
                            else:
                                a = 2
                        col.append(a)
                    elif 37 < j <= 42:
                        a = random.choice([0, 2, 2, 2, 2, 2, 2, 2])
                        if a == 2:
                            a = random.choice([2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 4, 4, 4])
                            if a != 2 and self.resources3_1[a] != 0:
                                self.resources3_1[a] -= 1
                            else:
                                a = 2
                        col.append(a)
                    elif 25 <= j < 31:
                        a = random.choice([0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2])
                        if a == 2:
                            a = random.choice([2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 5, 6, 6, 5, 4, 4])
                            if a != 2 and self.resources3_1[a] != 0:
                                self.resources3_1[a] -= 1
                            else:
                                a = 2
                        col.append(a)
                    elif 31 <= j < 37:
                        a = random.choice([0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2])
                        if a == 2:
                            a = random.choice([2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 5, 6, 6, 5, 4, 4])
                            if a != 2 and self.resources3_2[a] != 0:
                                self.resources3_2[a] -= 1
                            else:
                                a = 2
                        col.append(a)
                col.append(0)
                self.board.append(col)
        self.left = 60
        self.top = 30
        self.cell_size = 30

    def load_saves(self):
        load_file = open('data/save.txt', mode='r').readlines()
        exec(load_file[0])
        exec(load_file[1])
        self.place_of_war()

    def place_of_war(self):
        field_image = load_image("frame.png")
        field = pygame.sprite.Sprite(all_sprites)
        field.image = field_image
        field.rect = field.image.get_rect()
        field.rect.x, field.rect.y = 0, 0
        for y in range(self.height):
            for x in range(self.width):
                position = (x * self.cell_size + self.left, y * self.cell_size + self.top)
                size = self.cell_size, self.cell_size
                if self.board[y][x] == 2:
                    field_image = load_image("grass.png")
                    field = pygame.sprite.Sprite(all_sprites)
                    field.image = field_image
                    field.rect = field.image.get_rect()
                    field.rect.x, field.rect.y = position[0], position[1]
                elif self.board[y][x] == 3:
                    field_image = load_image("iron.png")
                    field = pygame.sprite.Sprite(all_sprites)
                    field.image = field_image
                    field.rect = field.image.get_rect()
                    field.rect.x, field.rect.y = position[0], position[1]
                elif self.board[y][x] == 4:
                    field_image = load_image("tree.png")
                    field = pygame.sprite.Sprite(all_sprites)
                    field.image = field_image
                    field.rect = field.image.get_rect()
                    field.rect.x, field.rect.y = position[0], position[1]
                elif self.board[y][x] == 5:
                    field_image = load_image("oil.png")
                    field = pygame.sprite.Sprite(all_sprites)
                    field.image = field_image
                    field.rect = field.image.get_rect()
                    field.rect.x, field.rect.y = position[0], position[1]
                elif self.board[y][x] == 6:
                    field_image = load_image("wolfram.png")
                    field = pygame.sprite.Sprite(all_sprites)
                    field.image = field_image
                    field.rect = field.image.get_rect()
                    field.rect.x, field.rect.y = position[0], position[1]
                if y <= 10:
                    position = (30, y * 2 * self.cell_size + self.top)
                    size = self.cell_size, self.cell_size
                    pygame.draw.rect(screen, (255, 215, 0), (position, size), 1)

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self):
        Artillery(units_sprites).update(30, self.top)
        Soldier(units_sprites).update(30, self.cell_size * 2 + self.top)
        Tank(units_sprites).update(30, self.cell_size * 4 + self.top)
        MotoBrigada(units_sprites).update(30, self.cell_size * 6 + self.top)

        Forester(builds_sprites).update(30, self.cell_size * 8 + self.top)
        IronMine(builds_sprites).update(30, self.cell_size * 10 + self.top)
        OilPump(builds_sprites).update(30, self.cell_size * 12 + self.top)
        WolframMine(builds_sprites).update(30, self.cell_size * 14 + self.top)
        for y in range(self.height):
            for x in range(self.width):
                position = (x * self.cell_size + self.left, y * self.cell_size + self.top)
                size = self.cell_size, self.cell_size
                pygame.draw.rect(screen, (128, 128, 128), (position, size), 1)
                if self.board[y][x] == 100:
                    Forester(units_sprites).update(position[0], position[1])
                elif self.board[y][x] == 200:
                    IronMine(units_sprites).update(position[0], position[1])
                elif self.board[y][x] == 300:
                    OilPump(units_sprites).update(position[0], position[1])
                elif self.board[y][x] == 400:
                    WolframMine(units_sprites).update(position[0], position[1])
        step.create_button(screen, (34, 139, 34), 1700, 1010, 200, 50, 100, 'Закончить ход', (255, 255, 255))

    def on_click(self, cell):
        pass

    def get_cell(self, mouse_pos):
        cell_x = (mouse_pos[0] - self.left) // self.cell_size
        cell_y = (mouse_pos[1] - self.top) // self.cell_size
        if (cell_x < 0 or cell_x >= self.width) or (cell_y < 0 or cell_y >= self.height):
            return None
        for x in range(len(self.board)):
            for y in range(len(self.board[x])):
                if x == cell_y and y == cell_x:
                    if self.board[x][y] == 1:
                        self.board[x][y] = 2
                    elif self.board[x][y] == 0:
                        self.board[x][y] = 0
                    else:
                        for i in range(len(self.board)):
                            for j in range(len(self.board[x])):
                                if self.board[i][j] == 1:
                                    self.board[i][j] = 2
        return cell_x, cell_y

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def get_board(self):
        return self.board

    def update_board(self, board):
        self.board = board

    def save(self):
        file = open('data/save.txt', 'w')
        file.write(f'self.board = {str(self.board)}\n')
        file.write(f'step_of_user = {str(step_of_user)}')
        file.close()

    def menu(self):
        background = pygame.image.load('data/start_menu.png')
        connection = Button()
        reg = Button()
        close = Button()
        start = Button()
        save = Button()
        load = Button()
        input_box1 = InputBox(1700, 1000, 200, 32)
        input_box2 = InputBox(50, 50, 200, 32)
        input_boxes = [input_box1, input_box2]
        show = True
        while show:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.nick = open('data/cfg.txt', mode='r').readlines()[0].split()[2][1:-1]
                    if close.pressed(event.pos):
                        exit()
                    elif start.pressed(event.pos) and self.nick:
                        start.create_button(screen, (34, 139, 34), 860, 430, 200, 50, 100,
                                            'Продолжить', (255, 255, 255))
                        sock.bind((server, port))
                        sock.listen(1)
                        show = False
                        self.b = 1
                    elif save.pressed(event.pos) and self.b == 1:
                        self.save()
                        show = False
                    elif load.pressed(event.pos):
                        self.load_saves()
                        show = False
                    if reg.pressed(event.pos):
                        input_box1.register()
                    if connection.pressed(event.pos):
                        input_box2.connect()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE and self.b == 1:
                        show = False
                for box in input_boxes:
                    box.handle_event(event)

            for box in input_boxes:
                box.update()
            screen.blit(background, (0, 0))
            for box in input_boxes:
                box.draw(screen)
            close.create_button(screen, (34, 139, 34), 860, 700, 200, 50, 100, 'Выйти', (255, 255, 255))
            reg.create_button(screen, (34, 139, 34), 1450, 991, 200, 50, 100,
                              'Принять Ник', (255, 255, 255))
            connection.create_button(screen, (34, 139, 34), 265, 40, 200, 50, 100,
                              'Connect', (255, 255, 255))
            save.create_button(screen, (34, 139, 34), 860, 520, 200, 50, 100, 'Сохранить', (255, 255, 255))
            load.create_button(screen, (34, 139, 34), 860, 610, 200, 50, 100, 'Загрузить', (255, 255, 255))
            if self.b == 0:
                start.create_button(screen, (34, 139, 34), 860, 430, 200, 50, 100, 'Старт', (255, 255, 255))
            else:
                start.create_button(screen, (34, 139, 34), 860, 430, 200, 50, 100, 'Продолжить', (255, 255, 255))

            pygame.display.update()
            clock.tick(60)
        screen.fill('black')


class Build(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.left = 60
        self.top = 30
        self.cell_size = 30

    def update(self, x, y):
        cell_x = (x - self.left) // self.cell_size
        cell_y = (y - self.top) // self.cell_size
        self.rect.x = self.left + cell_x * 30
        self.rect.y = self.top + cell_y * 30


class Forester(Build):
    image = load_image('house_of_forester.png')

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Forester.image
        self.rect = self.image.get_rect()
        self.rect.x = -30
        self.rect.y = -30


class IronMine(Build):
    image = load_image('rudnik-iron.png')

    def __init__(self, *group):
        super().__init__(*group)
        self.image = IronMine.image
        self.rect = self.image.get_rect()
        self.rect.x = -30
        self.rect.y = -30


class WolframMine(Build):
    image = load_image('rudnik-wolfram.png')

    def __init__(self, *group):
        super().__init__(*group)
        self.image = WolframMine.image
        self.rect = self.image.get_rect()
        self.rect.x = -30
        self.rect.y = -30


class OilPump(Build):
    image = load_image('oil_pumpers.png')

    def __init__(self, *group):
        super().__init__(*group)
        self.image = OilPump.image
        self.rect = self.image.get_rect()
        self.rect.x = -30
        self.rect.y = -30


class Unit(pygame.sprite.Sprite):
    def __init__(self, *group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__(*group)
        self.left = 60
        self.top = 30
        self.cell_size = 30
        self.board_un = [[0] * 62 for i in range(35)]

    def update(self, x, y):
        cell_x = (x - self.left) // self.cell_size
        cell_y = (y - self.top) // self.cell_size
#            self.board_un[cell_y][cell_x] = 30
        self.rect.x = self.left + cell_x * 30
        self.rect.y = self.top + cell_y * 30


class Soldier(Unit):
    image = load_image('Sprite Of Brigada_blue.png')

    def __init__(self, *group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__(*group)
        self.image = Soldier.image
        self.rect = self.image.get_rect()
        self.rect.x = -30
        self.rect.y = -30

    def update_icon(self):
        if step_of_user % 2 == 0:
            image = load_image('Sprite Of Brigada_blue.png')
        else:
            image = load_image('Sprite Of Brigada_red.png')
        self.image = image

    def update(self, x, y):
        cell_x = (x - self.left) // self.cell_size
        cell_y = (y - self.top) // self.cell_size
        self.board_un[cell_y][cell_x] = 20


class Artillery(Unit):
    image = load_image('Artillery_blue.png')

    def __init__(self, *group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__(*group)
        self.image = Artillery.image
        self.rect = self.image.get_rect()
        self.rect.x = -30
        self.rect.y = -30

    def update_icon(self):
        if step_of_user % 2 == 0:
            image = load_image('Artillery_blue.png')
        else:
            image = load_image('Artillery_red.png')
        self.image = image

    def update(self, x, y):
        cell_x = (x - self.left) // self.cell_size
        cell_y = (y - self.top) // self.cell_size
        self.board_un[cell_y][cell_x] = 10


class Tank(Unit):
    image = load_image('tank_blue.png')

    def __init__(self, *group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__(*group)
        self.image = Tank.image
        self.rect = self.image.get_rect()
        self.rect.x = -30
        self.rect.y = -30

    def update_icon(self):
        if step_of_user % 2 == 0:
            image = load_image('tank_blue.png')
        else:
            image = load_image('tank_red.png')
        self.image = image

    def update(self, x, y):
        cell_x = (x - self.left) // self.cell_size
        cell_y = (y - self.top) // self.cell_size
        self.board_un[cell_y][cell_x] = 40


class MotoBrigada(Unit):
    image = load_image('moto_brigada_blue.png')

    def __init__(self, *group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__(*group)
        self.image = MotoBrigada.image
        self.rect = self.image.get_rect()
        self.rect.x = -30
        self.rect.y = -30

    def update_icon(self):
        if step_of_user % 2 == 0:
            image = load_image('moto_brigada_blue.png')
        else:
            image = load_image('moto_brigada_red.png')
        self.image = image

    def update(self, x, y):
        cell_x = (x - self.left) // self.cell_size
        cell_y = (y - self.top) // self.cell_size
        self.board_un[cell_y][cell_x] = 30
        # for i in self.board_un:
        #     print(i)

if __name__ == '__main__':
    red = Red()
    blue = Blue()
    fps = 60  # количество кадров в секунду
    clock = pygame.time.Clock()
    pygame.init()
    pygame.display.set_caption('Victory is ours')
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    board = Board(62, 35)
    board.menu()
    board.set_view(60, 30, 30)
    running = True
    soldat = Soldier(units_sprites)
    artil = Artillery(units_sprites)
    tank = Tank(units_sprites)
    moto = MotoBrigada(units_sprites)
    board.place_of_war()    #    self.rect.x = self.left + cell_x * 30
    #    self.rect.y = self.top + cell_y * 30

    brd = board.get_board()
    d = 0
    step.create_button(screen, (34, 139, 34), 1700, 1010, 200, 50, 100, 'Закончить ход', (255, 255, 255))
    font = pygame.font.Font(None, 30)
    while running:
        if step_of_user % 2 == 0:
            resource = blue.res()
        else:
            resource = red.res()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                board.save()
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                board.get_click(event.pos)
                if event.button == 1:
                    if 30 <= x <= 60 and 30 <= y <= 60:
                        d = 10
                    if 90 <= y <= 120 and 30 <= x <= 60:
                        d = 20
                    if 150 <= y <= 180 and 30 <= x <= 60:
                        d = 30
                    if 210 <= y <= 240 and 30 <= x <= 60:
                        d = 40
                    if 270 <= y <= 300 and 30 <= x <= 60:
                        d = 100
                    if 330 <= y <= 360 and 30 <= x <= 60:
                        d = 200
                    if 390 <= y <= 420 and 30 <= x <= 60:
                        d = 300
                    if 450 <= y <= 480 and 30 <= x <= 60:
                        d = 400
                if event.button == 3:
                    cell_x = (x - 60) // 30
                    cell_y = (y - 30) // 30
                    if brd[cell_y][cell_x] in [1, 2, 3, 4, 5, 6]:
                        if d == 10 and resource[4] >= 2 and resource[3] >= 2:
                            artil.update(x, y)
                            resource[4] -= 1
                            resource[3] -= 2
                        elif d == 20 and resource[4] >= 2 and resource[3] >= 1:
                            soldat.update(x, y)
                            resource[4] -= 1
                            resource[3] -= 1
                        elif d == 30 and resource[3] >= 3 and resource[5] >= 1 and resource[6] >= 1:
                            tank.update(x, y)
                            resource[3] -= 3
                            resource[5] -= 1
                            resource[6] -= 1
                        elif d == 40 and resource[3] >= 2 and resource[4] >= 1 and resource[5] >= 1:
                            moto.update(x, y)
                            resource[4] -= 1
                            resource[3] -= 2
                            resource[5] -= 1
                        elif d == 100 and brd[cell_y][cell_x] == 4 and resource[4] >= 1:
                            brd[cell_y][cell_x] = 100
                            resource[4] += 2
                        elif d == 200 and brd[cell_y][cell_x] == 3 and resource[4] >= 2:
                            brd[cell_y][cell_x] = 200
                            resource[3] += 1
                            resource[4] -= 1
                        elif d == 400 and brd[cell_y][cell_x] == 6 and resource[3] >= 2 and resource[5] >= 1:
                            brd[cell_y][cell_x] = 400
                            resource[6] += 1
                            resource[4] -= 2
                            resource[5] -= 1
                        elif d == 300 and brd[cell_y][cell_x] == 5 and resource[4] >= 3 and resource[3] >= 2:
                            brd[cell_y][cell_x] = 300
                            resource[5] += 1
                            resource[4] -= 2
                            resource[3] -= 2
                        board.update_board(brd)
                if step.pressed(event.pos):
                    step_of_user += 1
                    artil.update_icon()
                    soldat.update_icon()
                    tank.update_icon()
                    moto.update_icon()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    board.save()
                    board.menu()
        screen.fill((42, 92, 3))
        pygame.draw.rect(screen, (10, 96, 150), (60, 30, 1860, 1050))
        text_f = font.render(str(resource[4]), True, (255, 0, 0))
        text_i = font.render(str(resource[3]), True, (255, 0, 0))
        text_o = font.render(str(resource[5]), True, (255, 0, 0))
        text_w = font.render(str(resource[6]), True, (255, 0, 0))
        screen.blit(text_f, (60, 270))
        screen.blit(text_i, (60, 330))
        screen.blit(text_o, (60, 390))
        screen.blit(text_w, (60, 450))
        all_sprites.draw(screen)
        board.render()
        builds_sprites.draw(screen)
        units_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(60)
        board.save()
    pygame.quit()