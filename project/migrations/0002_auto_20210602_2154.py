# Generated by Django 3.2.3 on 2021-06-02 11:54

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20210602_2154'),
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='IssuePriority',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('icon', models.ImageField(blank=True, null=True, upload_to='project/%Y/%m/%d')),
            ],
        ),
        migrations.CreateModel(
            name='IssueResolution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='LoggedTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=datetime.datetime(2021, 6, 2, 21, 54, 23, 558542))),
                ('hours_count', models.TimeField()),
                ('description', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='users',
            field=models.ManyToManyField(to='account.Profile'),
        ),
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=100)),
                ('type', models.CharField(max_length=100)),
                ('summary', models.TextField()),
                ('description', models.TextField(blank=True, null=True)),
                ('environment', models.TextField(blank=True, null=True)),
                ('ETA', models.DateTimeField()),
                ('percent', models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('created', models.DateTimeField()),
                ('updated', models.DateTimeField()),
                ('resolution_dated', models.DateTimeField()),
                ('executor', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='executor', to='account.profile')),
                ('priority', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.issuepriority')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.project')),
                ('resolution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.issueresolution')),
                ('verifier', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='verifier', to='account.profile')),
                ('watchers', models.ManyToManyField(to='account.Profile')),
            ],
        ),
    ]
