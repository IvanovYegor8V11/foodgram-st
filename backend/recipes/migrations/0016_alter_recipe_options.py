# Generated by Django 3.2.16 on 2025-01-10 09:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0015_auto_20250109_2033'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ('-created_at',), 'verbose_name': 'Рецепт', 'verbose_name_plural': 'Рецепты'},
        ),
    ]
