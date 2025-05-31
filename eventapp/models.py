from django.db import models
from ckeditor.fields import RichTextField

class Event(models.Model):
    title = models.CharField(max_length=255)
    content = RichTextField()  # ubah dari TextField ke RichTextField
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class EventImage(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='event_images/')

    def __str__(self):
        return f"Gambar untuk {self.event.title}"
