from django.forms import ModelForm, FileField, FileInput, ValidationError, MultiValueField, Textarea

from concursos.models import VideoRelacionado, ParticipanteVideo, Participante


class ParticipanteForm(ModelForm):
    # video = ModelChoiceField(
    #     queryset=VideoRelacionado.objects.all(),
    #     required=False)

    #video = FileField(widget=FileInput(attrs={'accept': 'video/*'}))
    video = FileField(widget=FileInput(attrs={'accept': 'video/x-flv, video/mp4, application/x-mpegURL, video/MP2T, video/3gpp, video/quicktime, video/x-msvideo, video/x-ms-wmv, .flv, video/*'}))

    class Meta:
        model = Participante
        fields = ('nombre', 'apellido', 'email', 'mensaje')
        widgets = {
            'mensaje': Textarea(attrs={'rows': 4, 'cols': 15}),
        }

    def __init__(self, *args, **kwargs):
        super(ParticipanteForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

        if self.instance.pk:
            self.fields['video'].initial = VideoRelacionado.objects.get(participantevideo__participante=self.instance).values_list('id', flat=True)

    def clean(self):
        cleaned_data = self.cleaned_data
        file = cleaned_data.get("video")

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
