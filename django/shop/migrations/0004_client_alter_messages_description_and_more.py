# Generated by Django 4.2.7 on 2023-11-29 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_messages_alter_category_options_alter_item_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('id', models.IntegerField(editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('group_subscription', models.BooleanField(choices=[(0, 'subscribed'), (1, 'not subscribed')], default=1, verbose_name='group_subscription')),
                ('channel_subscription', models.BooleanField(choices=[(0, 'subscribed'), (1, 'not subscribed')], default=1, verbose_name='channel_subscription')),
            ],
            options={
                'verbose_name': 'client',
                'verbose_name_plural': 'client',
                'db_table': 'content"."client',
            },
        ),
        migrations.AlterField(
            model_name='messages',
            name='description',
            field=models.TextField(verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='messages',
            name='status',
            field=models.BooleanField(choices=[(0, 'draft'), (1, 'published')], default=0, verbose_name='status'),
        ),
    ]
