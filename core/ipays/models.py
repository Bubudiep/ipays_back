from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
import logging
logger = logging.getLogger(__name__)

# Create your models here.
    
class Photos(models.Model):
    file_name = models.CharField(max_length=100, default="", blank=True, null=True)
    file_type = models.CharField(max_length=100, default="", blank=True, null=True)
    file_size = models.IntegerField(blank=True, null=True)
    img= models.TextField()
    user = models.ForeignKey(to=User, on_delete=models.SET_NULL, blank=True, null=True)
    Comment = models.CharField(max_length=1024, default="", blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def img_tag(self):
        try:
            return mark_safe('<img src = "{}" style="width:60px;border-radius: 10px;">'.format(
                self.img
            ))
        except Exception as e:
            logger.debug(e)
            return "aa"
    img_tag.short_description = 'Image'
    img_tag.allow_tags = True

    class Meta:
        ordering = ['-id']
    def __str__(self): 
        return f"{self.file_name}"
  
class UserProfile(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)

    avatar = models.ForeignKey(Photos, on_delete=models.SET_NULL, blank=True, null=True, related_name="avatars")
    wallpaper = models.ForeignKey(Photos, on_delete=models.SET_NULL, blank=True, null=True, related_name="wallpaper")
    level = models.IntegerField(default=0)
    fullname = models.CharField(max_length=100, default="", blank=True)
    birthday = models.DateField(null=True, blank=True)

    adr_tinh = models.CharField(max_length=100, default="", blank=True)
    adr_huyen = models.CharField(max_length=100, default="", blank=True)
    adr_xa = models.CharField(max_length=100, default="", blank=True)
    adr_details = models.CharField(max_length=100, default="", blank=True)
    adr_full = models.TextField(default="", blank=True)

    phone= models.CharField(max_length=20, default="", blank=True)
    zalo_key = models.CharField(unique=True ,max_length=100, default="", blank=True)
    zalo_name = models.CharField(max_length=100, default="", blank=True)
    sologan = models.TextField(default="", blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-id']
    def __str__(self): 
        return f"{self.user.username}"
    