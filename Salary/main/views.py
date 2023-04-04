from django.shortcuts import render, redirect
from django.db.utils import IntegrityError
from django.http import HttpResponseNotFound, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group
from .forms import UserForm, NewUserForm, add_bonuse, add_sanction
from .models import Salary, Bonuse, Sanctions, Sanction
from django.contrib.auth import login
from django.contrib import messages
from .get_salary import calc_salary, nnm_salary, get_bonuse_summ, get_sanctions_summ, get_summ_paid_salary, most_popular_summ_of_bonuse, most_popular_reason_of_sanctions, get_summ_nopaid_salary

class Popular:
    Place = 0
    Name = "Undefined"
    Count = 0
    Summ = 0

def index(request):
    if request.user.is_authenticated:      
        return HttpResponseRedirect('/salary')
    else:
        return render(request, 'demo.html')

def salary(request):
    if request.user.is_authenticated:
        salary = Salary.objects.all()
        paidSalarySumm = get_summ_paid_salary()
        nopaidSalarySumm = get_summ_nopaid_salary()
        bonuseSumm = get_bonuse_summ()
        sanctionSumm = get_sanctions_summ()
        PopSanction = most_popular_reason_of_sanctions()
        count = 1
        popularSanction = []
        for popSanct in PopSanction:
            popularSanct = []
            popularSanct.append(popSanct[0])
            popularSanct.append(popSanct[1])
            popularSanct.append(count)
            popularSanction.append(popularSanct)
            count += 1
        count = 1
        popularBonuse = []
        for popBonuse in most_popular_summ_of_bonuse():
            popularBon = []
            popularBon.append(popBonuse[0])
            popularBon.append(popBonuse[1])
            popularBon.append(count)
            popularBonuse.append(popularBon)
            count += 1
        return render(request, "content.html", {"salarys": salary,
                                                "salarySumm":paidSalarySumm,
                                                "bonuseSumm":bonuseSumm,
                                                "sanctionSumm":sanctionSumm,
                                                "nopaidSalarySumm":nopaidSalarySumm[0],
                                                "nopaidSalaryCount":nopaidSalarySumm[1],
                                                "popularSanction":popularSanction,
                                                "popularBonuse":popularBonuse,
                                                })
    else:
        return HttpResponseRedirect('/')
    
def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("/salary")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="register.html", context={"form":form})

@login_required
@permission_required('main.change_salary')
def salary_edit(request, id):
      try:
            salary = Salary.objects.get(id = id)
            if request.method == "POST":
                if salary.paid == False:
                    if request.POST.get("bool") == "on":
                        salary.paid = True
                    salary.summ = calc_salary(id)
                    salary.save()
                    return HttpResponseRedirect("#")
                else:
                    path = "/salary"
                    return HttpResponse(f"<h2>Данная зарплата уже выплачена и изменению не подлежит</h2> <a href=\"{path}\">Вернуться</a>")
                
            else:
                bonuses = salary.bonuse_set.all()
                sanctions = salary.sanctions_set.all()
                summ = calc_salary(id)
                bonuses_len = len(bonuses)
                bonuses_summ = 0
                for bonuse in bonuses:
                     bonuses_summ += bonuse.summ
                sanctions_len = len(sanctions)
                sanctions_summ = 0
                for sanction in sanctions:
                     sanctions_summ += sanction.sanction.summ
                return render(request, "edit.html", {"salary":salary, 
                                                     "summ":summ, 
                                                     "bonuses": bonuses, 
                                                     "sanctions":sanctions, 
                                                     "sanctions_len":sanctions_len,
                                                     "sanctions_summ":sanctions_summ,
                                                     "bonuses_len":bonuses_len,
                                                     "bonuses_summ":bonuses_summ,              
                                                     })
      except Salary.DoesNotExist:
            return HttpResponseNotFound("<h2>Salary not found</h2>")

@login_required
@permission_required('main.delete_salary')
def salary_delete(request, id):
    try: 
        salary = Salary.objects.get(id = id)
        salary.delete()
        return HttpResponseRedirect("/salary")
    except Salary.DoesNotExist:
        return HttpResponseNotFound("<h2>Salary not found</h2>")
    
