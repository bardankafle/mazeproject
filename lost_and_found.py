import json


USE = 'e'
EMPTY = ''
FLOOR = '_'
EXIT = 'x'
DOOR = 'd'
SECRET = 's'
WALL = '*'
ITEMS = 'i'
STARTING_LOCATION = 'start'
UP = 'w'
LEFT = 'a'
DOWN = 's'
RIGHT = 'd'
PLAYER = '\u1330'
QUIT = 'q'
REQUIRES = 'requires'


def load_map(map_file_name):
    """
        When a map file name is passed the file will load the grid and return it.
        Should you modify this function? No you shouldn't.

    :param map_file_name: a string representing the file name.
    :return: a 2D list which contains the current map.
    """
    with open(map_file_name) as map_file:
        the_map = json.loads(map_file.read())

    return the_map



def display_map(the_map):
    """
    :param the_map: 2D list of the eventual map acquired from a separate .map file
    """
    # basic display map stuff
    for i in range(len(the_map)):
        print(i, ' ', end='')
        for j in the_map[i]:
            list_dict_values = list(j.values())
            """print(list_dict_values)
            print(len(list_dict_values))"""
            if list_dict_values[0] == SECRET:
                list_dict_values[0] = WALL
            for item in list_dict_values[1]:
                if item:
                    if list_dict_values[0] != PLAYER:
                        list_dict_values[0] = ITEMS
            print(list_dict_values[0], end=' ')
        print()



def look_for_start(the_map, x_position, y_position):
    """
    :param the_map: A 2D list with the map.
    :param x_position: X coordinate of where the user is on the grid (start hasn't been determined so placeholder).
    :param y_position: Y coordinate of where the user is on the grid (start hasn't been determined so placeholder).
    :return: [x,y] coordinate of where the user should start based on the game map.
    """
    # if start: true in 2d list, start from that position
    for height in range(len(the_map)):
        for width in range(len(the_map[height])):
            for key in the_map[height][width].keys():
                if key == STARTING_LOCATION:
                    if the_map[height][width][key]:
                        y_position = height
                        x_position = width
                    else:
                        y_position = 0
                        x_position = 0
    return[x_position, y_position]



def grid_movement(the_map, position_x, position_y, move_command):
    """
    :param the_map: A 2D list with the map.
    :param position_x: x_position: X coordinate of where the user is on the grid.
    :param position_y: y_position: Y coordinate of where the user is on the grid.
    :param move_command: Input of what direction the user wants to move.
    :return: [x,y] coordinate after the move is executed.
    """
    # basic movement
    if move_command == UP:
        # this to ensure no list out of range error
        if position_y > 0:
            position_y -= 1
            # if the position after movement is a wall, unopened door, or secret spot, move back
            if the_map[position_y][position_x]['symbol'] == WALL or \
                    (the_map[position_y][position_x]['symbol'] == DOOR) or \
                    (the_map[position_y][position_x]['symbol'] == SECRET):
                position_y += 1
    if move_command == LEFT:
        if position_x > 0:
            position_x -= 1
            if (the_map[position_y][position_x]['symbol'] == WALL) or \
                    (the_map[position_y][position_x]['symbol'] == DOOR) or \
                    (the_map[position_y][position_x]['symbol'] == SECRET):
                position_x += 1
    if move_command == DOWN:
        if position_y < (len(the_map) - 1):
            position_y += 1
            if (the_map[position_y][position_x]['symbol'] == WALL) or \
                    (the_map[position_y][position_x]['symbol'] == DOOR) or \
                    (the_map[position_y][position_x]['symbol'] == SECRET):
                position_y -= 1
    if move_command == RIGHT:
        if position_x < ((len(the_map[0])) - 1):
            position_x += 1
            if (the_map[position_y][position_x]['symbol'] == WALL) or \
                    (the_map[position_y][position_x]['symbol'] == DOOR) or \
                    (the_map[position_y][position_x]['symbol'] == SECRET):
                position_x -= 1
    return[position_x, position_y]



