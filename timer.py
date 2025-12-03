from functools import wraps
import cProfile
import pstats

def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):    
        profiler = cProfile.Profile()
        profiler.enable()
        result = func(*args, **kwargs)
        profiler.disable()
    
        return result
    return wrapper