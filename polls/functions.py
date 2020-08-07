import math
from . import pathFinding as pf


# INPUT:   number of tiles in row, id
# OUTPUT:  tuple that represents co-ordinates of this ID on grid
def calc_x_y(num_in_row, id):
    x = id % (num_in_row+1)
    if id != 0:
        y = id // (1 + num_in_row)
    else:
        y = 0
    return x, y


# INPUT:    ids of walls(strings with separator ';' , how many tiles is in row
# OUTPUT:   Sorted array of tuples (X,Y). Sorted firstly by X, then Y
def cleaning_up_the_wall_list(walls_id, TILES_IN_ROW):      #deleting duplicates, changing ids to coords
    walls = []

    if type(walls_id) == str:
        walls_temp_holder_str = walls_id.split(';')

        walls_temp_holder_str.remove('')      #bc 0. element is empty

        for wall_str in walls_temp_holder_str:
            walls_x_y = calc_x_y(TILES_IN_ROW, int(wall_str))
            walls.append(walls_x_y)

        walls = list(dict.fromkeys(walls))      #deleting duplicates

    sort_2_dim(walls)

    return walls


#just Pythagoras
def calc_cost(current, other):
    sqrt_x = (current[0]-other[0])*(current[0]-other[0])
    sqrt_y = (current[1]-other[1])*(current[1]-other[1])

    return math.pow(sqrt_x + sqrt_y, 0.5)


# INPUT:    Array of nodes
# OUTPUT:   node in array that have lowest F_cost
def find_lowest_F_cost(queue):
    lowest_f = queue[0].F_cost
    node_with_lowest_cost = queue[0]
    for node in queue:
        if node.F_cost < lowest_f:
            lowest_f = node.F_cost
            node_with_lowest_cost = node
    return node_with_lowest_cost


# INPUT:    node(whom I want to find neighbours),  array with all nodes ever made,
#           array of tuples (X, Y) that represents walls,  tuple (X,Y) where is finish
# OUTPUT:   Array of nodes with all available neighbors
def get_neighbors(curr_node, queue_history, walls, finish_coords, accuracy):
    neighbors = []

    # searching in sorted walls array

    temp = find_coords_in__sorted_array_of_tuples(walls, curr_node.x - 1, (curr_node.y - 1, curr_node.y, curr_node.y +1))
    left_down = not temp[0]
    left_mid = not temp[1]
    left_up = not temp[2]

    temp = find_coords_in__sorted_array_of_tuples(walls, curr_node.x, (curr_node.y - 1, -9999, curr_node.y + 1))
    mid_down = not temp[0]
    mid_up = not temp[2]

    temp = find_coords_in__sorted_array_of_tuples(walls, curr_node.x + 1, (curr_node.y - 1, curr_node.y, curr_node.y +1))
    right_down = not temp[0]
    right_mid = not temp[1]
    right_up = not temp[2]

    ########### Ifs to not walk beyond borders ##############
    if curr_node.x-1 < 0 or curr_node.y-1 < 0:
        left_down = False
        if curr_node.x-1 < 0:
            left_mid = False
    if curr_node.x-1 < 0 or curr_node.y+1 > 43:
        left_up = False
        if curr_node.y+1 > 43:
            mid_up = False
    if curr_node.x+1 > 67 or curr_node.y-1 < 0:
        right_down = False
        if curr_node.y - 1 < 0:
            mid_down = False
    if curr_node.x+1 > 67 or curr_node.y+1 > 43:
        right_up = False
        if curr_node.x + 1 > 67:
            right_mid = False
    #########################################################


    #### Making going throught corners imposible ####
    if left_mid is False and mid_down is False:
        left_down = False
    if left_mid is False and mid_up is False:
        left_up = False
    if right_mid is False and mid_down is False:
        right_down = False
    if right_mid is False and mid_up is False:
        right_up = False
    #################################################

    ################################ Looking for better path to nodes that already exist ###############################
    for qh in queue_history:
        if left_down and (qh.x == curr_node.x-1 and qh.y == curr_node.y-1):
            if qh.G_cost > curr_node.G_cost + calc_cost((curr_node.x - 1, curr_node.y - 1), (curr_node.x, curr_node.y)):
                left_down = True
                queue_history.remove(qh)
            else:
                left_down = False
        elif left_mid and (curr_node.x-1 == qh.x and curr_node.y == qh.y):
            if qh.G_cost > curr_node.G_cost + calc_cost((curr_node.x - 1, curr_node.y), (curr_node.x, curr_node.y)):
                left_mid = True
                queue_history.remove(qh)
            else:
                left_mid = False
        elif left_up and (curr_node.x-1 == qh.x and curr_node.y+1 == qh.y):
            if qh.G_cost > curr_node.G_cost + calc_cost((curr_node.x - 1, curr_node.y + 1), (curr_node.x, curr_node.y)):
                left_up = True
                queue_history.remove(qh)
            else:
                left_up = False
        elif mid_up and (curr_node.x == qh.x and curr_node.y+1 == qh.y):
            if qh.G_cost > curr_node.G_cost + calc_cost((curr_node.x, curr_node.y + 1), (curr_node.x, curr_node.y)):
                mid_up = True
                queue_history.remove(qh)
            else:
                mid_up = False
        elif mid_down and (curr_node.x == qh.x and curr_node.y-1 == qh.y):
            if qh.G_cost > curr_node.G_cost + calc_cost((curr_node.x, curr_node.y - 1), (curr_node.x, curr_node.y)):
                mid_down = True
                queue_history.remove(qh)
            else:
                mid_down = False
        elif right_down and (curr_node.x+1 == qh.x and curr_node.y-1 == qh.y):
            if qh.G_cost > curr_node.G_cost + calc_cost((curr_node.x + 1, curr_node.y - 1), (curr_node.x, curr_node.y)):
                right_down = True
                queue_history.remove(qh)
            else:
                right_down = False
        elif right_mid and (curr_node.x+1 == qh.x and curr_node.y == qh.y):
            if qh.G_cost > curr_node.G_cost + calc_cost((curr_node.x + 1, curr_node.y), (curr_node.x, curr_node.y)):
                right_mid = True
                queue_history.remove(qh)
            else:
                right_mid = False
        elif right_up and (curr_node.x+1 == qh.x and curr_node.y+1 == qh.y):
            if qh.G_cost > curr_node.G_cost + calc_cost((curr_node.x + 1, curr_node.y + 1), (curr_node.x, curr_node.y)):
                right_up = True
                queue_history.remove(qh)
            else:
                right_up = False
    ####################################################################################################################
    ##################################################  MAKING NODES   #################################################
    if left_down:
        cost_to_finish = calc_cost((curr_node.x-1, curr_node.y-1), finish_coords)
        neighbors.append(pf.node(0, cost_to_finish, curr_node.x-1, curr_node.y-1, curr_node, accuracy))
    if left_mid:
        cost_to_finish = calc_cost((curr_node.x-1, curr_node.y), finish_coords)
        neighbors.append(pf.node(0, cost_to_finish, curr_node.x-1, curr_node.y, curr_node, accuracy))
    if left_up:
        cost_to_finish = calc_cost((curr_node.x-1, curr_node.y+1), finish_coords)
        neighbors.append(pf.node(0, cost_to_finish, curr_node.x-1, curr_node.y+1, curr_node, accuracy))
    if mid_up:
        cost_to_finish = calc_cost((curr_node.x, curr_node.y+1), finish_coords)
        neighbors.append(pf.node(0, cost_to_finish, curr_node.x, curr_node.y+1, curr_node, accuracy))
    if mid_down:
        cost_to_finish = calc_cost((curr_node.x, curr_node.y-1), finish_coords)
        neighbors.append(pf.node(0, cost_to_finish, curr_node.x, curr_node.y-1, curr_node, accuracy))
    if right_down:
        cost_to_finish = calc_cost((curr_node.x+1, curr_node.y-1), finish_coords)
        neighbors.append(pf.node(0, cost_to_finish, curr_node.x+1, curr_node.y-1, curr_node, accuracy))
    if right_mid:
        cost_to_finish = calc_cost((curr_node.x+1, curr_node.y), finish_coords)
        neighbors.append(pf.node(0, cost_to_finish, curr_node.x+1, curr_node.y, curr_node, accuracy))
    if right_up:
        cost_to_finish = calc_cost((curr_node.x+1, curr_node.y+1), finish_coords)
        neighbors.append(pf.node(0, cost_to_finish, curr_node.x+1, curr_node.y+1, curr_node, accuracy))
    ####################################################################################################################
    return neighbors


