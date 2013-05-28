
class CodeJamRunner(object):

    def execute(self):
        with open('%s-%s.in' % (self.problem_name,self.problem_size)) as f:
            case_count = int(f.readline())
            case =0
            results = []
            while case<case_count:
                results.append(self.execute_case(self.get_case_data(f)))

                case += 1

        with open('%s-%s.out' %
                           (self.problem_name,
                            self.problem_size), 'w') as output:
             for i, result in enumerate(results):
                 output.write('Case #%s: %s\n' % (i+1, result))

start_height = 0

class GridSquare(object):

    def movement_time(self, ceil, floor, dest_ceil, dest_floor, start_height):
        ceil = min(ceil, dest_ceil)
        floor = max(floor, dest_floor)
        if ceil -50 < floor:
            # too small to fit through gap
            return -1

        return max(0, (start_height - ceil + 50.0)/10)

    def set_time(self, time):
        if self.fastest == -1 or time < self.fastest:
            self.fastest = time
            return True
        return False
    
    def __init__(self, row, col, ceil, floor):
        self.row = row
        self.col = col
        self.ceil = ceil
        self.floor = floor

        self.slow_move = max((grid.start_height - grid.floor_map[self.n][self.m]-  20.0) / 10, 0)

        self.adjacents = []
        print ' '
        for position in offsets:
            try:
                if self.n + position[0] < 0 or self.m + position[1] < 0:
                    self.adjacents.append((-1, None))
                    #print '-1 issue: ' + str(self.adjacents[-1][0])
                    continue
                
                self.adjacents.append((
                                        self.movement_time(grid.ceiling_map[self.n][self.m],
                                                           grid.floor_map[self.n][self.m],
                                                           grid.ceiling_map[self.n + position[0]][self.m + position[1]],                                       
                                                           grid.floor_map[self.n + position[0]][self.m + position[1]],
                                                           grid.start_height),
                                        (self.n + position[0], self.m + position[1])))
                #print self.adjacents[-1][0]
            except IndexError as e:
                #import pdb;pdb.set_trace()
                self.adjacents.append((-1, None))
                #print 'too big issue ' + str(self.adjacents[-1][0])
            
        self.fastest = -1

    def get_options(self):
        return self.adjacents[:]
            
class Grid(object):

    offsets = [(0,-1), (1, 0), (0,1), (-1, 0)]
    def __init__(self, height, width):
        self.width= width
        self.height = height
        
        self.grid = [[0 * height] for i in range(width)]

    def get_adjacents(col, row):

        for offset in offsets:
            if (col + offset[0] <0 or row + offset[1] < 0 or
                col + offset == self.height or row + offset == self.width):
                continue

            yield self.grid[col + offset[0]][row + offset[1]]
    
class CavingJam(CodeJamRunner):
    problem_name = 'B'
    problem_size = 'demo'

    def print_fastest_grid(self):
        for row in self.squares:
            print ' '.join(['%2.3f' % s.fastest for s in row])
            print ' '
                

    def find_path(self,square, current_time):
        if square.n == self.grid.N -1 and square.m == self.grid.M -1:
            return
        print 'hello'
        options = square.get_options()

        for option in options:
            if option[0] == -1:
                break
            print 'there'
            
            target = self.squares[option[1][0]][option[1][1]]
            move_time = max(option[0], current_time)
            if move_time == 0:
                # account for the start before the tide has started to ebb
                if target.set_time(move_time):
                    print '%s %s' %(square.n, square.m)
                    self.print_fastest_grid()
                    self.find_path(target, move_time)
            elif move_time > square.slow_move:
                if target.set_time(move_time + 10):
                    
                    print '%s %s' %(square.n, square.m)
                    self.print_fastest_grid()
                    self.find_path(target, move_time+ 10)
            else:
                 if target.set_time(move_time + 1):
                     
                    print '%s %s' %(square.n, square.m)
                    self.print_fastest_grid()
                    self.find_path(target, move_time+ 1)   

    def calculate_entry_times(self):
        n=0
        self.squares = [[] for i in range(self.grid.N)]

        #import pdb;pdb.set_trace()
        while n< self.grid.N:
            m=0
            while m<self.grid.M:

                square = GridSquare(self.grid, (n,m))
                self.squares[n].append(square)
                
                m+=1
            n+= 1
    
    def get_case_data(self, f):
        
        grid = Grid()
        grid.start_height, grid.N, grid.M = [int(x) for x in f.readline().strip().split(' ')]
        start_height = grid.start_height
        grid.ceiling_map = [[] for i in range(grid.N)]
        grid.floor_map = [[] for i in range(grid.N)]

        n_counter = 0
        while n_counter < grid.N:
            row_data = [int(x) for x in f.readline().strip().split(' ')]
            for height in row_data:
                grid.ceiling_map[n_counter].append(height)
            n_counter += 1
            
        n_counter = 0
        while n_counter < grid.N:
            row_data = [int(x) for x in f.readline().strip().split(' ')]
            for height in row_data:
                grid.floor_map[n_counter].append(height)
            n_counter += 1
        self.grid = grid
        
        self.calculate_entry_times()
        return None

        
    def execute_case(self, levels):
        self.find_path(self.squares[0][0], 0)
        import pdb;pdb.set_trace()
        return self.squares[self.grid.N-1][self.grid.M-1].fastest

    def test(self):
       pass

if __name__ == '__main__':
    tdj = CavingJam()
    tdj.test()
    tdj.execute()

