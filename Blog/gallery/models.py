from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='products/')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    #edit the information
    def edit(self,name,description,image):
        self.name = name
        self.description = description
        self.image = image
        self.save()
    
    #Short description    
    def short_description(self):
        
        words = self.description.split()
        
        #if no. of words is greater than 50
        if len(words) > 50:
            return ' '.join(words[:30])+'....'
        else:
            return self.description