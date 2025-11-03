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
    if ' ' in command:
        components = command.split()
        match components[0]:
            case 'take':
                player_actions.take_item(game_state, components[1])
            case 'use':
                player_actions.use_item(game_state, components[1])
            case 'go':
                player_actions.move_player(game_state, components[1])
    else:
        match command:
            case 'look':
                utils.describe_current_room(game_state)
            case 'inventory':
                player_actions.show_inventory(game_state)
            case 'solve':
                if game_state['current_room'] == 'treasure_room':
                    utils.attempt_open_treasure(game_state)
                else:
                    utils.solve_puzzle(game_state) 
            case 'quit':
                exit()
            case 'help':
                utils.show_help()

def main():
    print("Добро пожаловать в Лабиринт сокровищ!\n")
    utils.describe_current_room(game_state)
    
    while not game_state['game_over']:
        command = player_actions.get_input()
        process_command(game_state, command)


if __name__ == "__main__":
    main()
