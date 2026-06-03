from django.db import migrations
import django.db.models.functions.text


class Migration(migrations.Migration):

    dependencies = [
        ('submissions', '0008_fair_material_submission_deadline'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={
                'ordering': ['-fair', django.db.models.functions.text.Lower('name')],
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.AlterModelOptions(
            name='accessory',
            options={
                'ordering': ['-fair', django.db.models.functions.text.Lower('name')],
                'verbose_name': 'accessory',
                'verbose_name_plural': 'accessories',
            },
        ),
        migrations.AlterModelOptions(
            name='submissionaccessory',
            options={
                'verbose_name': 'submission accessory',
                'verbose_name_plural': 'submission accessories',
            },
        ),
    ]
