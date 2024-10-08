# Generated by Django 5.1 on 2024-09-27 20:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_relation_from_user_alter_relation_to_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConnectPeople',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link_reason', models.CharField(blank=True, max_length=100, null=True)),
                ('linked_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='people', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='self', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'connect people',
                'verbose_name_plural': 'connect people',
                'unique_together': {('user', 'linked_user')},
            },
        ),
    ]
