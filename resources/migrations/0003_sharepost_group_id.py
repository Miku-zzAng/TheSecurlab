# Generated by Django 4.2.4 on 2023-08-26 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0002_sharepost_subinfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='sharepost',
            name='group_id',
            field=models.PositiveIntegerField(default=1, verbose_name='분류 여부'),
        ),
    ]