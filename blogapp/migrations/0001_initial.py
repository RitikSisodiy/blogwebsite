# Generated by Django 3.1.5 on 2021-01-13 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blog_title', models.CharField(max_length=50)),
                ('blog_content', models.CharField(max_length=5000)),
                ('blog_likes', models.IntegerField(default=0)),
                ('blog_share', models.IntegerField(default=0)),
                ('blog_views', models.IntegerField(default=0)),
                ('blog_owner', models.CharField(max_length=50)),
            ],
        ),
    ]
