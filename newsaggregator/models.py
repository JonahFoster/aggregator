from django.db import models

# Create your models here.

class Post(models.Model):
    title= models.CharField(max_length=200)
    description = models.TextField()
    pub_date = models.DateTimeField()
    link = models.URLField()
    image = models.URLField()
    website_name = models.CharField(max_length=100)
    post_id = models.CharField(max_length=200, null=True)

    def __str__(self) -> str:
        return f"{self.website_name}: {self.title}"