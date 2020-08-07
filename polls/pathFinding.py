from . import functions as f


TILES_IN_ROW = 67
ACCURACY = 1

def findPath(start_id, finish_id, walls_id, accuracy):
    START_COORD = f.calc_x_y(TILES_IN_ROW, int(start_id))
    FINISH_COORD = f.calc_x_y(TILES_IN_ROW, int(finish_id))
    WALLS = f.cleaning_up_the_wall_list(walls_id, TILES_IN_ROW)
    ACCURACY = accuracy

    start_node = node(f.calc_cost(START_COORD,START_COORD), f.calc_cost(START_COORD,FINISH_COORD), START_COORD[0], START_COORD[1],None,  accuracy)

    queue = [start_node]
    queue_history = [start_node]
    history = []
    next_step = start_node

    while f.if_finished(next_step, FINISH_COORD) is False:
        queue.remove(next_step)
        neighbors = f.get_neighbors(next_step,queue_history, WALLS, FINISH_COORD, accuracy)
        for neighbor in neighbors:
            queue.append(neighbor)
            queue_history.append(neighbor)
        if len(queue) == 0:       # when cant find a path
            return []
        next_step = f.find_lowest_F_cost(queue)
        history.append((next_step.prev_step ,next_step))

    path = f.find_path_backwards(next_step, START_COORD)
    path = f.nodes_to_id(path)
    history = f.nodes_to_id_history(history)

    return path, history


class node:

    def __init__(self,g_cost, h_cost, x, y, prev_step=None, accuracy=1):
        self.H_cost = h_cost
        if prev_step:
            self.G_cost = (prev_step.G_cost + f.calc_cost((prev_step.x, prev_step.y),(x,y))) * accuracy
        else:
            self.G_cost = g_cost
        self.F_cost =  self.G_cost + self.H_cost
        self.x = x
        self.y = y
        self.prev_step = prev_step

