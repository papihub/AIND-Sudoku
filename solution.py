
from utils import *
from copy import deepcopy

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diag_units = [[rows[x]+cols[x] for x in range(0,9)], [rows[x]+cols[8-x] for x in range(0,9)]]

unitlist = row_units + column_units + square_units + diag_units
#unitlist = row_units + column_units + square_units

# TODO: Update the unit list to add the new diagonal units
unitlist = unitlist

units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


def naked_twins(values):
    """Eliminate values using the naked twins strategy.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the naked twins eliminated from peers

    Notes
    -----
    Your solution can either process all pairs of naked twins from the input once,
    or it can continue processing pairs of naked twins until there are no such
    pairs remaining -- the project assistant test suite will accept either
    convention. However, it will not accept code that does not process all pairs
    of naked twins from the original input. (For example, if you start processing
    pairs of twins and eliminate another pair of twins before the second pair
    is processed then your code will fail the PA test suite.)

    The first convention is preferred for consistency with the other strategies,
    and because it is simpler (since the reduce_puzzle function already calls this
    strategy repeatedly).
    """
    if ( not values ):
        return values

    my_values = deepcopy(values)
    #display(values)
    for u in unitlist:
        for a in u:
            if len(my_values[a]) != 2:
                continue
            for b in u:
                if my_values[a] == my_values[b] and a != b:
                    for c in set(u) - set([a,b]):
                        my_values[c] = my_values[c].translate(str.maketrans('','',my_values[b]))
                
                                    
    return my_values
    # TODO: Implement this function!
    raise NotImplementedError

def naked_twins_superior(values):
    """Eliminate values using the naked twins strategy.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the naked twins eliminated from peers

    Notes
    -----
    Your solution can either process all pairs of naked twins from the input once,
    or it can continue processing pairs of naked twins until there are no such
    pairs remaining -- the project assistant test suite will accept either
    convention. However, it will not accept code that does not process all pairs
    of naked twins from the original input. (For example, if you start processing
    pairs of twins and eliminate another pair of twins before the second pair
    is processed then your code will fail the PA test suite.)

    The first convention is preferred for consistency with the other strategies,
    and because it is simpler (since the reduce_puzzle function already calls this
    strategy repeatedly).
    """
    if ( not values ):
        return values

    my_values = deepcopy(values)
    #display(values)

    board_changed=1
    while(board_changed):
        board_changed = 0
        for u in unitlist:
            occurs = dict((s,set()) for s in '123456789' )
            for b in u:
                for s in my_values[b]:
                    occurs[s].add(b)
            x=[s for s in '123456789' ]
            x_rem=set()
            for i in x:
                if i in x_rem:
                    continue
                for j in x[x.index(i)+1:]:
                    if j in x_rem:
                        continue
                    if(occurs[i] == occurs[j] and len(occurs[i]) == 2):
                        for b in occurs[i]:
                            if(len(my_values[b]) != 2):
                                my_values[b] = i+j
                                print("set ", b, " to ", i+j, u)
                                board_changed = 1
                        for b in set(u) - occurs[i]:
                            if i in my_values[b] or j in my_values[b]:
                                my_values[b] = my_values[b].translate(str.maketrans('','',i+j))
                                board_changed = 1
                                print("removed ", i+j, " from ", b, u)
                        x_rem.add(i)
                        x_rem.add(j)
            occurs = dict((s,set()) for s in '123456789' )
            for b in u:
                for s in my_values[b]:
                    occurs[s].add(b)
            u_rem=set()
            for i in u:
                if i in u_rem:
                    continue
                for j in u[u.index(i)+1:]:
                    if j in u_rem:
                        continue
                    if(my_values[i] == my_values[j] and len(my_values[i]) == 2):
                        x=set()
                        for s in my_values[i]:
                            x |= occurs[s]
                        x.discard(i)
                        x.discard(j)
                        if(len(x)>0):
                            print("removing ", my_values[i], " from ", x, u)
                        for b in x:
                            my_values[b] = my_values[b].translate(str.maketrans('','',my_values[i]))
                            board_changed = 2
                        u_rem.add(i)
                        u_rem.add(j)
                                    
    return my_values
    # TODO: Implement this function!
    raise NotImplementedError


def eliminate(values):
    """Apply the eliminate strategy to a Sudoku puzzle

    The eliminate strategy says that if a box has a value assigned, then none
    of the peers of that box can have the same value.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the assigned values eliminated from peers
    """
    if ( not values ):
        return values

    my_values = deepcopy(values)
    from collections import deque
    solved_boxes = deque([ b for b in values if len(my_values[b]) == 1 ])
    unsolved_peers = dict((b1,set(b2 for b2 in peers[b1] if len(my_values[b2]) > 1)) for b1 in my_values )

    while(len(solved_boxes)):
        x = solved_boxes.popleft()
        new_solved_peers = set()
        for b in unsolved_peers[x]:
            my_values[b] = my_values[b].translate(str.maketrans('','',my_values[x]))
            if(not my_values[b]):
                return False
            if (len(my_values[b]) == 1):
                solved_boxes.append(b)
                new_solved_peers.add(b)
        unsolved_peers[x] -= new_solved_peers
    

    return my_values
    # TODO: Copy your code from the classroom to complete this function
    raise NotImplementedError


