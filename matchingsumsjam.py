import codejam.utils.codejamrunner as cjr
import itertools

class Dynam(object):pass
    
    

def solve(data):

    base_set = frozenset(data.numbers)
    
    for size in range(1, data.set_size):
        for set_1 in itertools.combinations(data.numbers, size):
            set_1 = set(set_1)
            set_1_sum = sum(set_1)

            max_size = data.set_size - size
            for set_2size in range(1, max_size):
                for set_2 in itertools.combinations(base_set.difference(set_1), set_2size):
                    if sum(set_2) == set_1_sum:
                        return '\n%s \n%s' %(' '.join([str(x) for x in set_1]), ' '.join([str(x) for x in set_2]))

    return 'Impossible'

def builder(f):
    row = f.get_ints()
    data = Dynam()
    data.set_size = row[0]
    data.numbers = row[1:]

    return data

    



cjr = cjr.CodeJamRunner()
cjr.run(builder, solve, problem_name = "C", problem_size='small-practice')
