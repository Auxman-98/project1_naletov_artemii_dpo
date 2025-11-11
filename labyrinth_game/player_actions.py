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
        game_state['current_room'] = room_data['exits'][direction]
        game_state['steps_taken'] += 1
        utils.describe_current_room(game_state)
        print("\n")
        utils.random_event(game_state)
    else:
        print("Нельзя пойти в этом направлении.")

def take_item(game_state, item_name):
    rooms = constants.ROOMS

    curr_room = game_state['current_room']
    room_data = rooms[curr_room]
    if item_name in room_data['items']:
        if item_name == 'treasure_chest':
            print("Вы не можете поднять сундук, он слишком тяжёлый.")
        else:
            game_state['player_inventory'].append(item_name)
            room_data['items'].remove(item_name)
            print("Вы подняли:", item_name)
    else:
        print("Такого предмета здесь нет.")

def use_item(game_state, item_name):
    if item_name in game_state['player_inventory']:
        match item_name:
            case 'torch':
                print("Здесь стало светлее..")
            case 'sword':
                print("Чувствуете себя увереннее перед неизвестным.")
            case 'bronze_box':
                print("Бронзовая шкатулка открыта.")
                if 'rusty_key' not in game_state['player_inventory']:
                    game_state['player_inventory'].append('rusty_key')
                else:
                    print("Здесь пусто.")
            case _:
                print(f"Вы не знаете, как использовать {item_name}")
