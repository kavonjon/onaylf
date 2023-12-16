from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from users.models import User

# # Define an inline admin descriptor for Employee model
# # which acts a bit like a singleton
# class FairUserInline(admin.StackedInline):
#     model = FairUser
#     can_delete = False
#     verbose_name_plural = "fairUser"


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'organization', 'is_staff')
    ordering = ('email',)
    # inlines = [FairUserInline]

# Re-register UserAdmin
# admin.site.unregister(User)
admin.site.register(User, UserAdmin)
