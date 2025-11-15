#!/usr/bin/env python3
from . import constants
from . import player_actions
from . import utils

game_state = {
    'player_inventory': [], # Инвентарь игрока
    'current_room': 'entrance', # Текущая комната
    'game_over': False, # Индикатор окончания игры
    'steps_taken': 0 # Количество сделанных шагов
}

def process_command(game_state, command):
    """
    Обрабатывает команды, поступающие в консоль при вводе пользователем, и
    возвращает соответствующее им поведение в игре.

    Args:
        game_state (dict): словарь с данными о состоянии игрока на данный момент.
        command (str): строка, вводимая пользователем в консоль (команда).

    Returns:
        None: результат выполнения не возвращается из функции.
    """
    if ' ' in command:
        c_components = command.split()
        match c_components[0]:
            case 'take':
                player_actions.take_item(game_state, c_components[1])
            case 'use':
                player_actions.use_item(game_state, c_components[1])
            case 'go':
                player_actions.move_player(game_state, c_components[1])
    else:
        match command:
            case 'look':
                utils.describe_current_room(game_state)
            case 'inventory':
                player_actions.show_inventory(game_state)
            case 'north' | 'south' | 'east' | 'west':
                player_actions.move_player(game_state, command)
            case 'solve':
                if game_state['current_room'] == 'treasure_room':
                    utils.attempt_open_treasure(game_state)
                else:
                    utils.solve_puzzle(game_state)
            case 'quit':
                exit()
            case 'help':
                utils.show_help(constants.COMMANDS)

def main():
    """
    Запускает игровой цикл, принимает команды и выполняет их до тех пор, пока
    игра не будет окончена или пока пользователь не выйдет из игры.

    Returns:
        None: результат выполнения не возвращается из функции.
    """
    print("Добро пожаловать в Лабиринт сокровищ!\n")
    utils.describe_current_room(game_state)

    while not game_state['game_over']:
        command = player_actions.get_input()
        process_command(game_state, command)


if __name__ == "__main__":
    main()
