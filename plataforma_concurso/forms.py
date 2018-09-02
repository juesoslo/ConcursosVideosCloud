from django.forms import ModelForm, ModelChoiceField

from concursos.models import VideoRelacionado, ParticipanteVideo, Participante


class ParticipanteForm(ModelForm):
    video = ModelChoiceField(
        queryset=VideoRelacionado.objects.all(),
        required=False)

    class Meta:
        model = Participante
        fields = ('nombre', 'apellido', 'email', 'mensaje')

    def __init__(self, *args, **kwargs):
        super(ParticipanteForm, self).__init__(*args, **kwargs)
<<<<<<< HEAD
=======
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

>>>>>>> andres
        if self.instance.pk:
            self.fields['video'].initial = VideoRelacionado.objects.get(participantevideo__participante=self.instance).values_list('id', flat=True)

    def save(self, commit=True):
        super(ParticipanteForm, self).save(commit)
        video = self.cleaned_data.pop('video', None)
        if video:
            self.instance.surveyimage.delete()
            ParticipanteVideo.objects.create(participante=self.instance, video=video)
