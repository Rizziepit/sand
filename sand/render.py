import pygame


class Canvas(pygame.Rect):
    FONT_NAMES = 'ubuntu,arial'
    FONT_SIZE = 14
    FONT_COLOUR = (255, 255, 255)
    STATS_BACKGROUND = (0, 0, 0)

    def __init__(self, width, height, background=(64, 64, 64)):
        super(Canvas, self).__init__(0, 0, width, height)
        self.surface = pygame.display.set_mode((width, height))
        self.background = background
        self.font = pygame.font.SysFont(Canvas.FONT_NAMES, Canvas.FONT_SIZE)

    def render(self, objects=[], stats={}):
        self.render_background()
        for obj in objects:
            obj.render(self.surface)
        if stats:
            self.render_stats(stats)
        pygame.display.flip()

    def render_background(self):
        # if list/tuple the background is a colour
        if type(self.background) in (tuple, list):
            self.surface.fill(self.background, self)
        # otherwise assume it is an image
        else:
            self.surface.blit(self.background, self)

    def render_stats(self, stats):
        surfaces = []
        stats_height = 22
        stats_width = 100
        total_height = 0
        max_width = 0
        for label, value in stats:
            if type(value) is float:
                surface = (self.font.render('%s: %.2f'
                                            % (label, round(value, 2)),
                                            True, Canvas.FONT_COLOUR))
            else:
                surface = (self.font.render('%s: %s'
                                            % (label, value),
                                            True, Canvas.FONT_COLOUR))
            total_height += surface.get_height()
            width = surface.get_width()
            if width > max_width:
                max_width = width
            surfaces.append(surface)

        # 4px padding, 2px in between lines
        total_height += 8 + 2 * (len(surfaces) - 1)
        if total_height > stats_height:
            stats_height = total_height
        if max_width + 8 > stats_width:
            stats_width = max_width + 8

        stats_surface = pygame.Surface((stats_width, stats_height))
        stats_surface.fill(Canvas.STATS_BACKGROUND)

        x = 4
        y = stats_height - 2
        for i in range(len(surfaces) - 1, -1, -1):
            surface = surfaces[i]
            y -= surface.get_height() + 2
            stats_surface.blit(surface, (x, y))

        # draw stats surface in bottom right corner
        self.surface.blit(stats_surface,
                          (self.width - stats_width - 4,
                           self.height - stats_height - 4))
