# Generated by Django 4.1.5 on 2023-02-03 00:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('newsaggregator', '0002_rename_descrption_post_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='guid',
        ),
    ]
