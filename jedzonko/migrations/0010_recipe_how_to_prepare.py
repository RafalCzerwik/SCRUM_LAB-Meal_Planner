# Generated by Django 2.2.6 on 2024-01-27 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jedzonko', '0009_page'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='how_to_prepare',
            field=models.TextField(default="I don't know how to prepare it"),
        ),
    ]
