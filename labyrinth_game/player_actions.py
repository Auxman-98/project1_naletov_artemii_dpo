from . import constants
from . import utils

def show_inventory(game_state):
    if game_state['player_inventory'] != []:
        print(f"Инвентарь: {game_state['player_inventory']}")
    else:
        print("Ваш инвентарь пуст.")

def get_input(prompt="> "):
    try:
        return input(prompt)
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"

def move_player(game_state, direction):
    rooms = constants.ROOMS
    
    curr_room = game_state['current_room']
    room_data = rooms[curr_room]
    if direction in list(room_data['exits'].keys()):
        curr_room = room_data['exits'][direction]
        game_state['steps_taken'] += 1
        utils.describe_current_room(game_state)
    else:
        print("Нельзя пойти в этом направлении.")
