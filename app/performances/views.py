from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic.edit import FormView, DeleteView
from rest_framework import generics, viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import AllowAny #!!!!!!!!!!!!!!!!!
from .models import Fair, CurrentFair, Performance, Category, Instructor, Student, Accessory, PerformanceAccessory
from .serializers import CategorySerializer, PerformanceSerializer, InstructorSerializer, StudentSerializer, PerformanceAccessorySerializer
from .forms import PerformanceForm, InstructorForm, StudentForm


def is_member_of_moderators(user):
    return user.groups.filter(name="Moderator").exists()

@api_view(['GET'])
def performance_list(request):
    performances = Performance.objects.all()
    serializer = PerformanceSerializer(performances, many=True)
    return Response(serializer.data)

class CategoryUpdateView(generics.UpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]  # Example: Allow any user to update tasks !!!!!!!!!!!!!!!


class InstructorViewSet(viewsets.ModelViewSet):
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

class StudentViewSet(viewsets.ModelViewSet):
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


class PerformanceAccessoryViewSet(viewsets.ModelViewSet):
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




def home(request):

    currentUser = request.user.get_username()

    currentFair = CurrentFair.objects.first()

    performances = Performance.objects.select_related("user").filter(fair=currentFair.fair)


    template = 'home.html'
    context = {
        'currentUser': currentUser,
        'currentFair': currentFair.name,
        'performances': performances
    }
    return render(request, template, context)


def performance_detail(request, pk):

    currentFair = CurrentFair.objects.first()

    performance = Performance.objects.prefetch_related("instructors", "students", "accessories").get(pk=pk)

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
        return context
    def form_valid(self, form):
        if form.is_valid():
            currentFair = CurrentFair.objects.first()
            self.object = form.save(commit=False)
            self.object.fair = currentFair.fair
            self.object.user = self.request.user
            self.object.modified_by = self.request.user.get_username()
            self.object.save()
            form.save_m2m()
            return redirect("../%s/" % self.object.pk)
    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

def performance_instructors(request, pk):

    currentFair = CurrentFair.objects.first()

    performance = Performance.objects.get(pk=pk)

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
            self.object.user = self.request.user
            self.object.modified_by = self.request.user.get_username()
            self.object.save()
            return redirect("../")
    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)
    
def instructor_edit(request, perf_pk, instr_pk):

    currentFair = CurrentFair.objects.first()

    instructor = get_object_or_404(Instructor, id=instr_pk)

    if request.method == "POST":
        form = InstructorForm(request.POST, instance=instructor)
        if form.is_valid():
            form.save(commit=False)
            form.modified_by = request.user.get_username()
            form.save()
            return redirect("../../")
    else:
        form = InstructorForm(instance=instructor)

    template = 'instructor_edit.html'
    context = {
        'currentFair': currentFair.name,
        'form': form
    }
    return render(request, template, context)

def performance_students(request, pk):

    currentFair = CurrentFair.objects.first()

    performance = Performance.objects.get(pk=pk)

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
            self.object.user = self.request.user
            self.object.modified_by = self.request.user.get_username()
            self.object.save()
            return redirect("../")
    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)
    
def student_edit(request, perf_pk, stud_pk):

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

def performance_accessories(request, pk):

    currentFair = CurrentFair.objects.first()

    performance = Performance.objects.get(pk=pk)

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
def performance_edit(request, pk):
    performance = get_object_or_404(Performance, id=pk)
    if request.method == "POST":
        form = PerformanceForm(request.POST, instance=performance)
        if form.is_valid():
            form.save(commit=False)
            form.modified_by = request.user.get_username()
            form.save()
            return redirect("./instructors/")
    else:
        form = PerformanceForm(instance=performance)
    return render(request, 'performance_edit.html', {'form': form})
