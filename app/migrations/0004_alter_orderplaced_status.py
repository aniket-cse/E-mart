# Generated by Django 4.1.3 on 2023-04-22 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_product_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderplaced',
            name='status',
            field=models.CharField(choices=[('Accepted', 'Accepted'), ('Packed', 'Packed'), ('On The Way', 'On The Way'), ('Delivered', 'Delivered'), ('Cancel', 'Cancel')], default='Pending', max_length=50),
        ),
    ]
