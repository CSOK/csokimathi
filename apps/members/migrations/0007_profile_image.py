# Generated by Django 2.0.2 on 2018-03-03 23:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0006_remove_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='profile_image'),
        ),
    ]
