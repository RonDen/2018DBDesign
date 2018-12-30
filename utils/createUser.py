from django.contrib.auth.models import User
from random import choice

name_list = ['Aaron',
             'Abel',
             'Abraham',
             'Adam',
             'Adrian',
             'Aidan',
             'Alva',
             'Alex',
             'Alexander',
             'Alan',
             'Albert',
             'Alfred',
             'Andrew',
             'Andy',
             'Angus',
             'Anthony',
             'Apollo',
             'Arnold',
             'Arthur',
             'August', 'Austin']

the_name_list = ['Aaron', 'Abel', 'Abraham', 'Adam', 'Adrian', 'Aidan', 'Alva', 'Alex', 'Alexander', 'Alan', 'Albert',
                 'Alfred', 'Andrew', 'Andy', 'Angus', 'Anthony', 'Apollo', 'Arnold', 'Arthur', 'August', 'Austin',
                 'Marcus', 'Marcy', 'Mark', 'Marks', 'Mars', 'Marshal', 'Martin', 'Marvin', 'Mason', 'Matthew', 'Max',
                 'Michael', 'Mickey', 'Mike', 'Nathan', 'Nathaniel', 'Neil', 'Nelson', 'Nicholas', 'Nick', 'Noah',
                 'Norman', 'RandallRandal', 'Randolph', 'RandyRandallRandolph', 'Ray', 'Raymond', 'Reed', 'Rex',
                 'Richard', 'RichieRickRickyRitchie', 'Riley', 'Robert', 'RobinRobertRobinson', 'Robinson', 'Rock',
                 'Roger', 'Ronald', 'Rowan', 'Roy', 'Ryan', 'Jack', 'Jackson', 'Jacob', 'JamesJacob', 'Jason', 'Jay',
                 'Jeffery', 'Jerome', 'JerryGeraldJeremiahJerome', 'Jesse', 'JimJames', 'JimmyJames', 'JoeJoseph',
                 'John', 'Johnny', 'Jonathan', 'Jordan', 'JoseJoseph', 'Joshua', 'Justin']

mail_list = ['mail.buct.edu.cn', 'qq.com', 'sina.com', '163.com', '126.com', 'gmail']

def trime(line):
    s = ''
    for i in line:
        if i <= 'z' and i >= 'A':
            s += i
    return s

def make_password(name):
    res = name + 'passwd'
    while len(res) < 8:
        res += 'x'
    return res

if __name__ == '__main__':
    for name in the_name_list:
        user = User.objects.create_user(name, name+'@'+choice(mail_list), make_password(name) )
        user.first_name = name
        user.last_name = choice(the_name_list)
        user.save()
