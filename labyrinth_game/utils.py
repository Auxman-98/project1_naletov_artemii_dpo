import math
from . import constants
from . import player_actions

rooms = constants.ROOMS

def describe_current_room(game_state):
    curr_room = game_state['current_room']
    room_data = rooms[curr_room]

    print(f'== {curr_room.upper()} ==')
    print(f'{room_data["description"]}')
    print(f'\nЗаметные предметы: {room_data["items"]}')
    print(f'Выходы: {room_data["exits"]}')
    if room_data['puzzle'] is not None:
        print('Кажется, здесь есть загадка (используйте команду solve).')

def solve_puzzle(game_state):
    curr_room = game_state['current_room']
    room_data = rooms[curr_room]

    if room_data['puzzle'] is None:
        print("Загадок здесь нет.")
    else:
        puzzle = room_data['puzzle']
        print(puzzle[0])
        if player_actions.get_input() == puzzle[1]:
            print("Правильно!")
            constants.ROOMS[curr_room]['puzzle'] = None
            match curr_room:
                case 'trap_room' | 'library':
                    game_state['player_inventory'].append('rusty_key')
                case 'hall':
                    game_state['player_inventory'].append('treasure_key')
            if 'rusty_key' in room_data['items']:
                room_data['items'].remove('rusty_key')
            print("Вы получили награду:", game_state['player_inventory'][-1])
        else:
            print("Неверно. Попробуйте снова.")

def attempt_open_treasure(game_state):
    curr_room = game_state['current_room']
    global rooms
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
    num_1 = abs(math.sin(seed*13.9876) * 51062.7241)
    num_2 = (num_1 - math.floor(num_1)) * modulo
    x = math.floor(num_2)

    return x

def trigger_trap(game_state):
    print("Ловушка активирована! Пол стал дрожать...")

    inventory = game_state['player_inventory']
    steps = game_state['steps_taken']
    if inventory:
        num = pseudo_random(steps, len(inventory))
        loss = game_state['player_inventory'].pop(num)
        print(f"Вы потеряли {loss}")
    else:
        num = pseudo_random(steps, 7)
        if num < 2:
            print("Вы проиграли. Игра окончена.")
            game_state['game_over'] = True
        else:
            print("Вы уцелели!")

def random_event(game_state):
    steps = game_state['steps_taken']
    inventory = game_state['player_inventory']
    curr_room = game_state['current_room']
    num = pseudo_random(steps, 10)
    if num == 0:
        num_1 = pseudo_random(steps, 30)
        match num_1:
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

def show_help():
    print("\nДоступные команды:")
    print("  go <direction>  - перейти в направлении (north/south/east/west)")
    print("  look            - осмотреть текущую комнату")
    print("  take <item>     - поднять предмет")
    print("  use <item>      - использовать предмет из инвентаря")
    print("  inventory       - показать инвентарь")
    print("  solve           - попытаться решить загадку в комнате")
    print("  quit            - выйти из игры")
    print("  help            - показать это сообщение")
