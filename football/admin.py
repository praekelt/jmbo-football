from django.contrib import admin
from django import forms

from jmbo.admin import ModelBaseAdmin

from football.models import League, Team, Fixture, LogEntry, Trivia, Player, \
    LeagueGroup


class TeamInline(admin.StackedInline):
    model = Team


class FixtureInline(admin.StackedInline):
    model = Fixture
    
  
class LogEntryInline(admin.StackedInline):
    model = LogEntry


class LeagueAdmin(ModelBaseAdmin):   
    # The inlines may lead to slow UI when there are many teams. Use django 
    # simple autocomplete for teams to speed up the UI.
    # todo: limit team vocabulary by filtering on league
    inlines = [FixtureInline, LogEntryInline]

    def get_formsets(self, request, obj=None):
        # No fieldsets for a new object
        for inline in (obj is not None and self.inline_instances or []):
            yield inline.get_formset(request, obj)

    def response_add(self, request, obj, post_url_continue='../%s/'):
        if '_addanother' not in request.POST and '_popup' not in request.POST:
            request.POST['_continue'] = 1 
        return super(LeagueAdmin, self).response_add(request, obj, post_url_continue)


class LeagueGroupAdmin(admin.ModelAdmin):   
    list_display = ('title', 'subtitle', 'football365_ci', 'football365_di', 'position')
    list_editable = ('football365_ci', 'football365_di', 'position',)


class TeamAdmin(ModelBaseAdmin):
    pass


class TriviaAdmin(ModelBaseAdmin):
    pass


class PlayerAdmin(ModelBaseAdmin):
    pass


admin.site.register(League, LeagueAdmin)
admin.site.register(LeagueGroup, LeagueGroupAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Trivia, TriviaAdmin)
admin.site.register(Player, PlayerAdmin)
