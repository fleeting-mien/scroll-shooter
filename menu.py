import pygame as pg
# from classes import game_state
pg.init()
ARIAL_25 = pg.font.SysFont('arial', 25)
"""
Це шрифт
"""


class Menu:
    """
    Класс меню. Пока что кнопочки только Start и Quit.
    _option_surfaces - поверхности для пунктов меню
    _callbacks - что делают кнопки
    _current_option_index - выбранный пункт меню
    """
    def __init__(self):
        self._option_surfaces = []
        self._callbacks = []
        self._current_option_index = 0

    def append_option(self, option, callback):
        """
        Добавляет пункт меню
        option - отображаемый текст кнопки в меню
        callback - функция кнопки
        """
        self._option_surfaces.append(ARIAL_25.render(option, True, (255, 255, 255)))
        self._callbacks.append(callback)

    def switch(self, direction):
        """
        Переключение между пунктами меню.
        """
        self._current_option_index = max(0, min(self._current_option_index + direction, len(self._option_surfaces) - 1))

    def select(self):
        """
        Делаем "тык" в пункт меню
        """
        self._callbacks[self._current_option_index]()

    def check_current_index(self):
        return self._current_option_index

    def drawmenu(self, surf, x, y, option_y_padding):
        for i, option in enumerate(self._option_surfaces):
            option_rect = option.get_rect()
            option_rect.topleft = (x, y + i * option_y_padding)
            if i == self._current_option_index:
                pg.draw.rect(surf, (0, 100, 0), option_rect)
            surf.blit(option, option_rect)


menu_is_here = Menu()
menu_is_here.append_option('Start', lambda: "game")
menu_is_here.append_option('Pause', lambda: "pause")
menu_is_here.append_option('Quit', lambda: print('Дасвиданя, иди делай анжуманя'))
menu_is_here.append_option('Restart', lambda: "startscreen")
menu_is_here.append_option('About', lambda: "about")
