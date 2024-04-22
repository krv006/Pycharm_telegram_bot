def get_keyboard(keyboard_list: list, column_number: int):
    new_keyboard = []
    for index in range(0, len(keyboard_list), column_number):
        new_keyboard.append(keyboard_list[index:index + column_number])
    return new_keyboard
def get_keyboard(keyboard_list: list, column_number: int):
    new_keyboard = []
    for index in range(0, len(keyboard_list), column_number):
        new_keyboard.append(keyboard_list[index:index + column_number])
    return new_keyboard
