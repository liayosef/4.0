import pygame
import numpy as np

# Constants
WINDOW_WIDTH = 928
WINDOW_HEIGHT = 620
RED = (255, 0, 0)
BLUE = (0, 0, 160)
GameBord = np.array([[1,2,3,4,5],[1,2,3,4,5]])
IMAGE = "Capture1.PNG"
Finish = False


pygame.init()
size = (WINDOW_WIDTH, WINDOW_HEIGHT)
screen = pygame.display.set_mode(size)
img = pygame.image.load(IMAGE)
screen.blit(img,(0,0))
pygame.display.flip()
while not Finish:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Finish = True

pygame.quit()