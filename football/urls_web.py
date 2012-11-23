import warnings

from football.urls import *


warnings.warn(
    "urls_web.py to be deprecated since the layered decorator can resolve \
    layer specific functions",
    DeprecationWarning
)

urlpatterns += patterns('',
    
)
