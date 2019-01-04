from django.contrib import admin

from .models import Accident
# Register your models here.
from .models import Car
from .models import Driver
from .models import Proposer
from .models import Record


# TODO: Implement the admin web page


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    pass


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    pass


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    pass


@admin.register(Proposer)
class ProposerAdmin(admin.ModelAdmin):
    pass


@admin.register(Accident)
class AccidentAdmin(admin.ModelAdmin):
    pass
