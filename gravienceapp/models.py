from django.db import models
from django.contrib.auth.models import User  

class Grievance(models.Model):
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    student_name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"{self.student_name} - {self.subject}"
