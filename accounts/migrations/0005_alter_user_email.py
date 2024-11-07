# Generated by Django 5.1 on 2024-09-27 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_connectpeople'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(help_text='enter your email address', max_length=254, unique=True),
        ),
    ]