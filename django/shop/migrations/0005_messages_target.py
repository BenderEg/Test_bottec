# Generated by Django 4.2.7 on 2023-11-30 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_client_alter_messages_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='messages',
            name='target',
            field=models.CharField(choices=[('group', 'group'), ('channel', 'channel')], default='group', max_length=10, verbose_name='target'),
        ),
    ]
