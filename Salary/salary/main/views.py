from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group
from .forms import UserForm, NewUserForm, add_bonuse, add_sanction
from .models import Salary, Bonuse, Sanctions, Sanction
from django.contrib.auth import login
from django.contrib import messages
from .get_salary import calc_salary

def index(request):
    if request.user.is_authenticated:
        return render(request, "index.html", {'title':"index"})
    else:
        return render(request, 'demo.html')

def salary(request):
    if request.user.is_authenticated:
        salary = Salary.objects.all()
        return render(request, "content.html", {"salarys": salary})
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
@permission_required('change_salary')
def salary_edit(request, id):
      try:
            salary = Salary.objects.get(id = id)

            if request.method == "POST":
                salary.summ = calc_salary(id)
                salary.save()
                return HttpResponseRedirect("#")
                
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
                                                     "bonuses_summ":bonuses_summ, })
      except Salary.DoesNotExist:
            return HttpResponseNotFound("<h2>Salary not found</h2>")

@login_required
@permission_required('delete_salary')
def salary_delete(request, id):
    try: 
        salary = Salary.objects.get(id = id)
        salary.delete()
        return HttpResponseRedirect("/salary")
    except Salary.DoesNotExist:
        return HttpResponseNotFound("<h2>Salary not found</h2>")
    
@login_required
@permission_required('delete_salary')
def add_bonuse(request, id):
    try:
        salary = Salary.objects.get(id = id)
        if request.method == "POST":   
            bonuse = Bonuse()
            bonuse.salary = salary
            bonuse.date = request.POST.get("date")
            bonuse.reason = request.POST.get("reason")
            bonuse.summ = request.POST.get("summ")
            bonuse.save()
            return HttpResponseRedirect(f"/salary/edit/{id}")
        return render(request, "add_bonuse.html", context={"bonuse":Bonuse()})
    except Salary.DoesNotExist:
        return HttpResponseRedirect("/salary")

@login_required
@permission_required('delete_salary')
def add_sanction(request, id):
    try:
        salary = Salary.objects.get(id = id)
        if request.method == "POST":
            sanctions = Sanctions()
            sanctions.salary  =  salary
            sanctions.sanction = Sanction.objects.get(id=request.POST.get("sanction"))
            sanctions.date = request.POST.get("date")
            sanctions.save()
            return HttpResponseRedirect(f"/salary/edit/{id}")
        return render(request, "add_sanction.html", context={"sanctions":Sanction.objects.all()})
    except Salary.DoesNotExist:
        return HttpResponseRedirect("/salary")