import numpy as np
from django.contrib.auth import authenticate, login, logout, models
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, F
from django.db.models.functions import ExtractMonth, ExtractYear
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from DBDesign import settings
from TransportationManagement.models import Driver, Car, Accident, Proposer, Record
from .form import RegisterForm, CarForm, DriverForm, ProposerForm, AccidentForm, RecordForm
from .form import UserForm


def index(request):
    car_list = Car.objects.all()
    big_car_num = len(Car.objects.filter(CType='大型车'))
    small_car_num = len(Car.objects.filter(CType='小型车'))
    middle_car_num = len(Car.objects.filter(CType='中型车'))
    bus_num = len(Car.objects.filter(CType='公交车'))
    coach_num = len(Car.objects.filter(CType='长途车'))
    good_num = len(Car.objects.filter(isAvailable=True))
    bad_num = len(car_list) - good_num
    type_group = Car.objects.all().values('CType').annotate(c=Count('CNo'))
    pie_type = []
    for item in type_group:
        pie_type.append({'name': item['CType'], 'value': item['c']})
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
        'pie_type': pie_type,
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
    if request.session.get('is_login', None):
        # 登录状态不允许注册。你可以修改这条原则！
        return redirect("TransportationManagement:index")
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'register.html', locals())
            else:
                same_name_user = models.User.objects.filter(username=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:  # 邮箱地址唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'register.html', locals())

                new_user = models.User.objects.create_user(username=username, email=email, password=password1)
                new_user.save()
                return redirect('TransportationManagement:login')  # 自动跳转到登录页面
    register_form = RegisterForm()
    return render(request, 'register.html', locals())


@login_required
def car(request):
    car_list = Car.objects.all()
    type_group = Car.objects.all().values('CType').annotate(c=Count('CNo'))
    pie_type = []
    for item in type_group:
        pie_type.append({'name': item['CType'], 'value': item['c']})

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
        'pie_type': pie_type,
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
    print("收到表单")
    ctype = request.POST.get('ctype')
    cno = request.POST.get('cno')
    coil = request.POST.get('coil')
    Car.objects.update_or_create(CNo=cno, CType=ctype, COilConsumpution=int(coil))
    print("创建成功")
    return redirect('TransportationManagement:car')


@login_required
def change_car(request):
    oldNO = request.GET.get('cnoOld')
    newNo = request.GET.get('cno')
    car = Car.objects.get(pk=oldNO)
    ctype = request.GET.get('ctype')
    coil = request.GET.get('coil')
    isava = request.GET.get('isgood')
    if isava == 'true':
        isava = True
    else:
        isava = False
    if oldNO != newNo:
        print(oldNO, newNo)
        try:
            Car.objects.get(newNo)
            return JsonResponse({})
        except:
            car.CNo = newNo
    car.CType = ctype
    car.COilConsumpution = int(coil)
    car.isAvailable = isava
    car.save()
    data = {
        'newcno': car.CNo,
        'newctype': car.CType,
        'newoil': car.COilConsumpution,
        'ava': car.isAvailable
    }
    print(data)
    return JsonResponse(data)


@login_required
def delete_car(request):
    cno = request.GET.get('cno')
    car = get_object_or_404(Car, pk=cno)
    print(car.CType, car.COilConsumpution)
    data = {}
    car.delete()
    return JsonResponse(data)


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
    print("收到表单")
    dname = request.POST.get('name')
    dsex = request.POST.get('sex') == '男'
    dage = int(request.POST.get('age'))
    dphone = request.POST.get('phone')
    hiredate = request.POST.get('hiredate').replace('/', '-')
    driver, is_create = Driver.objects.update_or_create(DName=dname, DSex=dsex, DAge=dage, PhoneNum=dphone,
                                                        Hiredata=hiredate)
    driver.save()
    return redirect('TransportationManagement:driver')


@login_required
def change_driver(request):
    did = int(request.GET.get('did'))
    dname = request.GET.get('dname')
    dsex = request.GET.get('dsex') == '男'
    dage = request.GET.get('dage')
    dphone = request.GET.get('dphone')
    dtime = request.GET.get('dtime').replace('/', '-')
    dava = request.GET.get('dage') == 'true'
    driver = get_object_or_404(Driver, pk=did)
    driver.DName = dname
    driver.DAge = dage
    driver.DSex = dsex
    driver.PhoneNum = dphone
    driver.Hiredata = dtime
    driver.isAvailable = dava
    driver.save()
    data = {
        'newname': driver.DName,
        'newsex': driver.DSex,
        'newage': driver.DAge,
        'newphone': driver.PhoneNum,
        'newtime': driver.Hiredata,
        'newava': driver.isAvailable
    }
    print(data)
    return JsonResponse(data)


@login_required
def delete_driver(request):
    did = int(request.GET.get('did'))
    driver = Driver.objects.get(pk=did)
    driver.delete()
    return JsonResponse({})



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
    did = int(request.POST.get('did'))
    cno = request.POST.get('cno')
    stime = request.POST.get('stime').replace('/', '-')
    etime = request.POST.get('etime').replace('/', '-')
    oil = int(request.POST.get('oil'))
    try:
        dname = Driver.objects.get(pk=did).DName
        car = Car.objects.get(pk=cno)
    except:
        return redirect('TransportationManagement:record')
    record, iscreate = Record.objects.update_or_create(DNo_id=did, DName=dname, CNo=car, STime=stime, ETime=etime,
                                                       OilConsumpution=oil)
    record.save()
    print("加入成功！")
    return redirect('TransportationManagement:record')


@login_required
def change_record(request):
    rid = int(request.GET.get('rid'))
    did = int(request.GET.get('rid'))
    dname = request.GET.get('rid')
    cno = request.GET.get('cno')
    stime = request.GET.get('stime').replace('/', '-')
    etime = request.GET.get('etime').replace('/', '-')
    oil = int(request.GET.get('oil'))
    isdelete = request.GET.get('isdelete') == 'true'
    record = Record.objects.get(pk=rid)
    try:
        driver = Driver.objects.get(pk=did)
        car = Car.objects.get(CNo=cno)
        driver.DName = dname
        car.CNo = cno
        driver.save()
        car.save()
        record.DNo = driver
        record.CNo = car
        record.STime = stime
        record.ETime = etime
        record.OilConsumpution = oil
        record.isDelete = isdelete
        record.save()
    except:
        return JsonResponse({'failed': True})
    data = {
        'newdid': record.DNo_id,
        'newdname': record.DName,
        'newcno': record.CNo.CNo,
        'newstime': record.STime,
        'newetime': record.ETime,
        'newoil': record.OilConsumpution,
        'newdelete': record.isDelete
    }
    return JsonResponse(data)



@login_required
def delete_record(request):
    rid = int(request.GET.get('rid'))
    record = Record.objects.get(pk=rid)
    record.delete()
    return JsonResponse({})


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
    ctype = request.POST.get('ctype')
    print(ctype)
    print(request.POST.get('num'))
    print(request.POST.get('mile'))
    num = int(request.POST.get('num'))
    mile = int(request.POST.get('mile'))
    proposer, is_create = Proposer.objects.update_or_create(CType=ctype, Num=num, Mileage=mile)
    proposer.save()
    return redirect('TransportationManagement:addproposer')

@login_required
def change_proposer(request):
    pid = int(request.GET.get('pid'))
    ctype = request.GET.get('ctype')
    num = int(request.GET.get('num'))
    mile = int(request.GET.get('mile'))
    time = request.GET.get('time').replace('/', '-')
    isrec = request.GET.get('isrce') == 'true'
    proposer = Proposer.objects.get(pk=pid)
    proposer.CType = ctype
    proposer.Num = num
    proposer.Mileage = mile
    proposer.Date = time
    proposer.isRecived = isrec
    proposer.save()
    data = {
        'newctype': proposer.CType,
        'newnum': proposer.Num,
        'newmile': proposer.Mileage,
        'newtime': proposer.Date,
        'newrec': proposer.isRecived
    }
    print(data)
    return JsonResponse(data)


@login_required
def delete_proposer(request):
    pid = int(request.GET.get('pid'))
    proposer = get_object_or_404(Proposer, pk=pid)
    proposer.delete()
    return JsonResponse({})


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
    zdid = int(request.POST.get('zdid'))
    zcno = request.POST.get('zcno')
    scno = request.POST.get('scno')
    stime = request.POST.get('stime').replace('/', '-')
    spot = request.POST.get('spot')
    cause = request.POST.get('cause')
    money = int(request.POST.get('money'))
    try:
        car = Car.objects.get(pk=zcno)
        driver = Car.objects.get(pk=zdid)
        accident, is_create = Accident.objects.update_or_create(ZSCNo=car, SGCNo=scno, ZSDNo=driver, Time=stime,
                                                                Spot=spot, Cause=cause, Money=money)
        accident.save()
    except:
        return JsonResponse({'failed': True})
    return redirect('TransportationManagement:accident')


@login_required
def change_accident(request):
    aid = int(request.GET.get('aid'))
    zdid = int(request.GET.get('zdid'))
    zdname = request.GET.get('zdname')
    zcno = request.GET.get('zcno')
    scno = request.GET.get('scno')
    stime = request.GET.get('stime').replace('/', '-')
    spot = request.GET.get('spot')
    cause = request.GET.get('cause')
    money = int(request.GET.get('money'))
    isdelete = request.GET.get('isdelete') == 'true'
    accident = Accident.objects.get(pk=aid)
    try:
        driver = Driver.objects.get(pk=zdid)
        car = Car.objects.get(pk=zcno)
        driver.DName = zdname
        driver.save()
        accident.ZSCNo = car
        accident.ZSDNo = driver
        accident.ZSDName = driver.DName
        accident.Time = stime
        accident.SGCNo = scno
        accident.Spot = spot
        accident.Cause = cause
        accident.Money = money
        accident.isDelete = isdelete
        accident.save()
    except:
        return JsonResponse({'failed': True})
    data = {
        'newzdid': accident.ZSDNo_id,
        'newzdname': accident.ZSDName,
        'newzcno': accident.ZSCNo.CNo,
        'newscno': accident.SGCNo,
        'newstime': accident.Time,
        'newspot': accident.Spot,
        'newcause': accident.Cause,
        'newmoney': accident.Money,
        'newdelete': accident.isDelete
    }
    return JsonResponse(data)




@login_required
def delete_accident(request):
    aid = int(request.GET.get('aid'))
    accident = Accident.objects.get(pk=aid)
    accident.delete()
    return JsonResponse({})


def ajax_get(request):
    name = request.GET.get('name')
    try:
        car = Car.objects.get(pk=name)
        ctype = car.CType
    except:
        ctype = 'Not exists'

    data = {'name': name, 'ctype': ctype}
    return JsonResponse(data)
