from django.db import models
from django.forms import ModelForm


# TODO: add the create function for each model


class Car(models.Model):
    CNo = models.CharField(max_length=20, primary_key=True)
    CType = models.CharField(max_length=10)
    COilConsumpution = models.IntegerField()
    isAvailable = models.BooleanField(default=True)

    def __str__(self):
        return self.CNo

    class Meta:
        db_table = 'Car'


class CarForm(ModelForm):
    class Meta:
        model = Car
        exclude = ['isAvailable']
        # fields = ['CNo', 'CType', 'COilConsumpution']


class Driver(models.Model):
    DName = models.CharField(max_length=10, null=False)
    DSex = models.BooleanField(default=True)  # male is True, default male
    DAge = models.SmallIntegerField()
    PhoneNum = models.CharField(max_length=11)
    Hiredata = models.DateField()
    isAvailable = models.BooleanField(default=True)

    def __str__(self):
        return self.DName

    # tkX7nQqwXMDL8LV
    class Meta:
        db_table = 'Driver'


class DriverForm(ModelForm):
    class Meta:
        model = Driver
        exclude = ['isAvailable']
        # fields = ['DName', 'DSex', 'DAge', 'Hiredata']


class Proposer(models.Model):
    CType = models.CharField(max_length=10)
    Num = models.IntegerField()
    Mileage = models.IntegerField()
    Date = models.DateField(auto_now=True)
    # Date = models.DateTimeField(auto_now=True)
    isRecived = models.BooleanField(default=False)

    def __str__(self):
        return str(self.Date)

    class Meta:
        db_table = 'Proposer'


class ProposerForm(ModelForm):
    class Meta:
        model = Proposer
        exclude = ['isRecived']
        # fields = ['CType', 'Num', 'Mileage', 'Date']


class Record(models.Model):
    # Rid = models.AutoField(primary_key=True)
    CNo = models.ForeignKey(to=Car, related_name="cno_in_record", on_delete=models.CASCADE)
    DNo = models.ForeignKey(to=Driver, related_name="dno_in_record", on_delete=models.CASCADE)
    DName = models.CharField(max_length=20)
    STime = models.DateTimeField()
    ETime = models.DateTimeField()
    OilConsumpution = models.IntegerField()
    isDelete = models.BooleanField(default=False)

    class Meta:
        db_table = 'Record'
        ordering = ['-id']

    def __str__(self):
        return self.CNo.CNo + "---" + self.DName


class RecordManager(models.Manager):
    def create(self):
        pass


class AccidentManager(models.Manager):
    pass


class Accident(models.Model):
    ZSCNo = models.ForeignKey(to=Car, related_name="cno_case_accident", on_delete=models.CASCADE)
    SGCNo = models.CharField(max_length=20)
    ZSDNo = models.ForeignKey(to=Driver, related_name="dno_case_accident", on_delete=models.CASCADE)
    ZSDName = models.CharField(max_length=20)
    Time = models.DateTimeField()
    Spot = models.CharField(max_length=50)
    Cause = models.TextField()
    Money = models.IntegerField()
    isDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.ZSDName + str(self.Time)

    class Meta:
        db_table = 'Accident'
        ordering = ['-id']
