import random
import logging
import time
from .models import AudioUpload
from django.core.mail import send_mail
from celery import shared_task
from celery.exceptions import MaxRetriesExceededError
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

logger = logging.getLogger(__name__)

@shared_task(autoretry_for=(Exception,), max_retries=3, retry_backoff=True)
def send_email_task(recipient, subject, body):
    if random.choice([True, False]):
        raise Exception("Simulated email sending failure")
    try:
        send_mail(
            subject,
            body,
            'kapparovaak4@gmail.com',
            [recipient],
            fail_silently=False,
        )
        logger.info(f"Email successfully sent to {recipient}")
        return f"Email sent to {recipient} via SMTP"
    except Exception as e:
        logger.error(f"Error sending email to {recipient}: {e}")
        try:
            raise send_email_task.retry(exc=e)
        except MaxRetriesExceededError:
            logger.error(f"Max retries exceeded for sending email to {recipient}")
            raise e


@shared_task
def process_audio_file(upload_id):
    try:
        upload = AudioUpload.objects.get(id=upload_id)
        upload.status = 'processing'
        upload.save()

        file_size_mb = upload.file.size / (1024 * 1024)
        processing_steps = max(10, int(file_size_mb))

        channel_layer = get_channel_layer()
        group_name = f"audio_progress_{upload_id}"

        for i in range(processing_steps):
            chunk_progress = int(100 / processing_steps)
            upload.progress = min(upload.progress + chunk_progress, 100)
            upload.save()
            async_to_sync(channel_layer.group_send)(
                group_name,
                {
                    "type": "audio_progress_update",
                    "progress": upload.progress
                }
            )
            time.sleep(0.5)

        upload.status = 'completed'
        upload.save()

        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                "type": "audio_progress_update",
                "progress": 100,
                "status": "completed"
            }
        )
    except Exception as e:
        upload.status = 'failed'
        upload.progress = 0
        upload.save()
        print(f"Error processing audio file {upload_id}: {e}")