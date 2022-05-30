import pygame
import time

WHITE = (255, 255, 255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return
        screen.fill(WHITE)
        pygame.draw.lines(screen, BLUE, True, [(0, 0), (100, 100), (200, 0)], 1)

        pygame.display.update()

        time.sleep(0.1)

if __name__ == '__main__':
    main()
