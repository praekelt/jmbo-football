import sys

from django.conf import settings


class layered:
    """If a function or object with name "func_name + _ + layer" exists then it
    is called, else func is called normally."""    

    def __init__(self, default='basic'):
        self.default = default

    def __call__(self, func):
   
        def new(request, *args, **kwargs):
            # If layers not set then degrade gracefully
            if hasattr(settings, 'FOUNDRY'):
                layers = settings.FOUNDRY['layers']
            else:
                layers = [self.default]
            for layer in layers:
                method = getattr(
                    sys.modules[func.__module__],
                    '%s_%s' % (func.func_name, layer),                 
                    None
                )
                if method is not None:
                    return method(request, *args, **kwargs)

            return func(request, *args, **kwargs)
    
        return new
