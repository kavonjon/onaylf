from django.db import models
from django.contrib.auth import get_user_model

def get_superuser():
    User = get_user_model()
    superuser = User.objects.filter(is_superuser=True).first()
    if superuser:
        return superuser
    else:
        # Handle the case where there is no superuser
        # Just return the first user, probably an admin
        return User.objects.first()


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

PERFORMANCE_PART_STATUS = (('in_progress', 'In progress'),
                      ('pending', 'Pending'),
                      ('completed', 'Completed'))

GRADES = (('pk', 'PreK'),
            ('k', 'Kindergarten'),
            ('1', '1st'),
            ('2', '2nd'),
            ('3', '3rd'),
            ('4', '4th'),
            ('5', '5th'),
            ('6', '6th'),
            ('7', '7th'),
            ('8', '8th'),
            ('9', '9th'),
            ('10', '10th'),
            ('11', '11th'),
            ('12', '12th'))

GRADE_RANGES = (('pk_2', 'PreK-2nd'),
                ('3-5', '3rd-5th'),
                ('6-8', '6th-8th'),
                ('9-12', '9th-12th'))

STATE_CHOICES = (
    ('AL', 'Alabama'),
    ('AK', 'Alaska'),
    ('AZ', 'Arizona'),
    ('AR', 'Arkansas'),
    ('CA', 'California'),
    ('CO', 'Colorado'),
    ('CT', 'Connecticut'),
    ('DC', 'District of Columbia'),
    ('DE', 'Delaware'),
    ('FL', 'Florida'),
    ('GA', 'Georgia'),
    ('HI', 'Hawaii'),
    ('ID', 'Idaho'),
    ('IL', 'Illinois'),
    ('IN', 'Indiana'),
    ('IA', 'Iowa'),
    ('KS', 'Kansas'),
    ('KY', 'Kentucky'),
    ('LA', 'Louisiana'),
    ('ME', 'Maine'),
    ('MD', 'Maryland'),
    ('MA', 'Massachusetts'),
    ('MI', 'Michigan'),
    ('MN', 'Minnesota'),
    ('MS', 'Mississippi'),
    ('MO', 'Missouri'),
    ('MT', 'Montana'),
    ('NE', 'Nebraska'),
    ('NV', 'Nevada'),
    ('NH', 'New Hampshire'),
    ('NJ', 'New Jersey'),
    ('NM', 'New Mexico'),
    ('NY', 'New York'),
    ('NC', 'North Carolina'),
    ('ND', 'North Dakota'),
    ('OH', 'Ohio'),
    ('OK', 'Oklahoma'),
    ('OR', 'Oregon'),
    ('PA', 'Pennsylvania'),
    ('RI', 'Rhode Island'),
    ('SC', 'South Carolina'),
    ('SD', 'South Dakota'),
    ('TN', 'Tennessee'),
    ('TX', 'Texas'),
    ('UT', 'Utah'),
    ('VT', 'Vermont'),
    ('VA', 'Virginia'),
    ('WA', 'Washington'),
    ('WV', 'West Virginia'),
    ('WI', 'Wisconsin'),
    ('WY', 'Wyoming')
)

TSHIRT_SIZES = (
    ('ys', 'Youth Small (YS)'),
    ('ym', 'Youth Medium (YM)'),
    ('yl', 'Youth Large (YL)'),
    ('s', 'Adult Small (S)'),
    ('m', 'Adult Medium (M)'),
    ('l', 'Adult Large (L)'),
    ('xl', 'Adult Extra Large (XL)'),
    ('xxl', 'Adult Extra Extra Large (XXL)'),
    ('xxxl', 'Adult Extra Extra Extra Large (XXXL)'))

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
    # on delete set to superuser
    fair = models.ForeignKey('Fair', related_name='fair_instructors', on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', related_name='instructor_user', null=False, on_delete=models.SET(get_superuser)) # on delete set to superuser
    lastname = models.CharField(max_length=255)
    firstname = models.CharField(max_length=255)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=255)
    class Meta:
        ordering = ['lastname', 'firstname']
    def __str__(self):
        return self.lastname + ', ' + self.firstname

class Student(models.Model):
    fair = models.ForeignKey('Fair', related_name='fair_students', on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', related_name='student_user', null=False, on_delete=models.SET(get_superuser)) # on delete set to superuser
    lastname = models.CharField(max_length=255)
    firstname = models.CharField(max_length=255)
    languoids = models.ManyToManyField(Languoid, verbose_name="list of languoids", related_name='student_languoids', blank=True)
    grade = models.CharField(max_length=4, choices=GRADES, blank=True)
    hometown = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=2, choices=STATE_CHOICES, blank=True)
    tshirt_size = models.CharField(max_length=4, choices=TSHIRT_SIZES, blank=True)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=255)
    class Meta:
        ordering = ['lastname', 'firstname']
    def __str__(self):
        return self.lastname + ', ' + self.firstname

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

class PerformanceAccessory(models.Model):
    performance = models.ForeignKey('Performance', on_delete=models.CASCADE)
    accessory = models.ForeignKey('Accessory', on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0)

class Performance(models.Model):
    fair = models.ForeignKey('Fair', related_name='fair_performances', on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', related_name='performance_user', null=False, on_delete=models.SET(get_superuser)) # on delete set to superuser
    poster = models.BooleanField(default=False)
    title = models.CharField(max_length=500)
    group = models.CharField(max_length=255) #pull automatically from user
    languoids = models.ManyToManyField(Languoid, verbose_name="list of languoids", related_name='performance_languoids', blank=True)
    category = models.ForeignKey(Category, verbose_name="categories on performance", related_name='performance_category', null=True, on_delete=models.SET_NULL)
    grade_range = models.CharField(max_length=4, choices=GRADE_RANGES, blank=True)
    performance_type = models.CharField(max_length=10, choices=PERFORMANCE_TYPE, blank=True)
    instructors = models.ManyToManyField(Instructor, verbose_name="instructors on performance", related_name='performance_instructor', blank=True)
    students = models.ManyToManyField(Student, verbose_name="students on performance", related_name='performance_student', blank=True)
    accessories = models.ManyToManyField(Accessory, through='PerformanceAccessory', verbose_name="accessories on performance", related_name='performance_accessory', blank=True)
    comments = models.TextField(blank=True)
    submitted = models.BooleanField(default=False)
    status = models.CharField(max_length=12, choices=PERFORMANCE_STATUS, default="in_progress")
    instructors_status = models.CharField(max_length=12, choices=PERFORMANCE_PART_STATUS, default="pending")
    students_status = models.CharField(max_length=12, choices=PERFORMANCE_PART_STATUS, default="pending")
    accessories_status = models.CharField(max_length=12, choices=PERFORMANCE_PART_STATUS, default="pending")
    review_status = models.CharField(max_length=12, choices=PERFORMANCE_PART_STATUS, default="pending")
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
