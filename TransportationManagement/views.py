from django.shortcuts import render, redirect
from django.http import HttpResponse
from TransportationManagement.models import Driver,Car,Accident,Proposer,Record
from django.db.models import Avg,Count,Min,Max,Sum, F, Q
from django.db.models.functions import ExtractMonth, ExtractYear
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .form import UserForm, CarForm, DriverForm, ProposerForm, AccidentForm, RecordForm
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from .form import UserForm
from DBDesign import settings
import numpy as np



def index(request):
    car_list = Car.objects.all()
    big_car_num = len(Car.objects.filter(CType='大型车'))
    small_car_num = len(Car.objects.filter(CType='小型车'))
    middle_car_num = len(Car.objects.filter(CType='中型车'))
    bus_num = len(Car.objects.filter(CType='公交车'))
    coach_num = len(Car.objects.filter(CType='长途车'))
    good_num = len(Car.objects.filter(isAvailable=True))
    bad_num = len(car_list) - good_num
    pie_car_aviable = [
        {'name':'正常', 'value': good_num},
        {'name':'维修', 'value': bad_num}
    ]
    type_list = ['大型车', '中型车', '小型车', '公交车', '长途车']
    num_list = [big_car_num, middle_car_num, small_car_num, bus_num, coach_num]

    date_group = Driver.objects.all().annotate(year=ExtractYear('Hiredata'),
                                               month=ExtractMonth('Hiredata'),
                                               ).values('year','month').order_by('year', 'month').annotate(c=Count('id'))
    age_group = Driver.objects.all().order_by('DAge').values('DAge').annotate(c=Count('id'))
    age_list = []
    age_c = []
    for item in age_group:
        age_list.append(item['DAge'])
        age_c.append(item['c'])
    date_list = []
    date_c = []
    for item in date_group:
        date_list.append(str(item['year']) + '/' + str(item['month']))
        date_c.append(item['c'])
    male_num = len(Driver.objects.filter(DSex=True))
    female_num = len(Driver.objects.filter(DSex=False))

    proposer_group = Proposer.objects.all().annotate(year=ExtractYear('Date'),
                                               month=ExtractMonth('Date'),
                                               ).values('year','month').order_by('year', 'month').annotate(c=Count('id'))
    pro_date_list = []
    pro_date_c = []
    for item in proposer_group:
        pro_date_list.append(str(item['year']) + '/' + str(item['month']))
        pro_date_c.append(item['c'])
    pro_type_list = []
    pro_type_c = []
    type_group = Proposer.objects.all().order_by('CType').values('CType').annotate(c=Count('id'))
    for item in type_group:
        pro_type_list.append(item['CType'])
        pro_type_c.append(item['c'])

    pie_data = []
    for kind, c in zip(pro_type_list, pro_type_c):
        pie_data.append({'name': kind, 'value': c})

    record_oil_group = Record.objects.all().order_by('OilConsumpution').values('OilConsumpution').annotate(c=Count('id'))
    oil_list = []
    oil_count = []
    for item in record_oil_group:
        oil_list.append(item['OilConsumpution'])
        oil_count.append(item['c'])

    averoil = Record.objects.all().aggregate(Avg('OilConsumpution'))['OilConsumpution__avg']
    good_time_list = Record.objects.filter(ETime__gt=F('STime'))
    time_spent_list = good_time_list.order_by(F('ETime') - F('STime'))
    range_list = []
    for item in time_spent_list:
        range_list.append((item.ETime - item.STime).days)
    c, bins = np.histogram(range_list)
    c, bins = list(c), list(bins)
    bins = [int(b) for b in bins]
    avg_bins = int(np.average(bins))

    # record_time_spent = Record.objects.all().order_by(F('ETime')-F('STime')).reverse().values(F('ETime')-F('STime')).annotate(c=Count('id'))

    year16_conunt = len(Accident.objects.filter(Time__year=2016))
    year17_count = len(Accident.objects.filter(Time__year=2017))
    year18_count = len(Accident.objects.filter(Time__year=2018))
    year_count = [year16_conunt, year17_count, year18_count]

    money_lt1000 = len(Accident.objects.filter(Money__lt=1000))
    money_1000_3000 = len(Accident.objects.filter(Money__range=(1000, 3000)))
    money_3000_10000 = len(Accident.objects.filter(Money__range=(3000, 10000)))
    money_gt10000 = len(Accident.objects.filter(Money__gt=10000))
    money_list = [money_lt1000, money_1000_3000, money_3000_10000, money_gt10000]
    pie_money = [
        {'name': '少于1000元', 'value': money_lt1000},
        {'name': '1000元到3000元', 'value': money_1000_3000},
        {'name': '3000元到1万元', 'value': money_3000_10000},
        {'name': '大于一万元', 'value': money_gt10000},
    ]
    spot_group = Accident.objects.all().order_by('Spot').values('Spot').annotate(c=Count('id'))
    cause_group = Accident.objects.all().order_by('Cause').values('Cause').annotate(c=Count('id'))
    spot_list = []
    spot_c = []
    cause_list = []
    cause_c = []
    pie_spot = []
    pie_cause = []
    for item1, item2 in zip(spot_group, cause_group):
        spot_list.append(item1['Spot']), spot_c.append(item1['c'])
        pie_spot.append({'name': item1['Spot'], 'value': item1['c']})
        cause_list.append(item2['Cause']), cause_c.append(item2['c'])
        pie_cause.append({'name': item2['Cause'], 'value': item2['c']})


    context = {
        'type_list': type_list,
        'num_list': num_list,
        'pie_car_aviable': pie_car_aviable,
        'date_list': date_list,
        'date_c': date_c,
        'age_list': age_list,
        'age_c': age_c,
        'male_num': male_num,
        'female_num': female_num,
        'pro_date_list': pro_date_list,
        'pro_date_c':pro_date_c,
        'pro_type_list': pro_type_list,
        'pro_type_c':pro_type_c,
        'pie_data': pie_data,
        'oil_list': oil_list,
        'oil_count': oil_count,
        'average_oil': averoil,
        'c': c,
        'bins': bins,
        'avg_bins': avg_bins,
        'year_count':year_count,
        'pie_money': pie_money,
        'spot_list': spot_list,
        'spot_c': spot_c,
        'cause_list': cause_list,
        'cause_c': cause_c,
        'pie_spot': pie_spot,
        'pie_cause': pie_cause
            }
    return render(request, 'overview.html', context)