@login_required
@permission_required('main.delete_salary')
def add_bonuse(request, id):
    try:
        salary = Salary.objects.get(id = id)
        if request.method == "POST":  
            if salary.paid == False: 
                bonuse = Bonuse()
                bonuse.salary = salary
                bonuse.date = request.POST.get("date")
                bonuse.reason = request.POST.get("reason")
                bonuse.summ = request.POST.get("summ")
                bonuse.save()
                salary.summ = calc_salary(id)
                salary.save()
                return HttpResponseRedirect(f"/salary/edit/{id}")
            else:
                path = "/salary"
                return HttpResponse(f"<h2>Данная зарплата уже выплачена и изменению не подлежит</h2> <a href=\"{path}\">Вернуться</a>")
        return render(request, "add_bonuse.html", context={"bonuse":Bonuse()})
    except Salary.DoesNotExist:
        return HttpResponseRedirect("/salary")

@login_required
@permission_required('main.delete_salary')
def add_sanction(request, id):
    try:
        salary = Salary.objects.get(id = id)
        if request.method == "POST":
            if salary.paid == False:
                sanctions = Sanctions()
                sanctions.salary  =  salary
                sanctions.sanction = Sanction.objects.get(id=request.POST.get("sanction"))
                sanctions.date = request.POST.get("date")
                sanctions.save()
                salary.summ = calc_salary(id)
                salary.save()
                return HttpResponseRedirect(f"/salary/edit/{id}")
            else:
                path = "/salary"
                return HttpResponse(f"<h2>Данная зарплата уже выплачена и изменению не подлежит</h2> <a href=\"{path}\">Вернуться</a>")
        return render(request, "add_sanction.html", context={"sanctions":Sanction.objects.all()})
    except Salary.DoesNotExist:
        return HttpResponseRedirect("/salary")
    
@login_required
@permission_required('main.change_sanction')
def sanction(request):
    sanctions = Sanction.objects.all()
    if request.method == "POST":
        sanction = Sanction()
        sanction.reason = request.POST.get("reason")
        sanction.summ = request.POST.get("summ")
        sanction.save()
    return render(request,  "sanctions.html", context={"sanctions":sanctions})

@login_required
@permission_required('main.change_sanction')
def cahnge_sanction(request, id):
    try:
          sanction = Sanction.objects.get(id=id)
          if request.method == "POST":
               if request.POST.get("reason") != "": sanction.reason = request.POST.get("reason")
               if request.POST.get("summ") != "":sanction.summ = request.POST.get("summ")
               sanction.save()
               return HttpResponseRedirect("/salary/sanction")
          return render(request, "edit_sanction.html", context={"sanction":sanction})
    except Sanction.DoesNotExist:
         return  HttpResponseRedirect("/salary/sanction")
    
@login_required
@permission_required('main.delete_sanctions')
def delete_sanctions(request, id, sanct_id):
    try:
          salary = Salary.objects.get(id = id)
          if salary.paid == False:
            sanction = Sanctions.objects.get(id=sanct_id)
            sanction.delete()
            salary.summ = calc_salary(id)
            salary.save()
            return HttpResponseRedirect(f"/salary/edit/{id}/")
          else:
                path = "/salary"
                return HttpResponse(f"<h2>Данная зарплата уже выплачена и изменению не подлежит</h2> <a href=\"{path}\">Вернуться</a>")  
    except Sanction.DoesNotExist:
         return  HttpResponseRedirect("/salary/edit")
    
@login_required
@permission_required('main.delete_bonuse')
def delete_bonuse(request, id, bon_id):
    try:
        salary = Salary.objects.get(id = id)
        if salary.paid == False:
            bonuse = Bonuse.objects.get(id=bon_id)
            bonuse.delete()
            salary.summ = calc_salary(id)
            salary.save()
            return HttpResponseRedirect(f"/salary/edit/{id}/")
        else:
                path = "/salary"
                return HttpResponse(f"<h2>Данная зарплата уже выплачена и изменению не подлежит</h2> <a href=\"{path}\">Вернуться</a>")
    except Sanction.DoesNotExist:
         return  HttpResponseRedirect("/salary/edit")
    
