# Generated by Django 4.2 on 2024-02-14 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UL', '0003_alter_arbreisole_commentaire_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='toiletteisole',
            name='info_modifier_le',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
