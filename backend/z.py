from celery import Celery

def make_celery():
    celery = Celery("tasks", broker="redis://redis:6379/0")
    # celery.autodiscover_tasks(
    #     ["tasks"]
    # )
    return celery
celery_app = make_celery()
