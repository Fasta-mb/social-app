# Generated by Django 4.1.3 on 2023-01-01 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_emailsend'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailsend',
            name='message',
            field=models.CharField(max_length=320),
        ),
    ]
