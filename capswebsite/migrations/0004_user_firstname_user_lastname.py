# Generated by Django 4.1.2 on 2022-10-10 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('capswebsite', '0003_college_user_block_user_year_alter_user_numberid_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='firstName',
            field=models.CharField(blank=True, choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6')], max_length=10, null=True, verbose_name='First Name'),
        ),
        migrations.AddField(
            model_name='user',
            name='lastName',
            field=models.CharField(blank=True, choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6')], max_length=10, null=True, verbose_name='Last Name'),
        ),
    ]
