import sys
import pygame

from sand.render import Canvas
from sand.resources import load_image


pygame.init()
canvas = Canvas(800, 600, load_image('salvador_dali'))
clock = pygame.time.Clock()

while True:
    delta_time = clock.tick(60)
    fps = clock.get_fps()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.VIDEORESIZE:
            canvas.handle_resize(event.w, event.h)
    canvas.render(stats=(('FPS', fps),
                         ('Frame time', '%s ms' % delta_time)))
