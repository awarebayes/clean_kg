from typing import List

from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication

from my_types import Drawer, Point
from my_types import Edge, PixelColor
from lines import dda


def wait(delay):
    if delay != 0:
        QApplication.processEvents()
        QThread.msleep(delay)


def draw_edges(edges: List[Edge], drawer):
    for edge in edges:
        dda(edge.p1(), edge.p2(), drawer.pixel_edge)


def find_new_seed_pixels(x_left_edge: int, x_right_edge: int, y: int, drawer: Drawer) -> list:
    """
    Ищет новые затравочные пикселы на строке y
    Начиная с x_left_edge, заканчивая x_right_edge
    """
    new_pixels = []
    x = x_left_edge
    while x <= x_right_edge:
        bg_skipped_flag = False

        # Пропускаем фон
        while (
                drawer.check_color(x, y) == PixelColor.BACKGROUND
                and x < x_right_edge
        ):
            if not bg_skipped_flag:  # флаг, пропускали мы фон или нет
                bg_skipped_flag = True
            x = x + 1

        if bg_skipped_flag:
            # пришли в конец и оказались на фоне
            if (
                    x == x_right_edge
                    and drawer.check_color(x, y) == PixelColor.BACKGROUND
            ):
                new_pixels.append([x, y])
            # пришли куда то еще (на границу) и оказались не на фоне
            else:
                new_pixels.append([x - 1, y])

        # Пропускаем залитую область или границы
        x_started = x
        while (
                drawer.check_color(x, y) != PixelColor.BACKGROUND
        ) and x < x_right_edge:
            x = x + 1

        if x == x_started:
            x = x + 1
    return new_pixels


def find_bounds_and_fill(x, y, drawer: Drawer) -> tuple[int, int]:
    """
    Идет сначала направо, потом налево, заполняет, пока не доходит до границы
    """
    x_started = x
    # -->
    while drawer.check_color(x, y) != PixelColor.EDGE and x <= drawer.canvas_x_high:
        drawer.pixel_inside(x, y)
        x = x + 1

    x_right_edge = x - 1

    x = x_started

    # <-
    while drawer.check_color(x, y) != PixelColor.EDGE and x >= drawer.canvas_x_low:
        drawer.pixel_inside(x, y)
        x = x - 1

    x_left_edge = x + 1
    return x_left_edge, x_right_edge


def method_with_seed(edges: List[Edge], drawer: Drawer, seed_pixel: Point, delay: int):
    draw_edges(edges, drawer)

    stack = [seed_pixel]

    while stack:
        point = stack.pop()
        x, y = point
        if drawer.canvas_y_low > y or drawer.canvas_y_high < y:
            continue

        x_left_bound, x_right_bound = find_bounds_and_fill(x, y, drawer)
        stack += find_new_seed_pixels(x_left_bound, x_right_bound, y + 1, drawer)
        stack += find_new_seed_pixels(x_left_bound, x_right_bound, y - 1, drawer)
        wait(delay)
