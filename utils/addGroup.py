from django.contrib.auth.models import User, Group,Permission
from TransportationManagement.models import Car, Accident,Record,Driver,Proposer

def initial_usergroup():

    Group.objects.create(name='CarManager')
    Group.objects.create(name='DriverManager')
    Group.objects.create(name='ProposerManager')
    Group.objects.create(name='RecordManager')
    Group.objects.create(name='AccidentManager')

    car_view = Permission.objects.get(codename='view_car')
    car_add = Permission.objects.get(codename='add_car')
    car_change = Permission.objects.get(codename='change_car')
    car_delete = Permission.objects.get(codename='delete_car')

    driver_view = Permission.objects.get(codename='view_driver')
    driver_add = Permission.objects.get(codename='add_driver')
    driver_change = Permission.objects.get(codename='change_driver')
    driver_delete = Permission.objects.get(codename='delete_driver')

    proposer_view = Permission.objects.get(codename='view_proposer')
    proposer_add = Permission.objects.get(codename='add_proposer')
    proposer_change = Permission.objects.get(codename='change_proposer')
    proposer_delete = Permission.objects.get(codename='delete_proposer')

    record_view = Permission.objects.get(codename='view_record')
    record_add = Permission.objects.get(codename='add_record')
    record_change = Permission.objects.get(codename='change_record')
    record_delete = Permission.objects.get(codename='delete_record')

    accident_view = Permission.objects.get(codename='view_accident')
    accident_add = Permission.objects.get(codename='add_accident')
    accident_change = Permission.objects.get(codename='change_accident')
    accident_delete = Permission.objects.get(codename='delete_accident')

    CarManager = Group.objects.get(name='CarManager')
    DriverManager = Group.objects.get(name='DriverManager')
    ProposerManager = Group.objects.get(name='ProposerManager')
    RecordManager = Group.objects.get(name='RecordManager')
    AccidentManager = Group.objects.get(name='AccidentManager')

    CarManager.permissions.add(car_add)
    CarManager.permissions.add(car_view)
    CarManager.permissions.add(car_change)
    CarManager.permissions.add(car_delete)
    
    DriverManager.permissions.add(driver_add)
    DriverManager.permissions.add(driver_view)
    DriverManager.permissions.add(driver_change)
    DriverManager.permissions.add(driver_delete)

    ProposerManager.permissions.add(proposer_add)
    ProposerManager.permissions.add(proposer_view)
    ProposerManager.permissions.add(proposer_change)
    ProposerManager.permissions.add(proposer_delete)

    RecordManager.permissions.add(record_add)
    RecordManager.permissions.add(record_view)
    RecordManager.permissions.add(record_change)
    RecordManager.permissions.add(record_delete)

    AccidentManager.permissions.add(accident_add)
    AccidentManager.permissions.add(accident_view)
    AccidentManager.permissions.add(accident_change)
    AccidentManager.permissions.add(accident_delete)

    def add_user(divide_list):
         user_list = User.objects.all()
         k = 0
         for u in user_list:
             k += 1
             if k < divide_list[0]:
                 u.groups.add(CarManager)
             elif k < divide_list[1]:
                 u.groups.add(DriverManager)
             elif k < divide_list[2]:
                 u.groups.add(ProposerManager)
             elif k < divide_list[3]:
                 u.groups.add(RecordManager)
             elif k < divide_list[4]:
                 u.groups.add(AccidentManager)
             else:
                 u.groups.add(AccidentManager, CarManager, RecordManager, DriverManager, ProposerManager)
    user_list = User.objects.all()
    user_num = len(user_list) - 5
    add_user([user_num // 5, user_num // 5, user_num // 5, user_num // 5, user_num // 5])


if __name__ == '__main__':
    initial_usergroup()