@login_required
@permission_required('main.delete_sanctions')
def delete_sanction(request, id):
    try:
          sanction = Sanction.objects.get(id=id)
          sanction.delete()
          return HttpResponseRedirect(f"/salary/sanction")
    except Sanction.DoesNotExist:
         return  HttpResponseRedirect("/salary/edit")
    
@login_required
@permission_required('main.change_sanctions')
def cahnge_sanctions(request, id, sanct_id):
    try:
          salary = Salary.objects.get(id = id)
          if salary.paid == False:
            sanction = Sanctions.objects.get(id=sanct_id)
            sanctions = Sanction.objects.all()
            if request.method == "POST":
                    if request.POST.get("date") != "": sanction.date = request.POST.get("date")
                    if request.POST.get("sanct") != "":sanction.sanction = Sanction.objects.get(id=request.POST.get("sanct")) 
                    sanction.save()
                    salary.summ = calc_salary(id)
                    salary.save()
                    return HttpResponseRedirect(f"/salary/edit/{id}")
            return render(request, "edit_sanctions.html", context={"sanction":sanction, "sanctions":sanctions})
          else:
                path = "/salary"
                return HttpResponse(f"<h2>Данная зарплата уже выплачена и изменению не подлежит</h2> <a href=\"{path}\">Вернуться</a>")
    except Sanction.DoesNotExist:
         return  HttpResponseRedirect("/salary/sanction")
    

@login_required
@permission_required('main.change_bonuse')
def cahnge_bonuse(request, id, bon_id):
    try:
          salary = Salary.objects.get(id = id)
          if salary.paid == False:
            bonuse = Bonuse.objects.get(id=bon_id)
            if request.method == "POST":
                if request.POST.get("date") != "": bonuse.date = request.POST.get("date")
                if request.POST.get("reason") != "": bonuse.reason = request.POST.get("reason")
                if request.POST.get("summ") != "":bonuse.summ = request.POST.get("summ")
                bonuse.save()
                salary.summ = calc_salary(id)
                salary.save()
                return HttpResponseRedirect(f"/salary/edit/{id}")
            return render(request, "edit_bonuse.html", context={"bonuse":bonuse})
          else:
                path = "/salary"
                return HttpResponse(f"<h2>Данная зарплата уже выплачена и изменению не подлежит</h2> <a href=\"{path}\">Вернуться</a>")
    except Sanction.DoesNotExist:
         return  HttpResponseRedirect("/salary/sanction")
    
@login_required    
def edit_account(request):
    if request.method == "POST":
        try:
            if request.POST.get("first_name") != "": request.user.first_name = request.POST.get("first_name")
            if request.POST.get("last_name") != "":request.user.last_name = request.POST.get("last_name")
            if request.POST.get("username") != "":request.user.username = request.POST.get("username")
            if request.POST.get("email") != "":request.user.email = request.POST.get("email")
            request.user.save()
            return HttpResponseRedirect("/salary")
        except IntegrityError:
            print(IntegrityError)
            path = "/salary"
            return  HttpResponse(f"Данное имя пользователя уже существует <a href=\"{path}\">Вернуться</a>")
        except: HttpResponse("Непредвиденная ошибка")
             
    else:
        return render(request, "edit_account.html")
    
@login_required
@permission_required("main.add_salary")
def new_salarys(request):
    nnm_salary()
    return HttpResponseRedirect("/salary")

@login_required
@permission_required("auth.change_user")
def editrate(request, id):
    try:
        account = Salary.objects.get(id = id).account
        if request.method ==  "POST":
           if request.POST.get("rate") != "": account.rate = request.POST.get("rate")
           account.save()
           return  HttpResponseRedirect("/")
        return render(request, "editrate.html",{"account":account})
    except Salary.DoesNotExist:
        return  HttpResponseRedirect("/salary/edit")