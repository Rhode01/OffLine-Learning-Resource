from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from . import views
urlpatterns = [
     path('',views.login_page,name='login'),
     path('login',views.login_page,name='login'),
     path('signup',views.signup_page,name='signup'),
     path('dashboard',views.dashboard,name='dashboard'),
     path('logout',views.logout_view,name='logout'),
     path('exams',views.exams_list,name='exams'),
     path('exams/<str:exams_choice>/', views.exams_category, name='exams_category'),
     path('exams/<str:category>/questions/<str:subject>/', views.subject_questions, name="questions"),
     path('resources',views.learning_resources, name="resources"),
     path('resources/watch/<str:id>/',views. show_video,name="download"),
     path('resources/<str:category>/',views.learning_resources_subjects,name="subject_resource_name"),
     path('resources/<str:category>/<str:subject>/',views.open_subject_resources,name="subject_resources"),
     path('useranswers',views.handle_user_answers, name="handle_user_answer"),
     path('userprogress',views.user_progress, name="user_progress")
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
