from django.db import models
from django.utils.translation import ugettext_lazy as _

from ckeditor.fields import RichTextField
from jmbo.models import ModelBase
from jmbo.utils import generate_slug


class LeagueGroup(models.Model):
    title = models.CharField(max_length=64)
    subtitle = models.CharField(
        max_length=255, 
        null=True, 
        blank=True, 
        help_text='Some titles may be the same. A subtitle makes a distinction. It is not displayed on the site.',
    )
    position = models.PositiveIntegerField(default=0, db_index=True)
    football365_di = models.PositiveIntegerField(
        null=True, blank=True, db_index=True
    )
    football365_ci = models.PositiveIntegerField(
        null=True, blank=True, db_index=True
    )

    def __unicode__(self):
        if self.subtitle:
            return '%s (%s)' % (self.title, self.subtitle)
        else:
            return self.title


class League(ModelBase):
    region = models.CharField(
        max_length=32,
        choices=(
            ('local', 'Local'),
            ('regional', 'Regional'),
            ('international', 'International'),
        ),
    )
    position = models.PositiveIntegerField(default=0, db_index=True)    
    football365_di = models.PositiveIntegerField(
        null=True, blank=True, db_index=True
    )
    football365_ci = models.PositiveIntegerField(
        null=True, blank=True, db_index=True
    )
    groups = models.ManyToManyField(LeagueGroup, null=True, blank=True)

    @property
    def logentries(self):
        return self.logentry_set.all().order_by('group__position', '-points', '-goal_difference')


class Team(ModelBase):
    leagues = models.ManyToManyField(League)
    info = RichTextField(null=True, blank=True)
    history = RichTextField(null=True, blank=True)
    statistics = RichTextField(null=True, blank=True)
    football365_teamcode = models.CharField(
        max_length=64, null=True, blank=True, db_index=True
    )

    class Meta:
        ordering = ('title',)

    @property
    def players(self):
        return Player.permitted.filter(teams=self).order_by('title')


class Fixture(models.Model):
    league = models.ForeignKey(League)
    group = models.ForeignKey(LeagueGroup, null=True, blank=True)
    datetime = models.DateTimeField()
    home_team = models.ForeignKey(Team, related_name='home_team')
    away_team = models.ForeignKey(Team, related_name='away_team')
    home_score = models.PositiveIntegerField(null=True, blank=True)
    away_score = models.PositiveIntegerField(null=True, blank=True)
    completed = models.BooleanField(default=False)

    def __unicode__(self):
        return '%s vs. %s %s' % \
            (
                self.home_team.title, 
                self.away_team.title, 
                self.datetime.strftime('%d %B %Y')
            )


class LogEntry(models.Model):
    league = models.ForeignKey(League)
    group = models.ForeignKey(LeagueGroup, null=True, blank=True)
    team = models.ForeignKey(Team)
    played = models.PositiveIntegerField(default=0)
    won = models.PositiveIntegerField(default=0)
    drawn = models.PositiveIntegerField(default=0)
    lost = models.PositiveIntegerField(default=0)
    goals = models.PositiveIntegerField(default=0)
    points = models.PositiveIntegerField(default=0)
    goal_difference = models.IntegerField(default=0)

    class Meta:
        unique_together = (('league', 'team'),)
        verbose_name_plural = 'Log Entries'

class Trivia(ModelBase):
    pass

class Player(ModelBase):
    teams = models.ManyToManyField(Team)
