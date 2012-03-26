import json
import datetime

from django.core.cache import cache

from football365.management.commands.football365_fetch import Command as BaseCommand


class Command(BaseCommand):
    
    pipeline = {
        'live': ('live_raw', 'xml2dom', 'live_structure', 'live_commit'),
    }
    
    def live_commit(self, call, data):
        """
        Produces something like this:
            [{"AWAYTEAMSCORE": 0, 
              "HOMETEAMSCORE": 0, 
              "HOMETEAMCODE": null, 
              "MATCHSTATUS": "22:00 CAT", 
              "AWAYTEAMCODE": null, 
              "AWAYTEAM": "Sunderland", 
              "LIVE": false, 
              "AWAYTEAMCARDS": [], 
              "HOMETEAMGOALS": [], 
              "DATE": "20/03/12 20:00", 
              "HOMETEAMCARDS": [], 
              "AWAYTEAMGOALS": [], 
              "HOMETEAM": "Blackburn Rovers"
              },
              {"AWAYTEAMSCORE": 0, 
              "HOMETEAMSCORE": 0, 
              "HOMETEAMCODE": null, 
              "MATCHSTATUS": "22:00 CAT", 
              "AWAYTEAMCODE": null, 
              "AWAYTEAM": "Sunderland", 
              "LIVE": false, 
              "AWAYTEAMCARDS": [], 
              "HOMETEAMGOALS": [], 
              "DATE": "20/03/12 20:00", 
              "HOMETEAMCARDS": [], 
              "AWAYTEAMGOALS": [], 
              "HOMETEAM": "Blackburn Rovers"
              }]
        """
        
        # Fix the date/time to string, so we can serialize it in cache.
        for game in data:
            game['DATE'] = game['DATE'].strftime("%d/%m/%y %H:%M")
        
        if data:
            # Stick it in the cache for later retrieval.
            cache.set('FOOTBALL_LIVE_SCORES', json.dumps(data))
            
            print 'Got data:'
            print cache.get('FOOTBALL_LIVE_SCORES')
        else:
            print 'No live scores.'
            if cache.get('FOOTBALL_LIVE_SCORES'):
                cache.delete('FOOTBALL_LIVE_SCORES')
            
        
