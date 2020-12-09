import pygame
import random


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * (width - 1) for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30
        for i in self.board:
            i.append(2)
            random.shuffle(i)

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self):
        for y in range(self.height):
            for x in range(self.width):
                position = (x * self.cell_size + self.left, y * self.cell_size + self.top)
                size = (self.cell_size, self.cell_size)
                pygame.draw.rect(screen, 'white', (position, size), 1)
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

if __name__ == '__main__':
    fps = 60  # количество кадров в секунду
    clock = pygame.time.Clock()
    pygame.init()
    pygame.display.set_caption('Victory is ours')
    size = width, height = 800, 400
    screen = pygame.display.set_mode(size)
    board = Board(14, 7)
    board.set_view(100, 50, 50)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.get_click(event.pos)
        board.render()
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()