from django.shortcuts import render, redirect
from django.http import HttpResponse
from TransportationManagement.models import Driver,Car,Accident,Proposer,Record
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .form import UserForm, CarForm, DriverForm, ProposerForm
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from .form import UserForm



def index(request):
    form = UserForm()
    return render(request, 'index1.html', {'form': form})


def hello(request):
    return HttpResponse("Hello, nice to see you.")
    # return render(request, 'Accident.html')

def get_user(request):
    pass


@csrf_exempt
def ajax_submit(request):
    print(request.POST)

    return HttpResponse("response to ajax: " + request.POST['host'])


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
        return HttpResponse("登录失败.")


@csrf_exempt
@login_required
def mylogout(request):
    if not request.user.is_authenticated:
        return render(request, 'index1.html')
        # return redirect('/TransportationManagement/index/')
    request.session.flush()
    return render(request, 'index1.html')
    # return redirect('/TransportationManagement/index/')


def register(request):
    pass


def login_view(request):
    username = request.POST.GET('username')
    password = request.POST.GET('password')
    user = authenticate(username=username, password=password)
    if user:
        login(request, user)
        return redirect('index1.html')
    else:
        return HttpResponse("用户名或密码错误")

def logout_view(request):
    logout(request)
    return redirect('index1.html')


@login_required
def accident(request):
    request.GET('POST')
    acc_list = Accident.objects.all()
    return render(request, 'Accident.html', {'acc_list': acc_list})
    # return HttpResponse("The Accident Page")


@login_required
def driver(request):
    driver_list = Driver.objects.all()
    year16_num = len(Driver.objects.filter(Hiredata__year=2016))
    year17_num = len(Driver.objects.filter(Hiredata__year=2017))
    year18_num = len(Driver.objects.filter(Hiredata__year=2018))

    age18_25 = len(Driver.objects.filter(DAge__range=(18, 25)))
    age25_35 = len(Driver.objects.filter(DAge__range=(25, 35)))
    age35_45 = len(Driver.objects.filter(DAge__range=(25, 45)))

    gender_male = len(Driver.objects.filter(DSex=True))
    gender_female = len(Driver.objects.filter(DSex=False))

    context = {
        'driver_list': driver_list[:20],
        'year_nums': [year16_num, year17_num, year18_num],
        'age_nums': [age18_25, age25_35, age35_45],
        'male_num': gender_male,
        'female_num': gender_female
    }
    return render(request, 'Driver.html', context)
    # return HttpResponse("The Driver Page")


@login_required
def car(request):
    car_list = Car.objects.all()
    big_car_num = len(Car.objects.filter(CType='大型车'))
    small_car_num = len(Car.objects.filter(CType='小型车'))
    middle_car_num = len(Car.objects.filter(CType='中型车'))
    bus_num = len(Car.objects.filter(CType='公交车'))
    coach_num = len(Car.objects.filter(CType='长途车'))
    type_list = ['大型车', '中型车', '小型车', '公交车', '长途车']
    num_list = [big_car_num, middle_car_num, small_car_num, bus_num, coach_num]
    context = {'car_list': car_list[:20],
               'type_list': type_list,
               'num_list': num_list
               }
    return render(request, 'Car.html', context)
    # return HttpResponse("The Car Page")

@login_required
def record(request):
    rec_list = Record.objects.all()
    return render(request, 'Record.html', {'rec_list': rec_list})
    # return HttpResponse("The Record Page")

@login_required
def proposer(request):
    pro_list = Proposer.objects.all()
    return render(request, 'Proposer.html', {'pro_list': pro_list})
