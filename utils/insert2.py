from TransportationManagement.models import Driver, Car, Accident, Record, Proposer
from random import randint, choice, choices
from createUser import the_name_list
from django.utils import timezone
from datetime import timedelta

choice_list = ['豫B', '冀D', '豫E', '辽K', '皖A', '新B', '鲁N']
type_list = ['大型车', '中型车', '小型车', '公交车', '长途车']
coil_comsuption = {'大型车':1000, '中型车': 600, '小型车': 300, '公交车':200, '长途车': 350}
phone_first = ['155', '156', '181', '188', '136', '159', '137', '189', '177']
spot_list = ['市中心', '立交桥', '高速公路', '不详', '乡村小道']
cause_list = ['司机酒驾', '追尾', '超速驾驶', '超车事故', '天气因素', '疲劳驾驶', '不详']
money_list = [100, 200, 2000, 5000, 10000, 20000, 30000, 60000]



def get_cno():
    s = choice(choice_list)+randint(1001, 9999).__str__()
    return s

def add_car(num):
    for i in range(num):
        ctype = choice(type_list)
        try:
            Car.objects.create(CNo=get_cno(), CType=ctype, COilConsumpution=coil_comsuption[ctype], isAvailable=randint(1,10)<9)
        except:
            pass


def add_driver(num):
    for i in range(num):
        dname = choice(the_name_list)
        dsex = True if randint(1, 10) > 5 else False
        dage = randint(18, 45)
        dphone = choice(phone_first) + "%d%d" % (randint(1111, 9999), randint(1111, 9999))
        dhire = timezone.now() - timedelta(days=randint(10, 1000))
        try:
            Driver.objects.create(DName=dname, DSex=dsex, DAge=dage, PhoneNum=dphone, Hiredata=dhire, isAvailable=randint(1,10)<9)
        except:
            pass


def add_proposer(num):
    for i in range(num):
        ctype = choice(type_list)
        num = randint(100, 1000)
        mileage = randint(100, 10000)
        date = timezone.now() - timedelta(days=randint(10, 1000))
        try:
            Proposer.objects.create(CType=ctype, Num=num, Mileage=mileage, Date=date, isRecived=randint(1,10)>8)
        except:
            pass


def add_record(num):
    car_set = Car.objects.all()
    driver_set = Driver.objects.all()
    cars = choices(car_set, k=num)
    drivers = choices(driver_set, k=num)
    for car, driver in zip(cars, drivers):
        cno, ctype, dno, dname = car.CNo, car.CType, driver.id, driver.DName
        stime = timezone.now() - timedelta(days=randint(10, 1000))
        days = randint(5, 60)
        etime = stime + timedelta(days=days)
        oil = days * coil_comsuption[ctype]
        try:
            Record.objects.create(CNo=car, DName=dname, DNo=driver, STime=stime, ETime=etime, OilConsumpution=oil, isDelete=False)
        except:
            pass



def add_accident(num):
    records = choices(Record.objects.all(), k=num)
    for rec in records:
        zscar = rec.CNo
        zsdriver = rec.DNo
        zsdname = zsdriver.DName
        sgcno = get_cno()
        time = timezone.now() - timedelta(days=randint(10, 1000))
        money = choice(money_list)
        spot = choice(spot_list)
        cause = choice(cause_list)
        isdelete = False
        try:
            Accident.objects.create(ZSCNo=zscar,ZSDNo=zsdriver, ZSDName=zsdname, SGCNo=sgcno, Time=time,
                                    Money=money, Spot=spot, Cause=cause, isDelete=isdelete)
        except:
            pass







if __name__ == '__main__':
    # add_car(100)
    # add_driver(200)
    # add_proposer(500)
    add_record(500)
    add_accident(50)




