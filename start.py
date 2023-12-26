from objects import GameManager


status = input('Игра - 1, смотреть повтор - 2. Ввод: ')

if status == '1':
    while True:
        game = GameManager()
        game.play()
        status = input('Повторить катку? Введи 1, если да, 0 для выхода:')
        if status == '0':
            break
elif status == '2':
    game = GameManager()
    game.show_repeat()