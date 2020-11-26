'''This file will contain different constraint propagators to be used within
   bt_search.

   TODO: CLARA AND NOLAN CLEAN THIS UP
   '''

def prop_BT(csp, newVar=None):
    '''Do plain backtracking propagation. That is, do no
    propagation at all. Just check fully instantiated constraints'''

    if not newVar:
        return True, []
    for c in csp.get_constraints(newVar):
        if c.get_unassigned() == 0:
            vals = []
            vars = c.get_scope()
            for var in vars:
                vals.append(var.get_assigned_value())
            if not c.verify(vals):
                return False, []
    return True, []

def prop_FC(csp, newVar=None):
    '''Do forward checking. That is check constraints with
       only one uninstantiated variable. Remember to keep
       track of all pruned variable,value pairs and return '''
#IMPLEMENT

    pruned = []
    isDeadend = False

    if not newVar:
        cons = csp.get_all_cons()
        for con in cons:
            scope = con.get_scope()
            if len(scope) == 1:
                result = FCCheck(con, scope[0])
                pruned.extend(result[1])
                if not result[0]:
                    isDeadend = True
                    break

    cons = csp.get_all_cons()
    for con in cons:
        scope = con.get_scope()
        if con.get_unassigned() == 1:
            result = FCCheck(con, con.get_unasgn_vars()[0])
            pruned.extend(result[1])
            if not result[0]:
                isDeadend = True
                break
    if isDeadend:
        return (False, pruned)
    return (True, pruned)


def FCCheck(C, x):
    '''
    (Constraint, Variable) -> (Bool, list of tuple(Varialbe, Value))

    Given a constraint C and a variable x, return True if the current domain
    size of x is not zero; False otherwise. Also return a list of (var, val)
    tuples that pruned.
    '''
    pruned = []
    cur_dom = x.cur_domain()
    for val in cur_dom:
        if not C.has_support(x, val):
            x.prune_value(val)
            pruned.append((x, val))

    if not x.cur_domain_size():
        return (False, pruned)
    return (True, pruned)


def prop_GAC(csp, newVar=None):
    '''Do GAC propagation. If newVar is None we do initial GAC enforce
       processing all constraints. Otherwise we do GAC enforce with
       constraints containing newVar on GAC Queue'''
#IMPLEMENT

    queue = []
    pruned = []
    cons = csp.get_all_cons()

    if not newVar:
        queue = cons.copy()
    else:
        queue = csp.get_constraints(newVar).copy()

    # For looping queue use an indicator count. It avoids keep append and
    # remove items in the queue list that may slow down the program.
    count = 0
    while count < len(queue):

        con = queue[count]
        scope = con.get_scope()

        for i in range(len(scope)):
            var = scope[i]
            curdom = var.cur_domain()
            found = False
            for val in curdom:
                if con.has_support(var, val):
                    continue
                else:
                    found = True
                    var.prune_value(val)
                    pruned.append((var, val))
                    if not var.cur_domain_size():
                        queue = []
                        return (False, pruned)

            if found:
                cons = csp.get_constraints(var)
                for c in cons:
                    if c not in queue[count:]:
                        queue.append(c)
        count += 1

    return (True, pruned)
