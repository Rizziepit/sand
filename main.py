import sys
import pygame

from sand.render import Canvas


pygame.init()
canvas = Canvas(800, 600)
clock = pygame.time.Clock()

while True:
    delta_time = clock.tick(60)
    fps = clock.get_fps()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    canvas.render(stats=(('FPS', fps),
                         ('Frame time', '%s ms' % delta_time)))
