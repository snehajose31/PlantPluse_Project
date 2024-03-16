from django import forms
from .models import Appointment,Botanist

class AppointmentForm(forms.ModelForm):
    botanist = forms.ModelChoiceField(queryset=Botanist.objects.all())
    class Meta:
        model = Appointment
        fields = ['appointment_date', 'appointment_time', 'botanist', 'subject']
        
# class AppointmentForm(forms.ModelForm):
#     class Meta:
#         model = Appointment
#         fields = ['date', 'time_slot', 'reason']
#         widgets = {
#             'date': forms.DateInput(attrs={'type': 'date', 'style': 'width: 50%;'}),
#             'reason': forms.Textarea(attrs={'rows': 5, 'cols': 30, 'style': 'resize: none; padding: 8px; box-sizing: border-box;'}),
#         }


from .models import Video

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title','description','video_file']
        
from .models import Post       
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        
        
# requests/forms.py


from .models import Service

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name']
        
        
from .models import ServiceRequests

class ServiceRequestsForm(forms.ModelForm):
    class Meta:
        model = ServiceRequests
        fields = ['service', 'bot_profile']
        
        
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['method', 'reason']
        
        
from .models import BotanistWorks

class BotanistWorksForm(forms.ModelForm):
    class Meta:
        model = BotanistWorks
        fields = [ 'title', 'description', 'photo']
        
from .models import BotanistWorkk

class BotanistWorForm(forms.ModelForm):
    class Meta:
        model = BotanistWorkk
        fields = ['title', 'description', 'photo']
        
        
from .models import CustomerPhoto

class CustomerPhotoForm(forms.ModelForm):
    class Meta:
        model = CustomerPhoto
        fields = ['photo', 'submitted_by', 'chosen_botanist']
        
        
from .models import Itemss

class ItemForm(forms.ModelForm):
    class Meta:
        model = Itemss
        fields = ['title', 'link', 'image']