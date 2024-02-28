from django.db import models
from datetime import date
from tinymce.models import HTMLField
from useracc.models import CustomUser as user


NEWS_CATEGORY = (('Health', 'Health'), ('Research', 'Research'), ('Information', 'Information'), ('Anouncement', 'Anouncement'))
GALLERY_CATEGORY = (('Event', 'Event'), ('Seminar', 'Seminar'), ('Training', 'Training'), ('Report', 'Report'))
WING_CHOICES = (('Martin-Luther-University Halle-Wittenberg, Halle', 'Martin-Luther-University Halle-Wittenberg, Halle'), ('AAU', 'AAU'), ('Health-Center', 'Health-Center'))


class Application(models.Model):
    title = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    image = models.ImageField(upload_to='application_photos/')
    original_document = models.FileField(upload_to='application_documents/original/')
    cv_document = models.FileField(upload_to='application_documents/cv/')
    supplementary_document = models.FileField(upload_to='application_documents/supplementary/')
    letter = models.TextField(max_length=512, blank=True, null=True)
    submitted_date = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ('-id',)

    
class CallApplication(models.Model):
    title=models.CharField(max_length=255)
    phone=models.CharField(max_length=13)
    email=models.EmailField()
    start_date=models.DateTimeField(default=date.today)
    end_date=models.DateTimeField()
    assistant_name=models.CharField(max_length=30, null=True)
    status = models.CharField(max_length=50)
    document = models.FileField(upload_to='document/call/application')
    class Meta:
        ordering = ('-id',)


class Events(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='events_images/')
    event_handler = models.CharField(max_length=255)  # Assuming event handler is a person's name
    place = models.CharField(max_length=255)
    start_date = models.DateTimeField(default=date.today, editable=True)
    end_date = models.DateTimeField( blank=True, null=True)
    created_by = models.ForeignKey(user, on_delete=models.CASCADE)
    category = models.CharField(max_length=30, choices=(('seminar','seminar'), ('expo','expo')))
    status = models.CharField(max_length=30, default='upcoming event')
    class Meta:
        ordering = ('-id',)

class Feedback(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    interest = models.CharField(max_length=255)
    message = models.TextField()
    show = models.BooleanField(default=False)
    sent_date = models.DateTimeField(auto_now_add=True) 
    class Meta:
        ordering = ('-id',)
    


class Gallery(models.Model):
    title = models.CharField(max_length=500, blank=True, null=True)
    image = models.ImageField(upload_to='gallery_images', blank=True, null=True)
    category = models.CharField(max_length=30, choices=GALLERY_CATEGORY, default='Training', null=True, blank=True)
    created_by = models.ForeignKey(user, on_delete=models.PROTECT)
    created_date = models.DateTimeField(auto_now_add=True)


    
    class Meta:
        ordering = ('-id',)


class Gallery_Image(models.Model):
    title = models.ForeignKey(Gallery, on_delete=models.PROTECT)
    image = models.ImageField(upload_to='gallery_images', blank=True, null=True)

    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ('-id',)


class News(models.Model):
    title = models.CharField(max_length=150)
    image = models.ImageField(upload_to='news_images/')
    category = models.CharField(max_length=30, choices=NEWS_CATEGORY)
    description = HTMLField(blank=True, null=True)
    posted_by = models.CharField(user, max_length=30)
    post_date = models.DateField(auto_now_add=True)
    class Meta:
        ordering = ('-id',)



class Research(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=50)
    abstract = models.TextField(null=True)
    keywords = models.CharField(max_length=255)
    document = models.FileField(upload_to='research_outputs/')
    post_date = models.DateField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    class Meta:
        ordering = ('-id',)
    
class Team(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='team/', blank=True, null=True)
    wing = models.CharField(max_length=100, choices=WING_CHOICES, blank=True)
    role = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-id',)