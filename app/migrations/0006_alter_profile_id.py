# Generated by Django 4.2 on 2023-04-23 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
