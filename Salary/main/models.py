from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
import datetime

class Sanction(models.Model): # Сетка штрафов а именно какие штрафы есть и какая за них ответственность
    reason = models.CharField(max_length = 200)
    summ = models.IntegerField()
    def __str__(self):
        return f"{self.reason}, {self.summ}"
  
class Salary(models.Model): # Зарплата человека

    YEAR_CHOICES = [(y,y) for y in range(datetime.date.today().year, datetime.date.today().year+1)]
    MONTH_CHOICE = [(m,m) for m in range(1,13)]

    account = models.ForeignKey(User ,on_delete=models.CASCADE)
    year = models.IntegerField(choices=YEAR_CHOICES, default=None, null=True)
    month = models.IntegerField(choices=MONTH_CHOICE,  default=None, null=True)
    summ = models.IntegerField(default=20000)
    paid = models.BooleanField()
    def __str__(self):
        if self.month > 10:
            month = str(self.month)
        else:
            month = str("0"+str(self.month))
        return f"{self.account}, {month}.{self.year}, {self.summ}"

class Bonuse(models.Model): # Бонусы человека
    salary = models.ForeignKey(Salary, on_delete=models.CASCADE)
    date = models.DateField()
    reason = models.CharField(max_length = 200)
    summ = models.IntegerField()
    def __str__(self):
        return f"Получатель: {self.salary.account}; От: {self.date}; По причине: {self.reason}; Сумма: {self.summ};"

class Sanctions(models.Model): # Штрафы человека
    salary = models.ForeignKey(Salary, on_delete=models.CASCADE)
    date = models.DateField()
    sanction = models.ForeignKey(Sanction, on_delete=models.DO_NOTHING)
    def __str__(self):
        return f"Зарплата: {self.salary}; штраф:{self.sanction} Суммa: {self.salary.summ}; от {self.date}"