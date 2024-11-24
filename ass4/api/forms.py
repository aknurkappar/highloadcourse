from django import forms
from .models import AudioUpload

class AudioUploadForm(forms.ModelForm):
    class Meta:
        model = AudioUpload
        fields = ['file']