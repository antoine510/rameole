# Generated by Django 3.1.5 on 2021-05-16 13:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0002_auto_20210213_1657'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductionHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('watt_hours', models.FloatField(help_text='Cumulative watt-hours for this period')),
                ('producer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stats.producer')),
            ],
        ),
    ]
