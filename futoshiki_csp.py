#Look for #IMPLEMENT tags in this file.
'''
All models need to return a CSP object, and a list of lists of Variable objects 
representing the board. The returned list of lists is used to access the 
solution. 

For example, after these three lines of code

    csp, var_array = futoshiki_csp_model_1(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array[0][0].get_assigned_value() should be the correct value in the top left
cell of the Futoshiki puzzle.

1. futoshiki_csp_model_1 (worth 20/100 marks)
    - A model of a Futoshiki grid built using only 
      binary not-equal constraints for both the row and column constraints.

2. futoshiki_csp_model_2 (worth 20/100 marks)
    - A model of a Futoshiki grid built using only n-ary 
      all-different constraints for both the row and column constraints. 

'''
from cspbase import *
import itertools

def futoshiki_csp_model_1(futo_grid):
    # create CSP and let it automatically do vars to cons
    csp = CSP("Futoshiki Model 1")

    #create domains (board size and board + operators size)
    bs = len(futo_grid)
    bops = len(futo_grid[0])
    domain = []
    for i in range(bs):
        domain.append(i+1)

    #create variables and organize the data to return the var array
    var_array = []
    operators = []
    for i in range(bs):
        temprow = []
        tempops = []
        counter = 1
        for j in range(bops):
            if type(futo_grid[i][j]) == int:
                if futo_grid[i][j] == 0:
                    tempvar = Variable("V"+str(i)+str(counter), domain)
                else:
                    tempvar = Variable("V" + str(i) + str(counter), [futo_grid[i][j]])
                #adding variable to vars csp and let it handle vars to cons
                csp.add_var(tempvar)
                counter += 1
                temprow.append(tempvar)
            else:
                tempops.append(futo_grid[i][j])
        var_array.append(temprow)
        operators.append(tempops)

    #create constraints
    for i in range(bs):
        for j in range(bs):
            for k in range(j+1,bs):
                #row ij and ik, add constraint to csp, so csp auto handle vars to cons
                sat_tuples = []
                con = Constraint("C" + str(i) + str(j)+ str(i) + str(k), [var_array[i][j], var_array[i][k]])
                for x in itertools.product(var_array[i][j].cur_domain(),var_array[i][k].cur_domain()):
                    if k - j == 1:
                        #bin ineq and not equal
                        if satcon(x[0], x[1], operators[i][j]) and x[0] != x[1]:
                            sat_tuples.append(x)
                    else:
                        #not beside each other so just not equal
                        if x[0] != x[1]:
                            sat_tuples.append(x)
                con.add_satisfying_tuples(sat_tuples)
                csp.add_constraint(con)

                #col ji and ki, add constraint to csp, so csp auto handle vars to cons
                sat_tuples2 = []
                con2 = Constraint("C" + str(j) + str(i) + str(k) + str(i), [var_array[j][i], var_array[k][i]])
                for x in itertools.product(var_array[j][i].cur_domain(), var_array[k][i].cur_domain()):
                    # col doesn't have operators so just not equal
                    if x[0] != x[1]:
                        sat_tuples2.append(x)
                con2.add_satisfying_tuples(sat_tuples2)
                csp.add_constraint(con2)

    return csp, var_array

def satcon(var1, var2, operator):

    if operator == '>':
        return var1 > var2
    elif operator == '<':
        return var1 < var2

    return True

def futoshiki_csp_model_2(futo_grid):
    # create CSP and let it automatically do vars to cons
    csp = CSP("Futoshiki Model 2")

    # create domains (board size and board + operators size)
    bs = len(futo_grid)
    bops = len(futo_grid[0])
    domain = []
    for i in range(bs):
        domain.append(i + 1)

    # create variables and organize the data to return the var array
    var_array = []
    operators = []
    for i in range(bs):
        temprow = []
        tempops = []
        counter = 1
        for j in range(bops):
            if type(futo_grid[i][j]) == int:
                if futo_grid[i][j] == 0:
                    tempvar = Variable("V" + str(i) + str(counter), domain)
                else:
                    tempvar = Variable("V" + str(i) + str(counter), [futo_grid[i][j]])
                # adding variable to vars csp and let it handle vars to cons
                csp.add_var(tempvar)
                counter += 1
                temprow.append(tempvar)
            else:
                tempops.append(futo_grid[i][j])
        var_array.append(temprow)
        operators.append(tempops)

    #create constraint split by all different and binary operators

    #binary operators
    for i in range(len(operators)):
        for j in range(len(operators[0])):
            if operators[i][j] == '<':
                sat_tuples = []
                con = Constraint("C" + str(i) + str(j) + str(i) + str(j+1), [var_array[i][j], var_array[i][j+1]])
                for x in itertools.product(var_array[i][j].cur_domain(), var_array[i][j+1].cur_domain()):
                    # col doesn't have operators so just not equal
                    if x[0] < x[1]:
                        sat_tuples.append(x)
                con.add_satisfying_tuples(sat_tuples)
                csp.add_constraint(con)
            elif operators[i][j] == '>':
                sat_tuples = []
                con = Constraint("C" + str(i) + str(j) + str(i) + str(j + 1), [var_array[i][j], var_array[i][j + 1]])
                for x in itertools.product(var_array[i][j].cur_domain(), var_array[i][j + 1].cur_domain()):
                    # col doesn't have operators so just not equal
                    if x[0] > x[1]:
                        sat_tuples.append(x)
                con.add_satisfying_tuples(sat_tuples)
                csp.add_constraint(con)

    #alldif ops
    for i in range(bs):
        row = []
        rowvar = []
        col = []
        colvar = []
        for j in range(bs):
            row.append(var_array[i][j].cur_domain())
            rowvar.append(var_array[i][j])
            col.append(var_array[j][i].cur_domain())
            colvar.append(var_array[j][i])
        #row
        sat_tuples = []
        con = Constraint("Row" + str(i), rowvar)
        for t in itertools.product(*row):
            if alldif(t):
                sat_tuples.append(t)
        con.add_satisfying_tuples(sat_tuples)
        csp.add_constraint(con)

        #col
        sat_tuples2 = []
        con2 = Constraint("Col" + str(i), colvar)
        for t in itertools.product(*col):
            if alldif(t):
                sat_tuples2.append(t)
        con2.add_satisfying_tuples(sat_tuples2)
        csp.add_constraint(con2)

    return csp, var_array

def alldif(list):
    return len(list) == len(set(list))