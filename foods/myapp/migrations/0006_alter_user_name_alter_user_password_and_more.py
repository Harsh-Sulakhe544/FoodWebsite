# Generated by Django 4.2.1 on 2024-06-17 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_userauth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='userauth',
            name='password',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
