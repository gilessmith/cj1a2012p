import codejam.utils.codejamrunner as cjr
import itertools

class Dynam(object):pass
    
def solve(data):

    existings = {}

    for combo in itertools.combinations(data.numbers, 6):
        combo_sum = sum(combo)
        if combo_sum in existings:
            output =  '\n%s \n%s' %(' '.join([str(x) for x in combo]), ' '.join([str(x) for x in existings[combo_sum]]))
            print output
            return output
        else:
            existings[combo_sum] = combo
        
    return 'Impossible'

def builder(f):
    row = f.get_ints()
    data = Dynam()
    data.set_size = row[0]
    data.numbers = row[1:]

    return data

    



cjr = cjr.CodeJamRunner()
cjr.run(builder, solve, problem_name = "C", problem_size='large-practice')
