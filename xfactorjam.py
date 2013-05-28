
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


class XFactorJam(CodeJamRunner):
    problem_name = 'A'
    problem_size = 'large-practice'
    
    def get_case_data(self, f):
        return [int(x) for x in f.readline().strip().split(' ')[1:]]
        
    def execute_case(self, judge_scores):
        #import pdb;pdb.set_trace()
        score_volume = sum(judge_scores)
        groups = {}
        for contestant in judge_scores:
            try:
                groups[contestant] += 1

            except KeyError:
                groups[contestant] = 1

        #import pdb;pdb.set_trace()
        count = 0
        extra = 0    
        min_bound = score_volume * 2            
        for group in sorted(groups.keys()):
            if min_bound < group:
                break

            count += groups[group]
            extra += groups[group] * group
            min_bound = (0.0 + extra + score_volume) / count
        
        #import pdb;pdb.set_trace()
        output_dict = {}
        for group in groups.keys():

            ##import pdb;pdb.set_trace()
            dif = max((100.0 * (min_bound - group)) /score_volume , 0)
            output_dict[group] = '%.6f' % dif
        
        #import pdb;pdb.set_trace()    
        return ' '.join([output_dict[contestant] for contestant in judge_scores])

    def test(self):
        print self.execute_case([1,75,74,74,1,74,0,1,1])
        assert self.execute_case([20,10]) == '33.333333 66.666667'
        assert self.execute_case([10,0]) == '0.000000 100.000000'
        assert self.execute_case([25,25,25,25]) == '25.000000 25.000000 25.000000 25.000000'
        assert self.execute_case([24,30,21]) == '34.666667 26.666667 38.666667'

        print 'tests passed'

if __name__ == '__main__':
    tdj = XFactorJam()
    tdj.test()
    tdj.execute()

