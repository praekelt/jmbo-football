import datetime
import urllib2
from lxml import etree

from django.db.models import Q
from django.conf import settings

from football365.management.commands.football365_fetch import Command as BaseCommand
from football.models import LeagueGroup, League, Team, LogEntry, Fixture


class Command(BaseCommand):

    pipeline = {
        'table': ('table_raw', 'xml2dom', 'table_structure', 'table_commit'),
        'fixtures': ('fixtures_raw', 'xml2dom', 'fixtures_structure', 'fixtures_commit'),
        'results': ('results_raw', 'xml2dom', 'results_structure', 'results_commit'),
    }

    def table_commit(self, call, data):        
        leagues = League.objects.filter(football365_di=call.football365_service_id)
        for league in leagues:
            for obj in league.logentry_set.all():
                obj.delete()
            for row in data:
                try:
                    team = Team.objects.get(Q(football365_teamcode=row['TEAMCODE']) | Q(title=row['TEAM']), leagues=league)
                except (Team.DoesNotExist, Team.MultipleObjectsReturned):
                    continue
                LogEntry.objects.create(
                    league=league,
                    team=team,
                    played=row['PLAYED'],
                    won=row['WON'],
                    drawn=row['DRAWN'],
                    lost=row['LOST'],
                    goals=row['GOALSFOR'],
                    points=row['POINTS'],
                    goal_difference=row['GOALDIFFERENCE']
                )

        leagues = League.objects.all()
        for league in leagues:
            groups = LeagueGroup.objects.filter(league=league, football365_di=call.football365_service_id)
            for group in groups:
                for obj in league.logentry_set.filter(group=group):
                    obj.delete()
                for row in data:
                    try:
                        team = Team.objects.get(Q(football365_teamcode=row['TEAMCODE']) | Q(title=row['TEAM']), leagues=league)
                    except (Team.DoesNotExist, Team.MultipleObjectsReturned):
                        continue
                    LogEntry.objects.create(
                        league=league,
                        group=group,
                        team=team,
                        played=row['PLAYED'],
                        won=row['WON'],
                        drawn=row['DRAWN'],
                        lost=row['LOST'],
                        goals=row['GOALSFOR'],
                        points=row['POINTS'],
                        goal_difference=row['GOALDIFFERENCE']
                    )

    def fixtures_commit(self, call, data):        
        leagues = League.objects.filter(football365_di=call.football365_service_id)
        for league in leagues:
            for row in data:
                try:
                    home_team = Team.objects.get(Q(football365_teamcode=row['HOMETEAMCODE']) | Q(title=row['HOMETEAM']), leagues=league)
                    away_team = Team.objects.get(Q(football365_teamcode=row['AWAYTEAMCODE']) | Q(title=row['AWAYTEAM']), leagues=league)
                except (Team.DoesNotExist, Team.MultipleObjectsReturned):
                    continue

                # Does the fixture already exist?
                q = league.fixture_set.filter(
                    home_team=home_team, 
                    away_team=away_team,
                    datetime=row['STARTTIME']
                )
                if q.exists():
                    # Already stored
                    continue

                # New fixture
                Fixture.objects.create(
                    league=league,
                    home_team=home_team,
                    away_team=away_team,
                    datetime=row['STARTTIME']
                )

        leagues = League.objects.all()
        for league in leagues:
            groups = LeagueGroup.objects.filter(league=league, football365_di=call.football365_service_id)
            for group in groups:
                for row in data:
                    try:
                        home_team = Team.objects.get(Q(football365_teamcode=row['HOMETEAMCODE']) | Q(title=row['HOMETEAM']), leagues=league)
                        away_team = Team.objects.get(Q(football365_teamcode=row['AWAYTEAMCODE']) | Q(title=row['AWAYTEAM']), leagues=league)
                    except (Team.DoesNotExist, Team.MultipleObjectsReturned):
                        continue

                    # Does the fixture already exist?
                    q = league.fixture_set.filter(
                        group=group,
                        home_team=home_team, 
                        away_team=away_team,
                        datetime=row['STARTTIME']
                    )
                    if q.exists():
                        # Already stored
                        continue

                    # New fixture
                    Fixture.objects.create(
                        league=league,
                        group=group,
                        home_team=home_team,
                        away_team=away_team,
                        datetime=row['STARTTIME']
                    )


    def results_commit(self, call, data):        
        leagues = League.objects.filter(football365_di=call.football365_service_id)        
        for league in leagues:
            for row in data:
                try:
                    home_team = Team.objects.get(Q(football365_teamcode=row['HOMETEAMCODE']) | Q(title=row['HOMETEAM']), leagues=league)
                    away_team = Team.objects.get(Q(football365_teamcode=row['AWAYTEAMCODE']) | Q(title=row['AWAYTEAM']), leagues=league)
                except (Team.DoesNotExist, Team.MultipleObjectsReturned):
                    continue

                # Does the fixture already exist?
                q = league.fixture_set.filter(
                    home_team=home_team, 
                    away_team=away_team,
                    datetime__gte=row['DATE'],
                    datetime__lt=row['DATE'] + datetime.timedelta(days=1)
                )
                if q.exists():
                    # Update
                    fixture = q[0]
                    fixture.home_score = row['HOMETEAMSCORE']
                    fixture.away_score = row['AWAYTEAMSCORE']
                    fixture.completed = True
                    fixture.save()               
                else:
                    # New fixture - should not happen if fixtures are fetched daily
                    Fixture.objects.create(
                        league=league,
                        home_team=home_team,
                        away_team=away_team,
                        datetime=row['DATE'],
                        home_score=row['HOMETEAMSCORE'],
                        away_score=row['AWAYTEAMSCORE'],
                        completed=True
                    )

        leagues = League.objects.all()
        for league in leagues:
            groups = LeagueGroup.objects.filter(league=league, football365_di=call.football365_service_id)
            for group in groups:
                for row in data:
                    try:
                        home_team = Team.objects.get(Q(football365_teamcode=row['HOMETEAMCODE']) | Q(title=row['HOMETEAM']), leagues=league)
                        away_team = Team.objects.get(Q(football365_teamcode=row['AWAYTEAMCODE']) | Q(title=row['AWAYTEAM']), leagues=league)
                    except (Team.DoesNotExist, Team.MultipleObjectsReturned):
                        continue

                    # Does the fixture already exist?
                    q = league.fixture_set.filter(
                        group=group,
                        home_team=home_team, 
                        away_team=away_team,
                        datetime__gte=row['DATE'],
                        datetime__lt=row['DATE'] + datetime.timedelta(days=1)
                    )
                    if q.exists():
                        # Update
                        fixture = q[0]
                        fixture.home_score = row['HOMETEAMSCORE']
                        fixture.away_score = row['AWAYTEAMSCORE']
                        fixture.completed = True
                        fixture.save()               
                    else:
                        # New fixture - should not happen if fixtures are fetched daily
                        Fixture.objects.create(
                            league=league,
                            group=group,
                            home_team=home_team,
                            away_team=away_team,
                            datetime=row['DATE'],
                            home_score=row['HOMETEAMSCORE'],
                            away_score=row['AWAYTEAMSCORE'],
                            completed=True
                        )
