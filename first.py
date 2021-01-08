import os
import random
import sys
from pygame.locals import *
import pygame
pygame.init()
c = 0
# 0 - вода
# 1 - выделенная клетка
# 2 - земля
# 3 - железо(6)
# 4 - дерево(10)
# 5 - нефть(4)
# 6 - вольфрам(3)
# 9 - артиллерия
# 10 - пехота
# 20 - мотопехота
# 30 - танк
# 40 - самолёт
# 50 - вертолёт
all_sprites = pygame.sprite.Group()
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT = pygame.font.Font(None, 32)
pygame.mixer.music.load('data/Егор Летов - Моя оборона.mp3')
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


class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False
        nick = open('data/cfg.txt', mode='r').readlines()[0].split()[2]
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


class Board:
    # создание поля
    def __init__(self, width, height):
        self.b = 0
        self.width = width
        self.height = height
        self.board = []
        self.resources1_1 = {3: 7, 4: 30, 5: 3, 6: 4}
        self.resources1_2 = {3: 7, 4: 30, 5: 3, 6: 4}
        self.resources2_1 = {3: 7, 4: 30, 5: 3, 6: 4}
        self.resources2_2 = {3: 7, 4: 30, 5: 3, 6: 4}
        self.resources3_1 = {3: 7, 4: 30, 5: 3, 6: 4}
        self.resources3_2 = {3: 7, 4: 30, 5: 3, 6: 4}
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

    def place_of_war(self):
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
        screen.fill((42, 92, 3))
        pygame.draw.rect(screen, (10, 96, 150), (60, 30, 1860, 1050))
        for y in range(self.height):
            for x in range(self.width):
                position = (x * self.cell_size + self.left, y * self.cell_size + self.top)
                size = self.cell_size, self.cell_size
                pygame.draw.rect(screen, (128, 128, 128), (position, size), 1)
        Artillery(all_sprites).update(30, self.top)
        Soldier(all_sprites).update(30, self.cell_size * 2 + self.top)

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
                        self.board[x][y] = 1
        return cell_x, cell_y

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def menu(self):
        background = pygame.image.load('data/start_menu.png')
        reg = Button()
        close = Button()
        start = Button()
        save = Button()
        load = Button()
        input_box1 = InputBox(1700, 1000, 200, 32)
        input_boxes = [input_box1]
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
                        show = False
                        self.b = 1
                    elif save.pressed(event.pos) and self.b == 1:
                        file = open('data/save.txt', 'w')
                        for x in self.board:
                            file.write(str(x) + '\n')
                        file.close()
                        show = False
                    elif load.pressed(event.pos):
                        pass
                    if reg.pressed(event.pos):
                        input_box1.register()

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
            save.create_button(screen, (34, 139, 34), 860, 520, 200, 50, 100, 'Сохранить', (255, 255, 255))
            load.create_button(screen, (34, 139, 34), 860, 610, 200, 50, 100, 'Загрузить', (255, 255, 255))
            if self.b == 0:
                start.create_button(screen, (34, 139, 34), 860, 430, 200, 50, 100, 'Старт', (255, 255, 255))
            else:
                start.create_button(screen, (34, 139, 34), 860, 430, 200, 50, 100, 'Продолжить', (255, 255, 255))

            pygame.display.update()
            clock.tick(60)
        screen.fill('black')


class Unit(pygame.sprite.Sprite):
    def __init__(self, *group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__(*group)
        self.left = 60
        self.top = 30
        self.cell_size = 30

    def update(self, x, y):
        cell_x = (x - self.left) // self.cell_size
        cell_y = (y - self.top) // self.cell_size
        self.rect.x = self.left + cell_x * 30
        self.rect.y = self.top + cell_y * 30


class Soldier(Unit):
    image = load_image('Sprite Of Brigada.png')

    def __init__(self, *group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__(*group)
        self.image = Soldier.image
        self.rect = self.image.get_rect()
        self.rect.x = -30
        self.rect.y = -30


class Artillery(Unit):
    image = load_image('Artillery.png')

    def __init__(self, *group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__(*group)
        self.image = Artillery.image
        self.rect = self.image.get_rect()
        self.rect.x = -30
        self.rect.y = -30


if __name__ == '__main__':
    fps = 60  # количество кадров в секунду
    clock = pygame.time.Clock()
    pygame.init()
    pygame.display.set_caption('Victory is ours')
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    board = Board(62, 35)
    board.menu()
    board.set_view(60, 30, 30)
    running = True
    soldat = Soldier(all_sprites)
    artil = Artillery(all_sprites)
    board.place_of_war()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if event.button == 1:
                    board.get_click(event.pos)
                    if x >= 60 and y >= 30:
                        artil.update(x, y)
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    board.menu()
        board.render()
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()