def test(request):
    userform = UserForm()
    carform = CarForm()
    driverform = DriverForm()
    proposerform = ProposerForm()
    recordform = RecordForm()
    accidentform = AccidentForm()
    context = {
        'userform': userform,
        'carform': carform,
        'driverform': driverform,
        'proposerform': proposerform,
        'recordform': recordform,
        'accidentform':accidentform
    }
    return render(request, 'test.html', context)

def hello(request):
    return HttpResponse("Hello, nice to see you.")
    # return render(request, 'Accident.html')

@login_required
def overview(request):
    pass


def need_login(request):
    return render(request, 'login.html')


@csrf_exempt
def mylogin(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    print(request.POST)
    print(username)
    print(password)
    user = authenticate(username=username, password=password)
    if user:
        login(request, user)
        return redirect('/TransportationManagement/index/')
    else:
        return HttpResponse("登录失败，请重试。")


@csrf_exempt
@login_required
def mylogout(request):
    print("-------------------------")
    logout(request)
    return redirect("TransportationManagement:login")


def send_email(email, code):
    from django.core.mail import EmailMultiAlternatives
    subject = '这是一份用于注册车辆运营管理系统的邮件'

    text_content = """亲爱的用户，您正在注册车辆运输管理系统。"""

    html_content = '''
                    <p>感谢注册<a href="http://{}/confirm/?code={}" target=blank>https:localhost:8000</a>，\
                    <p>请点击站点链接完成注册确认！</p>
                    <p>此链接有效期为{}天！</p>
                    '''.format('127.0.0.1:8000', code, settings.CONFIRM_DAYS)
    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def register(request):
    return HttpResponse("zhucyem")


@login_required
def car(request):
    car_list = Car.objects.all()
    big_car_num = len(Car.objects.filter(CType='大型车'))
    small_car_num = len(Car.objects.filter(CType='小型车'))
    middle_car_num = len(Car.objects.filter(CType='中型车'))
    bus_num = len(Car.objects.filter(CType='公交车'))
    coach_num = len(Car.objects.filter(CType='长途车'))
    type_list = ['大型车', '中型车', '小型车', '公交车', '长途车']
    good_num = len(Car.objects.filter(isAvailable=True))
    bad_num = len(Car.objects.filter(isAvailable=False))
    pie_car_aviable = [
        {'name': '正常', 'value': good_num},
        {'name': '维修', 'value': bad_num}
    ]
    num_list = [big_car_num, middle_car_num, small_car_num, bus_num, coach_num]

    carForm = CarForm()
    context = {
        'car_list': car_list,
        'type_list': type_list,
        'num_list': num_list,
        'pie_car_aviable': pie_car_aviable,
        'carForm': carForm
               }
    return render(request, 'Car2.html', context)
    # return HttpResponse("The Car Page")


@login_required
def add_car(request):
    print("------------------------")
    ctype = request.POST.get('ctype')
    cno = request.POST.get('cno')
    coil = request.POST.get('coil')
    print('ctype:', ctype)
    print('cno:', cno)
    print('coil:', coil)
    return redirect('TransportationManagement:car')


@login_required
def change_car(request):
    pass


@login_required
def delete_car(request):
    pass


@login_required
def driver(request):
    driver_list = Driver.objects.all()

    date_group = Driver.objects.all().annotate(year=ExtractYear('Hiredata'),
                                               month=ExtractMonth('Hiredata'),
                                               ).values('year','month').order_by('year', 'month').annotate(c=Count('id'))
    age_group = Driver.objects.all().order_by('DAge').values('DAge').annotate(c=Count('id'))
    age_list = []
    age_c = []
    for item in age_group:
        age_list.append(item['DAge'])
        age_c.append(item['c'])
    date_list = []
    date_c = []
    for item in date_group:
        date_list.append(str(item['year']) + '/' + str(item['month']))
        date_c.append(item['c'])
    male_num = len(Driver.objects.filter(DSex=True))
    female_num = len(Driver.objects.filter(DSex=False))

    driverForm = DriverForm()
    context = {
        'driver_list': driver_list,
        'date_list': date_list,
        'date_c': date_c,
        'age_list': age_list,
        'age_c': age_c,
        'male_num': male_num,
        'female_num': female_num,
        'driverForm':driverForm
    }
    return render(request, 'Driver2.html', context)


@login_required
def add_driver(request):
    pass


@login_required
def change_driver(request):
    pass


@login_required
def delete_driver(request):
    pass



@login_required
def record(request):
    rec_list = Record.objects.all()
    record_oil_group = Record.objects.all().order_by('OilConsumpution').values('OilConsumpution').annotate(c=Count('id'))
    midian = record_oil_group[len(record_oil_group) // 2]['OilConsumpution']
    oil_list = []
    oil_count = []
    oil_all = 0
    for item in record_oil_group:
        oil_list.append(item['OilConsumpution'])
        oil_all += item['OilConsumpution']
        oil_count.append(item['c'])

    averoil = rec_list.aggregate(Avg('OilConsumpution'))['OilConsumpution__avg']
    good_time_list = Record.objects.filter(ETime__gt=F('STime'))
    time_spent_list = good_time_list.order_by(F('ETime')-F('STime'))
    range_list = []
    for item in time_spent_list:
        range_list.append((item.ETime - item.STime).days)
    c, bins = np.histogram(range_list)
    c, bins = list(c), list(bins)
    bins = [int(b) for b in bins]
    # bins = map(int, bins)
    avg_bins = int(np.average(bins))


    recordForm = RecordForm()
    context = {
        'record_list': rec_list,
        'oil_list': oil_list,
        'oil_count': oil_count,
        'average_oil': averoil,
        'c': c,
        'bins': bins,
        'avg_bins': avg_bins,
        'recordForm': recordForm
    }
    return render(request, 'Record2.html', context)


@login_required
def add_record(request):
    pass


@login_required
def change_record(request):
    pass


@login_required
def delete_record(request):
    pass


@login_required
def proposer(request):
    pro_list = Proposer.objects.all()
    pro_date_list = []
    pro_date_c = []
    proposer_group = Proposer.objects.all().annotate(year=ExtractYear('Date'),
                                                     month=ExtractMonth('Date'),
                                                     ).values('year', 'month').order_by('year', 'month').annotate(c=Count('id'))
    for item in proposer_group:
        pro_date_list.append(str(item['year']) + '/' + str(item['month']))
        pro_date_c.append(item['c'])
    pro_type_list = []
    pro_type_c = []
    type_group = Proposer.objects.all().order_by('CType').values('CType').annotate(c=Count('id'))
    for item in type_group:
        pro_type_list.append(item['CType'])
        pro_type_c.append(item['c'])

    pie_data = []
    for kind, c in zip(pro_type_list, pro_type_c):
        pie_data.append({'name': kind, 'value': c})

    proposerForm = ProposerForm()
    context = {
        'proposer_list': pro_list,
        'pro_date_list': pro_date_list,
        'pro_date_c':pro_date_c,
        'pro_type_list': pro_type_list,
        'pro_type_c':pro_type_c,
        'pie_data': pie_data,
        'proposerForm':proposerForm
    }
    return render(request, 'Proposer2.html', context)


@login_required
def add_proposer(request):
    pass


@login_required
def change_proposer(request):
    pass


@login_required
def delete_proposer(request):
    pass


@login_required
def accident(request):
    acc_list = Accident.objects.all()
    year16_conunt = len(Accident.objects.filter(Time__year=2016))
    year17_count = len(Accident.objects.filter(Time__year=2017))
    year18_count = len(Accident.objects.filter(Time__year=2018))
    year_count = [year16_conunt, year17_count, year18_count]

    money_lt1000 = len(Accident.objects.filter(Money__lt=1000))
    money_1000_3000 = len(Accident.objects.filter(Money__range=(1000, 3000)))
    money_3000_10000 = len(Accident.objects.filter(Money__range=(3000, 10000)))
    money_gt10000 = len(Accident.objects.filter(Money__gt=10000))
    money_list = [money_lt1000, money_1000_3000, money_3000_10000, money_gt10000]
    pie_money = [
        {'name': '少于1000元', 'value': money_lt1000},
        {'name': '1000元到3000元', 'value': money_1000_3000},
        {'name': '3000元到1万元', 'value': money_3000_10000},
        {'name': '大于一万元', 'value': money_gt10000},
    ]
    spot_group = Accident.objects.all().order_by('Spot').values('Spot').annotate(c=Count('id'))
    cause_group = Accident.objects.all().order_by('Cause').values('Cause').annotate(c=Count('id'))
    spot_list = []
    spot_c = []
    cause_list = []
    cause_c = []
    pie_spot = []
    pie_cause = []
    for item1, item2 in zip(spot_group, cause_group):
        spot_list.append(item1['Spot']), spot_c.append(item1['c'])
        pie_spot.append({'name': item1['Spot'], 'value': item1['c']})
        cause_list.append(item2['Cause']), cause_c.append(item2['c'])
        pie_cause.append({'name': item2['Cause'], 'value': item2['c']})
    accident_list = Accident.objects.all()

    accidentForm = AccidentForm()
    context = {
        'accident_list': accident_list,
        'year_count': year_count,
        'pie_money': pie_money,
        'spot_list': spot_list,
        'spot_c': spot_c,
        'cause_list': cause_list,
        'cause_c': cause_c,
        'pie_spot': pie_spot,
        'pie_cause': pie_cause,
        'accidentForm': accidentForm
    }
    return render(request, 'Accident2.html', context)
    # return HttpResponse("The Accident Page")


@login_required
def add_accident(request):
    pass


@login_required
def change_accident(request):
    pass


@login_required
def delete_accident(request):
    pass

