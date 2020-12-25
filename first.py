import random
from pygame.locals import *
import pygame
pygame.init()
# 0 - вода
# 1 - выделенная клетка
# 2 - земля
# 3 - железо
# 4 - дерево
# 5 - нефть
# 6 -
# 7 -
# 8 -
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
        self.color = {0: (0, 0, 255), 1: (255, 255, 255), 2: (0, 255, 0)}
        for i in range(height):
            if i < 5 or i > 29:
                self.board.append([0] * width)
            elif 5 <= i < 10 or 24 < i <= 29:
                col = []
                for j in range(width):
                    if j < 5 or j > 57:
                        col.append(0)
                    elif 5 <= j < 20 or 42 < j <= 57:
                        col.append(random.choice([0, 0, 0, 0, 2]))
                    elif 5 <= j < 20 or 42 < j <= 57:
                        col.append(random.choice([0, 2]))
                    else:
                        col.append(random.choice([0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]))
                self.board.append(col)
            else:
                col = []
                for j in range(width):
                    if j < 5 or j > 57:
                        col.append(0)
                    elif 5 <= j < 20 or 42 < j <= 57:
                        col.append(random.choice([0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]))
                    elif 20 <= j < 25 or 37 < j <= 42:
                        col.append(random.choice([0, 2, 2, 2, 2, 2, 2, 2]))
                    else:
                        col.append(random.choice([0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]))
                self.board.append(col)
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self):
        for y in range(self.height):
            for x in range(self.width):
                position = (x * self.cell_size + self.left, y * self.cell_size + self.top)
                size = self.cell_size, self.cell_size
                pygame.draw.rect(screen, (128, 128, 128), (position, size), 1)
                pygame.draw.rect(screen, self.color[int(self.board[y][x])], ((position[0] + 1, position[1] + 1),
                                                                             (size[0] - 2, size[1] - 2)), 0)

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
    pass


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
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    board.get_click(event.pos)
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    board.menu()
        board.render()
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()