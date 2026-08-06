from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Student, Attendance, Marks, Fees
from .models import CustomUser

admin.site.register(Student)
admin.site.register(Attendance)
admin.site.register(Marks)
admin.site.register(Fees)
admin.site.register(CustomUser)
