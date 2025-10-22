from . import constants

def describe_current_room(game_state):
    rooms = constants.ROOMS
    curr_room = game_state['current_room']
    print(f'== {curr_room.upper()} ==')
    
    room_data = rooms[curr_room]
    print(f'{room_data["description"]}')
    print(f'\nЗаметные предметы: {room_data["items"]}')
    print(f'Выходы: {room_data["exits"]}')
    if room_data['puzzle'] is not None:
        print('Кажется, здесь есть загадка (используйте команду solve).')

def solve_puzzle(game_state):
    rooms = constants.ROOMS
    curr_room = game_state['current_room']
    
    room_data = rooms[curr_room]
    if room_data['puzzle'] is None:
        print("Загадок здесь нет.")
    else:
        puzzle = room_data['puzzle']
        print(puzzle[0])
        if player_actions.get_input() == puzzle[1]:
            print("Правильно!")
            room_data.remove(puzzle)
            match curr_room:
                case 'trap_room' | 'library':
                    game_state['player_inventory'].append('rusty_key')
                case 'hall':
                    game_state['player_inventory'].append('treasure_key')
            print("Вы получили награду:", game_state['player_inventory'][-1])
        else:
            print("Неверно. Попробуйте снова.")
