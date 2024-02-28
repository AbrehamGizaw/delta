


from django.urls import path
from .views import *

app_name = "staff"

urlpatterns = [
    path('', Staff.as_view(), name= 'index'),
    path('staff_list/', StaffList.as_view(), name='staff_list'),

    # Application URLs
    path('application/', ApplicationList.as_view(), name='applications'),
    path('application-create/', ApplicationCreate.as_view(), name='add_application'),
    path('application-detail/<int:id>', ApplicationDetail.as_view(), name = 'application_detail'), 
    path('application-update/<int:id>', ApplicationUpdate.as_view(), name='application_update'),
    path('application-delete/<int:id>/', ApplicationDelete.as_view(), name='application_delete'),

     # Call_of
    path('Call_application/', CallApplicationList.as_view(), name='call_applications'),
    path('call_application-create/',CallApplicationCreate.as_view(), name='add_call_application'),
    path('call_application-update/<int:id>',CallApplicationUpdate.as_view(), name='call_application_update'),
    path('call_application-delete/<int:id>',CallApplicationDelete.as_view(), name='call_application_delete'),
    
    # Events URLs
    path('events/', EventsList.as_view(), name='event'),
    path('events-create/', EventsCreate.as_view(), name='add_event'),
    path('events-update/<int:id>', EventsUpdate.as_view(), name='events_update'),
    path('events-delete/<int:id>', EventsDelete.as_view(), name='events_delete'),
    
    # Feedback URL
    path('feedback/', FeedbackList.as_view(), name='feedbacks'),
    path('feedback-delete/<int:id>/', FeedbackDelete.as_view(), name='feedback_delete'),
    path('feedback-detail/<int:id>/', FeedbackDetail.as_view(), name = 'feedback_detail'),
    
     # Gallery URLs 
    path('gallery/', GalleryList.as_view(), name='gallery'),
    path('gallery-create/', GalleryCreate.as_view(), name='add_gallery'),
    path('gallery-update/<int:id>', GalleryUpdate.as_view(), name='gallery_update'),
    path('gallery-delete/<int:id>', GalleryDelete.as_view(), name='gallery_delete'),

    # News URLs
    path('news/', NewsList.as_view(), name='news'),
    path('news-create/', NewsCreate.as_view(), name='add_new'),
    path('news-update/<int:id>/', NewsUpdate.as_view(), name='news_update'),
    path('news-delete/<int:id>/', NewsDelete.as_view(), name='news_delete'),

   
    # Research URLs
    path('research/', ResearchList.as_view(), name='researches'),
    path('research/create/', ResearchCreate.as_view(), name='add_research'),
    path('research-update/<int:id>/', ResearchUpdate.as_view(), name='research_update'),
    path('research-delete/<int:id>/', ResearchDelete.as_view(), name='research_delete'),

    #
    path('team/create/', TeamCreate.as_view(), name='add_team'),
    path('team/', TeamList.as_view(), name='teams'),
    path('team-update/<int:id>', TeamUpdate.as_view(), name='team_update'),
    path('team-activate/<int:id>', TeamActivate.as_view(), name='team_activate'),
    path('team-delete/<int:id>', TeamDelete.as_view(), name='team_delete'),

]