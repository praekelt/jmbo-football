import datetime
from itertools import chain

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.db.models import Q
from django.core.cache import cache

from football.models import League, Team, Fixture


def _fixtures_batching(request, queryset, type='fixtures', window=1):
    """Common handling for batching of fixtures"""

    # This week's start
    this_week_start = datetime.date.today()
    this_week_start = this_week_start \
        - datetime.timedelta(days=this_week_start.weekday())

    # Adjust week start depending on type
    #if type == 'results':
    #    this_week_start = this_week_start - datetime.timedelta(days=window*7)

    # Get week's fixtures
    week_start = None
    raw_week_start = request.GET.get('week_start', None)
    if raw_week_start:        
        try:
            y, m, d = map(int, raw_week_start.split('-'))
            week_start = datetime.date(y, m, d)
        except:
            pass
    if not week_start:
        week_start = this_week_start
    week_end = week_start + datetime.timedelta(days=window*7)
    fixtures = queryset.filter(
        datetime__gte=week_start, datetime__lte=week_end,
        completed=(type == 'results') and True or False
    ).order_by('datetime')

    # List of weeks for span of fixtures
    weeks = []
    span = queryset.order_by('-datetime')[:1]
    if span.exists():
        n = this_week_start
        max_date = span[0].datetime.date()
        while n <= max_date:
            weeks.append(n)
            n = n + datetime.timedelta(days=window*7)

    # Previous, next week
    previous_week_start = None
    next_week_start = None
    if weeks:
        previous_week_start = week_start - datetime.timedelta(days=window*7)
        next_week_start = week_start + datetime.timedelta(days=window*7)

    return week_start, fixtures, weeks, previous_week_start, next_week_start


def league_logs(request, league_slug=None, template_name=None):
    league = None
    leagues = League.permitted.all().order_by('position', 'title')
    league_slug = league_slug or request.GET.get('league_slug', None)
    if league_slug:
        league = get_object_or_404(League, slug=league_slug)
    elif leagues.exists():
        league = leagues[0]
    extra = dict(
        league=league,
        leagues=leagues
    )
    return render_to_response(template_name or 'football/league_logs.html', extra, context_instance=RequestContext(request))


def league_fixtures(request, league_slug=None, template_name=None):
    league = None
    leagues = League.permitted.all().order_by('position', 'title')
    league_slug = league_slug or request.GET.get('league_slug', None)
    if league_slug:
        league = get_object_or_404(League, slug=league_slug)
    elif leagues.exists():
        league = leagues[0]
   
    qs = league.fixture_set.all()
    week_start, fixtures, weeks, previous_week_start, next_week_start = \
        _fixtures_batching(request, qs, window=1)

    extra = dict(
        league=league,
        leagues=leagues,
        week_start=week_start,
        weeks=weeks,
        fixtures=fixtures,        
        previous_week_start=previous_week_start,
        next_week_start=next_week_start
    )
    return render_to_response(template_name or 'football/league_fixtures.html', extra, context_instance=RequestContext(request))


def league_results(request, league_slug=None, template_name=None):
    league = None
    leagues = League.permitted.all().order_by('position', 'title')
    league_slug = league_slug or request.GET.get('league_slug', None)
    if league_slug:
        league = get_object_or_404(League, slug=league_slug)
    elif leagues.exists():
        league = leagues[0]

    qs = league.fixture_set.all()
    week_start, fixtures, weeks, previous_week_start, next_week_start = \
        _fixtures_batching(request, qs, type='results', window=1)

    extra = dict(
        league=league,
        leagues=leagues,
        week_start=week_start,
        weeks=weeks,
        fixtures=fixtures,        
        previous_week_start=previous_week_start,
        next_week_start=next_week_start
    )
    return render_to_response(template_name or 'football/league_results.html', extra, context_instance=RequestContext(request))


def league_logs_widget(request, league_slug):
    return league_logs(request, league_slug, 'football/league_logs_widget.html')


