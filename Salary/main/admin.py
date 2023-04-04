from django.contrib import admin
from .models import *

admin.site.register(Sanction)
admin.site.register(Sanctions)
admin.site.register(Bonuse)

@admin.register(Salary)
class SalaryAdmin(admin.ModelAdmin):
    list_display = ("id", "account_id", "month", "year" ,"summ", "paid")
    search_fields = ("account_id__username", "account_id__id",) # Позволяет производить поиск по полям. Так же можно делать поиск
    # по полям один ко многим через объект__полеОбъекта