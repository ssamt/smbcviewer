# Generated by Django 3.2.4 on 2021-07-01 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('comic', models.ImageField(upload_to='')),
                ('bonus', models.ImageField(upload_to='')),
                ('prev', models.CharField(max_length=50)),
                ('next', models.CharField(max_length=50)),
                ('title_text', models.TextField()),
            ],
        ),
    ]
