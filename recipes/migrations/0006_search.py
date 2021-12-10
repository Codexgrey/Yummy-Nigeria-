from django.db import migrations
from django.contrib.postgres.operations import TrigramExtension

class Migration(migrations.Migration):
    dependencies = [
        ('recipes', '0005_post_tag'),
    ]

    operations = [
        TrigramExtension(),
    ]