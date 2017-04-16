def print_move(origin, destination):
    """Print instructions to move a disk."""
    print("Move the top disk from rod", origin, "to rod", destination)

def move_stack(n, start, end):
    """Print the moves required to move n disks on the start pole to the end
    pole without violating the rules of Towers of Hanoi.

    n -- number of disks
    start -- a pole position, either 1, 2, or 3
    end -- a pole position, either 1, 2, or 3

    There are exactly three poles, and start and end must be different. Assume
    that the start pole has at least n disks of increasing size, and the end
    pole is either empty or has a top disk larger than the top n start disks.

    >>> move_stack(1, 1, 3)
    Move the top disk from rod 1 to rod 3
    >>> move_stack(2, 1, 3)
    Move the top disk from rod 1 to rod 2
    Move the top disk from rod 1 to rod 3
    Move the top disk from rod 2 to rod 3
    >>> move_stack(3, 1, 3)
    Move the top disk from rod 1 to rod 3
    Move the top disk from rod 1 to rod 2
    Move the top disk from rod 3 to rod 2
    Move the top disk from rod 1 to rod 3
    Move the top disk from rod 2 to rod 1
    Move the top disk from rod 2 to rod 3
    Move the top disk from rod 1 to rod 3
    """
    assert 1 <= start <= 3 and 1 <= end <= 3 and start != end, "Bad start/end"
    "*** YOUR CODE HERE ***"
    def move(n, start, end, mid=2):
        if n == 1:    
            print("Move the top disk from rod {} to rod {}".format(start, end))
        else:        
            move(n-1, start, mid, end)
            move(1, start, end, mid)
            move(n-1, mid, end, start)
        
    return move(n, start, end)

def interval(a, b):
    """Construct an interval from a to b."""
    return [a, b]

def lower_bound(x):
    """Return the lower bound of interval x."""
    "*** YOUR CODE HERE ***"
    return x[0]

def upper_bound(x):
    """Return the upper bound of interval x."""
    "*** YOUR CODE HERE ***"
    return x[1]

def str_interval(x):
    """Return a string representation of interval x."""
    return '{0} to {1}'.format(lower_bound(x), upper_bound(x))

def add_interval(x, y):
    """Return an interval that contains the sum of any value in interval x and
    any value in interval y."""
    lower = lower_bound(x) + lower_bound(y)
    upper = upper_bound(x) + upper_bound(y)
    return interval(lower, upper)

def mul_interval(x, y):
    """Return the interval that contains the product of any value in x and any
    value in y."""
    p1 = lower_bound(x) * lower_bound(y)
    p2 = lower_bound(x) * upper_bound(y)
    p3 = upper_bound(x) * lower_bound(y)
    p4 = upper_bound(x) * upper_bound(y)
    return interval(min(p1, p2, p3, p4), max(p1, p2, p3, p4))

def sub_interval(x, y):
    """Return the interval that contains the difference between any value in x
    and any value in y."""
    "*** YOUR CODE HERE ***"
    lower = lower_bound(x) - upper_bound(y)
    upper = upper_bound(x) - lower_bound(y)
    return interval(lower, upper)


def div_interval(x, y):
    """Return the interval that contains the quotient of any value in x divided by
    any value in y. Division is implemented as the multiplication of x by the
    reciprocal of y."""
    "*** YOUR CODE HERE ***"
    assert lower_bound(y) > 0 or upper_bound(y) < 0
    reciprocal_y = interval(1/upper_bound(y), 1/lower_bound(y))
    return mul_interval(x, reciprocal_y)

def par1(r1, r2):
    return div_interval(mul_interval(r1, r2), add_interval(r1, r2))

def par2(r1, r2):
    one = interval(1, 1)
    rep_r1 = div_interval(one, r1)
    rep_r2 = div_interval(one, r2)
    return div_interval(one, add_interval(rep_r1, rep_r2))

def check_par():
    """Return two intervals that give different results for parallel resistors.

    >>> r1, r2 = check_par()
    >>> x = par1(r1, r2)
    >>> y = par2(r1, r2)
    >>> lower_bound(x) != lower_bound(y) or upper_bound(x) != upper_bound(y)
    True
    """
    r1 = interval(2, 4) # Replace this line!
    r2 = interval(3, 5) # Replace this line!
    return r1, r2

def multiple_references_explanation():
    return """The multiple reference problem exits in par1. Since mul_interval and
    add_interval refers r1 and r2 respectively, and produce independent interval.
    Then, combining them would make the result larger than the fixed interval."""

def quadratic(x, a, b, c):
    """Return the interval that is the range of the quadratic defined by
    coefficients a, b, and c, for domain interval x.

    >>> str_interval(quadratic(interval(0, 2), -2, 3, -1))
    '-3 to 0.125'
    >>> str_interval(quadratic(interval(1, 3), 2, -3, 1))
    '0 to 10'
    """
    "*** YOUR CODE HERE ***"
    def f(t):
        return a*t*t + b*t + c
    extreme_point = -b / (2*a)
    p = [f(upper_bound(x)), f(lower_bound(x))]
    if lower_bound(x) < extreme_point < upper_bound(x):
        p.append(f(extreme_point))
    return interval(min(p), max(p))

def polynomial(x, c):
    """Return the interval that is the range of the polynomial defined by
    coefficients c, for domain interval x.

    >>> str_interval(polynomial(interval(0, 2), [-1, 3, -2]))
    '-3 to 0.125'
    >>> str_interval(polynomial(interval(1, 3), [1, -3, 2]))
    '0 to 10'
    >>> str_interval(polynomial(interval(0.5, 2.25), [10, 24, -6, -8, 3]))
    '18.0 to 23.0'
    """
    "*** YOUR CODE HERE ***"
    def improve(update, close, guess=1):
        while not close(guess):
            guess = update(guess)
        return guess
    
    def approx_eq(x, y, tolerance=1e-15):
        return abs(x - y) < tolerance

    def newton_update(f, df):
        def update(x):
            return x - f(x) / df(x)
        return update
    
    def find_zero(f, df, step):
        def near_zero(x):
            return approx_eq(f(x), 0)
        return improve(newton_update(f, df), near_zero, step)    

    def find_extreme_point(c, step):
        def f(t):
            return sum([val * i * pow(t, i-1) for i, val in enumerate(c) if i > 0])

        def df(t):
            return sum([val * i * (i-1) * pow(t, i-2) for i, val in enumerate(c) if i > 1])

        return find_zero(f, df, step)

    def f(t):
        return sum([val * pow(t, i) for i, val in enumerate(c)])

    step_size = 20
    one_step = (upper_bound(x) - lower_bound(x)) / step_size
    step = [lower_bound(x) + one_step * i for i in range(step_size+1)]

    extreme_point = []
    for i in range(step_size + 1):
        extreme_point.append(find_extreme_point(c, step[i]))
    extreme_point = set(extreme_point)

    p = [f(lower_bound(x)), f(upper_bound(x))]
    
    for point in extreme_point:
        if lower_bound(x) < point < upper_bound(x):
            p.append(f(point))
    
    return interval(min(p), max(p))
