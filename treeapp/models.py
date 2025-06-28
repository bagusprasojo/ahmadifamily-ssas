from django.db import models
from django.utils.timezone import now
from ckeditor.fields import RichTextField

# models.py
from django.db import models

class AboutArticle(models.Model):
    title = models.CharField(max_length=255)
    content = RichTextField()
    image = models.ImageField(upload_to='family_articles/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "About Article"
        verbose_name_plural = "About Articles"


class ImageCarousel(models.Model):
    image = models.ImageField(upload_to='carousel_images/')
    caption = models.CharField(max_length=255, blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Image {self.order} - {self.caption or 'No Caption'}"

    class Meta:
        ordering = ['order']
        verbose_name = "Image Carousel"
        verbose_name_plural = "Image Carousels"

class AppConfig(models.Model):
    name = models.CharField(max_length=100, unique=True)
    value = models.TextField(blank=True, null=True)

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
    
class Person(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    birth_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    is_root = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Marriage(models.Model):
    husband = models.ForeignKey(Person, related_name='marriages_as_husband', on_delete=models.CASCADE)
    wife = models.ForeignKey(Person, related_name='marriages_as_wife', on_delete=models.CASCADE)
    date_of_marriage = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.husband.name} + {self.wife.name}"

class Child(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE)
    marriage = models.ForeignKey(Marriage, on_delete=models.CASCADE, related_name='children')

    def __str__(self):
        return self.person.name
