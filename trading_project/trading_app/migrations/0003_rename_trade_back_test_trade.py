# Generated by Django 5.0.7 on 2024-08-02 16:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trading_app', '0002_alter_trade_timestamp'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Trade',
            new_name='Back_Test_Trade',
        ),
    ]
