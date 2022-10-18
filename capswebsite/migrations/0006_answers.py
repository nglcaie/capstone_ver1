# Generated by Django 4.1.2 on 2022-10-10 13:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('capswebsite', '0005_alter_user_firstname_alter_user_lastname'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question1', models.CharField(blank=True, max_length=1000, null=True, verbose_name='question1')),
                ('question2', models.CharField(blank=True, max_length=1000, null=True, verbose_name='question2')),
                ('question3', models.CharField(blank=True, max_length=1000, null=True, verbose_name='question3')),
                ('question4', models.CharField(blank=True, max_length=1000, null=True, verbose_name='question4')),
                ('question5', models.CharField(blank=True, max_length=1000, null=True, verbose_name='question5')),
                ('student', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Student')),
            ],
        ),
    ]