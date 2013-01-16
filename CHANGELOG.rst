Changelog
=========

0.3.3
-----
#. Update football_fetch command to allow a league and its league groups to have the same football365 service id without causing duplicates.

0.3.2
-----
#. Add an abbreviated title field to Team model.

0.3.1
-----
#. `ModelAdmin.inline_instances` has been removed in Django 1.4. Replace with `get_inline_instances(request)`.

0.3
---
#. Remove automatic `jmbo-foundry` url pattern includes.

0.2.6
-----
#. Filter for future fixtures.
#. Order log entries by league group so that the 'regroup' tag works correctly.

0.2.3
-----
#. Team dashboard for basic layer.

0.2.2
-----
#. Pass required parameter to layered decorator.
#. Minimum jmbo-foundry is now 0.5.1.

0.2.1
-----
#. Mark urls_web.py and urls_basic.py as deprecated. For the moment they exist for backwards compatibility.
#. Use fixtures to define photo sizes.

0.2
---
#. Better batching of fixtures and results.

0.1
---
#. French translations

0.0.3
-----
#. Migrate management commands and templates from jmbo-airtel.

0.0.1
-----
#. Initial release.

