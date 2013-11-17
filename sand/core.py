import math

import pygame

from sand.utils import cosine_interpolate


class GameObject(object):
    DISPLAY_FLAGS = pygame.SRCALPHA

    def __init__(self, x, y, width, height):
        '''
        x: float, x coordinate in world, range (-1, 1) is on screen
        y: float, y coordinate in world, range (-1, 1) is on screen
        width: float, width in world, scale 1:half_of_display
        height: float, height in world, scale 1:half_of_display
        '''
        self.x = x
        self.y = y
        self.width = width
        self.width_half = width / 2.0
        self.height = height
        self.height_half = height / 2.0
        self.dirty = True

    def draw(self):
        raise NotImplemented

    def render(self, surface):
        display_width = surface.get_width()
        display_height = surface.get_height()
        real_width = display_width * 0.5 * self.width
        real_height = display_height * 0.5 * self.height
        real_x = ((self.x - self.width_half) + 1) * (display_width * 0.5)
        real_y = ((self.y + self.height_half) * -1 + 1) * (display_height * 0.5)
        object_rect = pygame.Rect(real_x, real_y, real_width, real_height)

        # check if this object is off-screen
        if not object_rect.colliderect(surface.get_rect()):
            return

        if self.dirty:
            self.surface = pygame.Surface((real_width, real_height),
                                          GameObject.DISPLAY_FLAGS)
            self.draw()
            self.dirty = False

        surface.blit(self.surface, (real_x, real_y))

    def update(self, delta_time):
        raise NotImplemented


class SandCurve(GameObject):
    COLOUR = (193, 154, 107)

    def __init__(self, x, y, width, height,
                 offset_y=0.1, num_points=16, amplitude=0.1):
        super(SandCurve, self).__init__(x, y, width, height)
        self.num_points = num_points
        self.amplitude = amplitude
        self.offset_y = offset_y
        self.initialize_points()
        self.x_per_point = float(self.width) / (self.num_points - 1)

    def initialize_points(self):
        self.points = []
        val = self.amplitude
        for i in range(self.num_points):
            self.points.append(val)
            val *= -1

    def get_y(self, x):
        '''
        Do cosine interpolation to get
        y for specified x on the curve.
        '''
        point_pos = x / self.x_per_point
        y1_index = int(math.floor(point_pos))
        y2_index = int(math.ceil(point_pos))
        mu = point_pos - y1_index
        y1 = self.points[y1_index]
        y2 = self.points[y2_index]
        return self.offset_y + cosine_interpolate(y1, y2, mu)

    def draw(self):
        real_width = self.surface.get_width()
        real_height = self.surface.get_height()
        for x in range(real_width):
            x_in_object_space = float(x) / real_width * self.width
            y_in_object_space = self.get_y(x_in_object_space)
            y = (y_in_object_space * -1 + (self.height * 0.5)) / self.height * real_height
            self.surface.fill(SandCurve.COLOUR,
                              pygame.Rect(x, y, 1, real_height - y + 1))

    def update(self, delta_time):
        pass
