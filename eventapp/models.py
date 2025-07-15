from django.db import models
from ckeditor.fields import RichTextField
from treeapp.models import BaseModel, Family

class Event(BaseModel):
    title = models.CharField(max_length=255)
    content = RichTextField()  # ubah dari TextField ke RichTextField
    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name='events', default=None, null=True, blank=True)

    

    def __str__(self):
        return self.title
    
class EventImage(BaseModel):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='event_images/')
    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name='event_images', default=None, null=True, blank=True)

    def __str__(self):
        return f"Gambar untuk {self.event.title}"
