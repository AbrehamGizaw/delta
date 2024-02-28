from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic import ListView, CreateView
from django.apps import apps
from django.utils import timezone
from staff.models import CallApplication, Research, Gallery, Events, News
from staff.forms import ApplicationForm, FeedbackForm
from django.contrib import messages
from django.views import View
from django.db.models import Q
from .models import *
from tinymce.widgets import TinyMCE



class Home(View):
    template_name = "front/index.html"

    def get(self, request, *args, **kwargs):
        context = {"index": True}
        return render(request, self.template_name, context)


class About(View):
    template_name = "front/aboutus.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})


class Services(View):
    template_name = "front/services.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})


class Event(View):
    def get(self, *args, **kwargs):

        if self.kwargs["type"] == "upcoming":
            event = "event1"
        else:
            event = "event2"

        return render(
            self.request,
            "front/event.html",
            {"event": event, "type": self.kwargs["type"]},
        )

from django.shortcuts import render
from django.apps import apps

class Team(View):
    template_name = "front/team.html"

    def get(self, request):
        TeamModel = apps.get_model('staff', 'Team')
        wings = TeamModel.objects.values_list('wing', flat=True).distinct()
        team_data = {}
        for wing in wings:
            teams_in_wing = TeamModel.objects.filter(wing=wing)
            team_data[wing] = [
                {
                    'name': team.name,
                    'role': team.role,
                    'image_url': team.image.url if team.image else None,
                    'id': team.id
                }
                for team in teams_in_wing
            ]
        return render(request, self.template_name, {'team_data': team_data})


class TeamDetail(View):
    template_name = 'front/team_detail.html'

    def get(self, request, id):
        # Retrieve the Team object with the given id from the database
        Team = apps.get_model('staff', 'Team')
        team = get_object_or_404(Team, id=id)
        return render(request, self.template_name, {'team': team})
    
class FeedbackCreate(View):
    template_name = "front/contactus.html"

    def get(self, request):
        form = FeedbackForm
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = FeedbackForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "you have send your message succesfully")
            return redirect("contact")
        messages.warning(request, "please check your input again")
        return render(request, self.template_name, {"form": form})


class CallApplicationList(View):
    template_name = "front/call.html"
    def get(self, request):
        callapplication = CallApplication.objects.all()
        return render(request, self.template_name, {'callapplication':callapplication})
    paginate_by = 3


class ApplicationCreate(View):
    template_name = "front/add_application.html"

    def get(self, request, title):
        form = ApplicationForm(initial={'title': title})  # Pass title as initial data
        return render(request, self.template_name, {'form': form, 'title': title})

    def post(self, request, title):
        form = ApplicationForm(request.POST, request.FILES)  # Remove title from here
        if form.is_valid():
            form.save()
            messages.success(request, 'You have applied successfully')
            return redirect('call_application')
        messages.warning(request, 'Please check your input')
        return render(request, self.template_name, {'form': form})


class ResearchList(View):
    template_name = "front/research.html"
    def get(self, request):
        research = Research.objects.all()
        return render(request, self.template_name, {'research':research})


class GalleryList(ListView):
    template_name = "front/gallery.html"
    def get(self, request):
        gallery = Gallery.objects.all()
        return render(request, self.template_name, {'gallery':gallery})
    
from datetime import datetime

class EventsList(View):
    template_name = 'front/event.html'

    def get(self, request, type):
        # Filter events based on the type and date criteria
        now = datetime.now()
        

        if type == 'Ongoing':
            events = Events.objects.filter(start_date__lte=now, end_date__gte=now)
        elif type == 'Upcoming':
            events = Events.objects.filter(start_date__gt=now)
        elif type == 'Past':
            events = Events.objects.filter(end_date__lt=now)
        else:
            return HttpResponse("Invalid type")

        print(events)
        # Pass the events, type, and current date to the template
        context = {
            'type': type,
            'events': events,
            'now': now,
        }
        return render(request, self.template_name, context)

class NewsList(View):
    def get(self, *args, **kwargs):

        news = News.objects.all()
        category = NewsCategory.objects.all()
        return render(
            self.request, "front/news.html", {"news": news, "category": category}
        )


class NewsDetail(View):
    def get(self, *args, **kwargs):

        news = News.objects.get(id=self.kwargs["pk"])
        related_news = News.objects.filter(category=news.category).exclude(id=news.id)
        category = NewsCategory.objects.all()

        return render(
            self.request,
            "front/news_detail.html",
            {"news": news, "related_news": related_news, "category": category},
        )


class NewsSearch(View):
    def get(self, request):

        if "searched_item" in self.request.GET:
            searched_news_term = self.request.GET["searched_item"]

            category = NewsCategory.objects.all()

            news = News.objects.filter(
                Q(title__icontains=searched_news_term)
                | Q(category__name__icontains=searched_news_term),
            )
            return render(
                request,
                "front/news.html",
                {
                    "news": news,
                    "category": category,
                    "term": searched_news_term,
                    "search": True,
                },
            )
        else:
            return redirect(request, "news")


class NewsByCategory(View):
    def get(self, *args, **kwargs):

        selected_cat = NewsCategory.objects.get(id=self.kwargs["pk"])
        news = News.objects.filter(category=self.kwargs["pk"])
        categories = NewsCategory.objects.all()

        return render(
            self.request,
            "front/news.html",
            {
                "news": news,
                "category": categories,
                "selected_cat": selected_cat,
                "filter": True,
            },
        )