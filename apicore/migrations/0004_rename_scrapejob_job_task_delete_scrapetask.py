# Generated by Django 5.0.6 on 2024-06-11 18:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apicore', '0003_scrapejob_status'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ScrapeJob',
            new_name='Job',
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coin', models.CharField(max_length=50)),
                ('output', models.JSONField(blank=True, null=True)),
                ('status', models.CharField(default='pending', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='apicore.job')),
            ],
        ),
        migrations.DeleteModel(
            name='ScrapeTask',
        ),
    ]