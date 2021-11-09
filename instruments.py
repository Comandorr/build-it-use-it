from pygame import *
from random import *

clock = time.Clock()
font.init()
mixer.init()
f48 = font.Font(None, 48)
f44 = font.Font(None, 44)
f36 = font.Font(None, 36)
f34 = font.Font(None, 34)
f28 = font.Font(None, 28)
f24 = font.Font(None, 24)
f22 = font.Font(None, 22)
win_w = 1280
win_h = 720
center_x = int(win_w / 2)
center_y = int(win_h / 2)
black = (0, 0, 0)
gray = (150, 150, 150)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
items = [
    'images/circuitBoard.png',
    'images/diode.png',
    'images/gunpowder.png',
    'images/metal.png',
    'images/metalRod.png',
    'images/plastic.png',
    'images/processor.png',
    'images/wire.png', ]
crates = [
    'images/ammoBox.png',
    'images/ironCrateBig.png',
    'images/woodenCrateBig.png']
resources = {
    'circuitBoard': 0,
    'diode': 0,
    'gunpowder': 0,
    'metal': 0,
    'metalRod': 0,
    'plastic': 0,
    'processor': 0,
    'wire': 0}
robots = [
    'images/cargo.png',
    'images/searcher.png']
squad = {
    'cargo': 0,
    'searcher': 0}


class Buddy:
    def __init__(self, name, recipe, speed):
        self._txt = name
        self.name = name
        self.recipe = recipe
        self.speed = speed


def chance(c):
    ch = randint(0, 99)
    if ch < c:
        return True
    else:
        return False


def distance(s1, s2):
    x1 = s1.rect.x + s1.rect.width / 2
    y1 = s1.rect.y + s1.rect.height / 2
    x2 = s2.rect.x + s2.rect.width / 2
    y2 = s2.rect.y + s2.rect.height / 2
    d = float(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)
    d = abs(round(d, 3))
    return d


def distance_to_point(s1, x2, y2):
    x1 = s1.rect.x + s1.rect.width / 2
    y1 = s1.rect.y + s1.rect.height / 2
    d = float(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)
    d = round(d, 3)
    return d


def distance_p_to_p(x1, y1, x2, y2):
    d = float(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)
    d = round(d, 3)
    return d


class Group(sprite.Group):
    def reset(self):
        for i in self.sprites():
            i.reset()