def league_fixtures_widget(request, league_slug):
    return league_fixtures(request, league_slug, 'football/league_fixtures_widget.html')


def league_results_widget(request, league_slug):
    return league_results(request, league_slug, 'football/league_results_widget.html')


def league_dashboard_basic(request, slug):
    league = get_object_or_404(League, slug=slug)
    related_items = league.get_related_items('post_leagues', 'reverse')
    extra = dict(
        object=league,
        related_object_list_top=related_items[:1],
        related_object_list=related_items[1:4],
    )
    return render_to_response('football/league_dashboard.html', extra, context_instance=RequestContext(request))


def league_dashboard_web(request, slug):
    league = get_object_or_404(League, slug=slug)

    # Related items consist of galleries and posts
    # xxx: the related item fetches assumes too much. Needs scrutiny.
    galleries = league.get_related_items('league_galleries')
    posts = league.get_related_items('post_leagues', 'reverse')
    if galleries.count():
        related_object_list = list(chain(galleries[:1], posts[:1]))
    else:
        related_object_list = posts[:2]

    extra = dict(
        object=league,
        related_object_list=related_object_list,
        logs=league_logs_widget(request, league.slug).content,
        fixtures=league_fixtures_widget(request, league.slug).content,
        results=league_results_widget(request, league.slug).content,
    )
    return render_to_response('football/league_dashboard.html', extra, context_instance=RequestContext(request))


def team_fixtures_widget(request, team_slug):
    team = get_object_or_404(Team, slug=team_slug)

    qs = Fixture.objects.filter(Q(home_team=team)|Q(away_team=team))
    week_start, fixtures, weeks, previous_week_start, next_week_start = \
        _fixtures_batching(request, qs, window=4)

    extra = dict(
        team=team,
        week_start=week_start,
        weeks=weeks,
        fixtures=fixtures,        
        previous_week_start=previous_week_start,
        next_week_start=next_week_start
    )
    return render_to_response('football/team_fixtures_widget.html', extra, context_instance=RequestContext(request))


def team_results_widget(request, team_slug):
    team = get_object_or_404(Team, slug=team_slug)

    qs = Fixture.objects.filter(Q(home_team=team)|Q(away_team=team))
    week_start, fixtures, weeks, previous_week_start, next_week_start = \
        _fixtures_batching(request, qs, type='results', window=4)

    extra = dict(
        team=team,
        week_start=week_start,
        weeks=weeks,
        fixtures=fixtures,        
        previous_week_start=previous_week_start,
        next_week_start=next_week_start
    )
    return render_to_response('football/team_results_widget.html', extra, context_instance=RequestContext(request))


def team_players_widget(request, team_slug):
    team = get_object_or_404(Team, slug=team_slug)
    extra = dict(
        team=team,
        players=team.player_set.all().order_by('title'),
    )
    return render_to_response('football/team_players_widget.html', extra, context_instance=RequestContext(request))


def team_dashboard_web(request, slug):
    team = get_object_or_404(Team, slug=slug)
    extra = dict(
        object=team,
        related_object_list=team.get_related_items('post_teams', 'reverse')[:4],
        fixtures=team_fixtures_widget(request, team.slug).content,
        results=team_results_widget(request, team.slug).content,
        players=team_players_widget(request, team.slug).content,
    )
    return render_to_response('football/team_dashboard.html', extra, context_instance=RequestContext(request))


def live_scores(request):
    extra = {}
    live_scores = cache.get('FOOTALL_LIVE_SCORES')
    if live_scores:
        scores_array = []
        for score in json.loads(live_scores):
            if not score['LIVE']:
                scores_array.append(score)                
        extra = {'live_scores': scores_array}

    return render_to_response('football/live_scores.html', extra, context_instance=RequestContext(request))

def live_commentary(request):
    import datetime
    f = open('/tmp/commentary-%s' % datetime.datetime.now().strftime('%Y%m%d%H%M'), 'w')
    try:
        f.write(str(request))
    finally:
        f.close()
    return HttpResponse('thank you')

