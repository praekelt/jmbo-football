# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'LeagueGroup'
        db.create_table('football_leaguegroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('subtitle', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('position', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, db_index=True)),
            ('football365_di', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True, null=True, blank=True)),
            ('football365_ci', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True, null=True, blank=True)),
        ))
        db.send_create_signal('football', ['LeagueGroup'])

        # Adding model 'League'
        db.create_table('football_league', (
            ('modelbase_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['jmbo.ModelBase'], unique=True, primary_key=True)),
            ('region', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('position', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, db_index=True)),
            ('football365_di', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True, null=True, blank=True)),
            ('football365_ci', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True, null=True, blank=True)),
        ))
        db.send_create_signal('football', ['League'])

        # Adding M2M table for field groups on 'League'
        db.create_table('football_league_groups', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('league', models.ForeignKey(orm['football.league'], null=False)),
            ('leaguegroup', models.ForeignKey(orm['football.leaguegroup'], null=False))
        ))
        db.create_unique('football_league_groups', ['league_id', 'leaguegroup_id'])

        # Adding model 'Team'
        db.create_table('football_team', (
            ('modelbase_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['jmbo.ModelBase'], unique=True, primary_key=True)),
            ('info', self.gf('ckeditor.fields.RichTextField')(null=True, blank=True)),
            ('history', self.gf('ckeditor.fields.RichTextField')(null=True, blank=True)),
            ('statistics', self.gf('ckeditor.fields.RichTextField')(null=True, blank=True)),
            ('football365_teamcode', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=64, null=True, blank=True)),
        ))
        db.send_create_signal('football', ['Team'])

        # Adding M2M table for field leagues on 'Team'
        db.create_table('football_team_leagues', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('team', models.ForeignKey(orm['football.team'], null=False)),
            ('league', models.ForeignKey(orm['football.league'], null=False))
        ))
        db.create_unique('football_team_leagues', ['team_id', 'league_id'])

        # Adding model 'Fixture'
        db.create_table('football_fixture', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('league', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['football.League'])),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['football.LeagueGroup'], null=True, blank=True)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('home_team', self.gf('django.db.models.fields.related.ForeignKey')(related_name='home_team', to=orm['football.Team'])),
            ('away_team', self.gf('django.db.models.fields.related.ForeignKey')(related_name='away_team', to=orm['football.Team'])),
            ('home_score', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('away_score', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('completed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('football', ['Fixture'])

        # Adding model 'LogEntry'
        db.create_table('football_logentry', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('league', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['football.League'])),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['football.LeagueGroup'], null=True, blank=True)),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['football.Team'])),
            ('played', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('won', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('drawn', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('lost', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('goals', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('points', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('goal_difference', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('football', ['LogEntry'])

        # Adding unique constraint on 'LogEntry', fields ['league', 'team']
        db.create_unique('football_logentry', ['league_id', 'team_id'])

        # Adding model 'Trivia'
        db.create_table('football_trivia', (
            ('modelbase_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['jmbo.ModelBase'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('football', ['Trivia'])

        # Adding model 'Player'
        db.create_table('football_player', (
            ('modelbase_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['jmbo.ModelBase'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('football', ['Player'])

        # Adding M2M table for field teams on 'Player'
        db.create_table('football_player_teams', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('player', models.ForeignKey(orm['football.player'], null=False)),
            ('team', models.ForeignKey(orm['football.team'], null=False))
        ))
        db.create_unique('football_player_teams', ['player_id', 'team_id'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'LogEntry', fields ['league', 'team']
        db.delete_unique('football_logentry', ['league_id', 'team_id'])

        # Deleting model 'LeagueGroup'
        db.delete_table('football_leaguegroup')

        # Deleting model 'League'
        db.delete_table('football_league')

        # Removing M2M table for field groups on 'League'
        db.delete_table('football_league_groups')

        # Deleting model 'Team'
        db.delete_table('football_team')

        # Removing M2M table for field leagues on 'Team'
        db.delete_table('football_team_leagues')

        # Deleting model 'Fixture'
        db.delete_table('football_fixture')

        # Deleting model 'LogEntry'
        db.delete_table('football_logentry')

        # Deleting model 'Trivia'
        db.delete_table('football_trivia')

        # Deleting model 'Player'
        db.delete_table('football_player')

        # Removing M2M table for field teams on 'Player'
        db.delete_table('football_player_teams')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'category.category': {
            'Meta': {'ordering': "('title',)", 'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['category.Category']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'category.tag': {
            'Meta': {'ordering': "('title',)", 'object_name': 'Tag'},
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['category.Category']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'football.fixture': {
            'Meta': {'object_name': 'Fixture'},
            'away_score': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'away_team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'away_team'", 'to': "orm['football.Team']"}),
            'completed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['football.LeagueGroup']", 'null': 'True', 'blank': 'True'}),
            'home_score': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'home_team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'home_team'", 'to': "orm['football.Team']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'league': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['football.League']"})
        },
        'football.league': {
            'Meta': {'ordering': "('-created',)", 'object_name': 'League', '_ormbases': ['jmbo.ModelBase']},
            'football365_ci': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'football365_di': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['football.LeagueGroup']", 'null': 'True', 'blank': 'True'}),
            'modelbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['jmbo.ModelBase']", 'unique': 'True', 'primary_key': 'True'}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'db_index': 'True'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        'football.leaguegroup': {
            'Meta': {'object_name': 'LeagueGroup'},
            'football365_ci': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'football365_di': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'db_index': 'True'}),
            'subtitle': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'football.logentry': {
            'Meta': {'unique_together': "(('league', 'team'),)", 'object_name': 'LogEntry'},
            'drawn': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'goal_difference': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'goals': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['football.LeagueGroup']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'league': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['football.League']"}),
            'lost': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'played': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'points': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['football.Team']"}),
            'won': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        'football.player': {
            'Meta': {'ordering': "('-created',)", 'object_name': 'Player', '_ormbases': ['jmbo.ModelBase']},
            'modelbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['jmbo.ModelBase']", 'unique': 'True', 'primary_key': 'True'}),
            'teams': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['football.Team']", 'symmetrical': 'False'})
        },
        'football.team': {
            'Meta': {'ordering': "('title',)", 'object_name': 'Team', '_ormbases': ['jmbo.ModelBase']},
            'football365_teamcode': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'history': ('ckeditor.fields.RichTextField', [], {'null': 'True', 'blank': 'True'}),
            'info': ('ckeditor.fields.RichTextField', [], {'null': 'True', 'blank': 'True'}),
            'leagues': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['football.League']", 'symmetrical': 'False'}),
            'modelbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['jmbo.ModelBase']", 'unique': 'True', 'primary_key': 'True'}),
            'statistics': ('ckeditor.fields.RichTextField', [], {'null': 'True', 'blank': 'True'})
        },
        'football.trivia': {
            'Meta': {'ordering': "('-created',)", 'object_name': 'Trivia', '_ormbases': ['jmbo.ModelBase']},
            'modelbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['jmbo.ModelBase']", 'unique': 'True', 'primary_key': 'True'})
        },
        'jmbo.modelbase': {
            'Meta': {'ordering': "('-created',)", 'object_name': 'ModelBase'},
            'anonymous_comments': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'anonymous_likes': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['category.Category']", 'null': 'True', 'blank': 'True'}),
            'class_name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True'}),
            'comments_closed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'comments_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'crop_from': ('django.db.models.fields.CharField', [], {'default': "'center'", 'max_length': '10', 'blank': 'True'}),
            'date_taken': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'effect': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'modelbase_related'", 'null': 'True', 'to': "orm['photologue.PhotoEffect']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'likes_closed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'likes_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'primary_category': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'primary_modelbase_set'", 'null': 'True', 'to': "orm['category.Category']"}),
            'publish_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'publishers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['publisher.Publisher']", 'null': 'True', 'blank': 'True'}),
            'retract_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['sites.Site']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'unpublished'", 'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'subtitle': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['category.Tag']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'view_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        'photologue.photoeffect': {
            'Meta': {'object_name': 'PhotoEffect'},
            'background_color': ('django.db.models.fields.CharField', [], {'default': "'#FFFFFF'", 'max_length': '7'}),
            'brightness': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'color': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'contrast': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'filters': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'reflection_size': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'reflection_strength': ('django.db.models.fields.FloatField', [], {'default': '0.59999999999999998'}),
            'sharpness': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'transpose_method': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'})
        },
        'publisher.publisher': {
            'Meta': {'object_name': 'Publisher'},
            'class_name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'secretballot.vote': {
            'Meta': {'unique_together': "(('token', 'content_type', 'object_id'),)", 'object_name': 'Vote'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'vote': ('django.db.models.fields.SmallIntegerField', [], {})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['football']
