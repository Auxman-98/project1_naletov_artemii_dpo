import math
from . import constants
from . import player_actions

rooms = constants.ROOMS

def describe_current_room(game_state):
    """
    Выводит описание комнаты, в которой находится игрок (название, общий вид,
    заметные предметы, выходы), а также приглашает разгадать загадку в комнате
    при наличии таковой.

    Args:
        game_state (dict): данные о состоянии игрока на данный момент.

    Returns:
        None: результат выполнения не возвращается из функции.
    """
    curr_room = game_state['current_room']
    room_data = rooms[curr_room]

    print(f'== {curr_room.upper()} ==')
    print(f'{room_data["description"]}')
    print(f'\nЗаметные предметы: {room_data["items"]}')
    print(f'Выходы: {room_data["exits"]}')
    if room_data['puzzle'] is not None:
        print('Кажется, здесь есть загадка (используйте команду solve).')

def solve_puzzle(game_state):
    """
    Вызывается при желании игрока решить загадку в данной комнате (команда solve)
    и даёт либо попытаться решить загадку (число попыток неограниченно), либо
    увидеть, что загадок в комнате нет.

    Args:
        game_state (dict): данные о состоянии игрока на данный момент.

    Returns:
        None: результат выполнения не возвращается из функции.
    """
    curr_room = game_state['current_room']
    room_data = rooms[curr_room]

    if room_data['puzzle'] is None:
        print("Загадок здесь нет.")
    else:
        puzzle = room_data['puzzle']
        print(puzzle[0])
        match curr_room:
            case 'hall':
                if ((player_actions.get_input() == puzzle[1])
                    | (player_actions.get_input() == 'десять')):
                    print("Правильно!")
                    constants.ROOMS[curr_room]['puzzle'] = None
                    game_state['player_inventory'].append('treasure_key')
                    print("Вы получили награду:", \
                        game_state['player_inventory'][-1])
                else:
                    print("Неверно. Попробуйте снова.")
            case _:
                if player_actions.get_input() == puzzle[1]:
                    print("Правильно!")
                    constants.ROOMS[curr_room]['puzzle'] = None
                    game_state['player_inventory'].append('rusty_key')
                    if 'rusty_key' in room_data['items']:
                        room_data['items'].remove('rusty_key')
                    print("Вы получили награду:", \
                        game_state['player_inventory'][-1])
                else:
                    match curr_room:
                        case 'trap_room':
                            trigger_trap(game_state)
                        case _:
                            print("Неверно. Попробуйте снова.")

def attempt_open_treasure(game_state):
    """
    Вызывается только при условии, что игрок находится в сокровищнице
    (treasure_room) и хочет получить сокровища из сундука (команда solve).
    Возможны два варианта: либо попытаться решить загадку (с ключом или без)
    и при успехе выиграть игру, либо отступиться от сундука.

    Args:
        game_state (dict): данные о состоянии игрока на данный момент.

    Returns:
        None: результат выполнения не возвращается из функции.
    """
    curr_room = game_state['current_room']
    room_data = rooms[curr_room]
    puzzle = room_data['puzzle']

    if 'treasure_key' in game_state['player_inventory']:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        constants.ROOMS[curr_room]['puzzle'] = None
        room_data['items'].remove('treasure_chest')
        print("В сундуке сокровище! Вы победили!")
        game_state['game_over'] = True
    else:
        print("Сундук заперт. ... Ввести код (да/нет)?")
        match player_actions.get_input():
            case "нет":
                print("Вы отступаете от сундука.")
            case "да":
                print(puzzle[0])
                if player_actions.get_input() != puzzle[1]:
                    print("Неверно. Попробуйте снова.")
                else:
                    print("Замок щёлкает. Сундук открыт!")
                    constants.ROOMS[curr_room]['puzzle'] = None
                    room_data['items'].remove('treasure_chest')
                    print("В сундуке сокровище! Вы победили!")
                    game_state['game_over'] = True

def pseudo_random(seed, modulo):
    """
    Вычисляет псевдослучайное целое число по формуле с синусом и возвращает его.

    Args:
        seed (int): позиция, из которой запускается алгоритм генерации числа.
        modulo (int): количество вариантов значений числа в алгоритме.

    Returns:
        int: псевдослучайное целое число как результат выполнения алгоритма.
    """
    SEED_FACTOR = 13.9876
    SINE_FACTOR = 51062.7241

    x = abs(math.sin(seed*SEED_FACTOR) * SINE_FACTOR)
    x = (x - math.floor(x)) * modulo
    x = math.floor(x)

    return x

def trigger_trap(game_state):
    """
    Вызывается при выпадении соответствующего псевдослучайного числа с условием,
    что игрок находится в trap_room и в инвентаре нет факела, а также при
    неверном ответе на загадку в trap_room. Активирует ловушку и генерирует
    случайное поведение, в результате которого игрок может проиграть игру.

    Args:
        game_state (dict): данные о состоянии игрока на данный момент.

    Returns:
        None: результат выполнения не возвращается из функции.
    """
    print("Ловушка активирована! Пол стал дрожать...")

    inventory = game_state['player_inventory']
    steps = game_state['steps_taken']
    if inventory:
        rand_index = pseudo_random(steps, len(inventory))
        loss = game_state['player_inventory'].pop(rand_index)
        print(f"Вы потеряли {loss}")
    else:
        WORST_CASE_CARDINALITY = 7
        PIVOT = 2

        critical_num = pseudo_random(steps, WORST_CASE_CARDINALITY)
        if critical_num < PIVOT:
            print("Вы проиграли. Игра окончена.")
            game_state['game_over'] = True
        else:
            print("Вы уцелели!")

def random_event(game_state):
    """
    Генерирует одно из возможных случайных событий в комнате в зависимости от
    выпавшего псевдослучайного числа: или появление монетки, или появление
    неизвестного существа, или активацию ловушки (при условии, что игрок
    находится в trap_room и в инвентаре нет факела).

    Args:
        game_state (dict): данные о состоянии игрока на данный момент.

    Returns:
        None: результат выполнения не возвращается из функции.
    """
    CARDINALITY = 10
    SUCCESS_FACTOR = 3
    LUCKY_NUMBER = 0

    steps = game_state['steps_taken']
    inventory = game_state['player_inventory']
    curr_room = game_state['current_room']
    if pseudo_random(steps, CARDINALITY) == LUCKY_NUMBER:
        match pseudo_random(steps, CARDINALITY*SUCCESS_FACTOR):
            case 0:
                constants.ROOMS[curr_room]['items'].append('coin')
                print("На полу выпала монетка.")
            case 1:
                print("Чу, слышен какой-то шорох!")
                if 'sword' in inventory:
                    print("Вы отпугнули существо.")
            case 2:
                if (curr_room == 'trap_room') & ('torch' not in inventory):
                    trigger_trap(game_state)

def show_help(COMMANDS):
    """
    Вызывается при вводе пользователем команды help. Выводит перечень команд,
    доступных игроку, с описанием соответственно вызываемого ими поведения.

    Args:
        COMMANDS (dict): словарь команд, доступных игроку.

    Returns:
        None: результат выполнения не возвращается из функции.
    """
    print("\nДоступные команды:")
    for command in list(COMMANDS.keys()):
        print(f"  {command.ljust(16)}{COMMANDS[command]}")
    print()
