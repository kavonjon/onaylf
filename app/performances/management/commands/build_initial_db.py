from performances.models import Fair, CurrentFair, Languoid, Tribe, Instructor, Student, Category, Accessory, Performance, Prize
from users.models import User
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group


class Command(BaseCommand):
    def handle(self, **options):

        print("build initial db")

        # # createsuper user
        
        # # create fair
        
        # fair = Fair.objects.create(name="2024", modified_by="admin@nal.ou.edu")
        
        # # create/assign current fair
        
        # CurrentFair.objects.all().delete()
        # current_fair = CurrentFair.objects.create(name=fair.name, fair=fair, modified_by="admin@nal.ou.edu")
        

        # # create moderator user

        # nancy = User.objects.create_user(
        #     email='nancy@nal.ou.edu',
        #     password='bottombehindduckview',
        # )

        # raina = User.objects.create_user(
        #     email='raina@nal.ou.edu',
        #     password='topbehindduckview',
        # )

        # # create basic user
        
        # kavon = User.objects.create_user(
        #     email='kavon@nal.ou.edu',
        #     password='kavonspassword',
        # )

        # # create moderator group, assing to admin and moderator user
        
        # mod_group, created = Group.objects.get_or_create(name='moderator')
        # mod_group.user_set.add(nancy)
        # mod_group.user_set.add(raina)
        # admin_user = User.objects.get(email='admin@nal.ou.edu')
        # mod_group.user_set.add(admin_user)

        # # create languoids
        # lang_list = [
        #     ("abcd1234", "Other", "language"),
        #     ("arap1274", "Arapaho", "language"),
        #     ("assi1247", "Assiniboine", "language"),
        #     ("cher1273", "Cherokee", "language"),
        #     ("chey1247", "Cheyenne", "language"),
        #     ("chic1270", "Chickasaw", "language"),
        #     ("choc1276", "Choctaw (Oklahoma, Mississippi)", "language"),
        #     ("coma1245", "Comanche", "language"),
        #     ("cree1272", "Creek (Mvskoke, Seminole, Poarch Creek)", "family"),
        #     ("nava1243", "Diné/Navajo", "language"),
        #     ("east1472", "Eastern Keres", "language"),
        #     ("yuch1247", "Euchee (Yuchi)", "language"),
        #     ("hava1248", "Havasupai, Walapai, Yavapai", "language"),
        #     ("hida1246", "Hidatsa", "language"),
        #     ("hoch1243", "Ho-chunk", "language"),
        #     ("hopi1249", "Hopi", "language"),
        #     ("jica1244", "Jicarilla Apache", "language"),
        #     ("iowa1245", "Jiwere (Ioway, Otoe, Missouria)", "language"),
        #     ("kans1243", "Kansa/Kaw", "language"),
        #     ("kick1244", "Kickapoo", "language"),
        #     ("kiow1266", "Kiowa", "language"),
        #     ("lako1247", "Lakota", "language"),
        #     ("lipa1241", "Lipan Apache", "language"),
        #     ("mesc1238", "Mescalero-Chiricahua Apache", "language"),
        #     ("mika1239", "Mikasuki", "language"),
        #     ("moha1258", "Mohawk", "language"),
        #     ("muns1251", "Munsee (Delaware/Lenape)", "language"),
        #     ("miam1252", "Myaamia/Miami, Peoria", "language"),
        #     ("azte1234", "Nahuatl", "language"),
        #     ("natc1249", "Natchez", "language"),
        #     ("nort2954", "Northern Paiute", "language"),
        #     ("toho1245", "O'odham", "language"),
        #     ("onei1249", "Oneida", "language"),
        #     ("osag1243", "Osage", "language"),
        #     ("pawn1254", "Pawnee", "language"),
        #     ("kiow1264", "Plains Apache", "language"),
        #     ("omah1247", "Ponca, Omaha", "language"),
        #     ("pota1247", "Potawatomi", "language"),
        #     ("mesk1242", "Sauk, Meskwaki/Fox", "dialect"),
        #     ("sene1264", "Seneca", "language"),
        #     ("shaw1249", "Shawnee", "language"),
        #     ("shos1248", "Shoshoni", "language"),
        #     ("tonk1249", "Tonkawa", "language"),
        #     ("unam1242", "Unami (Delaware/Lenape)", "language"),
        #     ("west2615", "Western Apache", "language"),
        #     ("west2632", "Western Keres", "language"),
        #     ("wich1260", "Wichita", "language"),
        #     ("nucl1648", "Wyandot", "dialect"),
        #     ("zuni1245", "Zuni", "language")
        # ]
        
        # for lang in lang_list:
        #     languoid = Languoid.objects.create(glottocode=lang[0], name=lang[1], level=lang[2], modified_by="admin@nal.ou.edu")


        # # create tribes
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


        # # delete all categories
        # Category.objects.all().delete()

        # # create Categories
        # current_fair = CurrentFair.objects.first()
        # cat_list = [
        #     ("Books",),
        #     ("Comics and Cartoons",),
        #     ("Film and Video",),
        #     ("Master Performer",),
        #     ("Mobile Video",),
        #     ("Modern Song",),
        #     ("Poster",),
        #     ("Puppet Show",),
        #     ("Skit/Short Play",),
        #     ("Spoken Language",),
        #     ("Spoken Poetry",),
        #     ("Spoken Prayer",),
        #     ("Traditional Song",)
        # ]

        # for cat in cat_list:
        #     category = Category.objects.create(fair=current_fair.fair, name=cat[0], modified_by="admin@nal.ou.edu")

        # # delete all accessories
        # Accessory.objects.all().delete()

        # # create accessories
        # current_fair = CurrentFair.objects.first()
        # acc_list = [
        #     ("32 Inch Standard Round Tables",),
        #     ("32 Inch Tall Round Tables",),
        #     ("6 Foot Rectangle Tables",),
        #     ("Chairs",),
        #     ("Easel",)
        # ]

        # for acc in acc_list:
        #     accessory = Accessory.objects.create(fair=current_fair.fair, name=acc[0], modified_by="admin@nal.ou.edu")

        # # create instructors
        
        # # create students
        
        # # create performances