from django.db import models
from treeapp.models import BaseModel, Family

class Gallery(BaseModel):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    family = models.ForeignKey(Family, related_name='galleries', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class GalleryImage(BaseModel):
    gallery = models.ForeignKey(Gallery, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='gallery_images/')
    caption = models.CharField(max_length=255, blank=True)
    family = models.ForeignKey(Family, related_name='gallery_images', on_delete=models.CASCADE)

    def __str__(self):
        return f"Gambar untuk {self.gallery.title}"
