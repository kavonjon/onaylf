from submissions.models import Fair, CurrentFair, Languoid, Tribe, Instructor, Student, Category, Accessory, Submission, SubmissionAccessory
from users.models import User, Organization
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
import os
from dotenv import load_dotenv
from django.utils import timezone
from datetime import datetime, timedelta
load_dotenv()  # loads the configs from .env

class Command(BaseCommand):
    def handle(self, **options):

        print("build initial demo db")

        # Create a date in 2023 for admin and moderator users
        date_2023 = timezone.make_aware(datetime(2023, 3, 15))

        # # createsuperuser
        admin_user = User.objects.create_superuser(
            email='admin@exampleyouthlanguagefair.com',
            first_name='YLF',
            last_name='Administrator',
            password=str(os.getenv('ADMINS_PASSWORD')),
        )
        admin_user.confirmed = True
        admin_user.date_joined = date_2023
        admin_user.save()
        
        # create fair
        
        fair = Fair.objects.create(name="2024", modified_by="admin@exampleyouthlanguagefair.com")
        
        # create/assign current fair
        
        CurrentFair.objects.all().delete()
        current_fair = CurrentFair.objects.create(name=fair.name, fair=fair, modified_by="admin@exampleyouthlanguagefair.com")
        

        # create moderator user

        moderator_user = User.objects.create_user(
            email='moderator@exampleyouthlanguagefair.com',
            first_name='Moderator',
            last_name='Account',
            password=str(os.getenv('MODERATORS_PASSWORD')),
        )
        moderator_user.confirmed = True
        moderator_user.date_joined = date_2023 + timedelta(days=10)  # 10 days after admin user
        moderator_user.save()

        # create basic user
        
        basic_user_1 = User.objects.create_user(
            email='john@exampleyouthlanguagefair.com',
            first_name='John',
            last_name='Cash',
            password=str(os.getenv('BASIC_USER_PASSWORD')),
        )
        basic_user_1.confirmed = True
        basic_user_1.phone = '503-555-1234'
        basic_user_1.address = '123 Pine Street'
        basic_user_1.city = 'Portland'
        basic_user_1.state = 'OR'
        basic_user_1.zip = '97201'
        basic_user_1.save()

        basic_user_2 = User.objects.create_user(
            email='jane@exampleyouthlanguagefair.com',
            first_name='Jane',
            last_name='Smith',
            password=str(os.getenv('BASIC_USER_PASSWORD')),
        )
        basic_user_2.confirmed = True
        basic_user_2.phone = '512-555-8765'
        basic_user_2.alt_phone = '512-555-9876'
        basic_user_2.fax = '512-555-4321'
        basic_user_2.alt_email = 'jane.smith@sunnydalehigh.edu'
        basic_user_2.address = '456 Oak Avenue, Suite 200'
        basic_user_2.city = 'Austin'
        basic_user_2.state = 'TX'
        basic_user_2.zip = '78701'
        basic_user_2.save()

        basic_user_3 = User.objects.create_user(
            email='jim@exampleyouthlanguagefair.com',
            first_name='Jim',
            last_name='Baker',
            password=str(os.getenv('BASIC_USER_PASSWORD')),
        )
        basic_user_3.confirmed = True
        basic_user_3.phone = '312-555-3456'
        basic_user_3.alt_email = 'jbaker@highlandcharter.org'
        basic_user_3.address = '789 Maple Drive'
        basic_user_3.city = 'Chicago'
        basic_user_3.state = 'IL'
        basic_user_3.zip = '60601'
        basic_user_3.save()

        # create moderator group, assing to admin and moderator user
        
        mod_group, created = Group.objects.get_or_create(name='moderator')
        mod_group.user_set.add(moderator_user)
        mod_group.user_set.add(admin_user)



        # create organizations
        org_list = [
            "Oakridge Elementary School",
            "Pinecrest High School", 
            "Riverdale Middle School",
            "Westview Public Schools",
            "Clearwater Academy",
            "Sunnydale High School",
            "Meadowbrook Elementary",
            "Lakeside School District",
            "Highland Charter School",
            "Bridgeview Public Schools"
        ]

        created_orgs = []
        for org in org_list:
            org_obj, created = Organization.objects.get_or_create(name=org)
            created_orgs.append(org_obj)

        # Assign organizations to users
        basic_user_1.organization = "Oakridge Elementary School"
        basic_user_1.save()

        basic_user_2.organization = "Sunnydale High School"
        basic_user_2.save()

        basic_user_3.organization = "Highland Charter School"
        basic_user_3.save()

        # create languoids
        lang_list = [
            ("abcd1234", "Other", "language"),
            ("cher1273", "Cherokee", "language"),
            ("nava1243", "Diné/Navajo", "language"),
            ("lako1247", "Lakota", "language"),
            ("hopi1249", "Hopi", "language"),
            ("basq1248", "Basque", "language"),
            ("wels1247", "Welsh", "language"),
            ("tibe1272", "Tibetan", "language"),
            ("samo1305", "Samoan", "language"),
            ("hawa1245", "Hawaiian", "language"),
            ("coma1245", "Comanche", "language"),
            ("swah1253", "Swahili", "language"),
            ("malt1254", "Maltese", "language"),
            ("quec1387", "Quechua", "language"),
            ("maor1246", "Māori", "language"),
            ("chad1243", "Chad Arabic", "language"),
            ("ainu1240", "Ainu", "language"),
            ("bura1292", "Bura-Pabir", "language"),
            ("kala1399", "Kalaallisut (Greenlandic)", "language"),
            ("krio1253", "Krio", "language")
        ]
        
        for lang in lang_list:
            languoid = Languoid.objects.create(
                fair=current_fair.fair,
                glottocode=lang[0],
                name=lang[1],
                level=lang[2],
                modified_by="admin@exampleyouthlanguagefair.com"
            )


        # create tribes
        current_fair = CurrentFair.objects.first()
        tribe_list = [
            ('Other',),
            ('Altamar Cultural Society',),
            ('Meridian Heritage Group',),
            ('Sylvan Valley Community',),
            ('Azure Coast Federation',),
            ('Highland Preserve Council',),
            ('Evergreen Cultural Alliance',),
            ('Rivercrest Collective',),
            ('Stonebrook Assembly',),
            ('Willow Plains Association',)
        ]

        for tribe in tribe_list:
            tribe = Tribe.objects.create(fair=current_fair.fair, name=tribe[0], modified_by="admin@exampleyouthlanguagefair.com")


        # delete all categories
        Category.objects.all().delete()

        # create Categories
        current_fair = CurrentFair.objects.first()
        cat_list = [
            ("Books", "True"),
            ("Comics and Cartoons", "True"),
            ("Film and Video", "True"),
            ("Master Performer", "False"),
            ("Mobile Video", "True"),
            ("Modern Song", "False"),
            ("Poster", "True",2),
            ("Puppet Show", "True"),
            ("Skit/Short Play", "False"),
            ("Spoken Language", "False"),
            ("Spoken Poetry", "False"),
            ("Spoken Prayer", "False"),
            ("Traditional Song", "False")
        ]

        for cat in cat_list:
            max_students = cat[2] if len(cat) > 2 else None

            category = Category.objects.create(
                fair=current_fair.fair,
                name=cat[0],
                material_submission=cat[1],
                max_students=max_students,
                modified_by="admin@exampleyouthlanguagefair.com"
            )

        # delete all accessories
        Accessory.objects.all().delete()

        # create accessories
        current_fair = CurrentFair.objects.first()
        acc_list = [
            ("32 Inch Standard Round Tables",),
            ("32 Inch Tall Round Tables",),
            ("6 Foot Rectangle Tables",),
            ("Chairs",),
            ("Easel",)
        ]

        for acc in acc_list:
            accessory = Accessory.objects.create(fair=current_fair.fair, name=acc[0], modified_by="admin@exampleyouthlanguagefair.com")

        # create instructors
        print("Creating instructors...")
        
        instructors_data = [
            # For John Cash
            {
                'user': basic_user_1,
                'firstname': 'Maria', 
                'lastname': 'Rodriguez',
                'fair': current_fair.fair,
                'email': 'maria.r@example.com'
            },
            {
                'user': basic_user_1,
                'firstname': 'David', 
                'lastname': 'Chen',
                'fair': current_fair.fair,
                'email': 'david.chen@example.com'
            },
            # For Jane Smith
            {
                'user': basic_user_2,
                'firstname': 'Robert', 
                'lastname': 'Johnson',
                'fair': current_fair.fair,
                'email': 'r.johnson@example.com'
            },
            {
                'user': basic_user_2,
                'firstname': 'Sarah', 
                'lastname': 'Wilson',
                'fair': current_fair.fair,
                'email': 'wilson.s@example.com'
            },
            # For Jim Baker
            {
                'user': basic_user_3,
                'firstname': 'Michael', 
                'lastname': 'Davis',
                'fair': current_fair.fair,
                'email': 'michael.d@example.com'
            },
            {
                'user': basic_user_3,
                'firstname': 'Elizabeth', 
                'lastname': 'Taylor',
                'fair': current_fair.fair,
                'email': 'e.taylor@example.com'
            }
        ]
        
        instructors = {}
        for instructor_data in instructors_data:
            instructor = Instructor.objects.create(
                user=instructor_data['user'],
                lastname=instructor_data['lastname'],
                firstname=instructor_data['firstname'],
                fair=instructor_data['fair'],
                modified_by=instructor_data['user'].email
            )
            
            # Store instructors by user email and instructor name for easy reference
            key = f"{instructor_data['user'].email}_{instructor.firstname}_{instructor.lastname}"
            instructors[key] = instructor
        
        # create students
        print("Creating students...")
        
        students_data = [
            # For John Cash
            {
                'user': basic_user_1,
                'firstname': 'Sofia', 
                'lastname': 'Martinez',
                'fair': current_fair.fair,
                'grade': '2_03',  # 3rd grade
                'hometown': 'Portland',
                'state': 'OR',
                'tshirt_size': 'ym'
            },
            {
                'user': basic_user_1,
                'firstname': 'Lucas', 
                'lastname': 'Garcia',
                'fair': current_fair.fair,
                'grade': '2_04',  # 4th grade
                'hometown': 'Eugene',
                'state': 'OR',
                'tshirt_size': 'yl'
            },
            {
                'user': basic_user_1,
                'firstname': 'Olivia', 
                'lastname': 'Lee',
                'fair': current_fair.fair,
                'grade': '2_03',  # 3rd grade
                'hometown': 'Salem',
                'state': 'OR',
                'tshirt_size': 'ym'
            },
            {
                'user': basic_user_1,
                'firstname': 'Ethan', 
                'lastname': 'Kim',
                'fair': current_fair.fair,
                'grade': '2_05',  # 5th grade
                'hometown': 'Bend',
                'state': 'OR',
                'tshirt_size': 'yl'
            },
            # For Jane Smith
            {
                'user': basic_user_2,
                'firstname': 'Emma', 
                'lastname': 'Brown',
                'fair': current_fair.fair,
                'grade': '2_07',  # 7th grade
                'hometown': 'Austin',
                'state': 'TX',
                'tshirt_size': 'yl'
            },
            {
                'user': basic_user_2,
                'firstname': 'Noah', 
                'lastname': 'Davis',
                'fair': current_fair.fair,
                'grade': '2_08',  # 8th grade
                'hometown': 'San Antonio',
                'state': 'TX',
                'tshirt_size': 's'
            },
            {
                'user': basic_user_2,
                'firstname': 'Ava', 
                'lastname': 'Taylor',
                'fair': current_fair.fair,
                'grade': '2_06',  # 6th grade
                'hometown': 'Houston',
                'state': 'TX',
                'tshirt_size': 'ym'
            },
            {
                'user': basic_user_2,
                'firstname': 'Liam', 
                'lastname': 'Wilson',
                'fair': current_fair.fair,
                'grade': '2_07',  # 7th grade
                'hometown': 'Dallas',
                'state': 'TX',
                'tshirt_size': 's'
            },
            {
                'user': basic_user_2,
                'firstname': 'Isabella', 
                'lastname': 'Clark',
                'fair': current_fair.fair,
                'grade': '2_08',  # 8th grade
                'hometown': 'Fort Worth',
                'state': 'TX',
                'tshirt_size': 'm'
            },
            # For Jim Baker
            {
                'user': basic_user_3,
                'firstname': 'William', 
                'lastname': 'Walker',
                'fair': current_fair.fair,
                'grade': '2_10',  # 10th grade
                'hometown': 'Chicago',
                'state': 'IL',
                'tshirt_size': 'l'
            },
            {
                'user': basic_user_3,
                'firstname': 'Mia', 
                'lastname': 'Robinson',
                'fair': current_fair.fair,
                'grade': '2_11',  # 11th grade
                'hometown': 'Evanston',
                'state': 'IL',
                'tshirt_size': 'm'
            },
            {
                'user': basic_user_3,
                'firstname': 'James', 
                'lastname': 'Thomas',
                'fair': current_fair.fair,
                'grade': '2_09',  # 9th grade
                'hometown': 'Rockford',
                'state': 'IL',
                'tshirt_size': 'l'
            },
            {
                'user': basic_user_3,
                'firstname': 'Charlotte', 
                'lastname': 'Scott',
                'fair': current_fair.fair,
                'grade': '2_12',  # 12th grade
                'hometown': 'Naperville',
                'state': 'IL',
                'tshirt_size': 'm'
            },
            {
                'user': basic_user_3,
                'firstname': 'Benjamin', 
                'lastname': 'Green',
                'fair': current_fair.fair,
                'grade': '2_11',  # 11th grade
                'hometown': 'Aurora',
                'state': 'IL',
                'tshirt_size': 'xl'
            }
        ]
        
        students = {}
        for student_data in students_data:
            student = Student.objects.create(
                user=student_data['user'],
                lastname=student_data['lastname'],
                firstname=student_data['firstname'],
                fair=student_data['fair'],
                grade=student_data['grade'],
                hometown=student_data['hometown'],
                state=student_data['state'],
                tshirt_size=student_data['tshirt_size'],
                modified_by=student_data['user'].email
            )
            
            # Add a random tribe to each student
            tribe = Tribe.objects.filter(fair=current_fair.fair).exclude(name='Other').order_by('?').first()
            student.tribe.add(tribe)
            
            # Store students by user email and student name for easy reference
            key = f"{student_data['user'].email}_{student.firstname}_{student.lastname}"
            students[key] = student
        
        # create submissions
        print("Creating submissions...")
        
        # Get all categories
        categories = {}
        for category in Category.objects.filter(fair=current_fair.fair):
            categories[category.name] = category
        
        # Get all accessories
        accessories = {}
        for accessory in Accessory.objects.filter(fair=current_fair.fair):
            accessories[accessory.name] = accessory
        
        # Get all languoids
        languoids = list(Languoid.objects.filter(fair=current_fair.fair))
        
        # Create submissions for User 1 (John Cash)
        # Poster submission (material submission with 1 student, 1 instructor)
        poster_sub1 = Submission.objects.create(
            fair=current_fair.fair,
            user=basic_user_1,
            poster=True,
            title="Language Awareness Poster",
            organization="Oakridge Elementary School",
            group="3rd Grade Art Class",
            category=categories["Poster"],
            grade_range=Submission.GRADE_RANGES_DICT[students[f"{basic_user_1.email}_Sofia_Martinez"].grade],
            submission_type="individual",
            status="submitted",
            submitted_email_sent=True,
            modified_by=basic_user_1.email
        )
        
        # Add languoids
        poster_sub1.languoids.add(languoids[5])  # Basque
        
        # Add instructor and student
        poster_sub1.instructors.add(instructors[f"{basic_user_1.email}_Maria_Rodriguez"])
        poster_sub1.students.add(students[f"{basic_user_1.email}_Sofia_Martinez"])
        
        # Books submission (material submission with multiple students)
        books_sub1 = Submission.objects.create(
            fair=current_fair.fair,
            user=basic_user_1,
            poster=False,
            title="Our Language Journey",
            organization="Oakridge Elementary School",
            group="Reading Group A",
            category=categories["Books"],
            grade_range=Submission.GRADE_RANGES_DICT[students[f"{basic_user_1.email}_Lucas_Garcia"].grade],
            submission_type="group",
            comments="This book was created collaboratively during our language arts class.",
            status="approved",
            submitted_email_sent=True,
            approved_email_sent=True,
            modified_by=basic_user_1.email
        )
        
        # Add languoids
        books_sub1.languoids.add(languoids[7])  # Tibetan
        books_sub1.languoids.add(languoids[8])  # Samoan
        
        # Add instructor and students
        books_sub1.instructors.add(instructors[f"{basic_user_1.email}_David_Chen"])
        books_sub1.students.add(students[f"{basic_user_1.email}_Lucas_Garcia"])
        books_sub1.students.add(students[f"{basic_user_1.email}_Olivia_Lee"])
        
        # Spoken Language submission (non-material)
        spoken_sub1 = Submission.objects.create(
            fair=current_fair.fair,
            user=basic_user_1,
            poster=False,
            title="Cultural Storytelling",
            organization="Oakridge Elementary School",
            group="Language Club",
            category=categories["Spoken Language"],
            grade_range=Submission.GRADE_RANGES_DICT[students[f"{basic_user_1.email}_Ethan_Kim"].grade],
            submission_type="group",
            status="in_progress",
            modified_by=basic_user_1.email
        )
        
        # Add languoids
        spoken_sub1.languoids.add(languoids[3])  # Lakota
        
        # Add instructor and students
        spoken_sub1.instructors.add(instructors[f"{basic_user_1.email}_Maria_Rodriguez"])
        spoken_sub1.students.add(students[f"{basic_user_1.email}_Ethan_Kim"])
        spoken_sub1.students.add(students[f"{basic_user_1.email}_Sofia_Martinez"])
        spoken_sub1.students.add(students[f"{basic_user_1.email}_Olivia_Lee"])
        
        # Add accessories (since it's non-material)
        SubmissionAccessory.objects.create(
            submission=spoken_sub1,
            accessory=accessories["Chairs"],
            count=4
        )
        
        SubmissionAccessory.objects.create(
            submission=spoken_sub1,
            accessory=accessories["Easel"],
            count=1
        )
        
        # Modern Song submission (non-material)
        song_sub1 = Submission.objects.create(
            fair=current_fair.fair,
            user=basic_user_1,
            poster=False,
            title="Harmony of Cultures",
            organization="Oakridge Elementary School",
            group="Music Class",
            category=categories["Modern Song"],
            grade_range=Submission.GRADE_RANGES_DICT[students[f"{basic_user_1.email}_Lucas_Garcia"].grade],
            submission_type="group",
            comments="This song combines traditional melodies with modern elements.",
            status="submitted",
            submitted_email_sent=True,
            modified_by=basic_user_1.email
        )
        
        # Add languoids
        song_sub1.languoids.add(languoids[9])  # Hawaiian
        
        # Add instructor and students (all of them)
        song_sub1.instructors.add(instructors[f"{basic_user_1.email}_David_Chen"])
        for student_key in students:
            if basic_user_1.email in student_key:
                song_sub1.students.add(students[student_key])
        
        # Add accessories
        SubmissionAccessory.objects.create(
            submission=song_sub1,
            accessory=accessories["Chairs"],
            count=6
        )
        
        # Create submissions for User 2 (Jane Smith)
        # Poster submission
        poster_sub2 = Submission.objects.create(
            fair=current_fair.fair,
            user=basic_user_2,
            poster=True,
            title="Cultural Heritage Poster",
            organization="Sunnydale High School",
            group="Art Department",
            category=categories["Poster"],
            grade_range=Submission.GRADE_RANGES_DICT[students[f"{basic_user_2.email}_Emma_Brown"].grade],
            submission_type="individual",
            status="approved",
            submitted_email_sent=True,
            approved_email_sent=True,
            modified_by=basic_user_2.email
        )
        
        # Add languoids
        poster_sub2.languoids.add(languoids[11])  # Swahili
        
        # Add instructor and student
        poster_sub2.instructors.add(instructors[f"{basic_user_2.email}_Robert_Johnson"])
        poster_sub2.students.add(students[f"{basic_user_2.email}_Emma_Brown"])
        
        # Comic/Cartoon submission (material)
        comic_sub2 = Submission.objects.create(
            fair=current_fair.fair,
            user=basic_user_2,
            poster=False,
            title="Language Heroes",
            organization="Sunnydale High School",
            group="Creative Writing Club",
            category=categories["Comics and Cartoons"],
            grade_range=Submission.GRADE_RANGES_DICT[students[f"{basic_user_2.email}_Noah_Davis"].grade],
            submission_type="group",
            status="submitted",
            submitted_email_sent=True,
            modified_by=basic_user_2.email
        )
        
        # Add languoids
        comic_sub2.languoids.add(languoids[10])  # Mandarin
        comic_sub2.languoids.add(languoids[12])  # Maltese
        
        # Add instructor and students
        comic_sub2.instructors.add(instructors[f"{basic_user_2.email}_Sarah_Wilson"])
        comic_sub2.students.add(students[f"{basic_user_2.email}_Noah_Davis"])
        comic_sub2.students.add(students[f"{basic_user_2.email}_Ava_Taylor"])
        comic_sub2.students.add(students[f"{basic_user_2.email}_Liam_Wilson"])
        
        # Skit/Play submission (non-material)
        skit_sub2 = Submission.objects.create(
            fair=current_fair.fair,
            user=basic_user_2,
            poster=False,
            title="The Journey of Words",
            organization="Sunnydale High School",
            group="Drama Club",
            category=categories["Skit/Short Play"],
            grade_range=Submission.GRADE_RANGES_DICT[students[f"{basic_user_2.email}_Isabella_Clark"].grade],
            submission_type="group",
            comments="A dramatic interpretation of how languages evolve and change over time.",
            status="approved",
            submitted_email_sent=True,
            approved_email_sent=True,
            modified_by=basic_user_2.email
        )
        
        # Add languoids
        skit_sub2.languoids.add(languoids[6])  # Welsh
        skit_sub2.languoids.add(languoids[13])  # Quechua
        
        # Add instructor and all students
        skit_sub2.instructors.add(instructors[f"{basic_user_2.email}_Robert_Johnson"])
        for student_key in students:
            if basic_user_2.email in student_key:
                skit_sub2.students.add(students[student_key])
        
        # Add accessories
        SubmissionAccessory.objects.create(
            submission=skit_sub2,
            accessory=accessories["Chairs"],
            count=10
        )
        
        SubmissionAccessory.objects.create(
            submission=skit_sub2,
            accessory=accessories["6 Foot Rectangle Tables"],
            count=2
        )
        
        # Film submission
        film_sub2 = Submission.objects.create(
            fair=current_fair.fair,
            user=basic_user_2,
            poster=False,
            title="Languages Around Us",
            organization="Sunnydale High School",
            group="Media Studies",
            category=categories["Film and Video"],
            grade_range=Submission.GRADE_RANGES_DICT[students[f"{basic_user_2.email}_Liam_Wilson"].grade],
            submission_type="group",
            status="in_progress",
            modified_by=basic_user_2.email
        )
        
        # Add languoids
        film_sub2.languoids.add(languoids[14])  # Māori
        
        # Add instructor and students
        film_sub2.instructors.add(instructors[f"{basic_user_2.email}_Sarah_Wilson"])
        film_sub2.students.add(students[f"{basic_user_2.email}_Liam_Wilson"])
        film_sub2.students.add(students[f"{basic_user_2.email}_Isabella_Clark"])
        film_sub2.students.add(students[f"{basic_user_2.email}_Noah_Davis"])
        
        # Create submissions for User 3 (Jim Baker)
        # Traditional Song submission (non-material)
        trad_song_sub3 = Submission.objects.create(
            fair=current_fair.fair,
            user=basic_user_3,
            poster=False,
            title="Echoes of the Past",
            organization="Highland Charter School",
            group="Cultural Heritage Club",
            category=categories["Traditional Song"],
            grade_range=Submission.GRADE_RANGES_DICT[students[f"{basic_user_3.email}_William_Walker"].grade],
            submission_type="group",
            comments="A collection of songs performed in their original language with traditional instrumentation.",
            status="approved",
            submitted_email_sent=True,
            approved_email_sent=True,
            modified_by=basic_user_3.email
        )
        
        # Add languoids
        trad_song_sub3.languoids.add(languoids[2])  # Diné/Navajo
        
        # Add instructor and students
        trad_song_sub3.instructors.add(instructors[f"{basic_user_3.email}_Michael_Davis"])
        trad_song_sub3.students.add(students[f"{basic_user_3.email}_William_Walker"])
        trad_song_sub3.students.add(students[f"{basic_user_3.email}_Mia_Robinson"])
        trad_song_sub3.students.add(students[f"{basic_user_3.email}_James_Thomas"])
        
        # Add accessories
        SubmissionAccessory.objects.create(
            submission=trad_song_sub3,
            accessory=accessories["Chairs"],
            count=8
        )
        
        SubmissionAccessory.objects.create(
            submission=trad_song_sub3,
            accessory=accessories["32 Inch Standard Round Tables"],
            count=1
        )
        
        # Poster submission
        poster_sub3 = Submission.objects.create(
            fair=current_fair.fair,
            user=basic_user_3,
            poster=True,
            title="Language Preservation Poster",
            organization="Highland Charter School",
            group="Art Department",
            category=categories["Poster"],
            grade_range=Submission.GRADE_RANGES_DICT[students[f"{basic_user_3.email}_Charlotte_Scott"].grade],
            submission_type="individual",
            status="submitted",
            submitted_email_sent=True,
            modified_by=basic_user_3.email
        )
        
        # Add languoids
        poster_sub3.languoids.add(languoids[16])  # Ainu
        
        # Add instructor and student
        poster_sub3.instructors.add(instructors[f"{basic_user_3.email}_Elizabeth_Taylor"])
        poster_sub3.students.add(students[f"{basic_user_3.email}_Charlotte_Scott"])
        
        # Spoken Poetry submission (non-material)
        poetry_sub3 = Submission.objects.create(
            fair=current_fair.fair,
            user=basic_user_3,
            poster=False,
            title="Verses of Identity",
            organization="Highland Charter School",
            group="Creative Writing",
            category=categories["Spoken Poetry"],
            grade_range=Submission.GRADE_RANGES_DICT[students[f"{basic_user_3.email}_Benjamin_Green"].grade],
            submission_type="group",
            comments="Original poetry that explores themes of language, culture, and identity.",
            status="submitted",
            submitted_email_sent=True,
            modified_by=basic_user_3.email
        )
        
        # Add languoids
        poetry_sub3.languoids.add(languoids[15])  # Chad Arabic
        poetry_sub3.languoids.add(languoids[19])  # Krio
        
        # Add instructor and students
        poetry_sub3.instructors.add(instructors[f"{basic_user_3.email}_Michael_Davis"])
        poetry_sub3.students.add(students[f"{basic_user_3.email}_Benjamin_Green"])
        poetry_sub3.students.add(students[f"{basic_user_3.email}_Mia_Robinson"])
        
        # Add accessories
        SubmissionAccessory.objects.create(
            submission=poetry_sub3,
            accessory=accessories["Easel"],
            count=2
        )
        
        # Master Performer submission (non-material)
        master_sub3 = Submission.objects.create(
            fair=current_fair.fair,
            user=basic_user_3,
            poster=False,
            title="Languages of Our Ancestors",
            organization="Highland Charter School",
            group="Advanced Cultural Studies",
            category=categories["Master Performer"],
            grade_range=Submission.GRADE_RANGES_DICT[students[f"{basic_user_3.email}_James_Thomas"].grade],
            submission_type="individual",
            status="in_progress",
            modified_by=basic_user_3.email
        )
        
        # Add languoids
        master_sub3.languoids.add(languoids[1])  # Cherokee
        
        # Add instructor and student
        master_sub3.instructors.add(instructors[f"{basic_user_3.email}_Elizabeth_Taylor"])
        master_sub3.students.add(students[f"{basic_user_3.email}_James_Thomas"])
        
        # Add accessories
        SubmissionAccessory.objects.create(
            submission=master_sub3,
            accessory=accessories["32 Inch Tall Round Tables"],
            count=1
        )
        
        SubmissionAccessory.objects.create(
            submission=master_sub3,
            accessory=accessories["Chairs"],
            count=3
        )

        print("Done creating submissions")


        # create a submission for each user
        