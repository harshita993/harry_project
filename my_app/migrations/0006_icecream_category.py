# Generated by Django 5.1.7 on 2025-04-17 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0005_order_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='icecream',
            name='category',
            field=models.CharField(choices=[('Icecream', 'Icecream'), ('Softy', 'Softy'), ('Milkshake', 'Milkshake')], default='icecream', max_length=50),
            preserve_default=False,
        ),
    ]
