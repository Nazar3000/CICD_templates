# Generated by Django 3.2.16 on 2023-07-04 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0004_alter_subscription_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='field_a',
            field=models.CharField(db_index=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='subscription',
            name='field_b',
            field=models.CharField(db_index=True, default='', max_length=100),
        ),
    ]
