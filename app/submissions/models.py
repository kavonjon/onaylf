from django.db import models
from django.db.models.functions import Lower
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

class Fair(models.Model):
    name = models.CharField(max_length=255)
    registration_open = models.BooleanField(default=False)
    notes = models.CharField(max_length=255, blank=True)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=255)
    class Meta:
        ordering = ['-added']
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

class LanguoidManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().annotate(
            is_other=models.Case(
                models.When(name='Other', then=models.Value(0)),
                default=models.Value(1),
                output_field=models.IntegerField(),
            ),
            name_lower=Lower('name')
        ).order_by('is_other', 'name_lower')

class Languoid(models.Model):
    LANGUOID_LEVEL_CHOICES = (('family', 'Family'),
                          ('language', 'Language'),
                          ('dialect', 'Dialect'))
    glottocode = models.CharField(max_length=25)
    isocode = models.CharField(max_length=50)
    name = models.CharField(max_length=255, blank=True)
    level = models.CharField(max_length=8, choices=LANGUOID_LEVEL_CHOICES, default="language")
    active = models.BooleanField(default=True)
    fair = models.ForeignKey('Fair', related_name='fair_languoids', on_delete=models.CASCADE)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=255)

    objects = LanguoidManager()

    class Meta:
        ordering = ['name']
    def __str__(self):
        return self.name

class TribeManager(models.Manager):
    def get_queryset(self):
        # First get Other, then sort rest case-insensitively
        return super().get_queryset().annotate(
            name_lower=Lower('name')
        ).order_by(
            models.Case(
                models.When(name='Other', then=models.Value(0)),
                default=models.Value(1)
            ),
            'name_lower'
        )

class Tribe(models.Model):
    name = models.CharField(max_length=255)
    fair = models.ForeignKey('Fair', related_name='fair_tribes', on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=255)
    
    objects = TribeManager()
    
    class Meta:
        ordering = ['-fair', Lower('name')]
    def __str__(self):
        return self.name

class Instructor(models.Model):
    # on delete set to superuser
    fair = models.ForeignKey('Fair', related_name='fair_instructors', on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', related_name='instructor_user', null=False, on_delete=models.CASCADE)
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
    GRADES = (('0_pk', 'PreK'),
            ('1_k', 'Kindergarten'),
            ('2_01', '1st'),
            ('2_02', '2nd'),
            ('2_03', '3rd'),
            ('2_04', '4th'),
            ('2_05', '5th'),
            ('2_06', '6th'),
            ('2_07', '7th'),
            ('2_08', '8th'),
            ('2_09', '9th'),
            ('2_10', '10th'),
            ('2_11', '11th'),
            ('2_12', '12th'))
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
    fair = models.ForeignKey('Fair', related_name='fair_students', on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', related_name='student_user', null=False, on_delete=models.CASCADE)
    lastname = models.CharField(max_length=255)
    firstname = models.CharField(max_length=255)
    tribe = models.ManyToManyField(Tribe, verbose_name="tribes of student", related_name='student_tribe', blank=True)
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
    material_submission = models.BooleanField(default=False)
    max_students = models.PositiveIntegerField(default=None, null=True, blank=True)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=255)
    class Meta:
        ordering = ['-fair', Lower('name')]
    def __str__(self):
        return self.name

class Accessory(models.Model):
    fair = models.ForeignKey('Fair', related_name='fair_accessories', on_delete=models.CASCADE)
    name = models.CharField(max_length=500)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=255)
    class Meta:
        ordering = ['-fair', Lower('name')]
    def __str__(self):
        return "(" + self.fair.name + ") " + self.name

class SubmissionAccessory(models.Model):
    submission = models.ForeignKey('Submission', on_delete=models.CASCADE)
    accessory = models.ForeignKey('Accessory', on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0)

class Submission(models.Model):
    GRADE_RANGES = (('0_pk-2', 'PreK-2nd'),
                ('1_3-5', '3rd-5th'),
                ('1_6-8', '6th-8th'),
                ('1_9-12', '9th-12th'))
    GRADE_RANGES_DICT = {
        '0_pk': '0_pk-2',
        '1_k': '0_pk-2',
        '2_01': '0_pk-2',
        '2_02': '0_pk-2',
        '2_03': '1_3-5',
        '2_04': '1_3-5',
        '2_05': '1_3-5',
        '2_06': '1_6-8',
        '2_07': '1_6-8',
        '2_08': '1_6-8',
        '2_09': '1_9-12',
        '2_10': '1_9-12',
        '2_11': '1_9-12',
        '2_12': '1_9-12'
    }
    SUBMISSION_TYPE = (('individual', 'Individual'),
                    ('group', 'Group'),
                    ('both', 'Individual and group'))
    PERFORMANCE_STATUS = (('in_progress', 'In progress'),
                        ('submitted', 'Submitted'),
                        ('approved', 'Approved'),
                        ('disqualified', 'Disqualified'))
    PERFORMANCE_PART_STATUS = (('in_progress', 'In progress'),
                        ('pending', 'Pending'),
                        ('completed', 'Completed'))
    fair = models.ForeignKey('Fair', related_name='fair_submissions', on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', related_name='submission_user', null=False, on_delete=models.SET(get_superuser)) # on delete set to superuser
    poster = models.BooleanField(default=False)
    title = models.CharField(max_length=500)
    organization = models.CharField(max_length=255, blank=True)
    group = models.CharField(max_length=255, blank=True)
    languoids = models.ManyToManyField(Languoid, verbose_name="list of languoids", related_name='submission_languoids')
    other_languoid = models.CharField(max_length=255, blank=True)
    category = models.ForeignKey(Category, verbose_name="categories on submission", related_name='submission_category', null=True, on_delete=models.SET_NULL)
    grade_range = models.CharField(max_length=6, choices=GRADE_RANGES, blank=True)
    submission_type = models.CharField(max_length=10, choices=SUBMISSION_TYPE, blank=True)
    override_submission_type = models.BooleanField(default=False)
    instructors = models.ManyToManyField(Instructor, verbose_name="instructors on submission", related_name='submission_instructor', blank=True)
    students = models.ManyToManyField(Student, verbose_name="students on submission", related_name='submission_student', blank=True)
    accessories = models.ManyToManyField(Accessory, through='SubmissionAccessory', verbose_name="accessories on submission", related_name='submission_accessory', blank=True)
    comments = models.TextField(blank=True)
    submitted_email_sent = models.BooleanField(default=False)
    approved_email_sent = models.BooleanField(default=False)
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

# for perf in perfs:
#     if perf.poster:
#         print(perf.id)
#         perf.category = poster
#         print(str(perf.id) + ": " + perf.title + " added to poster category")
#         perf.save()
        