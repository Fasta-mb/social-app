# Generated by Django 4.1.4 on 2022-12-25 02:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_post_created_post_updated'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='picuser',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='profile', to='app.profileuser'),
        ),
    ]
