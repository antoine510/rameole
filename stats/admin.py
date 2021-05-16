from django.contrib import admin

from .models import Plant, PowerTransfer, Producer, Consumer
# Register your models here.

admin.site.register(Plant)
admin.site.register(PowerTransfer)
admin.site.register(Producer)
admin.site.register(Consumer)
