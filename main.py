import os
import random
import sys
import socket
from pygame.locals import *
import pygame
pygame.init()
b = 2
you = ''
c = 0
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
# 500 - баррак
step_of_person = 0
all_sprites = pygame.sprite.Group()
units_sprites = pygame.sprite.Group()
builds_sprites = pygame.sprite.Group()
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT = pygame.font.Font(None, 32)
sock = socket.socket()
host = ''
port = 5050
brd = None
client = None
pygame.mixer.music.load('data/Agression.mp3')
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)


class Red:
    # подсчёт ресурсов красного игрока
    def __init__(self):
        # self.resource = {3: 0, 4: 1, 5: 0, 6: 0}
        self.resource = {3: 100, 4: 100, 5: 100, 6: 100}

    def res(self):
        return self.resource


class Blue:
    # подсчёт ресурсов синего игрока
    def __init__(self):
        # self.resource = {3: 0, 4: 1, 5: 0, 6: 0}
        self.resource = {3: 100, 4: 100, 5: 100, 6: 100}

    def res(self):
        return self.resource


def load_image(name, colorkey=None):
    # загрузка изображений
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.con = 0
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False
        nick = open('data/cfg.txt', mode='r').readlines()[0].split()[2]
        if x == 1700:
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
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                print(self.text)
                self.txt_surface = FONT.render(self.text, True, self.color)

    def register(self):
        nick = open('data/cfg.txt', mode='r').readlines()[0].split()
        nick[2] = "'" + self.text + "'"
        f = open('data/cfg.txt', mode='w')
        f.write(' '.join(nick))

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def connect_to(self):
        con = str(self.text)
        port = 5050
        try:
            you = 'client'
            sock.connect((con, port))
            return (1, False)
        except:
            self.txt_surface = FONT.render('Connection lost', True, self.color)


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
        self.you = ''
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
        self.board[16][12], self.board[16][13], self.board[17][12], self.board[17][13] = 1000, '--', '--', '--'
        self.board[16][49], self.board[16][50], self.board[17][49], self.board[17][50] = 2000, '-|', '-|', '-|'

    def load_saves(self):
        # загрузка сохранений
        load_file = open('data/save.txt', mode='r').read()
        exec(load_file)
        self.place_of_war()

    def place_of_war(self):
        # загрузка спрайтов для поля
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
                elif self.board[y][x] == 1000:
                    field_image = load_image("main_build_blue.png")
                    field = pygame.sprite.Sprite(all_sprites)
                    field.image = field_image
                    field.rect = field.image.get_rect()
                    field.rect.x, field.rect.y = position[0], position[1]
                elif self.board[y][x] == 2000:
                    field_image = load_image("main_build_red.png")
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
        # обновление позиций построек
        Artillery(units_sprites).update(30, self.top)
        Soldier(units_sprites).update(30, self.cell_size * 2 + self.top)
        Tank(units_sprites).update(30, self.cell_size * 4 + self.top)
        MotoBrigada(units_sprites).update(30, self.cell_size * 6 + self.top)

        Forester(builds_sprites).update(30, self.cell_size * 8 + self.top)
        IronMine(builds_sprites).update(30, self.cell_size * 10 + self.top)
        OilPump(builds_sprites).update(30, self.cell_size * 12 + self.top)
        WolframMine(builds_sprites).update(30, self.cell_size * 14 + self.top)
        Barrak(builds_sprites).update(0, self.cell_size * 16 + self.top)
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
                elif self.board[y][x] == 500:
                    Barrak(units_sprites).update(position[0], position[1])
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
                    if self.board[x][y] == 0:
                        self.board[x][y] = 0
        return cell_x, cell_y

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def get_board(self):
        return self.board

    def update_board(self, board):
        self.board = board

    def menu(self):
        # главное меню игры
        background = pygame.image.load('data/start_menu.png')
        reg = Button()
        ip_conn = Button()
        close = Button()
        start = Button()
        cont = Button()
        save = Button()
        load = Button()
        input_box1 = InputBox(1700, 1000, 200, 32)
        ip = InputBox(50, 10, 200, 32)
        input_boxes = [input_box1, ip]
        show = True
        while show:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.nick = open('data/cfg.txt', mode='r').readlines()[0].split()[2][1:-1]
                    if close.pressed(event.pos):
                        exit()
                    elif start.pressed(event.pos) and self.nick:
                        cont.create_button(screen, (34, 139, 34), 860, 430, 200, 50, 100,
                                            'Продолжить', (255, 255, 255))
                        sock.bind((host, port))
                        sock.listen(1)
                        conn, addr = sock.accept()
                        conn.send((f'self.board = {str(self.board)}').encode('utf-8'))
                        client = conn
                        show = False
                        self.you = 'server'
                        self.b = 1
                    elif save.pressed(event.pos) and self.b == 1:
                        file = open('data/save.txt', 'w')
                        file.write(f'self.board = {str(self.board)}')
                        file.close()
                        show = False
                    elif load.pressed(event.pos):
                        self.load_saves()
                        show = False
                    if reg.pressed(event.pos):
                        input_box1.register()
                    if ip_conn.pressed(event.pos):
                        try:
                            self.b, show = ip.connect_to()
                            self.you = 'client'
                        except:
                            continue
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
            ip_conn.create_button(screen, (34, 139, 34), 275, 12, 200, 50, 100,
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

    def get_you(self):
        return self.you


class Build(pygame.sprite.Sprite):
    # создание построек
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


class Barrak(Build):
    image = load_image('barracks.png')

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Barrak.image
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
    # создание юнитов
    def __init__(self, *group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__(*group)
        self.left = 60
        self.top = 30
        self.cell_size = 30
        self.board_un = [[0] * 62 for i in range(35)]

    def update(self, x, y, n=0):
        cell_x = (x - self.left) // self.cell_size
        cell_y = (y - self.top) // self.cell_size
        if step_of_person == 0 and self.board_un[cell_y][cell_x] == 0:
            self.board_un[cell_y][cell_x] = [int(str(n) + '0'), 1]
        elif step_of_person == 1 and self.board_un[cell_y][cell_x] == 0:
            self.board_un[cell_y][cell_x] = [int(str(n) + '1'), 1]

    def get_board(self):
        return self.board_un

    def select(self, x, y):
        cell_x = (x - self.left) // self.cell_size
        cell_y = (y - self.top) // self.cell_size
        if self.board_un[cell_y][cell_x] != 0:
            return (x, y)
        else:
            return (-30, -30)

    def update_board(self, brd_un):
        self.board_un = brd_un

    def render(self):
        for y in range(35):
            for x in range(62):
                position = (x * self.cell_size + self.left, y * self.cell_size + self.top)
                if self.board_un[y][x] == 0:
                    number_of_unit = '000'
                else:
                    number_of_unit = str(self.board_un[y][x][0])
                if int(number_of_unit[0:2]) == 40 and int(number_of_unit[2]) == 0:
                    field_image = load_image('moto_brigada_blue.png')
                    field = pygame.sprite.Sprite(units_sprites)
                    field.image = field_image
                    field.rect = field.image.get_rect()
                    field.rect.x, field.rect.y = position[0], position[1]
                elif int(number_of_unit[0:2]) == 40 and int(number_of_unit[2]) == 1:
                    field_image = load_image('moto_brigada_red.png')
                    field = pygame.sprite.Sprite(units_sprites)
                    field.image = field_image
                    field.rect = field.image.get_rect()
                    field.rect.x, field.rect.y = position[0], position[1]
                if int(number_of_unit[0:2]) == 20 and int(number_of_unit[2]) == 0:
                    field_image = load_image('Sprite Of Brigada_blue.png')
                    field = pygame.sprite.Sprite(units_sprites)
                    field.image = field_image
                    field.rect = field.image.get_rect()
                    field.rect.x, field.rect.y = position[0], position[1]
                elif int(number_of_unit[0:2]) == 20 and int(number_of_unit[2]) == 1:
                    field_image = load_image('Sprite Of Brigada_red.png')
                    field = pygame.sprite.Sprite(units_sprites)
                    field.image = field_image
                    field.rect = field.image.get_rect()
                    field.rect.x, field.rect.y = position[0], position[1]
                if int(number_of_unit[0:2]) == 10 and int(number_of_unit[2]) == 0:
                    field_image = load_image('Artillery_blue.png')
                    field = pygame.sprite.Sprite(units_sprites)
                    field.image = field_image
                    field.rect = field.image.get_rect()
                    field.rect.x, field.rect.y = position[0], position[1]
                elif int(number_of_unit[0:2]) == 10 and int(number_of_unit[2]) == 1:
                    field_image = load_image('Artillery_red.png')
                    field = pygame.sprite.Sprite(units_sprites)
                    field.image = field_image
                    field.rect = field.image.get_rect()
                    field.rect.x, field.rect.y = position[0], position[1]
                if int(number_of_unit[0:2]) == 30 and int(number_of_unit[2]) == 0:
                    field_image = load_image('tank_blue.png')
                    field = pygame.sprite.Sprite(units_sprites)
                    field.image = field_image
                    field.rect = field.image.get_rect()
                    field.rect.x, field.rect.y = position[0], position[1]
                elif int(number_of_unit[0:2]) == 30 and int(number_of_unit[2]) == 1:
                    field_image = load_image('tank_red.png')
                    field = pygame.sprite.Sprite(units_sprites)
                    field.image = field_image
                    field.rect = field.image.get_rect()
                    field.rect.x, field.rect.y = position[0], position[1]


class Soldier(Unit):
    image = load_image('Sprite Of Brigada.png')

    def __init__(self, *group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__(*group)
        self.image = Soldier.image
        self.rect = self.image.get_rect()
        self.rect.x = 30
        self.rect.y = 90


class Artillery(Unit):
    image = load_image('Artillery.png')

    def __init__(self, *group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__(*group)
        self.image = Artillery.image
        self.rect = self.image.get_rect()
        self.rect.x = 30
        self.rect.y = 30


class Tank(Unit):
    image = load_image('tank.png')

    def __init__(self, *group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__(*group)
        self.image = Tank.image
        self.rect = self.image.get_rect()
        self.rect.x = 30
        self.rect.y = 150


class MotoBrigada(Unit):
    image = load_image('moto_brigada.png')

    def __init__(self, *group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__(*group)
        self.image = MotoBrigada.image
        self.rect = self.image.get_rect()
        self.rect.x = 30
        self.rect.y = 210


if __name__ == '__main__':
    fps = 60  # количество кадров в секунду
    clock = pygame.time.Clock()
    pygame.init()
    pygame.display.set_caption('Victory is ours')
    screen = pygame.display.set_mode((1920, 1080))
    board = Board(62, 35)
    board.menu()
    brd = None
    you = board.get_you()
    if you == 'client':
        f = sock.recv(10240)
        print(f)
        change_map = open('data/save.txt', mode='w')
        change_map.write(f.decode('utf-8'))
        change_map.close()
        board.load_saves()
    brd = board.get_board()
    board.set_view(60, 30, 30)
    running = True
    soldat = Soldier(units_sprites)
    artil = Artillery(units_sprites)
    tank = Tank(units_sprites)
    moto = MotoBrigada(units_sprites)
    blue = Blue()
    red = Red()
    board.place_of_war()
    unit = Unit()
    unit.update_board([[0] * 62 for i in range(35)])
    brd_un = unit.get_board()
    d = 0
    font = pygame.font.Font(None, 30)
    font2 = pygame.font.Font(None, 40)
    position = (-30, -30)
    if step_of_person == 0:
        resource = blue.res()
    else:
        resource = red.res()
    step.create_button(screen, (34, 139, 34), 1700, 1010, 200, 50, 100, 'Закончить ход', (255, 255, 255))
    text_f = font.render(str(resource[4]), True, (255, 0, 0))
    text_i = font.render(str(resource[3]), True, (255, 0, 0))
    text_o = font.render(str(resource[5]), True, (255, 0, 0))
    text_w = font.render(str(resource[6]), True, (255, 0, 0))
    remove_resource = {3: 0, 4: 0, 5: 0, 6: 0}
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
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
                    if 510 <= y <= 540 and 30 <= x <= 60:
                        d = 500
                    if x >= 60 and y >= 30:
                        cell_x = (x - 60) // 30
                        cell_y = (y - 30) // 30
                        position = unit.select(cell_x * 30 + 60, cell_y * 30 + 30)
                        d = 0
                if event.button == 3:
                    cell_x = (x - 60) // 30
                    cell_y = (y - 30) // 30
                    if position != (-30, -30):
                        brd_un = unit.get_board()
                        pos_x, pos_y = (position[0] - 60) // 30, (position[1] - 30) // 30
                        if step_of_person == 0 and brd[cell_y][cell_x] in [2000, '-|']:
                            b = 0
                        elif step_of_person == 1 and brd[cell_y][cell_x] in [1000, '--']:
                            b = 1
                        if (2 >= cell_y - pos_y >= -2) and (2 >= cell_x - pos_x >= -2) and (brd[cell_y][cell_x] == 2)\
                                and str(brd_un[pos_y][pos_x][0])[-1] == str(step_of_person)\
                                and brd_un[pos_y][pos_x][-1] == 1:
                            brd_un[cell_y][cell_x] = [brd_un[pos_y][pos_x][0], 0]
                            brd_un[pos_y][pos_x] = 0
                            unit.update_board(brd_un)
                            for sprite in units_sprites:
                                if sprite.rect.x == position[0] and sprite.rect.y == position[1]:
                                    sprite.kill()
                                if str(brd_un[cell_y][cell_x])[-1] == str(step_of_person) and \
                                        sprite.rect.x == cell_x * 30 + 60 and sprite.rect.y == cell_y * 30 + 30:
                                    sprite.kill()
                            position = (-30, -30)
                    if brd[cell_y][cell_x] in [1, 2, 111, 112, 3, 4, 5, 6, 4000, 4001, 5001, 5000, 6000, 6001, 3000,
                                               3001]:
                        # юниты
                        brd_un = unit.get_board()
                        if ((step_of_person == 0 and (5 >= cell_x - 12 >= -5 or 5 >= cell_x - 13 >= -5) and
                             (5 >= cell_y - 17 >= -5 or 5 >= cell_y - 16 >= -5)) or
                            (step_of_person == 1 and (5 >= cell_x - 49 >= -5 or 5 >= cell_x - 50 >= -5))
                            and (5 >= cell_y - 17 >= -5 or 5 >= cell_y - 16 >= -5)) \
                                or brd[cell_y][cell_x] == step_of_person + 111:
                            if d == 10 and resource[4] >= 1 and resource[3] >= 2 and resource[4] > remove_resource[4] \
                                    and resource[3] > remove_resource[3] and brd_un[cell_y][cell_x] == 0:
                                unit.update(x, y, 10)
                                resource[4] -= 1
                                resource[3] -= 2
                                text_f = font.render(str(resource[4]), True, (255, 0, 0))
                                text_i = font.render(str(resource[3]), True, (255, 0, 0))
                            elif d == 20 and resource[4] >= 1 and resource[3] >= 1 and resource[4] > remove_resource[4]\
                                    and resource[3] > remove_resource[3] and brd_un[cell_y][cell_x] == 0:
                                unit.update(x, y, 20)
                                resource[4] -= 1
                                resource[3] -= 1
                                text_f = font.render(str(resource[4]), True, (255, 0, 0))
                                text_i = font.render(str(resource[3]), True, (255, 0, 0))
                            elif d == 30 and resource[3] >= 3 and resource[5] >= 1 and resource[6] >= 1 \
                                    and resource[3] > remove_resource[3] and resource[5] > remove_resource[5] \
                                    and resource[6] > remove_resource[6] and brd_un[cell_y][cell_x] == 0:
                                unit.update(x, y, 30)
                                resource[3] -= 3
                                resource[5] -= 1
                                resource[6] -= 1
                                text_i = font.render(str(resource[3]), True, (255, 0, 0))
                                text_o = font.render(str(resource[5]), True, (255, 0, 0))
                                text_w = font.render(str(resource[6]), True, (255, 0, 0))
                            elif d == 40 and resource[3] >= 2 and resource[4] > 1 and resource[5] >= 1 \
                                    and resource[3] > remove_resource[3] and resource[5] > remove_resource[5] \
                                    and resource[4] > remove_resource[4] and brd_un[cell_y][cell_x] == 0:
                                unit.update(x, y, 40)
                                resource[4] -= 1
                                resource[3] -= 2
                                resource[5] -= 1
                                text_f = font.render(str(resource[4]), True, (255, 0, 0))
                                text_i = font.render(str(resource[3]), True, (255, 0, 0))
                                text_o = font.render(str(resource[5]), True, (255, 0, 0))
                            elif d == 500 and resource[4] >= 2 and resource[3] >= 2 \
                                    and resource[4] > remove_resource[4] + 1 and resource[3] >= remove_resource[3]\
                                    and brd[cell_y + 1][cell_x] in [2, 1, '--', '-|', 1000, 2000, 111, 112] and\
                                    brd[cell_y][cell_x + 1] in [2, 1, '--', '-|', 1000, 2000, 111, 112]\
                                    and brd[cell_y + 1][cell_x + 1] in [2, 1, '--', '-|', 1000, 2000, 111, 112]:
                                brd[cell_y][cell_x], brd[cell_y + 1][cell_x + 1], brd[cell_y + 1][cell_x],\
                                brd[cell_y][cell_x + 1] = 500, '-', '-', '-'
                                for i in range(10):
                                    for j in range(10):
                                        if brd[cell_y - 4 + i][cell_x - 4 + j] == 2:
                                            brd[cell_y - 4 + i][cell_x - 4 + j] = 111 + step_of_person
                                        elif brd[cell_y - 4 + i][cell_x - 4 + j] in [3, 4, 5, 6]:
                                            brd[cell_y - 4 + i][cell_x - 4 + j] = \
                                                int(str(brd[cell_y - 4 + i][cell_x - 4 + j]) +
                                                    '00' + str(step_of_person))
                                remove_resource[4] += 2
                                remove_resource[3] += 2
                            elif d == 100 and int(str(brd[cell_y][cell_x])[0]) == 4 and resource[4] > 0 \
                                    and resource[4] > remove_resource[4]:
                                brd[cell_y][cell_x] = 100
                                remove_resource[4] -= 3
                                remove_resource[4] += 1
                            elif d == 200 and int(str(brd[cell_y][cell_x])[0]) == 3 and resource[4] > 1 \
                                    and resource[4] > remove_resource[4] + 1 and resource[3] >= remove_resource[3]:
                                brd[cell_y][cell_x] = 200
                                remove_resource[3] -= 1
                                remove_resource[4] += 1
                            elif d == 400 and int(str(brd[cell_y][cell_x])[0]) == 6 and resource[3] >= 2 and \
                                    resource[5] >= 1 and resource[3] >= remove_resource[3] and \
                                    resource[5] >= remove_resource[5]:
                                brd[cell_y][cell_x] = 400
                                remove_resource[6] -= 1
                                remove_resource[3] += 2
                                remove_resource[5] += 1
                            elif d == 300 and int(str(brd[cell_y][cell_x])[0]) == 5 and resource[4] >= 2 and \
                                    resource[3] >= 2 and resource[4] > remove_resource[4] + 1 and \
                                    resource[3] >= remove_resource[3]:
                                brd[cell_y][cell_x] = 300
                                remove_resource[5] -= 1
                                remove_resource[4] += 2
                                remove_resource[3] += 2
                            # добыча ресурсов
                        if int(str(brd[cell_y][cell_x])[-1]) == step_of_person:
                            if d == 100 and int(str(brd[cell_y][cell_x])[0]) == 4 and resource[4] > 0 \
                                    and resource[4] > remove_resource[4]:
                                brd[cell_y][cell_x] = 100
                                remove_resource[4] -= 3
                                remove_resource[4] += 1
                            elif d == 200 and int(str(brd[cell_y][cell_x])[0]) == 3 and resource[4] > 1 \
                                    and resource[4] > remove_resource[4] + 1 and resource[3] >= remove_resource[3]:
                                brd[cell_y][cell_x] = 200
                                remove_resource[3] -= 1
                                remove_resource[4] += 1
                            elif d == 400 and int(str(brd[cell_y][cell_x])[0]) == 6 and resource[3] >= 2 and \
                                    resource[5] >= 1 and resource[3] >= remove_resource[3] and \
                                    resource[5] >= remove_resource[5]:
                                brd[cell_y][cell_x] = 400
                                remove_resource[6] -= 1
                                remove_resource[3] += 2
                                remove_resource[5] += 1
                            elif d == 300 and int(str(brd[cell_y][cell_x])[0]) == 5 and resource[4] >= 2 and \
                                    resource[3] >= 2 and resource[4] > remove_resource[4] + 1 and \
                                    resource[3] >= remove_resource[3]:
                                brd[cell_y][cell_x] = 300
                                remove_resource[5] -= 1
                                remove_resource[4] += 2
                                remove_resource[3] += 2
                        unit.render()
                        board.update_board(brd)
                if step.pressed(event.pos):
                    for x in resource.keys():
                        resource[x] -= remove_resource[x]
                    for y in brd_un:
                        for z in y:
                            if z != 0:
                                if z[-1] == 0:
                                    z[-1] = 1
                    unit.update_board(brd_un)
                    if step_of_person == 0:
                        step_of_person = 1
                        resource = red.res()
                    else:
                        step_of_person = 0
                        resource = blue.res()
                    remove_resource = {3: 0, 4: 0, 5: 0, 6: 0}
                    text_f = font.render(str(resource[4]), True, (255, 0, 0))
                    text_i = font.render(str(resource[3]), True, (255, 0, 0))
                    text_o = font.render(str(resource[5]), True, (255, 0, 0))
                    text_w = font.render(str(resource[6]), True, (255, 0, 0))
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    board.menu()
        pygame.draw.rect(screen, (10, 96, 150), (60, 30, 1860, 1050))
        screen.blit(text_f, (60, 270))
        screen.blit(text_i, (60, 330))
        screen.blit(text_o, (60, 390))
        screen.blit(text_w, (60, 450))
        all_sprites.draw(screen)
        if step_of_person == 0:
            screen.blit(font2.render('Xод синих', True, (0, 0, 255)), (1700, 0))
            # if you == 'server':
            #     new = board.get_board()
            #     client.send()
        else:
            screen.blit(font2.render('Xод красных', True, (255, 0, 0)), (1700, 0))
        if b == 0:
            screen.fill('blue')
        elif b == 1:
            screen.fill('red')
        board.render()
        builds_sprites.draw(screen)
        units_sprites.draw(screen)
        pygame.draw.rect(screen, 'white', (position, (30, 30)), 2)
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()