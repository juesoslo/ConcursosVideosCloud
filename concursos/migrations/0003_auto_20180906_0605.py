# Generated by Django 2.1 on 2018-09-06 11:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('concursos', '0002_auto_20180906_0311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participante',
            name='concurso',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participantes', to='concursos.Concurso'),
        ),
        migrations.AlterField(
            model_name='videorelacionado',
            name='concurso',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='videos', to='concursos.Concurso'),
        ),
    ]
