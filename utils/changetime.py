from django.utils import  timezone
from datetime import timedelta
from random import randint
from TransportationManagement.models import Car, Accident, Driver, Proposer, Record


def modfiy_driver():
    for d in Driver.objects.all():
        d.Hiredata -= timedelta(randint(100, 1000))
        d.save()


def modfiy_proposer():
    for p in Proposer.objects.all():
        p.Date -= timedelta(randint(1, 30))
        p.save()


def modif_record():
    for r in Record.objects.all():
        stimenew = r.STime - timedelta(randint(100, 1000))
        etimenew = r.ETime - timedelta(randint(50, 1000))
        if (etimenew < stimenew):
            temp = etimenew
            etimenew = stimenew
            etimenew = temp
        r.ETime = etimenew
        r.STime = stimenew
        r.save()


def modify_accdient():
    for a in Accident.objects.all():
        pass
        a.Time -= timedelta(randint(100, 1000))


if __name__ == '__main__':
    # modfiy_driver()
    # modfiy_proposer()
    modif_record()