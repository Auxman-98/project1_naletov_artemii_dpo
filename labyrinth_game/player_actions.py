from . import constants
from . import utils

def show_inventory(game_state):
    """
    Показывает содержимое инвентаря игрока или выводит сообщение о том, что он
    пуст.

    Args:
        game_state (dict): данные о состоянии игрока на данный момент.

    Returns:
        None: результат вычисления не возвращается из функции.
    """
    if game_state['player_inventory'] != []:
        print(f"Инвентарь: {game_state['player_inventory']}")
    else:
        print("Ваш инвентарь пуст.")

def get_input(prompt="> "):
    """
    Принимает команду, введённую игроком в консоль, и либо вызывает
    соответствующую функцию, либо вызывает выход из игры.

    Args:
        prompt="> " (str): подсказка к вводу

    Returns:
        str: команда, введённая игроком (в случае выхода - 'quit').
    """
    try:
        return input(prompt)
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"

def move_player(game_state, direction):
    """
    Выполняет перемещение игрока по комнатам в зависимости от состояния игрока
    на данный момент и взятого направления.

    Args:
        game_state (dict): данные о состоянии игрока на данный момент.
        direction (str): направление, в котором хочет пойти игрок.

    Returns:
        None: результат выполнения не возвращается из функции.
    """
    rooms = constants.ROOMS

    curr_room = game_state['current_room']
    room_data = rooms[curr_room]
    if direction in list(room_data['exits'].keys()):
        if room_data['exits'][direction] == 'treasure_room':
            if 'rusty_key' in game_state['player_inventory']:
                print("Вы используете найденный ключ, чтобы открыть путь", \
                "в комнату сокровищ.")
                game_state['current_room'] = room_data['exits'][direction]
                game_state['steps_taken'] += 1
                utils.describe_current_room(game_state)
                print("\n")
                utils.random_event(game_state)
            else:
                print("Дверь заперта. Нужен ключ, чтобы пройти дальше.")
        else:
            game_state['current_room'] = room_data['exits'][direction]
            game_state['steps_taken'] += 1
            utils.describe_current_room(game_state)
            print("\n")
            utils.random_event(game_state)
    else:
        print("Нельзя пойти в этом направлении.")

def take_item(game_state, item_name):
    """
    Вызывает или поднятие в данной комнате предмета и включение его в инвентарь
    игрока, или сообщение о том, что предмета нет. Сундук с сокровищами поднять
    невозможно.

    Args:
        game_state (dict): данные о состоянии игрока на данный момент.
        item_name (str): название предмета, который игрок хочет взять.

    Returns:
        None: результат выполнения не возвращается из функции.
    """
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
    """
    Позволяет игроку использовать предмет по определённому назначению, в
    некоторых случаях выводит сообщение о том, что игрок не может использовать
    данный предмет.

    Args:
        game_state (dict): данные о состоянии игрока на данный момент.
        item_name (str): название предмета, который игрок хочет использовать.

    Returns:
        None: результат выполнения не возвращается из функции.
    """
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
