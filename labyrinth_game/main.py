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

def main():
    print("Добро пожаловать в Лабиринт сокровищ!\n")
    utils.describe_current_room(game_state)
    
    while not game_state['game_over']:
        command = player_actions.get_input()


if __name__ == "__main__":
    main()
