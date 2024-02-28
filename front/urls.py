from django.urls import path
from .views import *

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("about/", About.as_view(), name="about"),
    path("services/", Services.as_view(), name="services"),
    path("team/", Team.as_view(), name="team"),
    path('team/<int:id>/', TeamDetail.as_view(), name='team_detail'),
    path("news/", NewsList.as_view(), name="news"),
    path("news_detail/<int:pk>/", NewsDetail.as_view(), name="news_detail"),
    path("news_search/", NewsSearch.as_view(), name="news_search"),
    path("news_by_category/<int:pk>", NewsByCategory.as_view(), name="news_by_cat"),
    path("events/<str:type>/", EventsList.as_view(), name="events"),
    
    path("events/", EventsList.as_view(), name="events"),
    path("gallery/", GalleryList.as_view(), name="gallery"),
    path("research/", ResearchList.as_view(), name="research"),
    path("application/<str:title>/", ApplicationCreate.as_view(), name="add_application"),
    path("contact/", FeedbackCreate.as_view(), name="contact"),
    path("CallOfApplication/", CallApplicationList.as_view(), name="call_application"),
]
