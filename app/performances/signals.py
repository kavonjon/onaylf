from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import CurrentFair, Performance

@receiver(post_save, sender=Performance)
def mark_performance_submitted(sender, instance, **kwargs):
    if ( instance.instructors_status=="completed" and
        instance.students_status=="completed" and
        instance.accessories_status=="completed" and
        instance.review_status=="completed" ):
        if instance.status == 'in_progress':
            instance.status = 'submitted'
            instance.save(update_fields=['status'])
            currentFair = CurrentFair.objects.first()
            year = currentFair.name
            performance_title = instance.title
            if len(performance_title) > 40:
                short_title = performance_title[:40].strip() + "..."
            else:
                short_title = performance_title
            template_subject = "[ONAYLF {year}] Performance submitted: {short_title}"
            template_email = """Performance title: {title}

Thank you for registering your student's performance for the {year} ONAYLF.

Please remember that your students' material submissions (Books, Comics & Cartoons, Film & Video, Mobile Video, Poster Art, and Puppet Shows) must be postmarked or submitted on or before March 8, {year}.

You will receive an email when this performance is approved by ONAYLF staff.

You can contact us at onaylf.samnoblemuseum@ou.edu with any questions.

Thank you,
ONAYLF Team"""
            send_mail(
                template_subject.format(year=year, short_title=short_title),
                template_email.format(title=performance_title, year=year),
                settings.EMAIL_HOST_USER,
                [instance.user.email, 'onaylf.samnoblemuseum@ou.edu'],  # the email address to send to
                fail_silently=True,
            )

@receiver(post_save, sender=Performance)
def at_performance_approved(sender, instance, **kwargs):
    if instance.status == 'approved':
        currentFair = CurrentFair.objects.first()
        year = currentFair.name
        performance_title = instance.title
        if len(performance_title) > 40:
            short_title = performance_title[:40].strip() + "..."
        else:
            short_title = performance_title
        template_subject = "[ONAYLF {year}] Performance approved: {short_title}"
        template_email = """Performance title: {title}

Your students' performance has been approved by the ONAYLF Team.  We look forward to seeing you and your students at the Fair.

You can contact us at onaylf.samnoblemuseum@ou.edu with any questions.

Thank you,
ONAYLF Team"""
        send_mail(
            template_subject.format(year=year, short_title=short_title),
            template_email.format(title=performance_title, year=year),
            settings.EMAIL_HOST_USER,
            [instance.user.email, 'onaylf.samnoblemuseum@ou.edu'],  # the email address to send to
            fail_silently=True,
        )

