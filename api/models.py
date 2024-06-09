from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
import os
# Create your models here.

class Image(models.Model):
    image = models.ImageField(upload_to='store/images')
    detected_image = models.ImageField(upload_to='store/images', null=True, blank=True)

@receiver(pre_delete, sender=Image)
def delete_image(sender, instance, **kwargs):
    # Delete the image file from the media folder
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
    if instance.detected_image:
        if os.path.isfile(instance.detected_image.path):
            os.remove(instance.detected_image.path)