from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction
from .models import CurrentFair, Submission
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=get_user_model())
def update_submissions_organization(sender, instance, created, raw, update_fields, **kwargs):
    if created or raw:
        # Skip if this is a new user being created or raw save
        return

    try:
        with transaction.atomic():
            # Get the original state from the database
            if hasattr(instance, '_loaded_values'):
                old_organization = instance._loaded_values.get('organization')
            else:
                # Fallback if _loaded_values not available
                old_organization = sender.objects.get(pk=instance.pk).organization
            
            # Log the values for debugging
            logger.info(f"Old organization: {old_organization}")
            logger.info(f"New organization: {instance.organization}")
            
            if old_organization != instance.organization:
                logger.info("Organization changed - updating submissions")
                
                # Get current fair
                current_fair = CurrentFair.objects.first()
                
                if current_fair:
                    # Update all submissions for this user in the current fair
                    updated_count = Submission.objects.filter(
                        user=instance,
                        fair=current_fair.fair
                    ).update(organization=instance.organization)
                    
                    logger.info(f"Updated {updated_count} submissions")
                else:
                    logger.warning("No current fair found")
            else:
                logger.info("Organization unchanged - no updates needed")
                
    except Exception as e:
        logger.error(f"Error updating submissions: {str(e)}")

@receiver(post_save, sender=Submission)
def mark_submission_submitted(sender, instance, created, **kwargs):
    # Skip email sending if in demo mode
    if getattr(settings, 'DEMO_MODE', False):
        logger.info("Skipping submission email in DEMO_MODE")
        return
        
    logger.info(f"Signal triggered for submission {instance.id} with status {instance.status}")
    
    if instance.status == 'submitted' and instance.submitted_email_sent == False:
        logger.info("Conditions met for sending submission email")
        try:
            # Log email details before sending
            logger.info(f"Preparing email for submission {instance.id}:")
            logger.info(f"User email: {instance.user.email}")
            logger.info(f"From email: {settings.EMAIL_HOST_USER}")
            logger.info(f"SMTP settings - Host: {settings.EMAIL_HOST}, Port: {settings.EMAIL_PORT}")
            
            instance.submitted_email_sent = True
            instance.save(update_fields=['submitted_email_sent'])
            currentFair = CurrentFair.objects.first()
            
            if not currentFair:
                logger.error("No current fair found")
                return

            # Create recipient list excluding nal.ou.edu emails
            recipient_list = ['onaylf.samnoblemuseum@ou.edu']
            if not instance.user.email.endswith('@nal.ou.edu'):
                recipient_list.append(instance.user.email)
                
            year = currentFair.name
            submission_title = instance.title
            if len(submission_title) > 40:
                short_title = submission_title[:40].strip() + "..."
            else:
                short_title = submission_title

            subject = f"[ONAYLF {year}] Submission submitted: {short_title}"
            body = f"""Submission title: {submission_title}

Thank you for registering your student's submission for the {year} ONAYLF.

Please remember that your students' material submissions (Books, Comics & Cartoons, Film & Video, Mobile Video, Poster Art, and Puppet Shows) must be postmarked or submitted on or before March 8, {year}.

You will receive an email when this submission is approved by ONAYLF staff.

You can contact us at onaylf.samnoblemuseum@ou.edu with any questions.

Thank you,
ONAYLF Team"""

            logger.info(f"Attempting to send email with subject: {subject}")
            
            send_mail(
                subject=subject,
                message=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=recipient_list,
                fail_silently=False,
            )
            logger.info(f"Email sent successfully for submission {instance.id}")
        except Exception as e:
            logger.error(f"Error sending email: {str(e)}")
            logger.error(f"Error type: {type(e).__name__}")
            # If there's a traceback available
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")

@receiver(post_save, sender=Submission)
def at_submission_approved(sender, instance, created, **kwargs):
    # Skip email sending if in demo mode
    if getattr(settings, 'DEMO_MODE', False):
        logger.info("Skipping approval email in DEMO_MODE")
        return
        
    if instance.status == 'approved' and instance.approved_email_sent == False:
        try:
            instance.approved_email_sent = True
            instance.save(update_fields=['approved_email_sent'])
            currentFair = CurrentFair.objects.first()
            
            if not currentFair:
                logger.error("No current fair found")
                return

            # Create recipient list excluding nal.ou.edu emails
            recipient_list = ['onaylf.samnoblemuseum@ou.edu']
            if not instance.user.email.endswith('@nal.ou.edu'):
                recipient_list.append(instance.user.email)
                
            year = currentFair.name
            submission_title = instance.title
            if len(submission_title) > 40:
                short_title = submission_title[:40].strip() + "..."
            else:
                short_title = submission_title

            subject = f"[ONAYLF {year}] Submission approved: {short_title}"
            body = f"""Submission title: {submission_title}

Your students' submission has been approved by the ONAYLF Team. We look forward to seeing you and your students at the Fair.

You can contact us at onaylf.samnoblemuseum@ou.edu with any questions.

Thank you,
ONAYLF Team"""

            send_mail(
                subject=subject,
                message=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=recipient_list,
                fail_silently=False,
            )
            logger.info(f"Approval email sent successfully for submission {instance.id}")
        except Exception as e:
            logger.error(f"Error sending approval email: {str(e)}")
            logger.error(f"Error type: {type(e).__name__}")
            logger.error(f"Traceback: {traceback.format_exc()}")

