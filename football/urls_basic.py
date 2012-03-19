from football.urls import *


urlpatterns += patterns('',

    url(
        r'^league-dashboard/(?P<slug>[\w-]+)/$', 
        'football.views.league_dashboard_basic', 
        {}, 
        name='league_object_detail'
    ),

)
