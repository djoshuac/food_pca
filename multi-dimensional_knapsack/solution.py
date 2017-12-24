def dim_array(dimensions, value):
    if len(dimensions) is 0:
        return value
    else:
        return [dim_array(dimensions[1:], value) for _ in range(dimensions[0])]

def vector_subtract(v1, v2):
    return [a1 - a2 for a1, a2 in zip(v1, v2)]

def vector_dist(v1, v2):
    return [abs(a1 - a2) for a1, a2 in zip(v1, v2)]

def in_bounds(space, location):
    for l in location:
        if l < 0 or l >= len(space):
            return False;
        space = space[0]
    return True

def get_value(space, location):
    for l in location:
        space = space[l]
    return space

def set_value(space, location, value):
    for l in location[:-1]:
        space = space[l]
    space[location[-1]] = value

def multi_dimensional_knapsack(items, knapsack):
    """
    items and knapsack are a list of vectors of size M
    The solution will find the closest subset of items (with replacement?)
    that sum up to a value closest to the knapsack size.

    Closest: The discrete count of items that minimizes the absolute
    normalized distance from knapsack
    """
    # normalize item values by subtracting sizes from the target knapsack??
    subproblems = dim_array(list(map(lambda x: 2*x, knapsack)), False)
    set_value(subproblems, [0 for _ in knapsack], True)

    min_d = [(sum(knapsack), knapsack), "stop"]

    def recurse_dimensions(location):
        if len(location) == len(knapsack):
            for m in items:
                prev_loc = vector_subtract(location, m)
                if in_bounds(subproblems, prev_loc) and get_value(subproblems, prev_loc):
                    set_value(subproblems, location, True)
                    d = sum(vector_dist(knapsack, location))
                    if d < min_d[0][0]:
                        min_d[0] = (d, list(location))
        else:
            for l, _ in enumerate(get_value(subproblems, location)):
                location.append(l)
                recurse_dimensions(location)
                location.pop()

    recurse_dimensions([])
    print(min_d)
    # How do we define distance?


if __name__ == "__main__":
    multi_dimensional_knapsack(
        [
            (1, 2),
            (3, 4),
            (7, 1),
            (1, 7)
        ],
        [10, 3]
    )
