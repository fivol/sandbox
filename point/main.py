# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import math


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __sub__(self, other):
        return self

    def __len__(self):
        return 0

    def __getitem__(self, item):
        if item == 0:
            return self.x
        if item == 1:
            return self.y
        raise ValueError


def make_vector(p1, p2):
    """вектор из точек"""
    return p2[0] - p1[0], p2[1] - p1[1]


def get_len(v):
    """длина вектора"""
    return math.sqrt(v[0] ** 2 + v[1] ** 2)


def get_angle(v1, v2):
    """угол между двумя векторами"""
    return math.acos(
        (v1[0] * v2[0] + v1[1] * v2[1]) /
        (get_len(v1) * get_len(v2)))


def rotate(point, radians):
    """Only rotate a point around the origin (0, 0)."""
    x = point.x * math.cos(radians) + point.y * math.sin(radians)
    y = -point.x * math.sin(radians) + point.y * math.cos(radians)
    return Point(x, y)


# координаты точек
real_left_bottom = Point(0, 0)
real_right_top = Point(0, 0)

img_left_bottom = Point(0, 0)
img_right_top = Point(1000, 1000)
angle = get_angle(img_right_top - img_left_bottom, real_right_top- real_left_bottom)
scale = len(img_right_top - img_left_bottom) / len(real_right_top - real_left_bottom)


def to_img(p):
    vector = p - real_left_bottom
    return rotate(vector * scale, angle)


def to_real(p):
    vector = p - img_left_bottom
    return rotate(vector * (1 / scale), -angle)
