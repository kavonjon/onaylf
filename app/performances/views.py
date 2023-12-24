from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import FormView, DeleteView
from rest_framework import generics, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import AllowAny #!!!!!!!!!!!!!!!!!
from .models import Fair, CurrentFair, Performance, Category, Instructor, Student
from .serializers import CategorySerializer, PerformanceSerializer, InstructorSerializer, StudentSerializer
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

    performance = Performance.objects.get(pk=pk)

    template = 'performance_detail.html'
    context = {
        'currentFair': currentFair.name,
        'performance': performance
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
            print(form)
            currentFair = CurrentFair.objects.first()
            self.object = form.save(commit=False)
            self.object.fair = currentFair.fair
            self.object.user = self.request.user
            self.object.modified_by = self.request.user.get_username()
            self.object.save()
            form.save_m2m()
            print(self.object.languoid)
            print(self.object.category)
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
