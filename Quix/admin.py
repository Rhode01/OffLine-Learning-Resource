from django.contrib import admin
from atexit import register
from .models import Question,Answer,UserAnswer,UserExamScore,Learning_Resource_Subject,Subjects,Category,UserProgress,Learning_Resources,Learning_Resource_Category

# admin.site.register(Exam)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Subjects)
admin.site.register(UserAnswer)
admin.site.register(UserExamScore)
admin.site.register(UserProgress)
admin.site.register(Category)
admin.site.register(Learning_Resource_Subject)
admin.site.register(Learning_Resource_Category)
admin.site.register(Learning_Resources)

