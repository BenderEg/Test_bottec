# Generated by Django 4.2.7 on 2023-11-29 16:21

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('description', models.TextField(blank=True, verbose_name='description')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Category',
                'db_table': 'content"."category',
            },
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.category')),
            ],
            options={
                'verbose_name': 'Subcategory',
                'verbose_name_plural': 'Subcategory',
                'db_table': 'content"."subcategory',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('file_path', models.FileField(blank=True, null=True, upload_to='items_photo/', verbose_name='file')),
                ('subcategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.subcategory')),
            ],
            options={
                'verbose_name': 'Item',
                'verbose_name_plural': 'Item',
                'db_table': 'content"."item',
            },
        ),
        migrations.AddIndex(
            model_name='category',
            index=models.Index(fields=['name'], name='category_name_idx'),
        ),
        migrations.AddIndex(
            model_name='subcategory',
            index=models.Index(fields=['name', 'category'], name='subcategory_name_idx'),
        ),
        migrations.AddIndex(
            model_name='item',
            index=models.Index(fields=['name', 'subcategory'], name='item_name_idx'),
        ),
    ]
