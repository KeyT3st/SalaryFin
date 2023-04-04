from django.contrib.auth.models import User
from .models import Sanction, Bonuse, Sanctions,  Salary
from django.core.exceptions import ObjectDoesNotExist
import datetime
from collections import Counter

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

def get_summ_paid_salary():
    salary = Salary.objects.all()
    total = 0
    for salary in salary:
        if salary.paid == True:
            total += salary.summ
    return total

def get_summ_nopaid_salary():
    salary = Salary.objects.all()
    total = 0
    count = 0
    for salary in salary:
        if salary.paid == False:
            count += 1
            total += salary.summ
    return [total,count]

def get_bonuse_summ():
    bonuse = Bonuse.objects.all()
    total = 0
    for bonuse in bonuse:
        total += bonuse.summ
    return total

def get_sanctions_summ():
    sanctions = Sanctions.objects.all()
    total = 0
    for sanction in sanctions:
        total += sanction.sanction.summ
    return total

def most_popular_summ_of_bonuse():
    bonuse = Bonuse.objects.all()
    reason = []
    for bonuse in bonuse:
        reason.append(bonuse.summ)
    counter = Counter(reason).most_common()
    return counter

def most_popular_reason_of_sanctions():
    sanctions = Sanctions.objects.all()
    reasons = []
    for sanction in sanctions:
        reasons.append(sanction.sanction.reason)
    counter = Counter(reasons).most_common()
    return counter