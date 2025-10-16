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