def only_choice(values):
    """Apply the only choice strategy to a Sudoku puzzle

    The only choice strategy says that if only one box in a unit allows a certain
    digit, then that box must be assigned that digit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with all single-valued boxes assigned

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    """
    if ( not values ):
        return values
    
    my_values = deepcopy(values)
    
    for u in unitlist:
        occurs = dict((s,set()) for s in '123456789' )
        for b in u:
            for x in my_values[b]:
                occurs[x].add(b)
        for s in occurs:
            if len(occurs[s]) == 1:
                x = occurs[s].pop()
                my_values[x] = s
    return my_values
    # TODO: Copy your code from the classroom to complete this function
    raise NotImplementedError

def is_solved(values):
    """Check if the puzzle is solved.
    
    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    0 - Error, 1 - solved or 2 - Unsolved
        The values dictionary with all boxes assigned or False
    """
    my_values = values
    #display(my_values)
    #print(my_values)
    if(not my_values):
        return 0
    
    for u in unitlist:
        u_sum = 0
        for b in u:
            if(my_values[b]):
                x = len(my_values[b])
            else:
                return 0
            if(x == 0):
                return 0
            elif(x > 1):
                return 2
            else:
                u_sum += int(my_values[b])
        if(u_sum != 45):
            return 0
    
    return 1

def print_dict_diff(x,y):
    print([(a,x[a],y[a]) for a in x if x[a] != y[a] ])
    

def reduce_puzzle(values):
    """Reduce a Sudoku puzzle by repeatedly applying all constraint strategies

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary after continued application of the constraint strategies
        no longer produces any changes, or False if the puzzle is unsolvable 
    """
    if ( not values ):
        return values

    my_values = deepcopy(values)
    new_values = dict()
    repeat_loop = 1
    while ( repeat_loop ):
        #display(my_values)
        x = eliminate(my_values)
        #print("After eliminate:")
        #print_dict_diff(x, my_values)
        new_values = x

        x = only_choice(new_values)
        #print("After only_choice:")
        #print_dict_diff(x, new_values)
        new_values = x

        x = naked_twins(new_values)
        #print("After naked_twins:")
        #print_dict_diff(x, new_values)
        new_values = x

        if new_values == my_values:
            repeat_loop = 0
        else:
            my_values = new_values
        
    if is_solved(my_values):
        return my_values
    else:
        return False
    # TODO: Copy your code from the classroom and modify it to complete this function
    raise NotImplementedError


def search(values):
    """Apply depth first search to solve Sudoku puzzles in order to solve puzzles
    that cannot be solved by repeated reduction alone.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary with all boxes assigned or False

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    and extending it to call the naked twins strategy.
    """
    if ( not values ):
        return values

    my_values = deepcopy(values)
    new_values = reduce_puzzle(my_values)
    i = is_solved(new_values)
    if(i == 1):
        return new_values
    elif(i == 0):
        return False
    
    min_l = 10
    min_b = 'X'
    for b in new_values:
        l = len(new_values[b])
        if(l == 2 ):
            min_b = b
            break
        elif(l < min_l and l > 2):
            min_l = l
            min_b = b
    #print("Ready to guess: b: "+b)
    #display(new_values)
    
    for x in new_values[min_b]:
        guess_values = deepcopy(new_values)
        guess_values[min_b] = x
        guess_values = search(guess_values)
        if(guess_values):
            return guess_values
    return False
    # TODO: Copy your code from the classroom to complete this function
    raise NotImplementedError


def solve(grid):
    """Find the solution to a Sudoku puzzle using search and constraint propagation

    Parameters
    ----------
    grid(string)
        a string representing a sudoku grid.
        
        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    Returns
    -------
    dict or False
        The dictionary representation of the final sudoku grid or False if no solution exists.
    """
    values = grid2values(grid)
    values = search(values)
    return values


if __name__ == "__main__":
    #diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    #diag_sudoku_grid = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
    diag_sudoku_grid = '9.1....8.8.5.7..4.2.4....6...7......5..............83.3..6......9................'
    #diag_sudoku_grid='........4......1.....6......7....2.8...372.4.......3.7......4......5.6....4....2.'
    display(grid2values(diag_sudoku_grid))
    result = solve(diag_sudoku_grid)
    display(result)

    try:
        import PySudoku
        PySudoku.play(grid2values(diag_sudoku_grid), result, history)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
