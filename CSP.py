'''
CSP Class and necessary dependencies
'''

class Variable:
    ''' CSP variables '''
    def __init__(self, domain=list()):
        self.domain = domain
        # is currentdomain necessary?!
        self.currentdomain = [True] * len(domain)
        self.assignedValue = None

    def add_domain_values(self, values):
        for value in values:
            self.domain.append(value)
            self.currentdomain.append(True)

    def domain_size(self):
        return(len(self.domain))

    def domain(self):
        return self.domain

    # pruning methods!
    def prune(self, value):
        self.currentdomain[self.find_index(value)] = False

    def unprune(self, value):
        self.currentdomain[self.find_index(value)] = True

    def current_domain(self):
        '''
        print the items in the current domain_size
        '''
        values = list()
        if self.is_assigned():
            values.append(self.get_assigned_value())
        else:
            for index, value in enumerate(self.domain):
                if self.currentdomain[i]:
                    values.append(value)
        return values

    def current_domain(self, value):
        '''
        check if the value is in the current domain
        '''
        if not value in self.domain:
            return False
        if self.is_assigned():
            return value == self.get_assigned_value()
        else:
            return self.currentdomain[self.find_index(value)]

    def current_domain_size(self):
        if self.is_assigned():
            return 1
        else:
            return sum(1 for value in self.currentdomain if value)

    def restore_currentdomain(self):
        for i in range(len(self.currentdomain)):
            self.currentdomain[i] = True

    def find_index(self, value):
        return self.domain.index(value)

    # assignment
    def is_assigned(self):
        return self.assignedValue is not None

    def assign(self, value):
        if self.is_assigned() or not self.current_domain(value):
            return
        self.assignedValue = value

    def unassign(self):
        if not self.is_assigned():
            return
        self.assignedValue = None

    def get_assigned_value(self):
        return self.assignedValue

class Constraint:
    def __init__(self, scope):
        self.scope = list(scope)
        self.satisfying_tuples = dict()
        self.sup_tuples = dict()

    def add_satisfying_tuples(self, tuples):
        for constraint in tuples:
            t = tuple(constraint)
            if not t in self.satisfying_tuples:
                self.satisfying_tuples[t] = True

            for i, value in enumerate(t):
                var = self.scope[i]
                if not (var, value) in self.sup_tuples:
                    self.sup_tuples[(var, value)] = list()
                self.sup_tuples[(var, value)].append(t)

    def get_scope(self):
        return list(self.scope)

    def verify(self, values):
        # Check if values satisfy the constraints
        return tuple(values) in self.satisfying_tuples

    def get_num_unassigned(self):
        num = 0
        for value in self.scope:
            if not value.is_assigned():
                num += 1
        return num

    def get_unassigned(self):
        values = list()
        for value in self.scope:
            if not value.is_assigned():
                values.append(value)
        return values

    def has_support(self, var, val):
        if (var, val) in self.sup_tuples:
            for tuple in self.sup_tuples[(var, val)]:
                if self.is_tuple_valid(t):
                    return True
        return False

    def is_tuple_valid(self, tuple):
        for index, variable in enumerate(self.scope):
            if not variable.in_current_domain(t[i]):
                return False
        return True


class CSP:
    def __init__(self, vars=list()):
        self.vars = vars
        self.cons = list()
        self.map = dict()
        for variable in vars:
            self.add_variable(v)

    def add_variable(self, var):
        if not type(var) is Variable:
            raise TypeError("All variables should be Variables")
        else:
            self.vars.append(var)
            self.map[var] = list()

    def add_constraint(self, cons):
        if not type(cons) is Constraint:
            raise TypeError("Constraints must be of type Constraint")
        for variable in cons.scope:
            if not variable in self.map:
                return
            self.map[variable].append(cons)
        self.cons.append(c)

    def get_constraints(self):
        return self.cons

    def get_constraint(self, variable):
        '''
        get a constraint with a specific variable in it
        '''
        return list(self.map[var])

    def get_vars(self):
        return list(self.vars)


