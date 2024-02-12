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