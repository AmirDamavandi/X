# Generated by Django 5.1 on 2024-11-08 08:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0002_rename_postview_view_alter_bookmark_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='view',
            options={'verbose_name': 'View', 'verbose_name_plural': 'Views'},
        ),
    ]
