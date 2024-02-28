from django.utils import timezone
from venv import logger
import logging
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from .models import *
from .forms import *
from django.forms import modelformset_factory
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
app_name = 'staff'

    
class ApplicationList(LoginRequiredMixin, View):
    def get(self, request):
        application=Application.objects.all()
        return render(request, 'staff/applications/list_applications.html', {'application':application})
class ApplicationCreate(LoginRequiredMixin, View):
   
   def get(self, request):
       form = ApplicationForm()
       return render(request, 'staff/applications/add_application.html', {'form': form})
   
   def post(self, request):
       form = ApplicationForm(request.POST, request.FILES)
       if form.is_valid():
           form.save()
           messages.success(request, 'You have saved the application successfully')
           return redirect('staff:applications')
       return render(request, 'staff/applications/add_application.html', {'form': form})

    
class ApplicationUpdate(LoginRequiredMixin, View):
    def get(self, request, id):
        application = Application.objects.get(id=id)
        form = ApplicationForm(instance=application, )
        context={'form':form, 'application':application }
        return render(request, 'staff/applications/add_application.html', context)
    def post(self, request, id):
        application=Application.objects.get(id=id)
        form=ApplicationForm(instance=application, data=self.request.POST, files=self.request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'you have edited the applications successfully')
            return redirect('staff:applications',)
        
        else:
            messages.warning(request, "check your inputs please")
            return render (request, 'staff/applications/add_application.html',{'form':form})
        
logger = logging.getLogger(__name__)


class ApplicationDetail(LoginRequiredMixin, View):
    def get(self, request, id):
        application = Application.objects.get(id = id)
        return render(request, 'staff/applications/application_detail.html', {'application':application} )

class ApplicationDelete(LoginRequiredMixin, View):
    def get(self, request, id):
        app = Application.objects.get(id=id)
        app.delete()
        messages.success(request, 'You have deleted the application successfully')
        return redirect ( 'staff:applications' )
        


class CallApplicationList(LoginRequiredMixin, View):
    def get(self, request):
        call_application=CallApplication.objects.all()
        template_name = 'staff/call_applications/list_call_applications.html'
        return render(request, template_name, {'call_application': call_application})
    
from django.utils import timezone

class CallApplicationCreate(LoginRequiredMixin, View):
    def get(self, request):
        form = CallApplicationForm()
        template_name = 'staff/call_applications/add_call_application.html'  # Fix the template path
        return render(request, template_name, {'form': form})

    def post(self, request):
        form = CallApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)  # Save the form but don't commit to database yet
            now = timezone.now()
            if instance.start_date > now:
                instance.status = 'pending'
            elif instance.start_date < now and now < instance.end_date:
                instance.status = 'active'
            else:
                instance.status = 'closed'
            instance.save()  # Now save the instance with updated status
            messages.success(request, 'You have successfully saved the call application')
            return redirect('staff:call_applications')    
        return render(request, 'staff/call_applications/add_call_application.html', {'form': form})


    

class CallApplicationUpdate(LoginRequiredMixin, View):
    template_name = 'staff/call_applications/add_call_application.html'
    def get(self, request, id):
        call_application=CallApplication.objects.get(id=id)
        form = CallApplicationForm(instance=call_application)
        context = {'form':form, 'call_application':call_application}
        return render(request, self.template_name, context )
    
    def post(self, request, id):
        call_application=CallApplication.objects.get(id=id) 
        form = CallApplicationForm(instance = call_application, data=self.request.POST, files=self.request.FILES)
        if form.is_valid():
            now = timezone.now()
            if call_application.start_date > now:
                call_application.status = 'pending'
            elif call_application.start_date < now and now < call_application.end_date:
                call_application.status = 'active'
            else:
                call_application.status = 'closed'
            
            form.save()
            messages.success(request, 'the form is updated successfully')
            return redirect('staff:call_applications')
        else:
            messages.warning(request, 'check your input please')
            return render(request, self.template_name, {'form':form})
    

