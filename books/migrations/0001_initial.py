# Generated by Django 4.2.4 on 2025-07-06 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isbn', models.CharField(max_length=17, unique=True)),
                ('title', models.CharField(max_length=400)),
                ('authors', models.CharField(max_length=400)),
                ('publisher', models.CharField(blank=True, max_length=200, null=True)),
                ('cover', models.URLField(blank=True, max_length=400, null=True)),
            ],
        ),
    ]
