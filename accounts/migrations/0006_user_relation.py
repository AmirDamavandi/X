# Generated by Django 5.1 on 2024-11-08 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_user_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='relation',
            field=models.ManyToManyField(related_name='user_following', to='accounts.relation'),
        ),
    ]