class CallApplicationDelete(LoginRequiredMixin, View):
    def get(self, request, id):
        call_application=CallApplication.objects.get(id=id)
        call_application.delete()
        messages.success(request, 'you have deleted call applications successfully')
        return redirect('staff:call_applications')


class EventsList(LoginRequiredMixin, View):
    def get(self, request):
        event = Events.objects.all()
        template_name='staff/events/list_events.html'
        return render(request, template_name, {'event':event})
   
  

class EventsCreate(LoginRequiredMixin, View):
    template_name = 'staff/events/add_event.html'
    def get(self, request):
        form = EventsForm        
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        
        form = EventsForm(request.POST, request.FILES)
        if form.is_valid():            
            form=form.save(commit=False)
            form.created_by=self.request.user

            now = timezone.now()
            if form.start_date < now  and now < form.end_date :
                form.status = 'ongoing events'
            elif now < form.start_date:
                form.status = 'upcoming events'
            elif form.end_date < now:
                form.status = 'past events'

            form.save()
            return redirect('staff:event')       
        return render(request, self.template_name, {'form': form})

class EventsUpdate(LoginRequiredMixin, View):
    template_name = 'staff/events/add_event.html'
    def get(self, request, id):
        event = Events.objects.get(id=id)
        form = EventsForm(instance=event)    
        context = {'event':event, 'form':form}    
        return render(request, self.template_name, context)
    
    def post(self, request, id):
        event = Events.objects.get(id=id)
        form = EventsForm(instance=event, data=request.POST, files=request.FILES)

        if form.is_valid():
            now = timezone.now()
            if event.start_date > now:
                event.status = 'upcoming event'
            elif event.start_date < now and event.end_date >now:
                event.status = 'opened event'
            else:
                event.status = 'past event'
            form.save()
            messages.success(request, 'you have successfully updated the Event')
            return redirect('staff:event')
        messages.warning(request, 'please check you input')
        return render(request, self.template_name, {'form':form})
    

class EventsDelete(LoginRequiredMixin, View):
    def get(self, request, id):
        event = Events.objects.get(id=id)
        event.delete()
        messages.success(request, 'you have deleted the event successfully')
        return redirect('staff:event')
   
    


  
class FeedbackList(LoginRequiredMixin, View):
    def get(self, request):
        feedback = Feedback.objects.all()
        template_name = 'staff/feedbacks/list_feedbacks.html'
        return render(request, template_name, {'feedback':feedback}) 
   

class FeedbackCreate(LoginRequiredMixin, View):
    template_name = 'staff/feedbacks/list_feedbacks.html'
    def get(self, request):
        form = FeedbackForm
        return render(request, self.template_name, {'form':form})
    def post(self, request):
        form = FeedbackForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'you have send the feedback correctly')
            return redirect('staff:feedbacks')
        return render(request, self.template_name, {'form':form})
    
   

class FeedbackDelete(LoginRequiredMixin, View):
    def get(self, request,id):
        feedback = Feedback.objects.get(id=id)
        feedback.delete()
        return redirect('staff:feedbacks')

class FeedbackDetail(LoginRequiredMixin, View):
    def get(self, request, id):
        feedback = Feedback.objects.get(id=id)
        return render(request, 'staff/feedbacks/feedback_detail.html', {'feedback':feedback})


class GalleryList(LoginRequiredMixin, View):
    template_name = 'staff/galleries/list_galleries.html'
    def get(self, request):
        gallery = Gallery.objects.all()
        galleryImage=Gallery_Image.objects.all()
        return render(request, self.template_name, {'gallery':gallery, 'galleryImage':galleryImage})
    

