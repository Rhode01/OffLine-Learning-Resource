from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
class Category(models.Model):
    EXAM_CHOICES = (
        ('midterm', 'Mid-term Exams'),
        ('continuous', 'Continuously Exams'),
        ('endterm', 'End-of-Term Exams'),
    )
    name = models.CharField(max_length=100, choices=EXAM_CHOICES, default='midterm', unique=True)
    def __str__(self):
        return self.name
class Subjects(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    class Meta:
        unique_together = ('name', 'category')

    def __str__(self):
        return self.name
class Question(models.Model):
    exam_category = models.ForeignKey(Category, on_delete=models.CASCADE,default=None)
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE, null= True)
    text = models.TextField()

    def __str__(self):
        return self.text

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=255)

    def __str__(self):
        return self.answer
class UserAnswer(models.Model):
    user = models.CharField(max_length=100000000)
    question = models.CharField(max_length=100000000)
    answer = models.CharField(max_length=100000000)

    def __str__(self):
        return f"{self.user} - {self.question}"

class UserExamScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exam_category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='exam_scores',null=True,default=None)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    subject = models.ForeignKey(Subjects,on_delete=models.CASCADE, default=None)
    def __str__(self):
        return f"{self.user.username} - {self.exam_category.name}: {self.score}"
        
class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subjects = models.ForeignKey(Subjects, on_delete=models.CASCADE, default=None)
    exam = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='user_progress')
    score = models.DecimalField(max_digits=5, decimal_places=2)
    def __str__(self):
        return f"{self.user.username} - {self.exam.name}: {self.score}"
    
class Learning_Resource_Category(models.Model):
    RESOURCE_CHOICES = (
        ('videos', 'Videos'),
        ('pdf', 'PDF'),
    )
    name = models.CharField(max_length=100, choices=RESOURCE_CHOICES, default='videos', unique=True)
    def __str__(self):
        return self.name    

    
class Learning_Resource_Subject(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Learning_Resource_Category, on_delete=models.CASCADE,default=None)
    class Meta:
        unique_together = ('name', 'name')
    def __str__(self):
        return self.name
    
class Learning_Resources(models.Model):
    subject = models.ForeignKey(Learning_Resource_Subject,on_delete=models.CASCADE, default=None)
    category = models.ForeignKey(Learning_Resource_Category, on_delete=models.CASCADE)
    name = models.TextField(max_length=300)
    file= models.FileField(upload_to='resources/', default=None, validators=[
        FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'png', 'jpeg', 'docx', 'txt', 'mp4', 'ts', 'avi']),
    ])
    def get_files_urls(self):
        if self.file:
            return self.file.url 
       
    def validate_file_size(self):
        if self.file:
            max_file_size = 104857600
            if self.file.size > max_file_size:
                    raise ValidationError(f"The file '{self.file.name}' exceeds the maximum file size of 100MB.")
    def save(self, *args, **kwargs):
        self.validate_file_size()
        super().save(*args, **kwargs)
    def __str__(self):
        return self.name 

    