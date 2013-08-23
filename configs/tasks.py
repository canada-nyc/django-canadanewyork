from celery import task
import simpleimages.utils


@task()
def transform_task(*args, **kwargs):
    simpleimages.utils.transform_field(*args, **kwargs)