class GalleryCreate(View):
    template_name = 'staff/galleries/add_gallery.html'
    def get( self, request):
        form = GalleryForm
        form2=Galley_ImageForm

        context = {'form': form, 'form2':form2}
        return render (request, self.template_name, context )
    
    def post ( self, request):
        form = GalleryForm(request.POST, request.FILES )
        form2 = Galley_ImageForm( files= self.request.FILES,  )
        if form.is_valid():
            gallery = form.save(commit=False)
            
            gallery.created_by = self.request.user
            gallery.save()
            
            images = self.request.FILES.getlist ('image')
            for img in images:
                img=Gallery_Image.objects.create( image=img, title=gallery )
                img.save() 


            messages.success(self.request, "You have successfully gallery.")
            return redirect( 'staff:gallery')
        else:
            context = {'form': form, 'form2':form2, 'submitted':True}
            
            messages.warning(self.request, "Please check your inputs again.")
            return render (request, self.template_name, context )

    
class GalleryUpdate(LoginRequiredMixin, View):
    template_name = 'staff/galleries/add_gallery.html'
    def get( self, request, id):
        gallery = Gallery.objects.get(id=id)
        form = GalleryForm(instance=gallery)
        form2=Galley_ImageForm

        context = {'form': form, 'form2':form2, 'gallery':gallery,'edit':True}
        return render (request, self.template_name, context )
    
    def post ( self, request, id):
        gallery = Gallery.objects.get(id=id)
        form = GalleryForm(instance=gallery, data=self.request.POST, files=self.request.FILES)
        form2=Galley_ImageForm(instance=gallery, data=self.request.POST, files=self.request.FILES)
        if form.is_valid():
            gallery.save()

            messages.success(self.request, "You have successfully updated gallery.")
            return redirect( 'staff:gallery')
        else:
            context = {'form': form,'form2':form2, 'edit':True, }
            messages.warning(self.request, "Please check your inputs again.")
            return render (request, self.template_name, context )


    

from django.shortcuts import get_object_or_404

class GalleryDelete(LoginRequiredMixin, View):
    
   def get(self, request, id):
        gallery = get_object_or_404(Gallery, id=id)
        
        # Delete associated images
        gallery.gallery_image_set.all().delete()  # Access related images through ForeignKey relationship
        
        # Delete the gallery
        gallery.delete()
        
        messages.success(request, 'You have deleted the gallery and its images successfully')
        return redirect('staff:gallery')

    

class NewsList(LoginRequiredMixin, View):
    def get(self, request):
        template_name = 'staff/news/list_news.html'
        new = News.objects.all()
        return render(request, template_name, {'new':new})

   
class NewsCreate(LoginRequiredMixin, View):
    template_name = 'staff/news/add_new.html'
    def get(self, request):
        form = NewsForm
        return render(request, self.template_name, {'form':form})
    def post(self, request):
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            news = form.save(commit=False)
            
            news.posted_by = self.request.user
            news.save()
            messages.success(request, 'you have successfully saved news')
            return redirect('staff:news')
        messages.warning(request, 'please check the inputs again')
        return render(request, self.template_name, {'form':form})
    
class NewsUpdate(LoginRequiredMixin, View):
    template_name = 'staff/news/add_new.html'
    def get(self, request, id):
        new = News.objects.get(id=id)
        form = NewsForm(instance=new)
        context = {'new':new, 'form':form}
        return render(request, self.template_name, context)
    def post(self, request, id):
        new = News.objects.get(id=id)
        form = NewsForm(instance=new, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'you have updated the news successfully')
            return redirect('staff:news')
        messages.warning(request, 'please check you input again')
        return render(request, self.template_name, {'form':form})



class NewsDelete(LoginRequiredMixin, View):
    def get(self, request, id):
        new = News.objects.get(id=id)
        new.delete()
        messages.success(request, 'you have deleted the new successfully')
        return redirect('staff:news')
    

class ResearchList(LoginRequiredMixin, View):
    def get(self, request):
        template_name = 'staff/researches/list_researches.html'
        research = Research.objects.all()
        return render(request, template_name, {'research':research})


