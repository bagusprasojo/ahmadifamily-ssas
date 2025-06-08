from django.db import models
from django.utils.timezone import now

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
