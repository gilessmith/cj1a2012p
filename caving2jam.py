from codejam.utils.codejamrunner import CodeJamRunner
import codejam.utils.graphing as graphing
import networkx as nx

class Dynam(object):pass

def calculate_height(time):
    return start_height - time*10.0

class Square(object):

    def __init__(self, floor, ceiling):
        self.floor = floor
        self.ceiling = ceiling
        self.earliest_time = -1

    def get_movement_speed(self, time):
        if time == 0:
            return 0
        elif self.floor +20 > calculate_height(time):
            return 10
        else:
            return 1
        
    def time_to_node(self, target):

        ceil = min(self.ceiling, target.ceiling)
        floor = max(self.floor, target.floor)
        if ceil - 50 < floor:
            return -1

        max_water_height = ceil - 50
        return max(0, (start_height - max_water_height) / 10.0)

    def set_time(self, time):
        if time < self.earliest_time or self.earliest_time < 0:
            self.earliest_time = time
            return True
        return False
        
    def __unicode__(self):
        return 'floor: %s, ceiling: %s' % (self.floor, self.ceiling)

    def __str__():
        return self.__unicode__()

def find_next_step(node, cave_exit, graph, time):
    best_time = 1000000000
    #print ' is  %s not %s at %s' %(node, cave_exit, time)
    if node == cave_exit:
        #print 'yes!!!'
        return time
    
    square = graph.node[node]['info']
    nodes = [[(node, time, square)]]
    while True:
        next_nodes = []
        for node, time, square in nodes[-1]:

            if node == cave_exit:
                #import pdb;pdb.set_trace()
                if best_time > time:
                    best_time = time
                continue
            
            for next_node in graph.neighbors(node):
                target = graph.node[next_node]['info']
                target_time_limit = square.time_to_node(target)
                if target_time_limit == -1:
                    continue
                target_time_limit = max(target_time_limit, time)
                delay = square.get_movement_speed(target_time_limit)
                
                if target.set_time(target_time_limit+delay):
                    next_nodes.append((next_node, target_time_limit+delay, graph.node[next_node]['info']))

        #import pdb;pdb.set_trace()
        if len(next_nodes) == 0:
            break
        else:
            nodes.append(next_nodes) 

    return best_time
                        
    for next_node in graph.neighbors(node):
        target = graph.node[next_node]['info']
        target_time_limit = square.time_to_node(target)
        if target_time_limit == -1:
            continue
        target_time_limit = max(target_time_limit, time)
        delay = square.get_movement_speed(target_time_limit)
        
        if target.set_time(target_time_limit+delay):
            max_path_time = find_next_step(next_node, cave_exit, graph,
                                           target_time_limit + delay)

            if max_path_time >=0 and (best_time > max_path_time):
                best_time = max_path_time
                
    return best_time
            

def solver(data):
    cave_exit = data.rows-1, data.cols-1
    output =  find_next_step((0,0), cave_exit, data.g, 0)
    #print output
    return output

    
def height_manip(node, data):
    return Square(data.floor_heights[node[0]][node[1]],
                  data.ceiling_heights[node[0]][node[1]],)


def data_builder(f):

    data = Dynam()
    
    global start_height
    start_height, data.rows, data.cols = f.get_ints()
    
    data.ceiling_heights = f.get_grid(data.rows)
    data.floor_heights = f.get_grid(data.rows)
    
    data.g = nx.grid_2d_graph(data.rows, data.cols)
    graphing.populate_graph(data.g, data, height_manip)
    #import pdb;pdb.set_trace()
    return data


def test():

    global start_height
    a = Square(10,500)
    b = Square(490, 1000)

    start_height = 200
    assert a.time_to_node(b) == -1

    print 'tests passed'

if __name__ == '__main__':
    test() 

cjr = CodeJamRunner()
cjr.run(data_builder, solver, problem_name = "B", problem_size='large-practice')
