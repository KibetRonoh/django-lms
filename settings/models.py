from django.core.exceptions import ValidationError
from django.db import models


class SiteSetting(models.Model):
    name = models.CharField(max_length=10)
    logo = models.ImageField(upload_to='media/site/')
    homepage_image = models.ImageField(upload_to='media/homepage/', default=0, help_text='Dimensions: 1200 x 1400')
    site_description = models.TextField(max_length=200)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.CharField(max_length=100, default='address')
    google_map_location = models.CharField(max_length=1000, null=True, blank=True)
    banner_message = models.CharField(max_length=100)
    facebook = models.URLField(max_length=1000)
    x = models.URLField(max_length=1000)
    linkedin = models.URLField(max_length=1000)
    instagram = models.URLField(max_length=1000)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Create only one SiteSettings instance
        """
        if not self.pk and SiteSetting.objects.exists():
            # This below line will render error by breaking page, you will see
            """
            raise ValidationError(
                "There can be only one SiteSetting you can not add another"
            )
            """
            # OR you can ever return None from here,
            # this will not save any data only you can update existing once
            return None

        return super(SiteSetting, self).save(*args, **kwargs)

