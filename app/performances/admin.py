from django.contrib import admin
from performances.models import Fair, CurrentFair, Languoid, Tribe, Instructor, Student, Category, Accessory, Performance, PerformanceAccessory

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('fair', 'name')  # Define fields to display in admin

admin.site.register(Category, CategoryAdmin)


admin.site.register(Fair)
admin.site.register(CurrentFair)
admin.site.register(Languoid)
admin.site.register(Tribe)
admin.site.register(Instructor)
admin.site.register(Student)
admin.site.register(Accessory)
admin.site.register(Performance)
admin.site.register(PerformanceAccessory)
