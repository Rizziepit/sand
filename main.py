import sys
import pygame

from sand.render import Canvas
from sand.resources import load_image
from sand.core import SandCurve


pygame.init()
canvas = Canvas(800, 600, load_image('salvador_dali'))
clock = pygame.time.Clock()
keys_down = set()
objects = [
    SandCurve(0, -0.8, 2, 0.4,
              num_points=32, amplitude=0.025),
]


while True:
    delta_time = clock.tick(60)
    fps = clock.get_fps()

    # handle some events
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

    for obj in objects:
        obj.update(delta_time)

    canvas.render(
        objects,
        (('FPS', fps),
         ('Frame time', '%s ms' % delta_time))
    )
