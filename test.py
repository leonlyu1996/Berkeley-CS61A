def keep_ints(n):
    """Returns a function which takes one parameter cond and 
    prints out all integers 1..i..n where calling cond(i) returns True.
    """
    def inner(cond):
        for i in range(n):
            if cond(i):
                print(i)
    return inner