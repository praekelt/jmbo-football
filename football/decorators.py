import sys

from django.conf import settings


def layered(func):
    """If a function with name "func_name + _ + layer" exists then it is called, 
    else func is called normally."""    
    def new(request, *args, **kwargs):
        for layer in settings.FOUNDRY['layers']:
            method = getattr(
                sys.modules[func.__module__],
                '%s_%s' % (func.func_name, layer),                 
                None
            )
            if method is not None:
                return method(request, *args, **kwargs)

        return func(request, *args, **kwargs)
    
    return new
