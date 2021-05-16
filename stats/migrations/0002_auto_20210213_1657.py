# Generated by Django 3.1.5 on 2021-02-13 15:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='producer',
            name='cumulative_production',
            field=models.FloatField(default=0.0, help_text='Cumulative power produced in watthours'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='producer',
            name='last_data',
            field=models.DateTimeField(auto_now=True, help_text='Last time data was received'),
        ),
        migrations.AddField(
            model_name='producer',
            name='last_production',
            field=models.DateTimeField(blank=True, help_text='Last time power was produced', null=True),
        ),
        migrations.CreateModel(
            name='ProductionLogs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('severity', models.CharField(choices=[('INFO', 'Info'), ('WARN', 'Warn'), ('ERROR', 'Error'), ('FATAL', 'Fatal')], max_length=6)),
                ('content', models.TextField()),
                ('producer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stats.producer')),
            ],
        ),
        migrations.CreateModel(
            name='ProductionData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('voltage', models.FloatField(blank=True, null=True)),
                ('amperage', models.FloatField(blank=True, null=True)),
                ('frequency', models.FloatField(blank=True, null=True)),
                ('producer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stats.producer')),
            ],
        ),
    ]