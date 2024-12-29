from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Folder(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='subfolders')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    

    def __str__(self):
        return self.name
    
    def get_ancestors(self):
        ancestors = []
        current_folder = self
        while current_folder.parent:
            ancestors.append(current_folder.parent)
            current_folder = current_folder.parent
        return ancestors[::-1]  # Reverse to get top-down order

class File(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads/')
    folder = models.ForeignKey(Folder, null=True, blank=True, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
