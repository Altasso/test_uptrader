# Generated by Django 5.2.3 on 2025-06-19 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0002_menuitem_slug_alter_menuitem_menu_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='named_url',
            field=models.CharField(blank=True, help_text='Имя URL из urls.py, например home', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='url',
            field=models.CharField(blank=True, help_text='Явный URL, например /about/', max_length=200, null=True),
        ),
    ]
