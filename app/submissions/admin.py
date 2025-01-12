from django.contrib import admin
from submissions.models import Fair, CurrentFair, Languoid, Tribe, Instructor, Student, Category, Accessory, Submission, SubmissionAccessory

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('fair', 'name')  # Define fields to display in admin
admin.site.register(Category, CategoryAdmin)

class SubmissionAdmin(admin.ModelAdmin):
    readonly_fields = ["added", "updated", "accessories_list"]
    
    def accessories_list(self, obj):
        accessories = SubmissionAccessory.objects.filter(submission=obj)
        return ", ".join([f"{acc.accessory} (x{acc.count})" for acc in accessories])
    accessories_list.short_description = 'Accessories'

admin.site.register(Submission, SubmissionAdmin)

admin.site.register(Fair)
admin.site.register(CurrentFair)
admin.site.register(Languoid)
admin.site.register(Tribe)
admin.site.register(Instructor)
admin.site.register(Student)
admin.site.register(Accessory)

admin.site.register(SubmissionAccessory)
