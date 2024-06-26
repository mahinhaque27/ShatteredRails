# Generated by Django 5.0.1 on 2024-02-03 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email',
            field=models.EmailField(default='default@example.com', max_length=254),
        ),
        migrations.AddField(
            model_name='user',
            name='name',
            field=models.CharField(default='Default Name', max_length=255),
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