# INPUT:    last node
# OUTPUT:   Bool, True if found, False if not
def if_finished(curr, fin):
    if curr.x == fin[0] and curr.y == fin[1]:
        return True
    return False


# INPUT:    Array Of Tuple (x,y)
# OUTPUT:   array of ids for grid with width 68
def nodes_to_id(nodes):
    path = []
    for node in nodes:
        tile_id = node.y * 68 + node.x
        path.append(tile_id)
    return path


# INPUT:    array of tuples(node, node)
# OUTPUT:   array of ids from second node in tuple for grid of id 68
def nodes_to_id_history(nodes):
    path = []
    for node in nodes:
        tile_id = node[1].y * 68 + node[1].x
        path.append(tile_id)
    return path


# INPUT: custom class:node , coords of start (x,y)
# OUTPUT: array of steps == shortest path
def find_path_backwards(next_step, start_coord):
    path = []
    temp = next_step
    while (temp.x, temp.y) != start_coord:
        path.append(temp)
        temp = temp.prev_step

    return path


# INPUT: Array of Tuples (x,y)
# OUTPUT: Sorted Array of Tuples (x,y), first by X, then by Y
def sort_2_dim(coords):
    coords.sort(key=lambda tup: (tup[0], tup[1]))


# INPUT:SORTED Array of Tuples (x,y), 3 times (X that u looking for,Y that u looking for)
# OUTPUT: tuple of bools, True if founded, False if not founded
def find_coords_in__sorted_array_of_tuples(arr, search_forX, search_forY):
    if arr[0][0] > search_forX: return False, False, False
    if arr[len(arr)-1][0] < search_forX: return False, False, False

    minus_one = False
    zero = False
    plus_one = False

    l = 0           #left pointer
    r = len(arr)    #right pointer
    while l <= r:
        mid = (l + r) // 2
        if arr[mid][0] > search_forX:  # '[0]' bc first element in tuple is X
            r = mid - 1
        elif arr[mid][0] < search_forX:
            l = mid + 1
        else:
            while mid != len(arr)-1 and arr[mid+1][0] == search_forX:   #moving 'mid' to last elemnt that fits
                mid = mid + 1
            for counter in reversed(range(0, mid+1)):
                if arr[counter][0] != search_forX:
                    return minus_one, zero, plus_one
                elif arr[counter][1] == search_forY[0]:
                    minus_one = True
                elif arr[counter][1] == search_forY[1]:
                    zero = True
                elif arr[counter][1] == search_forY[2]:
                    plus_one = True
                elif counter == 0:                                  #bo gdy w tablicy typu : (23, 14), (23, 15), (24, 14), (25, 14), (26, 6), (26, 7) szukalem np (23,5) to byl problem bo dochodzil do poczatku tabliucy i dupa
                    return minus_one, zero, plus_one
            return minus_one, zero, plus_one
    return minus_one, zero, plus_one






