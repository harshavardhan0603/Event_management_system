from django import forms
from .models import *


class booking_form(forms.ModelForm):

    class Meta:
        model = booking_data
        exclude = ('user','date','EventType','Amount')

class feedback_form(forms.ModelForm):

    class Meta:
        model = booking_review
        exclude = ('booking', 'user')


