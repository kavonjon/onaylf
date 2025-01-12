from submissions.models import Fair, CurrentFair, Languoid, Tribe, Instructor, Student, Category, Accessory, Submission
from users.models import User, Organization
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
import os
from dotenv import load_dotenv
load_dotenv()  # loads the configs from .env

class Command(BaseCommand):
    def handle(self, **options):

        print("build initial db")

        # # createsuperuser
        
        # create fair
        
        fair = Fair.objects.create(name="2024", modified_by="admin@nal.ou.edu")
        
        # create/assign current fair
        
        CurrentFair.objects.all().delete()
        current_fair = CurrentFair.objects.create(name=fair.name, fair=fair, modified_by="admin@nal.ou.edu")
        

        # create moderator user

        nancy = User.objects.create_user(
            email='nancy@nal.ou.edu',
            first_name='Nancy',
            last_name='C',
            password = str(os.getenv('NANCYS_PASSWORD')),
        )

        raina = User.objects.create_user(
            email='raina@nal.ou.edu',
            first_name='Raina',
            last_name='H',
            password=str(os.getenv('RAINAS_PASSWORD')),
        )

        will = User.objects.create_user(
            email='will@nal.ou.edu',
            first_name='Will',
            last_name='M',
            password=str(os.getenv('WILLS_PASSWORD')),
        )

        # create basic user
        
        kavon = User.objects.create_user(
            email='kavon@nal.ou.edu',
            first_name='Kavon',
            last_name='H',
            password=str(os.getenv('KAVONS_PASSWORD')),
        )

        # create moderator group, assing to admin and moderator user
        
        mod_group, created = Group.objects.get_or_create(name='moderator')
        mod_group.user_set.add(nancy)
        mod_group.user_set.add(raina)
        mod_group.user_set.add(will)
        admin_user = User.objects.get(email='admin@nal.ou.edu')
        mod_group.user_set.add(admin_user)
        # set the first_name and last_name of the admin user
        admin_user.first_name = 'NAL'
        admin_user.last_name = 'Administrator'
        admin_user.save()


        # create organizations
        org_list = [
            ("4 B Men"),
            ("Achille Public Schools"),
            ("Ak Biilaagaa Iiliia - Little Big Horn College"),
            ("Alabama Coushatta Youth Program"),
            ("Alabama Quassarte Tribal Town"),
            ("Alla Himita 4H Club"),
            ("Anadarko Public Schools"),
            ("Antlers Public Schools"),
            ("Apache Culture Program"),
            ("Ardmore Native American Club"),
            ("Atoka Public Schools"),
            ("Bennington Public Schools"),
            ("BIE Carnegie Adult Learning Center"),
            ("Bokoshe Public School"),
            ("Boswell Public Schools"),
            ("Broken Bow Public Schools"),
            ("Butner Public Schools"),
            ("Byng Public Schools"),
            ("Cache Public Schools"),
            ("Caddo Nation"),
            ("Caddo Nation Childcare Program"),
            ("Caddo Nation Head Start"),
            ("Caddo Public Schools"),
            ("Calera Public Schools"),
            ("Calumet Public Schools"),
            ("Cameron Public Schools"),
            ("Canton Community Class"),
            ("Carnegie Elementary Mini Indian Club"),
            ("Carnegie Native American Heritage Club"),
            ("Carnegie Public Schools"),
            ("Chahta Anumpa Aiikhvna"),
            ("Chahta Vlla Interlocal Preschool"),
            ("Chahta Vlla Vlheha"),
            ("Cherokee Immersion Charter School"),
            ("Cherokee Nation"),
            ("Cherokee Nation Foundation"),
            ("Cherokee Nation Head Start"),
            ("Cheyenne and Arapaho Tribes"),
            ("Cheyenne Arapaho Baptist Association"),
            ("Cheyenne Arapaho Churches Youth Group"),
            ("Cheyenne Language Outreach"),
            ("Chickasaw Children's Village"),
            ("Chickasaw Nation"),
            ("Chickasaw Nation Chokka Kilimpi Imatahli"),
            ("Chickasaw Nation Head Start"),
            ("Chickasaw Nation Oshi Language Club"),
            ("Chickasaw Nation Youth Leadership Program"),
            ("Chipota Chikashshanompoli - Children Speaking Chickasaw Club"),
            ("Choctaw Nation Norman Community Class"),
            ("Choctaw Nation School of Language"),
            ("Choctaw Tribal Alliance OKC"),
            ("Chokka Kilimpi Family Resource Center"),
            ("Citizen Potawatomi Nation Child Development Center"),
            ("Citizen Potawatomi Nation Language Department"),
            ("Citizen Potawatomi Nation Youth Choir"),
            ("Claremore Public Schools"),
            ("Coalgate Public Schools"),
            ("Colbert Public Schools"),
            ("Coleman Public Schools"),
            ("Comanche Academy Charter School"),
            ("Comanche Nation Child Care Center - Onaakani"),
            ("Comanche Nation IAMNDN"),
            ("Comanche Nation Youth Program"),
            ("Coushatta Tribe"),
            ("Crooked Oak Language Group"),
            ("Crowder Public Schools"),
            ("Cushing Public Schools"),
            ("Daposka Ahnkodapi"),
            ("Darlington Public Schools"),
            ("Dawkanah Hasinay"),
            ("Delaware Nation Cultural Preservation"),
            ("Dewar Public Schools"),
            ("Deyo Mission Youth Choir"),
            ("Durant Public Schools"),
            ("Eagletown Public School"),
            ("Eastern Shawnee Tribe"),
            ("Edmond Public Schools"),
            ("Edmond Schools Indian Education"),
            ("El Reno Public Schools"),
            ("Elgin Public Schools"),
            ("Euchee Language Learning Center"),
            ("Euchee Language Project"),
            ("Fort Sill Apache Language Program"),
            ("Fort Towson Public Schools"),
            ("Fred L. McGhee Early Learning Center"),
            ("Frontier Public Schools"),
            ("Glenpool Creek Indian Community"),
            ("Glenpool Public Schools"),
            ("Graham-Dustin Public Schools"),
            ("Grand View School"),
            ("Grove Public Schools"),
            ("Guthrie Public Schools"),
            ("Haileyville Public Schools"),
            ("Hammon Public Schools"),
            ("Hartshorne Public Schools"),
            ("Hasinai Society of the Caddo Nation"),
            ("Haworth Public Schools"),
            ("Holdenville Public Schools"),
            ("Howe Public Schools"),
            ("Hugo Public Schools"),
            ("Idabel Public Schools"),
            ("Indiahoma Public Schools"),
            ("Jenks Public Schools"),
            ("Jones Academy"),
            ("Justice Public School"),
            ("Kaáⁿze Íe - Kanza Language Project"),
            ("Kickapoo Tribe of Oklahoma"),
            ("Kinta Public Schools"),
            ("Kiononia Indian Mennonite Church"),
            ("Kiowa Child Care Center"),
            ("Kiowa Kids"),
            ("Kiowa Tribe"),
            ("Kiowa Tribe Head Start"),
            ("Kitikitish Little Sisters"),
            ("Konawa Public Schools"),
            ("Lawton Public Schools"),
            ("Le Flore Public Schools"),
            ("Legacy Cultural Learning Community"),
            ("Littlesun School"),
            ("Lomega Public Schools"),
            ("Mason Public Schools"),
            ("McAlester Public Schools"),
            ("McCurtain Public Schools"),
            ("McLoud Public Schools"),
            ("Meeker Public Schools"),
            ("Memorial Indian Baptist Church"),
            ("Mercy School Institute"),
            ("Meskwaki Settlement School"),
            ("Metro Caddo Culture Club"),
            ("Mill Creek Public Schools"),
            ("Moore Public Schools"),
            ("Morris Public Schools"),
            ("Mount Scott Kiowa United Methodist Church"),
            ("MOWA Band of Choctaw Indians Language Program - Chata Imissa"),
            ("Moyers Public Schools"),
            ("Mvskoke Language Program"),
            ("Mvskoke Nation Youth Council"),
            ("Mvskoke Nation Youth Services"),
            ("New Kituwah Academy"),
            ("New Lima Public Schools"),
            ("Norman First American United Methodist Church"),
            ("Norman Public Schools"),
            ("Numunu Turetu - Comanche Nation Early Childhood Development Center"),
            ("Okemah Public Schools"),
            ("Oklahoma City Muscogee Creek Association"),
            ("Oklahoma City Public Schools"),
            ("Oklahoma Virtual Charter Schools"),
            ("Osage County Interlocal Coop"),
            ("Osage Nation Language Department - Bartlesville"),
            ("Osage Nation Language Department - Grayhorse - Fairfax"),
            ("Osage Nation Language Department - Tulsa"),
            ("Osage Nation Wahzhazhe Early Learning Academy - Skiatook"),
            ("Osage Nation Wahzhazhe Early Learning Academy - Pawhuska"),
            ("Otoe Missouria Youth Programs"),
            ("Otoe-Missouria Language Department"),
            ("Owyhee High School"),
            ("Pawhuska Public Schools"),
            ("Pawnee Public Schools"),
            ("Petarsy Indian Mission UMC"),
            ("Pittsburg Public Schools"),
            ("Pleasant Grove Public Schools"),
            ("Poarch Band of Creek Indians"),
            ("Pocola Public Schools"),
            ("Ponca Tribe"),
            ("Poteau Public Schools"),
            ("Prairie Band Potawatomi Nation Language and Cultural Department"),
            ("Preston Public Schools"),
            ("Puhi Tekwap Comanche Class"),
            ("Riverside Indian School"),
            ("Rock Creek Public Schools"),
            ("Rocky Mountain School"),
            ("Royal Valley Public Schools"),
            ("Ryal Public Schools"),
            ("Salt Creek United Methodist Church"),
            ("Santee Community School"),
            ("Sauk Language Department"),
            ("School of Choctaw Language"),
            ("Seminole Nation Hopuetake Yekcakat (Strong Kids) Program"),
            ("Seminole Public Schools"),
            ("Sequoyah High School"),
            ("Shawnee Language Immersion Program"),
            ("Shawnee Public Schools"),
            ("Soper Public School"),
            ("Southern Plains Sign Language Ensemble"),
            ("St. Anthony Indian School"),
            ("Stillwater Public Schools"),
            ("Stilwell Public Schools"),
            ("Stringtown Public Schools"),
            ("Stroud Public Schools"),
            ("Stuart Public Schools"),
            ("Talihina Public Schools"),
            ("Tenkiller Public School"),
            ("Thomas Indian Education Afterschool Program"),
            ("Thomas Tribal Youth"),
            ("United Methodist Church of Apache"),
            ("Valliant Public Schools"),
            ("Vinita Public Schools"),
            ("Walters Service Club"),
            ("Watonga Public Schools"),
            ("Weatherford Public Schools"),
            ("Whitesboro Public Schools"),
            ("Wichita and Affiliated Tribes"),
            ("Wichita Child Development Center"),
            ("Wichita Cultural Education Program"),
            ("Wichita School Readiness Program"),
            ("Wichita STAR Academy"),
            ("Wilburton Public Schools"),
            ("Wilson Public School"),
            ("Wister Public Schools"),
            ("Wright City Head Start"),
            ("Wright City Public Schools"),
            ("Yuchi Language Project"),
            ("Zion School"),
            ("zOyaha School of Language"),
        ]

        for org in org_list:
            org = Organization.objects.get_or_create(name=org)


        # create languoids
        lang_list = [
            ("abcd1234", "Other", "language"),
            ("arap1274", "Arapaho", "language"),
            ("assi1247", "Assiniboine", "language"),
            ("cher1273", "Cherokee", "language"),
            ("chey1247", "Cheyenne", "language"),
            ("chic1270", "Chickasaw", "language"),
            ("choc1276", "Choctaw (Oklahoma, Mississippi)", "language"),
            ("coma1245", "Comanche", "language"),
            ("cree1272", "Creek (Mvskoke, Seminole, Poarch Creek)", "family"),
            ("nava1243", "Diné/Navajo", "language"),
            ("east1472", "Eastern Keres", "language"),
            ("yuch1247", "Euchee (Yuchi)", "language"),
            ("hava1248", "Havasupai, Walapai, Yavapai", "language"),
            ("hida1246", "Hidatsa", "language"),
            ("hoch1243", "Ho-chunk", "language"),
            ("hopi1249", "Hopi", "language"),
            ("jica1244", "Jicarilla Apache", "language"),
            ("iowa1245", "Jiwere (Ioway, Otoe, Missouria)", "language"),
            ("kans1243", "Kansa/Kaw", "language"),
            ("kick1244", "Kickapoo", "language"),
            ("kiow1266", "Kiowa", "language"),
            ("lako1247", "Lakota", "language"),
            ("lipa1241", "Lipan Apache", "language"),
            ("mesc1238", "Mescalero-Chiricahua Apache", "language"),
            ("mika1239", "Mikasuki", "language"),
            ("moha1258", "Mohawk", "language"),
            ("muns1251", "Munsee (Delaware/Lenape)", "language"),
            ("miam1252", "Myaamia/Miami, Peoria", "language"),
            ("azte1234", "Nahuatl", "language"),
            ("natc1249", "Natchez", "language"),
            ("nort2954", "Northern Paiute", "language"),
            ("toho1245", "O'odham", "language"),
            ("onei1249", "Oneida", "language"),
            ("osag1243", "Osage", "language"),
            ("pawn1254", "Pawnee", "language"),
            ("kiow1264", "Plains Apache", "language"),
            ("omah1247", "Ponca, Omaha", "language"),
            ("pota1247", "Potawatomi", "language"),
            ("mesk1242", "Sauk, Meskwaki/Fox", "dialect"),
            ("sene1264", "Seneca", "language"),
            ("shaw1249", "Shawnee", "language"),
            ("shos1248", "Shoshoni", "language"),
            ("tonk1249", "Tonkawa", "language"),
            ("unam1242", "Unami (Delaware/Lenape)", "language"),
            ("west2615", "Western Apache", "language"),
            ("west2632", "Western Keres", "language"),
            ("wich1260", "Wichita", "language"),
            ("nucl1648", "Wyandot", "dialect"),
            ("zuni1245", "Zuni", "language")
        ]
        
        for lang in lang_list:
            languoid = Languoid.objects.create(
                fair=current_fair.fair,
                glottocode=lang[0],
                name=lang[1],
                level=lang[2],
                modified_by="admin@nal.ou.edu"
            )


        # create tribes
        current_fair = CurrentFair.objects.first()
        tribe_list = [
            ('Other',),
            ('Absentee Shawnee Tribe',),
            ('Alabama-Quassarte Tribal Town',),
            ('Apache Tribe of Oklahoma',),
            ('Caddo Nation',),
            ('Cherokee Nation',),
            ('Cheyenne and Arapaho Tribes',),
            ('Chickasaw Nation',),
            ('Choctaw Nation of Oklahoma',),
            ('Citizen Potawatomi Nation',),
            ('Comanche Nation',),
            ('Delaware Nation',),
            ('Delaware Tribe of Indians',),
            ('Eastern Shawnee Tribe',),
            ('Euchee/Yuchi Tribe',),
            ('Fort Sill Apache Tribe',),
            ('Havasupai Tribe',),
            ('Hopi Tribe',),
            ('Iowa Tribe',),
            ('Kaw Nation',),
            ('Kialegee Tribal Town',),
            ('Kickapoo Tribe',),
            ('Kiowa Tribe',),
            ('Laguna Pueblo',),
            ('Miami Tribe',),
            ('Mississippi Band of Choctaw Indians',),
            ('Modoc Nation',),
            ('Muscogee Nation',),
            ('Navajo Nation',),
            ('Osage Nation',),
            ('Otoe-Missouria Tribe',),
            ('Ottawa Tribe',),
            ('Pawnee Nation',),
            ('Peoria Tribe of Indians',),
            ('Poarch Band of Creek Indians',),
            ('Ponca Tribe',),
            ('Quapaw Nation',),
            ('Sac and Fox Nation',),
            ('San Carlos Apache Tribe',),
            ('Seminole Nation',),
            ('Seneca-Cayuga Nation',),
            ('Shawnee Tribe',),
            ('Thlopthlocco Tribal Town',),
            ('Tonkawa Tribe',),
            ('United Keetoowah Band of Cherokees',),
            ('Wichita and Affiliated Tribes',),
            ('Wyandotte Nation',),
            ('Zuni Pueblo',)
        ]

        for tribe in tribe_list:
            tribe = Tribe.objects.create(fair=current_fair.fair, name=tribe[0], modified_by="admin@nal.ou.edu")


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
                modified_by="admin@nal.ou.edu"
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
            accessory = Accessory.objects.create(fair=current_fair.fair, name=acc[0], modified_by="admin@nal.ou.edu")

        # create instructors
        
        # create students
        
        # create submissions

        print("done")