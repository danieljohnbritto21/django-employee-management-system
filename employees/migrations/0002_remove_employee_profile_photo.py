# This migration is intentionally empty.
# profile_photo was removed directly in 0001_initial.py (squashed).

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0001_initial'),
    ]

    operations = [
        # No operations needed - profile_photo was never created in the squashed 0001.
    ]
