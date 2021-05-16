from django.db import models

class Plant(models.Model):
    name = models.CharField(max_length=63, unique=True)

    def __str__(self):
        return self.name

class ProductionData(models.Model):
    producer = models.ForeignKey('Producer', on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    voltage = models.FloatField(blank=True, null=True)
    amperage = models.FloatField(blank=True, null=True)
    frequency = models.FloatField(blank=True, null=True)

class ProductionHistory(models.Model):
    Timescale = models.TextChoices('Timescale', 'year month week day hour')

    producer = models.ForeignKey('Producer', on_delete=models.CASCADE)
    time_period = models.CharField(choices=Timescale.choices, max_length=6)
    time = models.DateTimeField()
    watt_hours = models.FloatField(help_text='Cumulative watt-hours for this period')


class ProductionLogs(models.Model):
    Severity = models.TextChoices('Severity', 'INFO WARN ERROR FATAL')

    producer = models.ForeignKey('Producer', on_delete=models.CASCADE)
    severity = models.CharField(choices=Severity.choices, max_length=6)
    content = models.TextField()

class PowerTransfer(models.Model):
    Connection = models.TextChoices('Connection', 'AC LVDC')

    producer = models.ForeignKey('Producer', on_delete=models.CASCADE)
    consumer = models.ForeignKey('Consumer', on_delete=models.CASCADE)
    connection = models.CharField(choices=Connection.choices, max_length=10)
    length = models.FloatField(help_text='Length of connection in meters')
    power = models.FloatField(help_text='Power handling capability in watts')
    typical_efficiency = models.FloatField(help_text='Typical efficiency in the range [0,1)')
    
    def __str__(self):
        return "Link from " + str(self.producer) + " to " + str(self.consumer)

class Producer(models.Model):
    PowerSource = models.TextChoices('PowerSource', 'SOLAR WIND')

    name = models.CharField(max_length=63, unique=True)
    plant = models.ForeignKey('Plant', on_delete=models.CASCADE)
    power_source = models.CharField(choices=PowerSource.choices, max_length=10)
    max_power = models.FloatField(help_text='Maximum power in watts')
    max_voltage = models.FloatField(help_text='Maximum voltage in volts')
    consumers = models.ManyToManyField('Consumer', through='PowerTransfer')
    cumulative_production = models.FloatField(help_text='Cumulative power produced in watthours')
    last_data = models.DateTimeField(auto_now=True, help_text='Last time data was received')
    last_production = models.DateTimeField(blank=True, null=True, help_text='Last time power was produced')

    def __str__(self):
        return self.name

class Consumer(models.Model):
    name = models.CharField(max_length=63, unique=True)
    plant = models.ForeignKey('Plant', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
