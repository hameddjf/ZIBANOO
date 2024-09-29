from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth import get_user_model
import threading
import time

User = get_user_model()


@receiver(post_save, sender=User)
def delete_unverified_user(sender, instance, created, **kwargs):
    if created and not instance.is_active:
        def check_user():
            time.sleep(120)
            user = User.objects.filter(id=instance.id).first()
            if user and not user.is_active:
                user.delete()

        threading.Thread(target=check_user).start()
