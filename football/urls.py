from django.conf.urls.defaults import patterns, url, include

from foundry.urls import *

from football.models import League, Team

urlpatterns += patterns('',

    url(
        r'^league-logs/$',
        'football.views.league_logs',
        name='league-logs'
    ),
    
    url(
        r'^league-fixtures/$',
        'football.views.league_fixtures',
        name='league-fixtures'
    ),

     url(
        r'^league-results/$',
        'football.views.league_results',
        name='league-results'
    ),

    url(
        r'^top-leagues-menu-ajax/$',
        'django.views.generic.simple.direct_to_template',
        {
            'template':'football/top_leagues_menu_ajax.html', 
        },
        name='top-leagues-menu-ajax'
    ),

    url(
        r'^more-leagues-menu-ajax/$',
        'django.views.generic.simple.direct_to_template',
        {
            'template':'football/more_leagues_menu_ajax.html', 
        },
        name='more-leagues-menu-ajax'
    ),

    url(
        r'^top-teams-menu-ajax/$',
        'django.views.generic.simple.direct_to_template',
        {
            'template':'football/top_teams_menu_ajax.html', 
        },
        name='top-teams-menu-ajax'
    ),

    url(
        r'^league-logs-widget/(?P<league_slug>[\w-]+)/$', 
        'football.views.league_logs_widget', 
        {}, 
        name='league-logs-widget'
    ),

    url(
        r'^league-fixtures-widget/(?P<league_slug>[\w-]+)/$', 
        'football.views.league_fixtures_widget', 
        {}, 
        name='league-fixtures-widget'
    ),

    url(
        r'^league-results-widget/(?P<league_slug>[\w-]+)/$', 
        'football.views.league_results_widget', 
        {}, 
        name='league-results-widget'
    ),

    url(
        r'^league-posts/(?P<slug>[\w-]+)/$', 
        'jmbo.generic.views.generic_object_detail',
        {'queryset':League.permitted.all(), 'template_name':'football/league_posts.html'},
        name='league-posts'
    ),

    url(
        r'^league-galleries/(?P<slug>[\w-]+)/$', 
        'jmbo.generic.views.generic_object_detail',
        {'queryset':League.permitted.all(), 'template_name':'football/league_galleries.html'},
        name='league-galleries'
    ),

    url(
        r'^team-fixtures-widget/(?P<team_slug>[\w-]+)/$', 
        'football.views.team_fixtures_widget', 
        {}, 
        name='team-fixtures-widget'
    ),

    url(
        r'^team-results-widget/(?P<team_slug>[\w-]+)/$', 
        'football.views.team_results_widget', 
        {}, 
        name='team-results-widget'
    ),
    
    url(
        r'^team-players-widget/(?P<team_slug>[\w-]+)/$', 
        'football.views.team_players_widget', 
        {}, 
        name='team-players-widget'
    ),

    url(
        r'^team-players/(?P<slug>[\w-]+)/$', 
        'jmbo.generic.views.generic_object_detail',
        {'queryset':Team.permitted.all(), 'template_name':'football/team_players.html'},
        name='team-players'
    ),

    url(
        r'^live-scores/$', 
        'football.views.live_scores', 
        {}, 
        name='live-scores'
    ),

    url(
        r'^football-live-commentary/$', 
        'football.views.live_commentary', 
        {}, 
        name='live-commentary'
    )

)   
