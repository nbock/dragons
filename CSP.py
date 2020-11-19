'''
CSP Class
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

    # TODO: didn't include any pruning methods

    # assignment
    def is_assigned(self):
        return self.assignedValue is not None

    def assign(self, value):
        if self.is_assigned() or not self.currentdomain

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

    # TODO: I think this is all we need for a CSP formulation


class CSP:
    def __init__(self, vars=list()):
        self.vars = vars
        self.cons = list()
        self.map = dict()
        for variable in vars:
            self.append_variable(v)

    def append_variable(self, var):
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
        retun self.cons

    def get_constraint(self, variable):
        '''
        get a constraint with a specific variable in it
        '''
        return list(self.map[var])

    def get_vars(self):
        return self.vars
