import math
import time

import numpy as np
from numpy.testing import assert_almost_equal


def cosine_interpolate(y1, y2, mu):
    mu2 = (1.0 - math.cos(mu * math.pi)) / 2.0;
    return (y1 * (1 - mu2) + y2 * mu2);


class PhysicalObject(object):
    density = 1.0

    @property
    def volume(self):
        raise NotImplemented

    @property
    def mass(self):
        return self.volume * self.density


class Move(object):
    
    def __init__(self, start, end, delta_time):
        self.start = start
        self.end = end
        self.delta_time = delta_time

    @property
    def direction(self):
        return self.end - self.start

    @property
    def distance(self):
        return np.linalg.norm(self.direction)

    @property
    def velocity(self):
        return self.direction / self.delta_time

    @property
    def speed(self):
        return self.distance / self.delta_time


class Drag(Move, PhysicalObject):

    def __init__(self, start, end, delta_time, radius):
        super(Drag, self).__init__(start, end, delta_time)
        self.radius = radius

    @property
    def volume(self):
        return (4.0 / 3.0) * math.pi * (self.radius ** 3)


if __name__ == '__main__':
    '''
    Test coverage of PhysicalObject, Move and Drag
    '''
    current_time = time.time()
    drag = Drag(
        np.float64([1, 2]),
        np.float64([3, 4]),
        0.33,
        1
    )
    assert_almost_equal(drag.mass, (4.0 / 3.0) * math.pi, decimal=5)
    direction = np.float64([3, 4]) - np.float64([1, 2])
    for i in range(len(direction)):
        assert_almost_equal(drag.direction[i], direction[i], decimal=5)
        assert_almost_equal(drag.velocity[i], direction[i] / 0.33, decimal=5)
    assert_almost_equal(drag.speed, np.linalg.norm(direction) / 0.33, decimal=5)
