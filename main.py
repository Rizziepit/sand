import sys
import pygame

from sand.render import Canvas
from sand.resources import load_image


pygame.init()
canvas = Canvas(800, 600, load_image('salvador_dali'))
clock = pygame.time.Clock()
keys_down = set()

while True:
    delta_time = clock.tick(60)
    fps = clock.get_fps()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.VIDEORESIZE:
            canvas.handle_resize(event.w, event.h)
        elif event.type == pygame.KEYDOWN:
            keys_down.add(event.key)
        elif event.type == pygame.KEYUP:
            if event.key in keys_down:
                # handle key press event
                keys_down.remove(event.key)
                if event.key == 27:
                    sys.exit()
    canvas.render(stats=(('FPS', fps),
                         ('Frame time', '%s ms' % delta_time)))
