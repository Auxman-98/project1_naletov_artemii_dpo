def show_inventory(game_state):
    if game_state['player_inventory'] != []:
        print(f"Инвентарь: {game_state['player_inventory']}")
    else:
        print("Ваш инвентарь пуст.")
