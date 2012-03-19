from football.urls import *

urlpatterns += patterns('',

    url(
        r'^league-dashboard/(?P<slug>[\w-]+)/$', 
        'football.views.league_dashboard_web', 
        {}, 
        name='league_object_detail'
    ),

    url(
        r'^team-dashboard/(?P<slug>[\w-]+)/$', 
        'football.views.team_dashboard_web', 
        {}, 
        name='team_object_detail'
    ),

)
