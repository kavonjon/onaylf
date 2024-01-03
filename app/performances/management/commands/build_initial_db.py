from performances.models import Fair, CurrentFair, Languoid, Instructor, Student, Category, Accessory, Performance, Prize
from users.models import User
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group


class Command(BaseCommand):
    def handle(self, **options):
        # now do the things that you want with your models here

        # createsuper user
        
        # create fair
        
        fair = Fair.objects.create(name="2020", modified_by="admin@nal.ou.edu")
        
        # create/assign current fair
        
        CurrentFair.objects.all().delete()
        current_fair = CurrentFair.objects.create(name=fair.name, fair=fair, modified_by="admin@nal.ou.edu")
        

        # create moderator user

        nancy = User.objects.create_user(
            email='nancy@nal.ou.edu',
            password='bottombehindduckview',
        )

        # create basic user
        
        kavon = User.objects.create_user(
            email='kavon@nal.ou.edu',
            password='kavonspassword',
        )

        # create moderator group, assing to admin and moderator user
        
        mod_group, created = Group.objects.get_or_create(name='moderator')
        mod_group.user_set.add(nancy)
        admin_user = User.objects.get(email='admin@nal.ou.edu')
        mod_group.user_set.add(admin_user)


        # create instructors
        
        # create students
        
        # create performances
        
        # create languoids
        lang_list = [
            ("alab1237", "Alabama", "language"),
            ("jica1244", "Apache (Jicarilla)", "language"),
            ("mesc1238", "Apache (Mescalero)", "language"),
            ("kiow1264", "Apache (Plains)", "language"),
            ("west2615", "Apache (Western)", "language"),
            ("arap1274", "Arapaho", "language"),
            ("arik1262", "Arikara", "language"),
            ("assi1247", "Assiniboine", "language"),
            ("siks1238", "Blackfoot", "language"),
            ("cadd1256", "Caddo", "language"),
            ("cayu1261", "Cayuga", "language"),
            ("cher1273", "Cherokee", "language"),
            ("chey1247", "Cheyenne", "language"),
            ("chic1270", "Chickasaw", "language"),
            ("chit1248", "Chitimacha", "language"),
            ("choc1276", "Choctaw", "language"),
            ("coeu1236", "Coeur d'Alene", "language"),
            ("coma1245", "Comanche", "language"),
            ("cree1272", "Cree", "family"),
            ("cree1270", "Creek (Mvskoke)", "language"),
            ("cree1269", "Creek (Poarch Creek)", "language"),
            ("crow1244", "Crow", "language"),
            ("dako1258", "Dakota", "language"),
            ("unam1242", "Delaware (Lenape)", "language"),
            ("muns1251", "Delaware (Munsee)", "language"),
            ("yuch1247", "Euchee (Yuchi)", "language"),
            ("hava1249", "Havasupai", "dialect"),
            ("hida1246", "Hidatsa", "language"),
            ("hoch1243", "Hochunk (Winnebago)", "language"),
            ("hopi1249", "Hopi", "language"),
            ("wala1270", "Hualapai", "language"),
            ("iowa1245", "Ioway", "language"),
            ("iroq1247", "Iroquois", "family"),
            ("jeme1245", "Jemez", "language"),
            ("iowa1245", "Jiwere (Otoe)", "language"),
            ("kans1243", "Kansa", "language"),
            ("kere1287", "Keres", "family"),
            ("kick1244", "Kickapoo", "language"),
            ("kiow1266", "Kiowa", "language"),
            ("koas1236", "Koasati (Coushatta Quassarte)", "language"),
            ("lako1247", "Lakota", "language"),
            ("male1292", "Maliseet", "language"),
            ("mand1446", "Mandan", "language"),
            ("meno1252", "Menominee", "language"),
            ("mesk1242", "Meskwaki (Fox)", "language"),
            ("miam1252", "Miami", "language"),
            ("mika1239", "Miccosukee", "language"),
            ("klam1254", "Modoc (Klamath)", "language"),
            ("moha1258", "Mohawk", "language"),
            ("natc1249", "Natchez", "language"),
            ("nava1243", "Navajo", "language"),
            ("nucl1723", "Ojibwe", "family"),
            ("omah1248", "Omaha", "dialect"),
            ("onei1249", "Oneida", "language"),
            ("onon1246", "Onondaga", "language"),
            ("toho1245", "O'odham", "language"),
            ("osag1243", "Osage", "language"),
            ("abcd1234", "OTHER", "language"),
            ("otta1242", "Ottawa", "language"),
            ("nort2954", "Paiute", "language"),
            ("pawn1254", "Pawnee", "language"),
            ("pima1248", "Pima", "language"),
            ("ponc1241", "Ponca", "dialect"),
            ("pota1247", "Potawatomi", "language"),
            ("powh1243", "Powhatan", "language"),
            ("quap1242", "Quapaw", "language"),
            ("sacc1239", "Sauk", "dialect"),
            ("semi1265", "Seminole", "dialect"),
            ("sene1264", "Seneca", "language"),
            ("shaw1249", "Shawnee", "language"),
            ("shos1248", "Shoshone", "language"),
            ("siou1253", "Sioux", "family"),
            ("stoc1240", "Stockbridge", "language"),
            ("tewa1261", "Tewa", "family"),
            ("tiwa1255", "Tiwa", "family"),
            ("tonk1249", "Tonkawa", "language"),
            ("tusc1257", "Tuscarora", "language"),
            ("utee1244", "Ute", "dialect"),
            ("wamp1249", "Wampanoag", "language"),
            ("wyan1247", "Wandat (Huron)", "language"),
            ("wich1260", "Wichita", "language"),
            ("nako1239", "Yankton", "dialect"),
            ("yava1252", "Yavapai", "dialect"),
            ("yuro1248", "Yurok", "language"),
            ("zuni1245", "Zuni", "language")
        ]
        
        for lang in lang_list:
            languoid = Languoid.objects.create(glottocode=lang[0], name=lang[1], level=lang[2], modified_by="admin@nal.ou.edu")


        # delete all categories
        Category.objects.all().delete()

        # create Categories
        current_fair = CurrentFair.objects.first()
        cat_list = [
            ("Books",),
            ("Comics and Cartoons",),
            ("Film and Video",),
            ("Master Performer",),
            ("Mobile Video",),
            ("Modern Song",),
            ("Puppet Show",),
            ("Skit/Short Play",),
            ("Spoken Language",),
            ("Spoken Poetry",),
            ("Spoken Prayer",),
            ("Traditional Song",)
        ]

        for cat in cat_list:
            category = Category.objects.create(fair=current_fair.fair, name=cat[0], modified_by="admin@nal.ou.edu")

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