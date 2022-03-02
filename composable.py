from functools import reduce, partial

class Composable:
    '''
    A class that wraps functions and makes them composable.
    The @ operator is used for function composition.
    The | operator is reverse function composition.
    Composable functions can be composed with any callable.
    For example, if
        f = Composable(lambda x: x+1)
        g = lambda x: 2*x
        fog = f@g
    Then
             fog(x) == (2*x)+1
        x | (g | f) == (2*x)+1
    Notice that bitwise or "|" operates from left to right, so the 
    first function in the pipeline must be Composable, or the
    pipline must be wrapped in parens to ensure it is converted
    to a Composable before evaluation.
    '''

    def __init__(self, f=None):
        if isinstance(f, Composable):
            self.function_tuple = f.function_tuple
        elif callable(f):
            self.function_tuple = (f,)
        elif f is None:
            self.function_tuple = (identity, )
        else:
            raise ValueError('Input must be a callable')
        
        
    def __call__(self, x):
        def _call(x, f):
            return f(x)
        return reduce(_call, self.function_tuple, x)
        
    def __matmul__(self, g):
        '''
        We are f.
        Return f o g
        '''
        fog = Composable()
        assert callable(g)
        if isinstance(g, Composable):
            fog.function_tuple = g.function_tuple + self.function_tuple
        else:
            fog.function_tuple = (g,) + self.function_tuple
        return fog
        
    def __rmatmul__(self, f):
        '''
        We are g.
        Return f o g
        '''
        assert callable(f)
        fog = Composable()
        if isinstance(f, Composable):
            fog.function_tuple = self.function_tuple + f.function_tuple
        else:
            fog.function_tuple = self.function_tuple + (f,)
        return fog

    def __or__(self, g):
        '''
        Pipe our output into g.
        We are f, return g o f
        '''
        return g@self
        
    def __ror__(self, g):
        '''
        Pipe g, or the output of g into us.
        We are f. 
        If g is a value, return f(g). 
        If g is a function return f o g.
        '''
        if callable(g):
            return self @ g
        else:
            return self(g)

    def __repr__(self):
        return 'Composable [' + ' | '.join(f.__repr__() for f in self.function_tuple) + ']'

    def __str__(self):
        return ' | '.join(callable_to_string(f) for f in self.function_tuple)
    
# Helpers

def identity(x):   
    '''
    A provided identity function for printing purposes.
    '''
    return x

def callable_to_string(f):
    '''
    For printing purposes. Returns a valid string for named functions,
    lambdas, maps, filters, and partials. Defaults to str(f) if not
    recognized.
    '''
    if hasattr(f, '__name__'):
        return f.__name__

    if isinstance(f, partial):
        return 'partial(' + callable_to_string(f.func) + ', ' + ', '.join(callable_to_string(arg) for arg in f.args) + ')'

    if f is map:
        return 'map'

    if f is filter:
        return 'filter'

    return str(f)


