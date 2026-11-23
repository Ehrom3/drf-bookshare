from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    title = models.CharField(max_length=200)
    
    def __str__(self):
        return self.title
    
class City(models.Model):
    name = models.CharField(max_length=245)

    def __str__(self):
        return self.name

class Books(models.Model):
    STATUS = [
        ('NEW','New'),
        ('NOTBAD','Not bad'),
        ('OLD','Old'),

    ]
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    name = models.CharField(max_length=245)
    description = models.TextField()
    author = models.CharField()
    book_conditions = models.CharField(max_length=100, choices=STATUS)
    is_free = models.CharField(default=False)
    location = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
class Trade(models.Model):
    STATUS = [
        ('PENDING','Pending'),
        ('CANCEL','Cancel'),
        ('ACCEPTED','Accepted'),
        ('RETURNED','Returned')
    ]
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    getter = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS, default='PENDING')
    
    def __str__(self):
        return self.book