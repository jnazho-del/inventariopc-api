from django.contrib import admin
from .models import Repuesto

# Register your models here.
class RepuestoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'categoria', 'precio', 'stock']

admin.site.register(Repuesto, RepuestoAdmin)