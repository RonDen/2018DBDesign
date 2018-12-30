from __future__ import absolute_import
from django.db import connection
from TransportationManagement.models import Car, Driver, Accident, Proposer, Record
from random import randint, choice
from .createUser import the_name_list
from django.utils import timezone
from datetime import timedelta
import MySQLdb


choice_list = ['豫B', '冀D', '豫E', '辽K', '皖A', '新B', '鲁N']
type_list = ['大型车', '中型车', '小型车', '公交车', '长途车']
coil_comsuption = {'大型车':1000, '中型车': 600, '小型车': 300, '公交车':200, '长途车': 350}
phone_first = ['155', '156', '181', '188', '136', '159', '137', '189', '177']
spot_list = ['市中心', '立交桥', '高速公路', '不详', '乡村小道']
cause_list = ['司机酒驾', '追尾', '超速驾驶', '超车事故', '天气因素', '疲劳驾驶', '不详']
money_list = [100, 200, 2000, 5000, 10000, 20000, 30000, 60000]

db = MySQLdb.connect('localhost', 'root', 'newpassword', 'transportation', charset='utf8')



def get_cno():
    s = choice(choice_list)+randint(1001, 9999).__str__()
    return s


def insert_car(num):
    for i in range(num):
        ctype = choice(type_list)
        c = Car(get_cno(), ctype, coil_comsuption[ctype], isAvailable=True)
        try:
            c.save()
        except:
            pass


def insert_record(num):
    sql1 = 'select cno, COilConsumpution from transportation.Car'
    sql2 = 'select dno, dname from driver'
    cursor = db.cursor()
    cursor.excute(sql1)
    result1 = cursor.fetchall()
    cursor.excute(sql2)
    result2 = cursor.fetchall()
    for i in range(num):
        a, b = choice(result1), choice(result2)
        cno, coil, dno, dname = a[0], a[1], b[0], b[1]
        stime = timezone.now()
        etime = stime + timedelta(days=randint(1, 30))
        r = Record(CNo=cno, DNo=dno, DName=dname, STime=stime, ETime=etime, OilConsumpution=coil, isDelete=False)
        try:
            r.save()
        except:
            pass


def insert_driver(num):
    for i in range(num):
        dname = choice(the_name_list)
        dsex = True if randint(1, 10) > 5 else False
        dage = randint(18, 45)
        dphone = choice(phone_first) + "%d%d" % (randint(1111, 9999), randint(1111, 9999))
        dhire = timezone.now()
        isdelete = False
        d = Driver(DName=dname, DSex=dsex, DAge=dage, PhoneNum=dphone, Hiredata=dhire, isAvailable=True)
        try:
            d.save()
        except:
            pass


def insert_accident(num):
    sql = 'select CNo_id, DNo_id, DName_id from transportation.record'
    cursor = db.cursor()
    cursor.excute(sql)
    result = cursor.fetchall()
    for i in range(num):
        a = choice(result)
        zscno, zsdno, zsdname = a[0], a[1], a[2]
        sgcno = get_cno()
        if sgcno == zscno:
            continue
        time = timezone.now()
        spot = choice(spot_list)
        cause = choice(cause_list)
        money = choice(money_list)
        acc = Accident(ZSCNo=zscno, SGCNo=sgcno, ZSDNo=zsdno, ZSDName=zsdname, Time=time, Spot=spot, Cause=cause, Money=money, isDelete=False)
        try:
            acc.save()
        except:
            pass


def insert_proposer(num):
    ctype = choice(type_list)
    num = randint(10, 30)
    date = timezone.now()
    p = Proposer(CType=ctype, Num=num, Date=date, isRecived=choice([True, False]))
    try:
        p.save()
    except:
        pass


if __name__ == '__main__':
    insert_car(1000)
    insert_driver(1000)
    insert_proposer(1000)
    insert_record(1000)
    insert_accident(100)
