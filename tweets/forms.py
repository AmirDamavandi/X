from django import forms
from django.forms import inlineformset_factory
from .models import Tweet, Media



class TweetModelForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['tweet']
        widgets = {
            'tweet': forms.TextInput(attrs={'class': 'text-box', 'placeholder': 'What\'s happening?'}),
        }

class MediaModelForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(MediaModelForm, self).clean()


MediaFormSet = inlineformset_factory(
    # only these types of extensions are allowed to be uploaded: 'png', 'gif', 'jpg', 'mp4', 'webm', 'ogg'
    parent_model=Tweet,
    model=Media,
    fields=('media',),
    extra=1,
    can_delete = False,
    widgets={
        'media': forms.ClearableFileInput(
            attrs={
                'hidden': True, 'accept': 'image/png, image/gif, image/jpeg, image/heic, video/mp4, video/webm, video/ogg'
            }
        ),
    },
    labels={'media': ''},

)
