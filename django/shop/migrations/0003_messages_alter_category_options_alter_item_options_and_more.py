# Generated by Django 4.2.7 on 2023-11-29 18:16

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_remove_item_file_path_item_image_path'),
    ]

    operations = [
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('header', models.CharField(max_length=255, verbose_name='header')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('status', models.BooleanField(default=False, verbose_name='status')),
            ],
            options={
                'verbose_name': 'messages',
                'verbose_name_plural': 'messages',
                'db_table': 'content"."messages',
            },
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'сategory', 'verbose_name_plural': 'сategory'},
        ),
        migrations.AlterModelOptions(
            name='item',
            options={'verbose_name': 'item', 'verbose_name_plural': 'item'},
        ),
        migrations.AlterModelOptions(
            name='subcategory',
            options={'verbose_name': 'subcategory', 'verbose_name_plural': 'subcategory'},
        ),
    ]
