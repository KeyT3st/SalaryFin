from django.contrib.auth.models import User
from .models import Sanction, Bonuse, Sanctions,  Salary

def calc_salary(salary_id):
    salary = Salary.objects.get(id=salary_id)
    sanctions = salary.sanctions_set.all()
    bonuses = salary.bonuse_set.all()
    summ = salary.account.rate
    for bonus in bonuses:
        summ += bonus.summ
    for sanction in sanctions:
        summ -= sanction.sanction.summ
    return summ