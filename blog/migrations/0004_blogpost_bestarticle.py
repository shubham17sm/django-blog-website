# Generated by Django 2.1.5 on 2020-04-13 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_blogpost_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='bestarticle',
            field=models.BooleanField(default=False),
        ),
    ]
