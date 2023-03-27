from django.contrib.auth.models import User
from .models import Sanction, Bonuse, Sanctions,  Salary
from django.core.exceptions import ObjectDoesNotExist
import datetime
import main

Users = User.objects.all()

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

def nnm_salary(Users=Users): #new next month salary
    for User in Users:
        try:
            next_month = int(datetime.datetime.now().month) + 1
            Salary.objects.get(account_id=User.id, month=next_month)
        except ObjectDoesNotExist:
                salary = Salary()
                salary.account = User
                if datetime.datetime.now().month < 12:
                    salary.month = datetime.datetime.now().month+1
                else:
                    salary.month = 1
                if datetime.datetime.now().month == 12:
                    salary.year = datetime.datetime.now().year +1
                else:
                    salary.year = datetime.datetime.now().year
                salary.summ = User.rate
                salary.paid = False
                salary.save()
        except:
            print("Обратитесь за помощью к программистам")