class ResearchCreate(LoginRequiredMixin, View):
    template_name = 'staff/researches/add_research.html'
    def get(self, request):
        form = ResearchForm
        return render(request, self.template_name, {'form':form})
    def post(self, request):
        form = ResearchForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            expiry_age = request.session.get_expiry_age()
            print("Session Expiry Age:", expiry_age)  # Print the session expiry age
            messages.success(request, 'you have added research successfully')
            return redirect('staff:researches')
        messages.warning(request, 'please check your input once')
        return render(request, self.template_name, {'form':form})
        

class ResearchUpdate(LoginRequiredMixin, View):
    template_name = 'staff/researches/add_research.html'
    def get(self, request, id):
        research = Research.objects.get(id=id)
        form = ResearchForm(instance=research)
        context = {'research':research, 'form':form}
        return render(request, self.template_name, context)
    def post(self, request, id):
        research = Research.objects.get(id=id)
        form = ResearchForm(instance=research, data = request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'you have updated the Research successfully')
            return redirect('staff:researches')
        messages.warning(request, 'please check you input again')
        return render(request, self.template_name, {'form':form})

class ResearchDelete(LoginRequiredMixin, View):
    def get(self, request, id):
        research = Research.objects.get(id=id)
        research.delete()
        messages.success(request, 'You have succesfully deleted the research')
        return redirect('staff:researches')


    
class TeamList(LoginRequiredMixin, View):
    def get(self, request):
        template_name='staff/teams/list_team.html'
        team=Team.objects.all()
        return render (request, template_name, {'team':team}) 

class TeamCreate(LoginRequiredMixin, View):
    template_name = 'staff/teams/add_team.html'
    def get(self, request):
        form = TeamForm()  
        return render(request, self.template_name, {'form': form})
    def post(self, request):
        form = TeamForm(request.POST, request.FILES)
        if form.is_valid():
            team = form.save(commit=False)
            team.save()
            messages.success(request, "You have successfully added a new member.")
            return redirect('staff:teams')
        messages.warning(request, "Please check your inputs again.")
        return render(request, self.template_name, {'form': form})

        

class TeamUpdate(LoginRequiredMixin, View):
    template_name='staff/teams/add_team.html'
    def get( self, request, id):
        team = Team.objects.get(id=id)
        form = TeamForm(instance=team)

        context = {'form': form, 'team':team, 'edit':True}
        return render (request, self.template_name, context )
    
    def post ( self, request, id):
        team = Team.objects.get(id=id)
        form = TeamForm(instance=team, data=self.request.POST, files=self.request.FILES, )
        if form.is_valid():
            team.save()
            messages.success(self.request, "You have successfully updated a member's info.")
            return redirect( 'staff:list_team')
        messages.warning(self.request, "Please check your inputs again.")
        return render (request, self.template_name, {'form': form} ) 
        
class TeamActivate (LoginRequiredMixin, View):
    def get (self, request, id):
        team = Team.objects.get(id=id)
        if team.is_active == False:
            team.is_active = True
            messages.success(request, "You have successfully activated a member")
        else:
            team.is_active = False
            messages.success(request, "You have successfully suspended a member")
        team.save()
        return redirect ( 'staff:teams')

class TeamDelete (LoginRequiredMixin, View):
    def get (self, request, id):
        team = Team.objects.get(id=id)
        team.delete()
        messages.success(request, "You have successfully deleted a member")
        return redirect ( 'staff:teams')

class StaffList(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        staff = user.objects.filter(is_staff = True)
        return render (self.request, 'staff/list_staff.html', {'staff':staff})

class Staff(LoginRequiredMixin, View):
    def get(self, request):
        research = Research.objects.all()
        application = Application.objects.all()
        event = Events.objects.all()
        call_application = CallApplication.objects.all()
        users = user.objects.all()
        news = News.objects.all()
        feedback = Feedback.objects.all()

        context = {
            'research': research,
            'call_application': call_application,
            'event': event,
            'application': application,
            'users': users,
            'feedback': feedback,
            'news': news,
        }
        return render(request, 'staff/index.html', context)