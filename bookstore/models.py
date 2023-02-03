from django.db import models
from django.contrib.auth.models import AbstractUser,User
from django.contrib.auth import get_user_model
from django.conf import settings

class User(AbstractUser):
    is_publisher = models.BooleanField(default=False)
    is_librarian = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    class Meta:
        swappable = "AUTH_USER_MODEL"
        

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    year = models.CharField(max_length=100)
    publisher = models.CharField(max_length=200)
    desc = models.CharField(max_length=1000)
    uploaded_by = models.CharField(max_length=100, null=True, blank=True)
    user_id = models.CharField(max_length=100, null=True, blank=True)
    pdf = models.FileField(upload_to='bookapp/pdfs/')
    cover = models.ImageField(upload_to='bookapp/covers/', null=True, blank=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ("-id",)
    
class Chat(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    message = models.TextField()
    posted_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.message)
    
    class Meta:
        ordering = ("-posted_at",)

class DeleteRequest(models.Model):
    delete_request = models.CharField(max_length=100, null=True, blank=True)
    book = models.ForeignKey(Book,on_delete=models.CASCADE)

    def __str__(self):
        return self.delete_request
    
class Feedback(models.Model):
    feedback = models.CharField(max_length=100, null=True, blank=True)


    def __str__(self):
        return self.feedback