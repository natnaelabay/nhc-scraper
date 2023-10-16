# Generated by Django 3.2.13 on 2023-10-14 23:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_parsed', models.BooleanField(default=False)),
                ('status', models.IntegerField(choices=[(0, 'Not Scraped'), (1, 'Scraped - Failed'), (2, 'Scraped - Successful')], default=0)),
                ('published_date', models.DateField()),
                ('url', models.URLField()),
                ('title', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page', models.IntegerField()),
                ('url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='ArticleContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500)),
                ('published_date', models.DateField()),
                ('content', models.TextField()),
                ('article', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.article')),
            ],
        ),
    ]
