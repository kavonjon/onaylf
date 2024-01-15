from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic.edit import FormView, DeleteView
from rest_framework import generics, viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import AllowAny #!!!!!!!!!!!!!!!!!
from users.models import User
from .models import Fair, CurrentFair, Performance, Category, Instructor, Student, Accessory, PerformanceAccessory
from .serializers import CategorySerializer, PerformanceSerializer, PosterSerializer, InstructorSerializer, StudentSerializer, PerformanceAccessorySerializer
from .forms import PerformanceForm, PerformanceCommentsForm, InstructorForm, StudentForm, PosterForm

def custom_500_view(request):
    return render(request, "500.html", status=500)

@api_view(['GET'])
def performance_list(request):
    performances = Performance.objects.filter(poster=False)
    user_id = request.GET.get('user_id')
    if user_id is not None:
        user = get_object_or_404(User, pk=user_id)
        performances = performances.filter(user=user)
    serializer = PerformanceSerializer(performances, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def poster_list(request):
    performances = Performance.objects.filter(poster=True)
    serializer = PosterSerializer(performances, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def performance_poster_list(request):
    performances = Performance.objects.all()
    user_id = request.GET.get('user_id')
    if user_id is not None:
        user = User.objects.get(pk=user_id)
        performances = performances.filter(user=user)
    serializer = PerformanceSerializer(performances, many=True)
    return Response(serializer.data)

class CategoryUpdateView(LoginRequiredMixin, generics.UpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]  # Example: Allow any user to update tasks !!!!!!!!!!!!!!!


class InstructorViewSet(LoginRequiredMixin, viewsets.ModelViewSet):
    serializer_class = InstructorSerializer

    def get_queryset(self):
        queryset = Instructor.objects.all()
        user_id = self.request.query_params.get('user_id', None)
        performance_id = self.request.query_params.get('performance_id', None)
        if user_id is not None:
            queryset = queryset.filter(user__id=user_id)
        if performance_id is not None:
            queryset = queryset.filter(performance_instructor__id=performance_id)
        return queryset

class StudentViewSet(LoginRequiredMixin, viewsets.ModelViewSet):
    serializer_class = StudentSerializer

    def get_queryset(self):
        queryset = Student.objects.all()
        user_id = self.request.query_params.get('user_id', None)
        performance_id = self.request.query_params.get('performance_id', None)
        if user_id is not None:
            queryset = queryset.filter(user__id=user_id)
        if performance_id is not None:
            queryset = queryset.filter(performance_student__id=performance_id)
        return queryset

class PerformanceUpdateView(LoginRequiredMixin, generics.UpdateAPIView):
    queryset = Performance.objects.all()
    serializer_class = PerformanceSerializer

class PerformanceAccessoryCreateView(LoginRequiredMixin, generics.CreateAPIView):
    queryset = PerformanceAccessory.objects.all()
    serializer_class = PerformanceAccessorySerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

class PerformanceAccessoryUpdateView(LoginRequiredMixin, generics.UpdateAPIView):
    queryset = PerformanceAccessory.objects.all()
    serializer_class = PerformanceAccessorySerializer

    def get_object(self):
        performance_id = self.kwargs.get('perf_pk')
        accessory_id = self.kwargs.get('acc_pk')
        return get_object_or_404(PerformanceAccessory, performance=performance_id, accessory=accessory_id)

@login_required
def select_fair(request, pk=None):

    currentFair = CurrentFair.objects.first()

    if pk:
        get_fair_to_update = Fair.objects.get(id=pk)
        if get_fair_to_update:
            currentFair.fair = get_fair_to_update
            currentFair.name = get_fair_to_update.name
            currentFair.save()

    fairs = Fair.objects.values('id', 'name')
    fairs_ordered = fairs.order_by('-updated')

    recent_fairs = fairs.order_by('-updated') # this modification of fairs is currently redundant, but it would be needed if the ordering of fairs above needed to change
    if len(recent_fairs) > 3:
        recent_fairs = recent_fairs[:3]

    template = 'select_fair.html'
    context = {
        'currentFair': currentFair.name,
        'recent_fairs': recent_fairs,
        'fairs': fairs_ordered
    }
    return render(request, template, context)


class PerformanceAccessoryViewSet(LoginRequiredMixin, viewsets.ModelViewSet):
    queryset = PerformanceAccessory.objects.all()
    serializer_class = PerformanceAccessorySerializer

    def get_queryset(self):
        queryset = PerformanceAccessory.objects.all()
        performance_id = self.request.query_params.get('performance_id', None)
        accessory_id = self.request.query_params.get('accessory_id', None)

        if performance_id is not None:
            queryset = queryset.filter(performance__id=performance_id)
        if accessory_id is not None:
            queryset = queryset.filter(accessory__id=accessory_id)
        return queryset

@login_required
def edit_fair(request, pk):

    currentFair = CurrentFair.objects.first()

    fair = Fair.objects.prefetch_related("fair_categories", "fair_accessories").get(id=pk)

    print(fair.fair_categories)
    template = 'edit_fair.html'
    context = {
        'currentFair': currentFair.name,
        'fair': fair,
    }
    return render(request, template, context)

@login_required
def home(request):

    currentUserEmail = request.user.get_username()

    currentUser = User.objects.get(email=currentUserEmail)

    # Check if the user is a moderator
    is_moderator = currentUser.groups.filter(name='moderator').exists()
    print(is_moderator)

    currentFair = CurrentFair.objects.first()

    performances = Performance.objects.prefetch_related("user", "category").filter(fair=currentFair.fair)

    if not is_moderator:
        print("this is working")
        print(performances)
        performances = performances.filter(user=currentUser)
        print(performances)

    template = 'home.html'
    context = {
        'currentUser': currentUser,
        'moderator': is_moderator,
        'currentFair': currentFair.name,
        'performances': performances
    }
    return render(request, template, context)

@login_required
def user_detail(request, user_pk):

    currentUser = User.objects.get(pk=user_pk)

    currentFair = CurrentFair.objects.first()

    allPerformances = Performance.objects.prefetch_related("user", "students").filter(fair=currentFair.fair).filter(user=currentUser.pk)

    performances = allPerformances.filter(poster=False)

    posters = allPerformances.filter(poster=True)

    template = 'user_detail.html'
    context = {
        'currentUser': currentUser,
        'currentFair': currentFair.name,
        'performances': performances,
        'posters': posters
    }
    return render(request, template, context)

@login_required
def performance_detail(request, perf_pk):

    currentFair = CurrentFair.objects.first()

    performance = Performance.objects.prefetch_related("instructors", "students", "accessories").get(pk=perf_pk)

    performance_user_organization = performance.user.organization

    # Fetch the PerformanceAccessory instances related to the current performance
    performance_accessories = PerformanceAccessory.objects.filter(performance=performance)

    # Create a dictionary mapping accessory IDs to counts
    accessory_counts = {pa.accessory.id: pa.count for pa in performance_accessories}

    # Fetch the accessories
    accessories = Accessory.objects.filter(fair=currentFair.fair)

    # Update the count attribute of each accessory with the count from the performance_accessories
    for accessory in accessories:
        if accessory.id in accessory_counts:
            accessory.count = accessory_counts[accessory.id]



    template = 'performance_detail.html'
    context = {
        'currentFair': currentFair.name,
        'performance': performance,
        'organization': performance_user_organization,
        'accessories': accessories

    }
    return render(request, template, context)

class performance_add(FormView):
    def handle_no_permission(self):
        return redirect('/no-permission')
    form_class = PerformanceForm
    template_name = "add.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['add_type'] = 'Performance'
        if 'user_pk' in self.kwargs:
            user_pk = self.kwargs['user_pk']  # Access the pk value
            user = User.objects.get(pk=user_pk)  # Get the user object
            context['owning_user'] = user
        return context
    def form_valid(self, form):
        if form.is_valid():
            currentFair = CurrentFair.objects.first()
            self.object = form.save(commit=False)
            self.object.fair = currentFair.fair
            if 'user_pk' in self.kwargs:
                user_pk = self.kwargs['user_pk']  # Access the pk value
                user = User.objects.get(pk=user_pk)  # Get the user object
                self.object.user = user
            else:
                self.object.user = self.request.user
            self.object.modified_by = self.request.user.get_username()
            self.object.save()
            form.save_m2m()
            return redirect("/performance/%s/instructors" % self.object.pk)
    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

class performance_add_admin(UserPassesTestMixin, performance_add):
    def test_func(self):
        return self.request.user.groups.filter(name='moderator').exists()
    
@login_required
def performance_instructors(request, perf_pk):

    currentFair = CurrentFair.objects.first()

    performance = Performance.objects.get(pk=perf_pk)

    if performance.instructors_status != "in_progress":
        performance.instructors_status = "in_progress"
        performance.save()

    template = 'performance_instructors.html'
    context = {
        'currentFair': currentFair.name,
        'performance': performance
    }
    return render(request, template, context)

class instructor_add(LoginRequiredMixin, FormView):
    def handle_no_permission(self):
        return redirect('/no-permission')
    form_class = InstructorForm
    template_name = "instructor_add.html"
    def form_valid(self, form):
        if form.is_valid():
            currentFair = CurrentFair.objects.first()
            self.object = form.save(commit=False)
            self.object.fair = currentFair.fair
            if 'perf_pk' in self.kwargs:
                performance_id = self.kwargs['perf_pk']  # Access the pk value
                performance = Performance.objects.get(id=performance_id)
                self.object.user = performance.user
            else:
                self.object.user = self.request.user
            self.object.modified_by = self.request.user.get_username()
            self.object.save()
            # Determine the redirect URL based on the request path
            if 'performance/' in self.request.path:
                # return redirect(reverse('performance:performance_instructors_add', kwargs={'perf_pk': self.kwargs['perf_pk']}))
                return redirect("../")
            else:
                return redirect("../../")
    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

@login_required    
def instructor_edit(request, instr_pk, perf_pk=None):

    currentFair = CurrentFair.objects.first()

    instructor = get_object_or_404(Instructor, id=instr_pk)

    if request.method == "POST":
        form = InstructorForm(request.POST, instance=instructor)
        if form.is_valid():
            form.save(commit=False)
            form.modified_by = request.user.get_username()
            form.save()
            if perf_pk:
                return redirect("../../")
            else:
                return redirect("../../../")
    else:
        form = InstructorForm(instance=instructor)

    template = 'instructor_edit.html'
    context = {
        'currentFair': currentFair.name,
        'form': form
    }
    return render(request, template, context)

@login_required
def performance_students(request, perf_pk):

    currentFair = CurrentFair.objects.first()

    performance = Performance.objects.get(pk=perf_pk)

    if performance.students_status != "in_progress":
        performance.students_status = "in_progress"
        performance.save()

    template = 'performance_students.html'
    context = {
        'currentFair': currentFair.name,
        'performance': performance
    }
    return render(request, template, context)

class student_add(LoginRequiredMixin, FormView):
    def handle_no_permission(self):
        return redirect('/no-permission')
    form_class = StudentForm
    template_name = "student_add.html"
    def form_valid(self, form):
        if form.is_valid():
            currentFair = CurrentFair.objects.first()
            self.object = form.save(commit=False)
            self.object.fair = currentFair.fair
            if 'perf_pk' in self.kwargs:
                performance_id = self.kwargs['perf_pk']  # Access the pk value
                performance = Performance.objects.get(id=performance_id)
                self.object.user = performance.user
            else:
                self.object.user = self.request.user
            self.object.modified_by = self.request.user.get_username()
            self.object.save()
            # Determine the redirect URL based on the request path
            if 'performance/' in self.request.path:
                # return redirect(reverse('performance:performance_students_add', kwargs={'perf_pk': self.kwargs['perf_pk']}))
                return redirect("../")
            else:
                return redirect("../../")

            return redirect("../")
    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

@login_required
def student_edit(request, stud_pk, perf_pk=None):

    currentFair = CurrentFair.objects.first()

    student = get_object_or_404(Student, id=stud_pk)

    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save(commit=False)
            form.modified_by = request.user.get_username()
            form.save()
            return redirect("../../")
    else:
        form = StudentForm(instance=student)

    template = 'student_edit.html'
    context = {
        'currentFair': currentFair.name,
        'form': form
    }
    return render(request, template, context)

@login_required
def performance_accessories(request, perf_pk):

    currentFair = CurrentFair.objects.first()

    performance = Performance.objects.get(pk=perf_pk)

    if performance.accessories_status != "in_progress":
        performance.accessories_status = "in_progress"
        performance.save()

    # Fetch the PerformanceAccessory instances related to the current performance
    performance_accessories = PerformanceAccessory.objects.filter(performance=performance)

    # Create a dictionary mapping accessory IDs to counts
    accessory_counts = {pa.accessory.id: pa.count for pa in performance_accessories}

    # Fetch the accessories
    accessories = Accessory.objects.filter(fair=currentFair.fair)

    # Update the count attribute of each accessory with the count from the performance_accessories
    for accessory in accessories:
        if accessory.id in accessory_counts:
            accessory.count = accessory_counts[accessory.id]

    template = 'performance_accessories.html'
    context = {
        'currentFair': currentFair.name,
        'performance': performance,
        'accessories': accessories
    }
    return render(request, template, context)

@login_required
def performance_edit(request, perf_pk):
    performance = get_object_or_404(Performance, id=perf_pk)
    if request.method == "POST":
        form = PerformanceForm(request.POST, instance=performance)
        if form.is_valid():
            form.save(commit=False)
            form.modified_by = request.user.get_username()
            form.save()
            return redirect("/performance/%s/instructors/" % performance.pk)
    else:
        form = PerformanceForm(instance=performance)
    return render(request, 'performance_edit.html', {'form': form})

@login_required
def performance_review(request, perf_pk):

    currentFair = CurrentFair.objects.first()

    performance = Performance.objects.prefetch_related("instructors", "students", "accessories").get(pk=perf_pk)

    if performance.review_status != "in_progress":
        performance.review_status = "in_progress"
        performance.save()

    performance_user_organization = performance.user.organization

    # Fetch the PerformanceAccessory instances related to the current performance
    performance_accessories = PerformanceAccessory.objects.filter(performance=performance)

    # Create a dictionary mapping accessory IDs to counts
    accessory_counts = {pa.accessory.id: pa.count for pa in performance_accessories}

    # Fetch the accessories
    accessories = Accessory.objects.filter(fair=currentFair.fair)

    # Update the count attribute of each accessory with the count from the performance_accessories
    for accessory in accessories:
        if accessory.id in accessory_counts:
            accessory.count = accessory_counts[accessory.id]

    if request.method == "POST":
        form = PerformanceCommentsForm(request.POST, instance=performance)
        if form.is_valid():
            print("valid penis")
            performance_form = form.save(commit=False)
            performance_form.review_status = "completed"
            if ( performance_form.instructors_status == "completed" and 
                performance_form.students_status == "completed" and 
                performance_form.accessories_status == "completed" and
                performance_form.review_status == "completed" ):
                performance_form.status = "in_progress"
            performance_form.modified_by = request.user.get_username()
            performance_form.save()
            return redirect("/")
    else:
        form = PerformanceCommentsForm(instance=performance)

    template = 'performance_review.html'
    context = {
        'currentFair': currentFair.name,
        'performance': performance,
        'organization': performance_user_organization,
        'accessories': accessories,
        'form': form
    }
    return render(request, template, context)

class poster_add(LoginRequiredMixin, FormView):
    def handle_no_permission(self):
        return redirect('/no-permission')
    form_class = PosterForm
    template_name = "poster_add.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'user_pk' in self.kwargs:
            user_pk = self.kwargs['user_pk']  # Access the pk value
            user = User.objects.get(pk=user_pk)  # Get the user object
        else:
            user = self.request.user
        context['owning_user'] = user
        return context
    def form_valid(self, form):
        if form.is_valid():
            if 'user_pk' in self.kwargs:
                user_pk = self.kwargs['user_pk']  # Access the pk value
                user = User.objects.get(pk=user_pk)  # Get the user object
            else:
                user = self.request.user
            currentFair = CurrentFair.objects.first()
            self.object = form.save(commit=False)
            self.object.fair = currentFair.fair
            self.object.poster = True
            self.object.user = user
            self.object.modified_by = self.request.user.get_username()
            self.object.save()
            self.object.title = "Poster " + str(self.object.pk)  # Set the name here
            self.object.save()  # Save the object again to store the new name
            form.save_m2m()
            return redirect("../../")
    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)


class poster_add_admin(UserPassesTestMixin, poster_add):
    def test_func(self):
        return self.request.user.groups.filter(name='moderator').exists()

@login_required
def poster_detail(request, post_pk):

    currentFair = CurrentFair.objects.first()

    performance = Performance.objects.prefetch_related("instructors", "students").get(pk=post_pk)

    performance_user_organization = performance.user.organization

    template = 'poster_detail.html'
    context = {
        'currentFair': currentFair.name,
        'performance': performance,
        'organization': performance_user_organization

    }
    return render(request, template, context)


@login_required
def poster_edit(request, post_pk):
    currentFair = CurrentFair.objects.first()

    performance = Performance.objects.prefetch_related("instructors", "students", "accessories").get(pk=post_pk)

    performance_user_organization = performance.user.organization

    if request.method == "POST":
        form = PosterForm(request.POST, instance=performance)
        if form.is_valid():
            form.save(commit=False)
            form.modified_by = request.user.get_username()
            form.save()
            return redirect("../")
    else:
        form = PerformanceForm(instance=performance)

    template = 'poster_edit.html'
    context = {
        'currentFair': currentFair.name,
        'performance': performance,
        'organization': performance_user_organization,
        'form': form
    }
    return render(request, template, context)