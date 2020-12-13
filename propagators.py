#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete problem solution.  

'''This file will contain different constraint propagators to be used within 
   bt_search.

   propagator == a function with the following template
      propagator(csp, newly_instantiated_variable=None)
           ==> returns (True/False, [(Variable, Value), (Variable, Value) ...]

      csp is a CSP object---the propagator can use this to get access
      to the variables and constraints of the problem. The assigned variables
      can be accessed via methods, the values assigned can also be accessed.

      newly_instaniated_variable is an optional argument.
      if newly_instantiated_variable is not None:
          then newly_instantiated_variable is the most
           recently assigned variable of the search.
      else:
          progator is called before any assignments are made
          in which case it must decide what processing to do
           prior to any variables being assigned. SEE BELOW

       The propagator returns True/False and a list of (Variable, Value) pairs.
       Return is False if a deadend has been detected by the propagator.
       in this case bt_search will backtrack
       return is true if we can continue.

      The list of variable values pairs are all of the values
      the propagator pruned (using the variable's prune_value method). 
      bt_search NEEDS to know this in order to correctly restore these 
      values when it undoes a variable assignment.

      NOTE propagator SHOULD NOT prune a value that has already been 
      pruned! Nor should it prune a value twice

      PROPAGATOR called with newly_instantiated_variable = None
      PROCESSING REQUIRED:
        for plain backtracking (where we only check fully instantiated 
        constraints) 
        we do nothing...return true, []

        for forward checking (where we only check constraints with one
        remaining variable)
        we look for unary constraints of the csp (constraints whose scope 
        contains only one variable) and we forward_check these constraints.

        for gac we establish initial GAC by initializing the GAC queue
        with all constaints of the csp


      PROPAGATOR called with newly_instantiated_variable = a variable V
      PROCESSING REQUIRED:
         for plain backtracking we check all constraints with V (see csp method
         get_cons_with_var) that are fully assigned.

         for forward checking we forward check all constraints with V
         that have one unassigned variable left

         for gac we initialize the GAC queue with all constraints containing V.
		 
		 
var_ordering == a function with the following template
    var_ordering(csp)
        ==> returns Variable 

    csp is a CSP object---the heuristic can use this to get access to the
    variables and constraints of the problem. The assigned variables can be
    accessed via methods, the values assigned can also be accessed.

    var_ordering returns the next Variable to be assigned, as per the definition
    of the heuristic it implements.
   '''

def prop_BT(csp, newVar=None):
    '''Do plain backtracking propagation. That is, do no 
    propagation at all. Just check fully instantiated constraints'''
    
    if not newVar:
        return True, []
    for c in csp.get_cons_with_var(newVar):
        if c.get_n_unasgn() == 0:
            vals = []
            vars = c.get_scope()
            for var in vars:
                vals.append(var.get_assigned_value())
            if not c.check(vals):
                return False, []
    return True, []

def prop_FC(csp, newVar=None):
    '''Do forward checking. That is check constraints with 
       only one uninstantiated variable. Remember to keep 
       track of all pruned variable,value pairs and return '''

    pruned = []

    if not newVar:
        constraint = csp.get_all_cons()
    else:
        constraint = csp.get_cons_with_var(newVar)

    #for every constraint indicator to check whether it has a possible assignment for the unassigned variable
    for con in constraint:
        indicator = True
        if con.get_n_unasgn() == 1:
            indicator = False

            #current value location and whether we found it or not
            curvalloc = 0
            found = False

            var = con.get_scope()
            vallist = []

            #vallist for future constraint check and grab unassigned variable location
            for v in var:
                if v.get_assigned_value() == None:
                    curvar = v
                    found = True
                vallist.append(v.get_assigned_value())

                #if havent found the unassigned val keep updating
                if found == False:
                    curvalloc +=1

            curdom = curvar.cur_domain()

            #Checking and pruning
            for val in curdom:
                vallist[curvalloc] = val

                if not con.check(vallist):
                    pruned.append((curvar, val))
                    curvar.prune_value(val)
                else:
                    indicator = True

        if indicator == False:
            return False, pruned

    return True, pruned







def prop_GAC(csp, newVar=None):
    '''Do GAC propagation. If newVar is None we do initial GAC enforce 
       processing all constraints. Otherwise we do GAC enforce with
       constraints containing newVar on GAC Queue'''
    pruned = []

    if not newVar:
        constraint = csp.get_all_cons()
    else:
        constraint = csp.get_cons_with_var(newVar)

    while len(constraint) > 0:
        con = constraint.pop(0)
        var = con.get_scope()
        for v in var:

            #identify whether an variable has been modified if so, update constraint
            changedind = False
            for val in v.cur_domain():

                #no support, prune
                if not con.has_support(v, val):
                    pruned.append((v, val))
                    v.prune_value(val)
                    changedind = True

                    #if no more values to test in domain, means failed
                    if v.cur_domain_size() < 1:
                        return False, pruned

            #variable has been pruned so update constraint
            if changedind == True:
                for newcon in csp.get_cons_with_var(v):
                    if newcon in constraint:
                        continue
                    else:
                        constraint.append(newcon)

    return True, pruned




def ord_mrv(csp):
    ''' return variable according to the Minimum Remaining Values heuristic '''
    # we only want first value and not whole list..., but I've left it here as a referrence.
    vars = csp.get_all_unasgn_vars()
    '''
    templist = []
    for v in vars:
        templist.append([v, v.cur_domain_size()])

    newlist = sec_elem_srt(templist)
    mrvlist = []
    for i in newlist:
        mrvlist.append(i[0])'''

    lowest = vars[0].cur_domain_size()
    lowestvar = vars[0]

    for v in vars:
        if v.cur_domain_size() < lowest:
            lowest = v.cur_domain_size()
            lowestvar = v

    return lowestvar



#def sec_elem_srt(list):
#    list.sort(key = lambda x: x[1])
#    return list