# Generated by Django 2.0.5 on 2018-05-21 13:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_tag_tagging'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tagging',
            old_name='article_id',
            new_name='article',
        ),
        migrations.RenameField(
            model_name='tagging',
            old_name='tag_id',
            new_name='tag',
        ),
    ]