# Generated by Django 3.0.4 on 2020-03-23 23:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('description', models.TextField()),
                ('type', models.IntegerField(choices=[(2, 'Organizacja pozarządowa'), (3, 'Zbiórka lokalna'), (1, 'Fundacja')], default=1)),
                ('categories', models.ManyToManyField(to='charityapp.Category')),
            ],
        ),
    ]
