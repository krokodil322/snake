from objects import *

import os


status = input('Игра - 1, Компания - 2, Смотреть повтор - 3. Ввод: ')
if status == '1':
    while True:
        snake = Snake(start_points=[(1, 1), (1, 2)])
        field = Field(snake=snake)
        game = GameManager(snake=snake, field=field, delay=0.1)
        game.play()
        status = input('Повторить катку? Введи 1, если да, 0 для выхода:')
        if status == '0':
            break
elif status == '2':
    lvls = os.listdir('lvls')
    print('Доступные уровни:')
    for index, filename in enumerate(lvls, 1):
        print(f'\t{index}. {filename}')
    filename = GameManager.get_user_index(dir=lvls)
    lvl, _ = filename.split('.pkl')
    lvl = int(lvl)
    game = GameManager.get_game_by_lvl(lvl)
    game.play()
elif status == '3':
    snake = Snake(start_points=[(1, 1), (1, 2)])
    field = Field(snake=snake)
    game = GameManager(snake=snake, field=field)
    game.show_repeat()