from django.db import models
# from django.contrib.auth.models import User



LANGUOID_LEVEL_CHOICES = (('family', 'Family'),
                          ('language', 'Language'),
                          ('dialect', 'Dialect'))

PERFORMANCE_TYPE = (('individual', 'Individual'),
                    ('group', 'Group'),
                    ('both', 'Individual and group'))

PERFORMANCE_STATUS = (('in_progress', 'In progress'),
                      ('pending', 'Pending'),
                      ('approved', 'Approved'),
                      ('disqualified', 'Disqualified'))

GRADE_RANGES = (('pk_2', 'PreK-2nd'),
                ('3-5', '3rd-5th'),
                ('6-8', '6th-8th'),
                ('9-12', '9th-12th'))

class Fair(models.Model):
    name = models.CharField(max_length=255)
    notes = models.CharField(max_length=255, blank=True)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=255)
    class Meta:
        ordering = ['name']
    def __str__(self):
        return self.name

class CurrentFair(models.Model):
    name = models.CharField(max_length=255)
    fair = models.ForeignKey('Fair', related_name='the_current_fair', on_delete=models.CASCADE)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=255)
    class Meta:
        ordering = ['name']
    def __str__(self):
        return self.name

class Languoid(models.Model):
    glottocode = models.CharField(max_length=25)
    isocode = models.CharField(max_length=50)
    name = models.CharField(max_length=255, blank=True)
    level = models.CharField(max_length=8, choices=LANGUOID_LEVEL_CHOICES, default="language")
    active = models.BooleanField(default=True)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=255)
    class Meta:
        ordering = ['name']
    def __str__(self):
        return self.name

class Instructor(models.Model):
    lastname = models.CharField(max_length=255)
    firstname = models.CharField(max_length=255)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=255)
    class Meta:
        ordering = ['lastname', 'firstname']
    def __str__(self):
        return self.lastname + self.firstname

class Student(models.Model):
    lastname = models.CharField(max_length=255)
    firstname = models.CharField(max_length=255)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=255)
    class Meta:
        ordering = ['lastname', 'firstname']
    def __str__(self):
        return self.lastname + self.firstname

class Category(models.Model):
    fair = models.ForeignKey('Fair', related_name='fair_categories', on_delete=models.CASCADE)
    name = models.CharField(max_length=500)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=255)
    class Meta:
        ordering = ['-fair', 'name']
    def __str__(self):
        return self.name

class Accessory(models.Model):
    fair = models.ForeignKey('Fair', related_name='fair_accessories', on_delete=models.CASCADE)
    name = models.CharField(max_length=500)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=255)
    class Meta:
        ordering = ['-fair', 'name']
    def __str__(self):
        return "(" + self.fair.name + ") " + self.name

class Performance(models.Model):
    fair = models.ForeignKey('Fair', related_name='fair_performances', on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', related_name='performance_user', null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=500)
    group = models.CharField(max_length=255) #pull automatically from user
    languoid = models.ForeignKey(Languoid, verbose_name="list of languoids", related_name='performance_languoid', null=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, verbose_name="categories on performance", related_name='performance_category', null=True, on_delete=models.SET_NULL)
    grade_range = models.CharField(max_length=4, choices=GRADE_RANGES, blank=True)
    performance_type = models.CharField(max_length=10, choices=PERFORMANCE_TYPE, blank=True)
    # instructors
    # students
    accessory = models.ManyToManyField(Accessory, verbose_name="accessories on performance", related_name='performance_accessory', blank=True)
    # comments
    submitted = models.BooleanField(default=False)
    status = models.CharField(max_length=12, choices=PERFORMANCE_STATUS, default="in_progress")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=255)
    class Meta:
        ordering = ['-fair', 'title']
    def __str__(self):
        return "(" + self.fair.name + ") " + self.title

class Prize(models.Model):
    fair = models.ForeignKey('Fair', related_name='fair_prizes', on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, verbose_name="categories on prize", related_name='prize_categories', blank=True)
    # grade
    performance_type = models.CharField(max_length=10, choices=PERFORMANCE_TYPE, blank=True)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=255)
    class Meta:
        ordering = ['-fair', 'id']
    def __str__(self):
        return "(" + self.fair.name + ") " + self.id
