assignments = []

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s + t for s in A for t in B]

"""Global Variables used in following functions"""
rows = 'ABCDEFGHI'
cols = '123456789'

boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diag_units = [[i[0] + i[1] for i in zip(rows, cols)], [i[0] + i[1] for i in zip(rows[::-1], cols)]]
unitlist = row_units + column_units + square_units + diag_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    if type(values) is bool:
        return values
    # Find all instances of naked twins
    for unit in unitlist:
        # get all boxes with two values in this unit
        possibletwins = [box for box in unit if len(values[box]) == 2]
        twins = []
        twinvalues = []
        if len(possibletwins) > 1:
            cmptwins = possibletwins.copy()
            # we have to do n * (n - 1) / 2 comparisons with n = len(possibleTwins)
            for b1 in possibletwins:
                # compare b1 just with following boxes
                cmptwins = cmptwins[1:].copy()
                for b2 in cmptwins:
                    # check if values are equal, if True save boxes and value
                    # there may be more than one twin pair in an unit
                    if values[b1] == values[b2]:
                        twins.append(b1)
                        twins.append(b2)
                        twinvalues.append(values[b1])
            # now eliminate the naked twins as possibilities from their peers
            if len(twins) > 0:
                # loop over peers
                for u in unit:
                    # check if box is a twin. As we want to eliminate twin values, we have to be sure that we do not
                    # delete the values in a twin box
                    if u not in twins:
                        # eliminate twin values from boxes in box u
                        for v in twinvalues:
                            for vv in v:
                                values = assign_value(values, u, values[u].replace(vv, ""))
    return values


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values = assign_value(values, peer, values[peer].replace(digit,''))
    return values

def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values = assign_value(values, dplaces[0], digit)
    return values

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if type(values) is bool:
        return values

    # Choose one of the unfilled squares with the fewest possibilities
    vMin = 10
    vValues = ''
    kMin = ''
    for k, v in values.items():
        vLen = len(v)
        if vLen > 1:
            if vLen < vMin:
                kMin = k
                vMin = len(v)
                vValues = v
        elif vLen == 0:
            return False

    if kMin == '':
        return values
    else:
        for v in vValues:
            valuesCP = values.copy()
            valuesCP = assign_value(valuesCP, kMin, v)
            searchReturn = search(valuesCP)
            if type(searchReturn) is dict:
                return searchReturn
        return False

    return values

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    # generate grid
    values = grid_values(grid)

    # solve soduko
    return search(values)


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
