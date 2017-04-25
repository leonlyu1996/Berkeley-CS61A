from lab07 import *
from functools import reduce
import operator

def max_product(lst):
    """Return the maximum product that can be formed using lst
    without using any consecutive numbers
    >>> max_product([10,3,1,9,2]) # 10 * 9
    90
    >>> max_product([5,10,5,10,5]) # 5 * 5 * 5
    125
    >>> max_product([])
    1
    """
    if not lst:
        return 1
    if len(lst) <= 2:
        return max(lst)
    return max(lst[0]*max_product(lst[2:]), max_product(lst[1:]))

def eval_tree(tree):
    """Evaluates an expression tree with functions as root
    >>> eval_tree(Tree(1))
    1
    >>> expr = Tree('*', [Tree(2), Tree(3)])
    >>> eval_tree(expr)
    6
    >>> eval_tree(Tree('+', [expr, Tree(4), Tree(5)]))
    15
    """
    if tree.root == '+':
        return reduce(operator.add, [eval_tree(b) for b in tree.branches], 0)
    if tree.root == '*':
        return reduce(operator.mul, [eval_tree(b) for b in tree.branches], 1)
    return tree.root

def quicksort_list(lst):
    """
    >>> quicksort_list([3, 1, 4])
    [1, 3, 4]
    """
    if len(lst) == 1:
        return lst
    pivot = lst[0]
    less = [a for a in lst if a < pivot]
    greater = [a for a in lst if a > pivot]
    return quicksort_list(less) + [pivot] + quicksort_list(greater)