# TODO: backtrack I need to change
class Backtrack:
    def __init__(self, csp):
        '''csp == CSP object specifying the CSP to be solved'''

        self.csp = csp
        self.nDecisions = 0 #nDecisions is the number of variable
                            #assignments made during search
        self.nPrunings  = 0 #nPrunings is the number of value prunings during search
        unasgn_vars = list() #used to track unassigned variables
        self.TRACE = False
        self.runtime = 0

    def trace_on(self):
        '''Turn search trace on'''
        self.TRACE = True

    def trace_off(self):
        '''Turn search trace off'''
        self.TRACE = False


    def clear_stats(self):
        '''Initialize counters'''
        self.nDecisions = 0
        self.nPrunings = 0
        self.runtime = 0

    def print_stats(self):
        print("Search made {} variable assignments and pruned {} variable values".format(
            self.nDecisions, self.nPrunings))

    def restoreValues(self,prunings):
        '''Restore list of values to variable domains
           each item in prunings is a pair (var, val)'''
        for var, val in prunings:
            var.unprune_value(val)

    def restore_all_variable_domains(self):
        '''Reinitialize all variable domains'''
        for var in self.csp.vars:
            if var.is_assigned():
                var.unassign()
            var.restore_curdom()

    def extractMRVvar(self):
        '''Remove variable with minimum sized cur domain from list of
           unassigned vars. Would be faster to use heap...but this is
           not production code.
        '''

        md = -1
        mv = None
        for v in self.unasgn_vars:
            if md < 0:
                md = v.cur_domain_size()
                mv = v
            elif v.cur_domain_size() < md:
                md = v.cur_domain_size()
                mv = v
        self.unasgn_vars.remove(mv)
        return mv

    def restoreUnasgnVar(self, var):
        '''Add variable back to list of unassigned vars'''
        self.unasgn_vars.append(var)

    def bt_search(self,propagator):
        self.clear_stats()
        stime = time.process_time()

        self.restore_all_variable_domains()

        self.unasgn_vars = []
        for v in self.csp.vars:
            if not v.is_assigned():
                self.unasgn_vars.append(v)

        status, prunings = propagator(self.csp) # initial propagate no assigned variables.
        self.nPrunings = self.nPrunings + len(prunings)

        if self.TRACE:
            print(len(self.unasgn_vars), " unassigned variables at start of search")
            print("Root Prunings: ", prunings)

        if status == False:
            print("CSP{} detected contradiction at root".format(
                self.csp.name))
        else:
            status = self.bt_recurse(propagator, 1)   #now do recursive search


        self.restoreValues(prunings)
        if status == False:
            print("CSP{} unsolved. Has no solutions".format(self.csp.name))
        if status == True:
            print("CSP {} solved. CPU Time used = {}".format(self.csp.name,
                                                             time.process_time() - stime))
            self.csp.print_soln()

        print("bt_search finished")
        self.print_stats()

    def bt_recurse(self, propagator, level):
        '''Return true if found solution. False if still need to search.
           If top level returns false--> no solution'''

        if self.TRACE:
            print('  ' * level, "bt_recurse level ", level)

        if not self.unasgn_vars:
            # all variables assigned
            return True
        else:
            var = self.extractMRVvar()

            if self.TRACE:
                print('  ' * level, "bt_recurse var = ", var)

            for val in var.cur_domain():

                if self.TRACE:
                    print('  ' * level, "bt_recurse trying", var, "=", val)

                var.assign(val)
                self.nDecisions = self.nDecisions+1

                status, prunings = propagator(self.csp, var)
                self.nPrunings = self.nPrunings + len(prunings)

                if self.TRACE:
                    print('  ' * level, "bt_recurse prop status = ", status)
                    print('  ' * level, "bt_recurse prop pruned = ", prunings)

                if status:
                    if self.bt_recurse(propagator, level+1):
                        return True

                if self.TRACE:
                    print('  ' * level, "bt_recurse restoring ", prunings)
                self.restoreValues(prunings)
                var.unassign()

            self.restoreUnasgnVar(var)
            return False


    def bt_search_MS(self,propagator):
        '''This is modified from bt_search function.
        1. Keep assigned value for variables.
        2. Use bt_recurse_MS instead of bt_recurse
        '''

        self.clear_stats()
        stime = time.process_time()

        self.unasgn_vars = []
        for v in self.csp.vars:
            if not v.is_assigned():
                self.unasgn_vars.append(v)

        status, prunings = propagator(self.csp) # initial propagate no assigned variables.
        self.nPrunings = self.nPrunings + len(prunings)

        if self.TRACE:
            print(len(self.unasgn_vars), " unassigned variables at start of search")
            print("Root Prunings: ", prunings)

        if status == False:
            print("CSP{} detected contradiction at root".format(
                self.csp.name))
        else:
            status = self.bt_recurse_MS(propagator, 1) # now do recursive search


        self.restoreValues(prunings)
        if status == False:
            print("CSP{} unsolved. Has no solutions".format(self.csp.name))

        return self.nDecisions

    def bt_recurse_MS(self, propagator, level):
        '''This is modified from bt_recurse function.
        1. Using extractMRVvar_MS() instead of extractMRVvar()
        Return true if found solution. False if still need to search.
        If top level returns false--> no solution'''

        if self.TRACE:
            print('  ' * level, "bt_recurse level ", level)

        if not self.unasgn_vars:
            # all variables assigned
            return True
        else:
            var = self.extractMRVvar_MS()
            if not var:
                return True
            if self.TRACE:
                print('  ' * level, "bt_recurse var = ", var)

            for val in var.cur_domain():

                if self.TRACE:
                    print('  ' * level, "bt_recurse trying", var, "=", val)

                var.assign(val)
                self.nDecisions = self.nDecisions+1

                status, prunings = propagator(self.csp, var)
                self.nPrunings = self.nPrunings + len(prunings)

                if self.TRACE:
                    print('  ' * level, "bt_recurse prop status = ", status)
                    print('  ' * level, "bt_recurse prop pruned = ", prunings)

                if status:
                    if self.bt_recurse_MS(propagator, level+1):
                        return True

                if self.TRACE:
                    print('  ' * level, "bt_recurse restoring ", prunings)
                self.restoreValues(prunings)
                var.unassign()

            self.restoreUnasgnVar(var)
            return False

    def extractMRVvar_MS(self):
        '''Remove variable from list of unassigned vars. The variable with cur_domain size 1 or
        it's the only unassign variable in a constraint.
        Would be faster to use heap...but this is not production code.
        '''
        for var in self.unasgn_vars:
            if var.cur_domain_size() == 1:
                self.unasgn_vars.remove(var)
                return var

        for con in self.csp.get_constraints():
            if con.get_n_unasgn() == 0:
                continue
            if con.get_n_unasgn() == 1:
                mv = con.get_unasgn_vars()[0]
                self.unasgn_vars.remove(mv)
                return mv
        return None
