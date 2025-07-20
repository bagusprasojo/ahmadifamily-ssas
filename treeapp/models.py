from django.db import models
from django.utils.timezone import now
from ckeditor.fields import RichTextField
from django.contrib.auth.models import AbstractUser
import uuid

class CustomUser(AbstractUser):
    family = models.ForeignKey('Family', on_delete=models.SET_NULL, null=True, blank=True)
    role = models.CharField(
        max_length=20,
        choices=[('admin', 'Admin'), ('viewer', 'Viewer')],
        default='viewer'
    )

    def __str__(self):
        return self.username

class BaseModel(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        abstract = True

class Family(BaseModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)  # untuk akses URL unik misal: domain.com/keluarga-prasojo
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class AboutArticle(BaseModel):
    title = models.CharField(max_length=255)
    content = RichTextField()
    image = models.ImageField(upload_to='family_articles/', blank=True, null=True)
    family = models.ForeignKey(Family, on_delete=models.RESTRICT, related_name='about_articles', default=None, null=True, blank=True)
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "About Article"
        verbose_name_plural = "About Articles"


class ImageCarousel(BaseModel):
    image = models.ImageField(upload_to='carousel_images/')
    caption = models.CharField(max_length=255, blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    family = models.ForeignKey(Family, on_delete=models.RESTRICT, related_name='carousels', default=None, null=True, blank=True  )
    

    def __str__(self):
        return f"Image {self.order} - {self.caption or 'No Caption'}"

    class Meta:
        ordering = ['order']
        verbose_name = "Image Carousel"
        verbose_name_plural = "Image Carousels"

class AppConfig(BaseModel):
    name = models.CharField(max_length=100)
    value = models.TextField(blank=True, null=True)
    family = models.ForeignKey(Family, on_delete=models.RESTRICT, related_name='app_configs', default=None, null=True, blank=True)
    

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "App Configuration"
        verbose_name_plural = "App Configurations"

class VisitorLog(models.Model):
    path = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    referer = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.ip_address} - {self.path} @ {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
    
class Person(BaseModel):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    birth_date = models.DateField(null=True, blank=True)
    is_root = models.BooleanField(default=False)
    family = models.ForeignKey(Family, on_delete=models.RESTRICT, related_name='members', default=None, null=True, blank=True  )
    
    def __str__(self):
        return self.name

class Marriage(BaseModel):
    husband = models.ForeignKey(Person, related_name='marriages_as_husband', on_delete=models.RESTRICT)
    wife = models.ForeignKey(Person, related_name='marriages_as_wife', on_delete=models.RESTRICT)
    date_of_marriage = models.DateField(null=True, blank=True)
    family = models.ForeignKey(Family, on_delete=models.RESTRICT, related_name='marriages', default=None, null=True, blank=True  )
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['husband', 'wife'], name='unique_husband_wife')
        ]
        
    def __str__(self):
        return f"{self.husband.name} + {self.wife.name}"

class Child(BaseModel):
    person = models.OneToOneField(Person, on_delete=models.RESTRICT)
    marriage = models.ForeignKey(Marriage, on_delete=models.RESTRICT, related_name='children')
    family = models.ForeignKey(Family, on_delete=models.RESTRICT, related_name='children_family', default=None, null=True, blank=True  )
    
    def __str__(self):
        return self.person.name
