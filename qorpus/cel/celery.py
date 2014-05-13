from __future__ import absolute_import

from celery import Celery

BROKER_URL='redis://localhost:6379/0'
CELERY_RESULTS_BACKEND='redis'

app = Celery('qorpus',
             broker=BROKER_URL,
             include=['cel.tasks'])

if __name__ == "__main__":
    app.start()
