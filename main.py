import pygame
import random
from pygame.locals import *

pygame.init()


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
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30
        for i in range(len(self.board)):
            self.board[i].append(2)
            random.shuffle(self.board[i])

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
                if self.board[y][x] == 0:
                    pygame.draw.rect(screen, (0, 0, 0), ((position[0] + 1, position[1] + 1),
                                                         (size[0] - 2, size[1] - 2)), 0)
                elif self.board[y][x] == 2:
                    pygame.draw.rect(screen, (0, 255, 0), ((position[0] + 1, position[1] + 1),
                                                           (size[0] - 2, size[1] - 2)), 0)
                else:
                    pygame.draw.rect(screen, (255, 255, 255), ((position[0] + 1, position[1] + 1),
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
                        self.board[x][y] = 0
                    elif self.board[x][y] == 2:
                        self.board[x][y] = 2
                    else:
                        self.board[x][y] = 1
        return cell_x, cell_y

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def menu(self):
        background = pygame.image.load('orange.bmp.jpg')
        close = Button()
        show = True
        while show:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if close.pressed(event.pos):
                        exit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        show = False
            screen.blit(background, (0, 0))
            close.create_button(screen, (34, 139, 34), 100, 100, 100, 100, 100, 'Выйти', (255, 255, 255))
            pygame.display.update()
            clock.tick(60)
        screen.fill('black')


if __name__ == '__main__':
    fps = 60  # количество кадров в секунду
    clock = pygame.time.Clock()
    pygame.init()
    pygame.display.set_caption('Victory is ours')
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    board = Board(38, 21)
    board.set_view(20, 30, 50)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.get_click(event.pos)
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    board.menu()
        board.render()
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
