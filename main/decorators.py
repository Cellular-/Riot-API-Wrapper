import functools, time

def rate_limit(func):
    """Puts process to sleep between each call."""
    @functools.wraps(func)
    def wrapper_rate_limiter(*args, **kwargs):
        f = func(*args, **kwargs)
        time.sleep(.5)

        return f
    return wrapper_rate_limiter