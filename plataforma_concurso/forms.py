from django.forms import ModelForm, FileField, FileInput, ValidationError

from concursos.models import VideoRelacionado, ParticipanteVideo, Participante


class ParticipanteForm(ModelForm):
    # video = ModelChoiceField(
    #     queryset=VideoRelacionado.objects.all(),
    #     required=False)

    video = FileField(widget=FileInput(attrs={'accept': 'video/*'}))

    class Meta:
        model = Participante
        fields = ('nombre', 'apellido', 'email', 'mensaje')

    def __init__(self, *args, **kwargs):
        super(ParticipanteForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

        if self.instance.pk:
            self.fields['video'].initial = VideoRelacionado.objects.get(participantevideo__participante=self.instance).values_list('id', flat=True)

    def clean(self):
        cleaned_data = self.cleaned_data
        file = cleaned_data.get("video")
        file_exts = ('.avi', '.mp4', '.webm', '.mkv', '.flv',)

        if file is None:
            raise ValidationError('Seleccione archivo video ')

        if not file:
            raise ValidationError('Solo se permiten archivos de video')

        return cleaned_data


    def save(self, commit=True):
        super(ParticipanteForm, self).save(commit)
        video = self.cleaned_data.pop('video', None)
        if video:
            self.instance.surveyimage.delete()
            ParticipanteVideo.objects.create(participante=self.instance, video=video)
