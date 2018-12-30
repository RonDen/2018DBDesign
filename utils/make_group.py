from TransportationManagement.models import Car, Driver, Accident, Proposer, Record
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

car_content_type = ContentType.objects.get_for_model(Car)
driver_content_type = ContentType.objects.get_for_model(Driver)
proposer_content_type = ContentType.objects.get_for_model(Proposer)
record_content_type = ContentType.objects.get_for_model(Record)
accident_content_type = ContentType.objects.get_for_model(Accident)

# permission = Permission.objects.create(codename=)

omd = Group.objects.get(name='OMD')
omd.permissions()
omd.user_set.add()