def open_door(x, y, the_map, temp_list):
    """
    :param x: X coordinate of where the user is on the grid.
    :param y: Y coordinate of where the user is on the grid.
    :param the_map: A 2D list with the map.
    :param temp_list: An unfiltered list with all items picked up.
    """
    if y > 0:
        if x > 0:
            # checks if door in vicinity
            if the_map[y - 1][x - 1]['symbol'] == DOOR:
                for i in the_map[y - 1][x - 1].keys():
                    # checks if keys includes requires
                    if i == REQUIRES:
                        for j in the_map[y - 1][x - 1]['requires']:
                            # checks items in inventory
                            if j in temp_list:
                                # if requirement full-filled, changes symbol to FLOOR
                                the_map[y - 1][x - 1]['symbol'] = FLOOR
                                # else keeps it a door so user can find requirement
                            else:
                                the_map[y - 1][x - 1]['symbol'] = DOOR
                    # else opens the door since no requirement
                    else:
                        the_map[y - 1][x - 1]['symbol'] = FLOOR
        if the_map[y - 1][x]['symbol'] == DOOR:
            for i in the_map[y - 1][x].keys():
                print(i)
                if i == REQUIRES:
                    print('yes')
                    for j in the_map[y - 1][x]['requires']:
                        if j in temp_list:
                            the_map[y - 1][x]['symbol'] = FLOOR
                        else:
                            the_map[y - 1][x]['symbol'] = DOOR
                else:
                    the_map[y - 1][x]['symbol'] = FLOOR
        if x < ((len(the_map[0])) - 1):
            if the_map[y - 1][x + 1]['symbol'] == DOOR:
                for i in the_map[y - 1][x + 1].keys():
                    if i == REQUIRES:
                        for j in the_map[y - 1][x + 1]['requires']:
                            if j in temp_list:
                                the_map[y - 1][x + 1]['symbol'] = FLOOR
                            else:
                                the_map[y - 1][x + 1]['symbol'] = DOOR
                    else:
                        the_map[y - 1][x + 1]['symbol'] = FLOOR
    if x > 0:
        if the_map[y][x - 1]['symbol'] == DOOR:
            for i in the_map[y][x - 1].keys():
                if i == REQUIRES:
                    for j in the_map[y][x - 1]['requires']:
                        if j in temp_list:
                            the_map[y][x - 1]['symbol'] = FLOOR
                        else:
                            the_map[y][x - 1]['symbol'] = DOOR
                else:
                    the_map[y][x - 1]['symbol'] = FLOOR
    if x < ((len(the_map[0])) - 1):
        if the_map[y][x + 1]['symbol'] == DOOR:
            for i in the_map[y][x + 1].keys():
                if i == REQUIRES:
                    for j in the_map[y][x + 1]['requires']:
                        if j in temp_list:
                            the_map[y][x + 1]['symbol'] = FLOOR
                        else:
                            the_map[y][x + 1]['symbol'] = DOOR
                else:
                    the_map[y][x + 1]['symbol'] = FLOOR
    if y < (len(the_map) - 1):
        if x > 0:
            if the_map[y + 1][x - 1]['symbol'] == DOOR:
                for i in the_map[y + 1][x - 1].keys():
                    if i == REQUIRES:
                        for j in the_map[y + 1][x - 1]['requires']:
                            if j in temp_list:
                                the_map[y + 1][x - 1]['symbol'] = FLOOR
                            else:
                                the_map[y + 1][x - 1]['symbol'] = DOOR
                    else:
                        the_map[y + 1][x - 1]['symbol'] = FLOOR
        if the_map[y + 1][x]['symbol'] == DOOR:
            for i in the_map[y + 1][x].keys():
                if i == REQUIRES:
                    for j in the_map[y + 1][x]['requires']:
                        if j in temp_list:
                            the_map[y + 1][x]['symbol'] = FLOOR
                        else:
                            the_map[y + 1][x]['symbol'] = DOOR
                else:
                    the_map[y + 1][x]['symbol'] = FLOOR
        if x < ((len(the_map[0])) - 1):
            if the_map[y + 1][x + 1]['symbol'] == DOOR:
                for i in the_map[y + 1][x + 1].keys():
                    if i == REQUIRES:
                        for j in the_map[y + 1][x + 1]['requires']:
                            if j in temp_list:
                                the_map[y + 1][x + 1]['symbol'] = FLOOR
                            else:
                                the_map[y + 1][x + 1]['symbol'] = DOOR
                    else:
                        the_map[y + 1][x + 1]['symbol'] = FLOOR



