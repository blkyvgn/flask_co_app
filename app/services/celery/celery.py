from celery import Celery
from app.vendors.helpers.config import cfg

celery = Celery('app.app', broker=cfg('CELERY_BROKER_URL'))
