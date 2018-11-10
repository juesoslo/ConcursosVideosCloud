from __future__ import absolute_import, unicode_literals
import os
import celery
from hirefire.procs.celery import CeleryProc

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project0.settings')
app = celery.Celery('project0')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

class WorkerProc(CeleryProc):
    name = 'worker'
    queues = ['cloudg7-videos-queue']
    app = app

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