def secret_check(x, y, the_map, secret):
    """
    :param x: X coordinate of where the user is on the grid.
    :param y: Y coordinate of where the user is on the grid.
    :param the_map: A 2D list of the map.
    :param secret: Boolean flag for if/when secret is found.
    :return: Boolean Flag for secret, whether one was found or not.
    """
    # outer if statements for borders
    # inner if statements for changing secrets to doors
    if y > 0:
        if x > 0:
            if the_map[y - 1][x - 1]['symbol'] == SECRET:
                the_map[y - 1][x - 1]['symbol'] = DOOR
                secret = True
        if the_map[y - 1][x]['symbol'] == SECRET:
            the_map[y - 1][x]['symbol'] = DOOR
            secret = True
        if x < ((len(the_map[0])) - 1):
            if the_map[y - 1][x + 1]['symbol'] == SECRET:
                the_map[y - 1][x + 1]['symbol'] = DOOR
                secret = True
    if x > 0:
        if the_map[y][x - 1]['symbol'] == SECRET:
            the_map[y][x - 1]['symbol'] = DOOR
            secret = True
    if x < ((len(the_map[0])) - 1):
        if the_map[y][x + 1]['symbol'] == SECRET:
            the_map[y][x + 1]['symbol'] = DOOR
            secret = True
    if y < (len(the_map) - 1):
        if x > 0:
            if the_map[y + 1][x - 1]['symbol'] == SECRET:
                the_map[y + 1][x - 1]['symbol'] = DOOR
                secret = True
        if the_map[y + 1][x]['symbol'] == SECRET:
            the_map[y + 1][x]['symbol'] = DOOR
            secret = True
        if x < ((len(the_map[0])) - 1):
            if the_map[y + 1][x + 1]['symbol'] == SECRET:
                the_map[y + 1][x + 1]['symbol'] = DOOR
                secret = True
    return secret



def check_for_key(x,y, the_map, item_list, temp_list):
    """
    :param x: X coordinate of where the user is on the grid.
    :param y: Y coordinate of where the user is on the grid.
    :param the_map: A 2D list with the map.
    :param item_list: Filtered list of item_list used for inventory later.
    :param temp_list: Unfiltered list of items.
    """
    for val in the_map[y][x]['items']:
        if len(val) > 0:
            if val not in item_list:
                temp_list.append(val)
                val_split = val.split('-')
                item_list.append(' '.join(val_split))
                # resets the items list in that position so no duplicate items
                the_map[y][x]['items'] = []



def play_game(game_map):
    """
    :param game_map: A 2D list with the map.
    :return: When the user reaches the exit, game stops.
    """
    x_pos = 0
    y_pos = 0
    start_position = look_for_start(game_map, x_pos, y_pos)
    x_pos = start_position[0]
    y_pos = start_position[1]
    movement_input = ''
    list_of_items = []
    # changes current position to PLAYER symbol
    game_map[y_pos][x_pos]['symbol'] = PLAYER
    unfiltered_items = []
    while movement_input != QUIT:
        display_map(game_map)
        if game_map[y_pos][x_pos]['symbol'] == ITEMS:
            game_map[y_pos][x_pos]['symbol'] = FLOOR
        # changes current position symbol back to FLOOR
        game_map[y_pos][x_pos]['symbol'] = FLOOR
        print("Your inventory is:", ', '.join(list_of_items))
        # boolean for found a secret print statement
        found_a_secret = False
        movement_input = input("Enter Move (wasd) (e to activate doors or secrets, q to quit): ")
        new_pos = grid_movement(game_map, x_pos, y_pos, movement_input)
        y_pos = new_pos[1]
        x_pos = new_pos[0]
        check_for_key(x_pos, y_pos, game_map, list_of_items, unfiltered_items)
        if movement_input == USE:
            # open door comes before finding a secret so the secret space isn't changed to a FLOOR until next run
            open_door(x_pos, y_pos, game_map, unfiltered_items)
            found_a_secret = secret_check(x_pos, y_pos, game_map, found_a_secret)
        if game_map[y_pos][x_pos]['symbol'] == EXIT:
            print('You Win!')
            return
        # changes current position to PLAYER once the movement has all been applied
        game_map[y_pos][x_pos]['symbol'] = PLAYER
        if found_a_secret:
            print("You found a secret!")
    print('You die!')



if __name__ == '__main__':
    map_file_name = input('What map do you want to load? ')
    the_game_map = load_map(map_file_name)
    if the_game_map:
        play_game(the_game_map)
