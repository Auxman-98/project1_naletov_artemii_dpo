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
