# Generated by Django 2.2.6 on 2024-01-22 20:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jedzonko', '0004_auto_20240122_2135'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipeplan',
            old_name='order',
            new_name='meal_order',
        ),
    ]