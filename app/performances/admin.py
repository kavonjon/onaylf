from django.contrib import admin
from performances.models import Fair, CurrentFair, Languoid, Tribe, Instructor, Student, Category, Accessory, Performance, PerformanceAccessory

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('fair', 'name')  # Define fields to display in admin
admin.site.register(Category, CategoryAdmin)

class PerformanceAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Performance._meta.fields]

    def get_readonly_fields(self, request, obj=None):
        return [field.name for field in Performance._meta.fields if field.auto_now or field.auto_now_add]

admin.site.register(Performance, PerformanceAdmin)

admin.site.register(Fair)
admin.site.register(CurrentFair)
admin.site.register(Languoid)
admin.site.register(Tribe)
admin.site.register(Instructor)
admin.site.register(Student)
admin.site.register(Accessory)

admin.site.register(PerformanceAccessory)
