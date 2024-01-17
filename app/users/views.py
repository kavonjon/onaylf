from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import User
from performances.models import CurrentFair
from .forms import UserProfileForm

class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    # success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

    def get_success_url(self):
        return '/accounts/profile/edit/'

@login_required
def user_account_detail(request):

    currentUser = User.objects.get(pk=request.user.pk)

    currentFair = CurrentFair.objects.first()

    template = 'registration/user_account_detail.html'
    context = {
        'currentUser': currentUser,
        'currentFair': currentFair.name,
    }
    return render(request, template, context)

@login_required
def user_account_edit(request):

    currentFair = CurrentFair.objects.first()

    currentUser = User.objects.get(pk=request.user.pk)

    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=currentUser)
        if form.is_valid():
            form.save()
            return redirect("../")
    else:
        form = UserProfileForm(instance=currentUser)

    template = 'registration/user_account_edit.html'
    context = {
        'currentFair': currentFair.name,
        'form': form
    }
    return render(request, template, context)